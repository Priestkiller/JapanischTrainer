package de.priestkiller.japanischtrainer

import androidx.test.core.app.ActivityScenario
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.*
import org.junit.Test
import org.junit.Before
import org.junit.After
import org.junit.runner.RunWith
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import org.json.JSONArray
import java.io.File
import android.graphics.Bitmap
import android.content.pm.ActivityInfo
import android.webkit.WebView

@RunWith(AndroidJUnit4::class)
class MobileInstrumentedTest {
    private lateinit var testProfile:android.util.AtomicFile
    private var previousProfile:ByteArray?=null
    private fun writeProfile(bytes:ByteArray) {
        val output=testProfile.startWrite()
        try { output.write(bytes);testProfile.finishWrite(output) }
        catch(e:Exception) { testProfile.failWrite(output);throw e }
    }
    @Before fun isolateEveryNativeProfile() {
        val instrumentation=InstrumentationRegistry.getInstrumentation()
        instrumentation.waitForIdleSync()
        val context=instrumentation.targetContext
        check(context.packageName=="de.priestkiller.japanischtrainer.test") { "Only the separate debug test package may be reset" }
        testProfile=android.util.AtomicFile(File(context.filesDir,"progress.json"))
        previousProfile=if(testProfile.baseFile.exists() || File(testProfile.baseFile.path+".bak").exists())testProfile.readFully() else null
        writeProfile("""{"xp":0,"completed":[]}""".toByteArray(Charsets.UTF_8))
    }
    @After fun restoreNativeProfileAfterActivityHasClosed() {
        // Closing a WebView saves its in-memory state on visibilitychange.
        // Restore only after ActivityScenario.use has actually closed it.
        InstrumentationRegistry.getInstrumentation().waitForIdleSync()
        previousProfile?.let { writeProfile(it) } ?: testProfile.delete()
    }
    @Test fun regularAndTestUpdatesUseSeparateReleaseTags() {
        fun release(tag:String,preview:Boolean=false,draft:Boolean=false)=org.json.JSONObject()
            .put("tag_name",tag).put("prerelease",preview).put("draft",draft)
        assertTrue(AppUpdates.acceptsRelease(release("android-v11.0.2-1",true),false))
        assertFalse(AppUpdates.acceptsRelease(release("android-test-v11.0.5-1",true),false))
        assertTrue(AppUpdates.acceptsRelease(release("android-test-v11.0.5-1",true),true))
        assertFalse(AppUpdates.acceptsRelease(release("android-v11.0.4-1"),true))
        assertFalse(AppUpdates.acceptsRelease(release("android-test-v11.0.5-1",true,true),true))
        assertFalse(AppUpdates.acceptsRelease(release("android-test-v11.0.5-1",false),true))
        assertFalse(AppUpdates.acceptsRelease(release("windows-test-v11.0.5",true),true))
    }
    private fun screenshot(scenario:ActivityScenario<MainActivity>,name:String) {
        val instrumentation=InstrumentationRegistry.getInstrumentation()
        // JavaScript completion can precede the WebView compositor by several frames.
        val rendered=CountDownLatch(1)
        scenario.onActivity { activity ->
            activity.web.postVisualStateCallback(System.nanoTime(),object:WebView.VisualStateCallback() {
                override fun onComplete(requestId:Long) { activity.web.invalidate(); rendered.countDown() }
            })
        }
        check(rendered.await(15,TimeUnit.SECONDS)) { "WebView did not finish drawing" }
        instrumentation.waitForIdleSync()
        Thread.sleep(2000)
        var focused=false
        scenario.onActivity { focused=it.hasWindowFocus() }
        assertTrue("A system dialog must not cover the app screenshot",focused)
        assertEquals("true",eval(scenario,"!document.body.classList.contains('focus-mode') || (()=>{const d=document.querySelector('.focus-dock').getBoundingClientRect();return d.top>=0 && d.bottom<=innerHeight+1 && document.documentElement.scrollWidth<=innerWidth})()"))
        val folder=File(requireNotNull(InstrumentationRegistry.getArguments().getString("additionalTestOutputDir"))).apply { mkdirs() }
        val bitmap=instrumentation.uiAutomation.takeScreenshot()
        File(folder,"$name.png").outputStream().use { bitmap.compress(Bitmap.CompressFormat.PNG,100,it) }
        bitmap.recycle()
    }
    private fun eval(scenario:ActivityScenario<MainActivity>,script:String):String {
        var result="";val latch=CountDownLatch(1)
        scenario.onActivity { it.web.evaluateJavascript(script) { value -> result=value;latch.countDown() } }
        check(latch.await(10,TimeUnit.SECONDS));return result
    }
    private fun waitFor(s:ActivityScenario<MainActivity>,condition:String) {
        val deadline=System.currentTimeMillis()+30000
        while(System.currentTimeMillis()<deadline) { if(eval(s,condition)=="true")return;Thread.sleep(200) }
        fail("Condition did not become true: $condition")
    }
    @Test fun nativeAppStartsAndKeepsTheLessonOnRestart() {
        ActivityScenario.launch(MainActivity::class.java).use { scenario ->
            waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
            assertEquals("true",eval(scenario,"document.documentElement.scrollWidth <= innerWidth"))
            screenshot(scenario,"android-home")
            eval(scenario,"document.querySelector('#hero-resume').click()")
            waitFor(scenario,"!!document.querySelector('#record')")
            eval(scenario,"document.querySelector('.focus-sheet-close')?.click()")
            assertEquals("true",eval(scenario,"document.body.innerText.includes('Aussprachehilfe')"))
            screenshot(scenario,"android-lesson")
            assertEquals("true",eval(scenario,"document.querySelector('#step-count').textContent === 'Schritt 1/6' && document.querySelector('#advance').disabled"))
            eval(scenario,"document.querySelector('#advance').click()")
            assertEquals("true",eval(scenario,"!!document.querySelector('#record') && !document.querySelector('[data-choice]')"))
            // A persisted successful first step is a fixture, not a simulated microphone pass.
            eval(scenario,"(()=>{const p=JSON.parse(AndroidTrainer.getProfile());const s=p.lesson_sessions[p.last_lesson.key];s.passed=['speak'];s.phase='meaning';AndroidTrainer.saveProfile(JSON.stringify(p));return true})()")
            scenario.recreate()
            waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
            eval(scenario,"document.querySelector('#hero-resume').click()")
            waitFor(scenario,"!!document.querySelector('[data-choice]')")
            assertEquals("true",eval(scenario,"document.querySelector('#step-count').textContent === 'Schritt 2/6' && !document.querySelector('#record') && !document.querySelector('.romaji')"))
            assertEquals("true",eval(scenario,"document.documentElement.scrollWidth <= innerWidth"))
            screenshot(scenario,"android-meaning")
            eval(scenario,"document.querySelector('#settings-shortcut').click()")
            waitFor(scenario,"!!document.querySelector('#check-updates')")
            assertEquals("true",eval(scenario,"!!document.querySelector('#check-test-updates') && typeof AndroidTrainer.checkTestUpdates === 'function'"))
            assertEquals("true",eval(scenario,"document.body.innerText.includes('Lernstand sichern')"))
            scenario.onActivity { it.web.settings.textZoom=150 }
            Thread.sleep(500)
            assertEquals("true",eval(scenario,"document.documentElement.scrollWidth <= innerWidth"))
            screenshot(scenario,"android-settings-large-text")
            scenario.onActivity { it.requestedOrientation=ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE }
            InstrumentationRegistry.getInstrumentation().waitForIdleSync()
            // Rotation now retains the current view (including settings), as
            // required for the active exercise; it must not jump to Home.
            waitFor(scenario,"innerWidth > innerHeight && document.documentElement.dataset.ready === 'true' && !!document.querySelector('#check-updates')")
            assertEquals("true",eval(scenario,"document.documentElement.scrollWidth <= innerWidth"))
            screenshot(scenario,"android-landscape")
        }
    }
    @Test fun offlineConversationBranchesAndKeepsDraftOnRestart() {
        ActivityScenario.launch(MainActivity::class.java).use { scenario ->
            waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
            eval(scenario,"document.querySelector('[data-nav=talk]').click()")
            waitFor(scenario,"document.querySelectorAll('[data-talk-scene]').length === 5")
            screenshot(scenario,"android-talk-hub")
            eval(scenario,"document.querySelector('[data-talk-scene=cafe]').click()")
            waitFor(scenario,"!!document.querySelector('#talk-draft')")
            // Typed answers test native WebView and persistence. This is not a microphone test.
            eval(scenario,"(()=>{const f=document.querySelector('#talk-draft');f.value='コーヒーをお願いします。';f.dispatchEvent(new Event('input',{bubbles:true}));document.querySelector('#talk-form').requestSubmit()})()")
            waitFor(scenario,"document.querySelector('.talk-cue').textContent.includes('warmes oder kaltes')")
            eval(scenario,"document.querySelector('#talk-translation').click()")
            eval(scenario,"document.querySelector('#talk-reading').click()")
            assertEquals("true",eval(scenario,"document.documentElement.scrollWidth <= innerWidth"))
            screenshot(scenario,"android-talk-cafe")
            eval(scenario,"(()=>{const f=document.querySelector('#talk-draft');f.value='冷たいものをお願いします。';f.dispatchEvent(new Event('input',{bubbles:true}));document.querySelector('[data-nav=talk]').click()})()")
            scenario.recreate()
            waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
            eval(scenario,"document.querySelector('[data-nav=talk]').click();document.querySelector('[data-talk-scene=cafe]').click()")
            waitFor(scenario,"!!document.querySelector('#talk-draft')")
            assertEquals("true",eval(scenario,"document.querySelector('#talk-draft').value === '冷たいものをお願いします。'"))
            assertEquals("true",eval(scenario,"JSON.parse(AndroidTrainer.getProfile()).talk.sessions.cafe.slots.drink === 'コーヒー'"))
            eval(scenario,"document.querySelector('#talk-form').requestSubmit()")
            waitFor(scenario,"document.querySelector('.talk-cue').textContent.includes('klein oder groß')")
        }
    }
    @Test fun packageTwoExplainsErrorsAndRetainsAnOldProfile() {
        ActivityScenario.launch(MainActivity::class.java).use { scenario ->
            waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
            val previous=eval(scenario,"AndroidTrainer.getProfile()")
            try {
                eval(scenario,"""
                    (async()=>{try {
                      const raw=await fetch('data/course.json').then(r=>r.json());
                      const lessons=raw.units.flatMap(u=>u.lessons).filter(l=>l.study_guide?.package===2);
                      window.package2Inventory=lessons.length===25 && lessons.reduce((n,l)=>n+l.cards.length,0)===121;
                    }catch(e){window.package2Inventory=false;}})()
                """.trimIndent())
                waitFor(scenario,"window.package2Inventory === true")
                // Fixture represents an earned fifth step from 11.0.2; no real
                // microphone success is claimed by this persistence/UI test.
                eval(scenario,"""
                    (()=>{const p=JSON.parse(AndroidTrainer.getProfile());
                      p.course_revision=11;p.xp=321;p.completed=['0:0'];p.teacher_id='ren';
                      p.legacy_unlocked=['15:0'];p.last_lesson={key:'15:0',card:0};
                      p.lesson_sessions={'15:0':{flow_revision:2,index:0,phase:'apply',passed:['speak','meaning','listen','build','write'],mode:'learn',recap:[],recap_total:0,recap_passed:0}};
                      AndroidTrainer.saveProfile(JSON.stringify(p));return true;})()
                """.trimIndent())
                scenario.recreate();waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
                eval(scenario,"document.querySelector('#hero-resume').click()")
                waitFor(scenario,"document.querySelector('#step-count')?.textContent === 'Schritt 6/6'")
                assertEquals("true",eval(scenario,"!document.querySelector('.romaji') && document.querySelector('#advance').disabled"))
                eval(scenario,"Array.from(document.querySelectorAll('[data-choice]')).find(b=>b.textContent==='In beiden Sätzen nur ein Verkehrsmittel.').click()")
                assertEquals("true",eval(scenario,"document.querySelector('#task-feedback').textContent.includes('えき ist der Bahnhof') && document.querySelector('#advance').disabled"))
                assertEquals("true",eval(scenario,"document.documentElement.scrollWidth <= innerWidth"))
                screenshot(scenario,"android-package2-wrong-answer")
                eval(scenario,"document.querySelector('#show-hint').click()")
                assertEquals("true",eval(scenario,"!!document.querySelector('.exercise-hint') && document.querySelector('#advance').disabled && JSON.parse(AndroidTrainer.getProfile()).xp===321"))
                scenario.recreate();waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
                eval(scenario,"document.querySelector('#hero-resume').click()")
                waitFor(scenario,"document.querySelector('#step-count')?.textContent === 'Schritt 6/6'")
                assertEquals("true",eval(scenario,"!!document.querySelector('.exercise-hint') && document.querySelector('#advance').disabled && JSON.parse(AndroidTrainer.getProfile()).teacher_id==='ren'"))
            } finally {
                eval(scenario,"AndroidTrainer.saveProfile($previous)")
            }
        }
    }
    @Test fun packageThreeExplainsErrorsAndRetainsAnOldProfile() {
        ActivityScenario.launch(MainActivity::class.java).use { scenario ->
            waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
            val previous=eval(scenario,"AndroidTrainer.getProfile()")
            try {
                eval(scenario,"""
                    (async()=>{try {
                      const raw=await fetch('data/course.json').then(r=>r.json());
                      const lessons=raw.units.flatMap(u=>u.lessons).filter(l=>l.study_guide?.package===3);
                      window.package3Inventory=lessons.length===25 && lessons.reduce((n,l)=>n+l.cards.length,0)===119;
                    }catch(e){window.package3Inventory=false;}})()
                """.trimIndent())
                waitFor(scenario,"window.package3Inventory === true")
                // Fixture represents an earned fifth step from 11.0.4; no real
                // microphone success is claimed by this persistence/UI test.
                eval(scenario,"""
                    (()=>{const p=JSON.parse(AndroidTrainer.getProfile());
                      p.course_revision=11;p.xp=321;p.completed=['0:0'];p.teacher_id='ren';
                      p.legacy_unlocked=['6:0'];p.last_lesson={key:'6:0',card:0};
                      p.lesson_sessions={'6:0':{flow_revision:2,index:0,phase:'apply',passed:['speak','meaning','listen','build','write'],mode:'learn',recap:[],recap_total:0,recap_passed:0}};
                      AndroidTrainer.saveProfile(JSON.stringify(p));return true;})()
                """.trimIndent())
                scenario.recreate();waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
                eval(scenario,"document.querySelector('#hero-resume').click()")
                waitFor(scenario,"document.querySelector('#step-count')?.textContent === 'Schritt 6/6'")
                assertEquals("true",eval(scenario,"!document.querySelector('.romaji') && document.querySelector('#advance').disabled"))
                eval(scenario,"Array.from(document.querySelectorAll('[data-choice]')).find(b=>b.textContent==='ここでおねがいします。').click()")
                assertEquals("true",eval(scenario,"document.querySelector('#task-feedback').textContent.includes('hier vor Ort') && document.querySelector('#advance').disabled"))
                assertEquals("true",eval(scenario,"document.documentElement.scrollWidth <= innerWidth"))
                screenshot(scenario,"android-package3-wrong-answer")
                eval(scenario,"document.querySelector('#show-hint').click()")
                assertEquals("true",eval(scenario,"!!document.querySelector('.exercise-hint') && document.querySelector('#advance').disabled && JSON.parse(AndroidTrainer.getProfile()).xp===321"))
                scenario.recreate();waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
                eval(scenario,"document.querySelector('#hero-resume').click()")
                waitFor(scenario,"document.querySelector('#step-count')?.textContent === 'Schritt 6/6'")
                assertEquals("true",eval(scenario,"!!document.querySelector('.exercise-hint') && document.querySelector('#advance').disabled && JSON.parse(AndroidTrainer.getProfile()).teacher_id==='ren'"))
            } finally {
                eval(scenario,"AndroidTrainer.saveProfile($previous)")
            }
        }
    }
    @Test fun packageFourExplainsErrorsAndRetainsAnOldProfile() {
        ActivityScenario.launch(MainActivity::class.java).use { scenario ->
            waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
            val previous=eval(scenario,"AndroidTrainer.getProfile()")
            try {
                eval(scenario,"""
                    (async()=>{try {
                      const raw=await fetch('data/course.json').then(r=>r.json());
                      const lessons=raw.units.flatMap(u=>u.lessons).filter(l=>l.study_guide?.package===4);
                      window.package4Inventory=lessons.length===25 && lessons.reduce((n,l)=>n+l.cards.length,0)===123;
                    }catch(e){window.package4Inventory=false;}})()
                """.trimIndent())
                waitFor(scenario,"window.package4Inventory === true")
                // Fixture represents an earned fifth step from 11.0.5; no real
                // microphone success is claimed by this persistence/UI test.
                eval(scenario,"""
                    (()=>{const p=JSON.parse(AndroidTrainer.getProfile());
                      p.course_revision=11;p.xp=321;p.completed=['0:0'];p.teacher_id='ren';
                      p.legacy_unlocked=['v11:clock-hours'];p.last_lesson={key:'v11:clock-hours',card:0};
                      p.lesson_sessions={'v11:clock-hours':{flow_revision:2,index:0,phase:'apply',passed:['speak','meaning','listen','build','write'],mode:'learn',recap:[],recap_total:0,recap_passed:0}};
                      AndroidTrainer.saveProfile(JSON.stringify(p));return true;})()
                """.trimIndent())
                scenario.recreate();waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
                eval(scenario,"document.querySelector('#hero-resume').click()")
                waitFor(scenario,"document.querySelector('#step-count')?.textContent === 'Schritt 6/6'")
                assertEquals("true",eval(scenario,"!document.querySelector('.romaji') && document.querySelector('#advance').disabled"))
                eval(scenario,"Array.from(document.querySelectorAll('[data-choice]')).find(b=>b.textContent==='さんじはん').click()")
                assertEquals("true",eval(scenario,"document.querySelector('#task-feedback').textContent.includes('3:30') && document.querySelector('#advance').disabled"))
                assertEquals("true",eval(scenario,"document.documentElement.scrollWidth <= innerWidth"))
                screenshot(scenario,"android-package4-wrong-answer")
                eval(scenario,"document.querySelector('#show-hint').click()")
                assertEquals("true",eval(scenario,"!!document.querySelector('.exercise-hint') && document.querySelector('#advance').disabled && JSON.parse(AndroidTrainer.getProfile()).xp===321"))
                scenario.recreate();waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
                eval(scenario,"document.querySelector('#hero-resume').click()")
                waitFor(scenario,"document.querySelector('#step-count')?.textContent === 'Schritt 6/6'")
                assertEquals("true",eval(scenario,"!!document.querySelector('.exercise-hint') && document.querySelector('#advance').disabled && JSON.parse(AndroidTrainer.getProfile()).teacher_id==='ren'"))
            } finally {
                eval(scenario,"AndroidTrainer.saveProfile($previous)")
            }
        }
    }
    @Test fun numbersPreparationDoesNotUnlockTheOldWrittenTask() {
        ActivityScenario.launch(MainActivity::class.java).use { scenario ->
            waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
            val previous=eval(scenario,"AndroidTrainer.getProfile()")
            try {
                eval(scenario,"""
                    (()=>{const p=JSON.parse(AndroidTrainer.getProfile());p.course_revision=11;p.xp=321;p.completed=['0:0'];p.teacher_id='ren';
                      p.legacy_unlocked=['12:0'];p.last_lesson={key:'12:0',card:4};
                      p.lesson_sessions={'12:0':{flow_revision:2,index:4,phase:'write',passed:['speak','meaning','listen','build'],mode:'learn',recap:[],recap_total:0,recap_passed:0}};
                      AndroidTrainer.saveProfile(JSON.stringify(p));return true;})()
                """.trimIndent())
                scenario.recreate();waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
                eval(scenario,"document.querySelector('#hero-resume').click()")
                waitFor(scenario,"document.querySelector('#step-count')?.textContent === 'Schritt 5/6'")
                assertEquals("true",eval(scenario,"!document.querySelector('.exercise-hint') && document.querySelector('#advance').disabled"))
                eval(scenario,"document.querySelector('#show-hint').click()")
                assertEquals("true",eval(scenario,"document.querySelector('.exercise-hint').textContent.includes('drei Paaren') && document.querySelector('.exercise-hint').textContent.includes('Miniübung 3') && document.querySelector('#advance').disabled"))
                assertEquals("true",eval(scenario,"document.documentElement.scrollWidth <= innerWidth"))
                screenshot(scenario,"android-numbers-preparation")
                scenario.recreate();waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
                eval(scenario,"document.querySelector('#hero-resume').click()")
                waitFor(scenario,"document.querySelector('#step-count')?.textContent === 'Schritt 5/6'")
                assertEquals("true",eval(scenario,"!!document.querySelector('.exercise-hint') && document.querySelector('#advance').disabled && JSON.parse(AndroidTrainer.getProfile()).xp===321 && JSON.parse(AndroidTrainer.getProfile()).last_lesson.card===4"))
            } finally { eval(scenario,"AndroidTrainer.saveProfile($previous)") }
        }
    }
    @Test fun exerciseVarietyNativeShellPreservesDraftRotationAndKeyboard() {
        // Native WebView/AtomicFile and actual device keyboard. Audio outcomes
        // are not manufactured here; all uncompleted speech phases stay open.
        ActivityScenario.launch(MainActivity::class.java).use { scenario ->
            waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
            eval(scenario,"""
                (async()=>{const data=await fetch('data/exercises.json').then(r=>r.json());
                  const pack=data.packs.find(p=>p.lesson==='5:0');
                  const p=JSON.parse(AndroidTrainer.getProfile());p.xp=321;p.completed=['0:0'];p.legacy_unlocked=['5:0'];p.last_lesson={key:'5:0',card:0};
                  p.lesson_sessions={'5:0':{flow_revision:2,index:0,phase:'speak',passed:[],mode:'learn'}};
                  p.lesson_sessions['exercises:5:0']={revision:1,queue:pack.tasks,index:5,stage:'main',review:[],review_index:0,reviewed:[],outcomes:[],task:{}};
                  AndroidTrainer.saveProfile(JSON.stringify(p));window.fixtureReady=true;})()
            """.trimIndent())
            waitFor(scenario,"window.fixtureReady === true")
            scenario.recreate();waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
            eval(scenario,"document.querySelector('#hero-resume').click();document.querySelector('#exercise-round').click()")
            waitFor(scenario,"!!document.querySelector('#ex-input')")
            eval(scenario,"const input=document.querySelector('#ex-input');input.value='mi';input.dispatchEvent(new Event('input'));document.querySelector('#ex-help').click()")
            assertEquals("true",eval(scenario,"document.querySelector('#ex-input').value==='mi' && document.querySelector('#ex-next').disabled"))
            scenario.recreate();waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
            eval(scenario,"document.querySelector('#hero-resume').click();document.querySelector('#exercise-round').click()")
            assertEquals("true",eval(scenario,"document.querySelector('#ex-input').value==='mi' && !!document.querySelector('.exercise-hint') && document.querySelector('#ex-next').disabled"))
            scenario.onActivity { it.requestedOrientation=ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE }
            waitFor(scenario,"innerWidth > innerHeight")
            assertEquals("true",eval(scenario,"document.querySelector('#ex-input').value==='mi' && document.documentElement.scrollWidth<=innerWidth"))
            screenshot(scenario,"android-exercises-landscape")
            scenario.onActivity { it.requestedOrientation=ActivityInfo.SCREEN_ORIENTATION_PORTRAIT;it.web.settings.textZoom=140 }
            waitFor(scenario,"innerHeight > innerWidth")
            eval(scenario,"document.querySelector('#ex-help').click()")
            // A programmatic JS focus alone need not open the Android IME.
            // Tap the real WebView input and verify native keyboard visibility.
            Thread.sleep(700)
            // Use the same visible page controls as a learner; do not scroll a hidden column into view.
            eval(scenario,"(()=>{const input=document.querySelector('#ex-input'),view=document.querySelector('.focus-task-viewport');for(let i=0;i<20;i++){const r=input.getBoundingClientRect(),v=view.getBoundingClientRect();if(r.left>=v.left-1&&r.right<=v.right+1)break;document.querySelector('.focus-page-nav button:last-child').click();}})()")
            assertEquals("true",eval(scenario,"(()=>{const r=document.querySelector('#ex-input').getBoundingClientRect(),v=document.querySelector('.focus-task-viewport').getBoundingClientRect();return r.left>=v.left-1&&r.right<=v.right+1&&r.top>=v.top-1&&r.bottom<=v.bottom+1})()"))
            val point=JSONArray(eval(scenario,"(()=>{const r=document.querySelector('#ex-input').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2,innerWidth]})()"))
            var tapX=0f;var tapY=0f
            scenario.onActivity { activity ->
                val origin=IntArray(2);activity.web.getLocationOnScreen(origin)
                val scale=activity.web.width/point.getDouble(2)
                tapX=(origin[0]+point.getDouble(0)*scale).toFloat();tapY=(origin[1]+point.getDouble(1)*scale).toFloat()
            }
            val instrumentation=InstrumentationRegistry.getInstrumentation();val down=android.os.SystemClock.uptimeMillis()
            for(action in listOf(android.view.MotionEvent.ACTION_DOWN,android.view.MotionEvent.ACTION_UP)) {
                val event=android.view.MotionEvent.obtain(down,android.os.SystemClock.uptimeMillis(),action,tapX,tapY,0)
                instrumentation.sendPointerSync(event);event.recycle()
            }
            var keyboard=false
            for(attempt in 0..30) {
                scenario.onActivity { keyboard=it.web.rootWindowInsets?.isVisible(android.view.WindowInsets.Type.ime())==true }
                if(keyboard)break
                Thread.sleep(200)
            }
            assertTrue("The real Android keyboard must be open for this test",keyboard)
            Thread.sleep(1000)
            assertEquals("true",eval(scenario,"(()=>{const i=document.querySelector('#ex-input').getBoundingClientRect(),w=document.querySelector('.focus-workspace').getBoundingClientRect();return i.top>=w.top-1&&i.bottom<=w.bottom+1})()"))
            assertEquals("true",eval(scenario,"document.documentElement.scrollWidth<=innerWidth && document.querySelector('#ex-input').value==='mi'"))
            screenshot(scenario,"android-exercises-large-text-keyboard")
            eval(scenario,"document.querySelector('#ex-check').scrollIntoView({block:'center'});document.querySelector('#ex-check').click()")
            assertEquals("true",eval(scenario,"document.querySelector('#ex-next').disabled && JSON.parse(AndroidTrainer.getProfile()).xp===321 && JSON.parse(AndroidTrainer.getProfile()).lesson_sessions['5:0'].passed.length===0"))
            scenario.onActivity { activity ->
                (activity.getSystemService(android.content.Context.INPUT_METHOD_SERVICE) as android.view.inputmethod.InputMethodManager).hideSoftInputFromWindow(activity.web.windowToken,0)
                activity.web.settings.textZoom=100
            }
        }
    }
    @Test fun lessonStageAndPagedGuideDoNotRequireVerticalScrolling() {
        ActivityScenario.launch(MainActivity::class.java).use { scenario ->
            waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
            eval(scenario,"document.querySelector('#hero-resume').click()")
            waitFor(scenario,"!!document.querySelector('.focus-sheet:not([hidden])')")
            assertEquals("true",eval(scenario,"document.querySelector('.focus-sheet-reading').scrollHeight<=document.querySelector('.focus-sheet-reading').clientHeight+1"))
            eval(scenario,"JTBack()")
            waitFor(scenario,"document.querySelector('.focus-sheet').hidden")
            assertEquals("true",eval(scenario,"document.querySelector('#advance').disabled && JSON.parse(AndroidTrainer.getProfile()).xp===0"))
            assertEquals("true",eval(scenario,"(()=>{const w=document.querySelector('.focus-workspace');return w.scrollHeight<=w.clientHeight+1 && document.documentElement.scrollHeight<=innerHeight+1})()"))
            assertEquals("true",eval(scenario,"(()=>{const t=document.querySelector('.focus-teacher').getBoundingClientRect(),w=document.querySelector('.focus-workspace').getBoundingClientRect();return t.top>=w.top && t.top<innerHeight-100 && t.width>100})()"))
            assertEquals("true",eval(scenario,"document.querySelector('.focus-page-nav').hidden"))
            println("Native stage viewport and type size: "+eval(scenario,"[innerWidth,innerHeight,getComputedStyle(document.documentElement).fontSize]"))
            screenshot(scenario,"android-stage-without-scroll")
        }
    }
    @Test fun recordingReplayRejectsWrongIdentityAndClearsOnCancel() {
        val context=InstrumentationRegistry.getInstrumentation().targetContext
        val events=java.util.concurrent.LinkedBlockingQueue<String>()
        val engine=SpeechEngine(ModelStore(context)) { type,_ -> events.offer(type) }
        try {
            engine.playRecording("unknown","r1");assertEquals("audioError",events.poll(5,TimeUnit.SECONDS))
            val field=SpeechEngine::class.java.getDeclaredField("ownRecording");field.isAccessible=true
            field.set(engine,Pair("real-id",FloatArray(1600))) // Synthetic RAM buffer, not human speech.
            engine.playRecording("old-id","r2");assertEquals("audioError",events.poll(5,TimeUnit.SECONDS))
            engine.stopAll();assertNull(field.get(engine))
            engine.playRecording("real-id","r3");assertEquals("audioError",events.poll(5,TimeUnit.SECONDS))
        } finally { engine.close() }
    }
    @Test fun realAndroidSpeechModelInferenceWithoutMicrophone() {
        val context=InstrumentationRegistry.getInstrumentation().targetContext
        val models=ModelStore(context)
        models.install { _,_ -> }
        assertTrue(models.ready())
        val engine=SpeechEngine(models) { _,_ -> }
        try {
            val result=engine.diagnostic()
            println("Real Android TTS: 8 voices, 16 normal/slow outputs. SenseVoice recognized: $result")
            assertTrue("Real SenseVoice result: $result",result.contains("ありがとう"))
        } finally { engine.close() }
    }
    @Test fun shortSpeechPreparationRejectsSilenceClicksClippingAndKeepsQuietSignal() {
        val negatives=listOf(FloatArray(32000),FloatArray(16000){if(it==8000).5f else 0f},FloatArray(16000){if(it%2==0)1f else -1f},floatArrayOf(Float.NaN))
        for(x in negatives) { var rejected=false;try{SpeechInput.prepare(x,true)}catch(e:IllegalArgumentException){rejected=true};assertTrue(rejected) }
        val short=FloatArray(1600) { (.003*kotlin.math.sin(2*Math.PI*220*it/16000)).toFloat() }
        val prepared=SpeechInput.prepare(short,true)
        assertTrue(prepared.gain>1f);assertTrue(prepared.gain<=10f);assertEquals(100,prepared.samples.size*1000/16000)
        assertEquals(prepared.samples.size+6400,SpeechInput.padded(prepared.samples).size)
        var longRejected=false;try{SpeechInput.prepare(short,false)}catch(e:IllegalArgumentException){longRejected=true};assertTrue(longRejected)
    }
    @Test fun bundledVadAndShortRecognizerWorkOnActualSyntheticAudio() {
        // Real native model execution on generated audio, explicitly no microphone.
        val context=InstrumentationRegistry.getInstrumentation().targetContext
        val models=ModelStore(context);models.install { _,_ -> }
        val engine=SpeechEngine(models) { _,_ -> }
        try {
            val ttsMethod=SpeechEngine::class.java.getDeclaredMethod("tts").apply { isAccessible=true }
            val tts=ttsMethod.invoke(engine) as com.k2fsa.sherpa.onnx.OfflineTts
            val audio=tts.generateWithConfig("あ",com.k2fsa.sherpa.onnx.GenerationConfig(sid=2,speed=.95f,extra=mapOf("lang" to "ja")))
            val x=FloatArray(audio.samples.size*16000/audio.sampleRate) { i ->
                val position=i.toDouble()*audio.sampleRate/16000;val lo=position.toInt();val hi=minOf(lo+1,audio.samples.lastIndex)
                (audio.samples[lo]*(1-(position-lo))+audio.samples[hi]*(position-lo)).toFloat()*.025f
            }
            val detect=SpeechEngine::class.java.getDeclaredMethod("detectSpeech",FloatArray::class.java,Boolean::class.javaPrimitiveType).apply { isAccessible=true }
            val prepared=SpeechInput.prepare(x,true)
            assertTrue("Quiet synthetic vowel must reach recognition",detect.invoke(engine,prepared.samples,true) as Boolean)
            for(seed in listOf(1L,77L,123L)) {
                val random=java.util.Random(seed);val noise=FloatArray(32000){(random.nextGaussian()*.01).toFloat()}
                assertFalse("Noise must not enable the self-check",detect.invoke(engine,SpeechInput.prepare(noise,true).samples,true) as Boolean)
            }
            val method=SpeechEngine::class.java.getDeclaredMethod("asr",Boolean::class.javaPrimitiveType).apply { isAccessible=true }
            val recognizer=method.invoke(engine,true) as com.k2fsa.sherpa.onnx.OfflineRecognizer
            val stream=recognizer.createStream()
            try { stream.acceptWaveform(SpeechInput.padded(prepared.samples),16000);recognizer.decode(stream)
                val result=recognizer.getResult(stream).text
                println("Native quiet synthetic あ, gain=${prepared.gain}, activeMs=${prepared.activeMs}, transcript=$result")
                assertTrue("The model must produce actual output",result.isNotBlank())
            } finally { stream.release() }
        } finally { engine.close() }
    }
}
