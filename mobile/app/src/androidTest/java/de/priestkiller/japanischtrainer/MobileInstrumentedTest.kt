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

@RunWith(AndroidJUnit4::class)
class MobileInstrumentedTest {
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
            eval(scenario,"document.querySelector('#hero-resume').click()")
            waitFor(scenario,"!!document.querySelector('#record')")
            assertEquals("true",eval(scenario,"document.body.innerText.includes('Aussprachehilfe:')"))
            eval(scenario,"document.querySelector('#advance').click()")
            assertEquals("true",eval(scenario,"!!document.querySelector('[data-choice]')"))
            scenario.recreate()
            waitFor(scenario,"document.documentElement.dataset.ready === 'true'")
            eval(scenario,"document.querySelector('#hero-resume').click()")
            waitFor(scenario,"!!document.querySelector('[data-choice]')")
            assertEquals("true",eval(scenario,"document.documentElement.scrollWidth <= innerWidth"))
            eval(scenario,"document.querySelector('#settings-shortcut').click()")
            waitFor(scenario,"!!document.querySelector('#check-updates')")
            assertEquals("true",eval(scenario,"document.body.innerText.includes('Lernstand sichern')"))
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
            assertTrue("Real SenseVoice result: $result",result.contains("ありがとう"))
        } finally { engine.close() }
    }
}
