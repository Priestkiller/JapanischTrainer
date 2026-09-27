package de.priestkiller.japanischtrainer

import androidx.test.core.app.ActivityScenario
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.*
import org.junit.Test
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
            assertEquals("true",eval(scenario,"document.body.innerText.includes('Aussprachehilfe:')"))
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
            assertEquals("true",eval(scenario,"document.body.innerText.includes('Lernstand sichern')"))
            scenario.onActivity { it.web.settings.textZoom=150 }
            Thread.sleep(500)
            assertEquals("true",eval(scenario,"document.documentElement.scrollWidth <= innerWidth"))
            screenshot(scenario,"android-settings-large-text")
            scenario.onActivity { it.requestedOrientation=ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE }
            InstrumentationRegistry.getInstrumentation().waitForIdleSync()
            waitFor(scenario,"innerWidth > innerHeight && document.documentElement.dataset.ready === 'true' && !!document.querySelector('#hero-resume')")
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
}
