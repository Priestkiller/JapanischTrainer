package de.priestkiller.japanischtrainer

import android.Manifest
import android.app.Activity
import android.app.AlertDialog
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Color
import android.net.Uri
import android.os.*
import android.provider.Settings
import android.util.AtomicFile
import android.view.ViewGroup
import android.webkit.*
import android.widget.FrameLayout
import androidx.core.content.FileProvider
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.webkit.WebViewAssetLoader
import java.io.ByteArrayInputStream
import java.io.File
import java.util.concurrent.Executors
import org.json.JSONObject
import kotlin.math.roundToInt

class MainActivity:Activity() {
    lateinit var web:WebView; private set
    lateinit var models:ModelStore; private set
    lateinit var speech:SpeechEngine; private set
    private val io=Executors.newSingleThreadExecutor()
    private lateinit var updates:AppUpdates
    private lateinit var profile:AtomicFile
    @Volatile private var downloading=false
    private var pendingRecording:String?=null
    private var pendingShortKana=false
    private var availableUpdate:JSONObject?=null
    private var readyApk:File?=null
    private var exportText:String?=null
    private var closed=false
    private var profileWarning=""

    override fun onCreate(savedInstanceState:Bundle?) {
        super.onCreate(savedInstanceState)
        profile=AtomicFile(File(filesDir,"progress.json")); models=ModelStore(this); updates=AppUpdates(this)
        speech=SpeechEngine(models) { type,data -> emit(type,JSONObject(data)) }
        val root=FrameLayout(this); root.setBackgroundColor(Color.rgb(7,23,45)); setContentView(root)
        web=WebView(this); web.setBackgroundColor(Color.rgb(247,243,237))
        root.addView(web,FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,ViewGroup.LayoutParams.MATCH_PARENT))
        ViewCompat.setOnApplyWindowInsetsListener(root) { v,insets ->
            val bars=insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.displayCutout() or WindowInsetsCompat.Type.ime())
            v.setPadding(bars.left,bars.top,bars.right,bars.bottom); insets
        }
        val loader=WebViewAssetLoader.Builder().addPathHandler("/assets/",WebViewAssetLoader.AssetsPathHandler(this)).build()
        web.settings.apply {
            javaScriptEnabled=true; domStorageEnabled=true
            textZoom=(resources.configuration.fontScale*100).roundToInt().coerceIn(80,200)
            allowFileAccess=false; allowContentAccess=false; mixedContentMode=WebSettings.MIXED_CONTENT_NEVER_ALLOW
            mediaPlaybackRequiresUserGesture=true; setSupportMultipleWindows(false)
        }
        web.webViewClient=object:WebViewClient() {
            override fun shouldInterceptRequest(view:WebView,request:WebResourceRequest):WebResourceResponse {
                if(request.url.scheme=="https" && request.url.host=="appassets.androidplatform.net") {
                    return loader.shouldInterceptRequest(request.url) ?: blocked()
                }
                return blocked()
            }
            private fun blocked()=WebResourceResponse("text/plain","UTF-8",403,"Blocked",mapOf(),ByteArrayInputStream(ByteArray(0)))
            override fun shouldOverrideUrlLoading(view:WebView,request:WebResourceRequest):Boolean =
                request.url.scheme!="https" || request.url.host!="appassets.androidplatform.net"
            override fun onPageFinished(view:WebView,url:String) { emit("capabilities",capabilities()) }
        }
        web.webChromeClient=WebChromeClient() // Web pages never get direct microphone permission.
        web.addJavascriptInterface(Bridge(),"AndroidTrainer")
        WebView.setWebContentsDebuggingEnabled(BuildConfig.DEBUG)
        web.loadUrl("https://appassets.androidplatform.net/assets/index.html")
        if(Build.VERSION.SDK_INT>=33) onBackInvokedDispatcher.registerOnBackInvokedCallback(0) { goBack() }
    }
    private fun goBack() { web.evaluateJavascript("window.JTBack && window.JTBack()",null) }
    @Deprecated("Handled through the platform dispatcher on Android 13+")
    override fun onBackPressed() { goBack() }
    private fun emit(type:String,data:JSONObject=JSONObject()) {
        runOnUiThread { if(!closed) web.evaluateJavascript("window.JTNative && window.JTNative(${JSONObject.quote(type)},$data)",null) }
    }
    private fun capabilities()=JSONObject().put("native",true).put("models",models.ready())
        .put("modelBytes",models.manifest.getLong("bytes")).put("version",BuildConfig.VERSION_NAME).put("profileWarning",profileWarning)
    private fun message(text:String) { emit("message",JSONObject().put("message",text)) }
    private fun save(text:String):Boolean {
        if(text.length>2_000_000)return false
        return synchronized(profile) {
            var output:java.io.FileOutputStream?=null
            try {
                val data=JSONObject(text)
                require(data.optJSONArray("completed")!=null && data.optInt("xp",-1)>=0)
                output=profile.startWrite(); output.write(text.toByteArray(Charsets.UTF_8)); profile.finishWrite(output); true
            } catch(e:Exception) { if(output!=null)profile.failWrite(output); false }
        }
    }
    inner class Bridge {
        @JavascriptInterface fun getProfile():String = synchronized(profile) {
            if(!profile.baseFile.exists() && !File(profile.baseFile.path+".bak").exists())return@synchronized "{}"
            val bytes=profile.readFully()
            val raw=String(bytes,Charsets.UTF_8).removePrefix("\uFEFF")
            try {
                val parsed=JSONObject(raw)
                require(parsed.optJSONArray("completed")!=null && parsed.optInt("xp",-1)>=0)
                raw
            } catch(e:Exception) {
                File(filesDir,"progress-unreadable-${System.currentTimeMillis()}.json").writeBytes(bytes)
                profileWarning="Die Lernstand-Datei war nicht lesbar und wurde intern gesichert. Du kannst eine JSON-Sicherung importieren."
                "{}"
            }
        }
        @JavascriptInterface fun saveProfile(json:String)=save(json)
        @JavascriptInterface fun getCapabilities()=capabilities().toString()
        @JavascriptInterface fun speak(text:String,sid:Int,speed:Double,request:String) {
            if(text.isBlank()||text.length>1000||sid !in 0..9||speed !in .5..1.4||request.length>100)return
            speech.speak(text,sid,speed.toFloat(),request)
        }
        @JavascriptInterface fun stopAudio() { speech.stopPlayback() }
        @JavascriptInterface fun playRecording(original:String,request:String) {
            if(original.length<=100 && request.length<=100)speech.playRecording(original,request)
        }
        @JavascriptInterface fun record(request:String) = recordForMode(request,false)
        @JavascriptInterface fun recordKana(request:String) = recordForMode(request,true)
        private fun recordForMode(request:String,shortKana:Boolean) { runOnUiThread {
            if(request.length>100)return@runOnUiThread
            if(checkSelfPermission(Manifest.permission.RECORD_AUDIO)==PackageManager.PERMISSION_GRANTED) speech.startRecording(request,shortKana)
            else { pendingRecording=request;pendingShortKana=shortKana;requestPermissions(arrayOf(Manifest.permission.RECORD_AUDIO),10) }
        } }
        @JavascriptInterface fun stopRecording(cancel:Boolean) { pendingRecording=null; speech.stopRecording(cancel) }
        @JavascriptInterface fun downloadModels() { runOnUiThread { askModels() } }
        @JavascriptInterface fun cancelDownload() { models.cancelled=true }
        @JavascriptInterface fun checkUpdates() { runOnUiThread { checkUpdate() } }
        @JavascriptInterface fun checkTestUpdates() { runOnUiThread { checkUpdate(true) } }
        @JavascriptInterface fun installUpdate() { runOnUiThread { this@MainActivity.installUpdate() } }
        @JavascriptInterface fun exportProfile(json:String) { runOnUiThread {
            if(json.length>2_000_000)return@runOnUiThread
            exportText=json
            startActivityForResult(Intent(Intent.ACTION_CREATE_DOCUMENT).addCategory(Intent.CATEGORY_OPENABLE)
                .setType("application/json").putExtra(Intent.EXTRA_TITLE,"JapanischTrainer-Lernstand.json"),20)
        } }
        @JavascriptInterface fun importProfile() { runOnUiThread {
            startActivityForResult(Intent(Intent.ACTION_OPEN_DOCUMENT).addCategory(Intent.CATEGORY_OPENABLE).setType("*/*"),21)
        } }
        @JavascriptInterface fun confirmImport(json:String) { runOnUiThread {
            if(json.length>2_000_000)return@runOnUiThread
            AlertDialog.Builder(this@MainActivity).setTitle("Lernstand übernehmen?")
                .setMessage("Der aktuelle Lernstand wird zuvor in der App gesichert. Danach ersetzt die gewählte Datei den Lernstand auf diesem Handy.")
                .setNegativeButton("Abbrechen",null).setPositiveButton("Übernehmen") { _,_ ->
                    val current=getProfile()
                    File(filesDir,"before-import-${System.currentTimeMillis()}.json").writeText(current)
                    if(save(json))emit("profileImported",JSONObject(json)) else message("Lernstand konnte nicht gespeichert werden.")
                }.show()
        } }
        @JavascriptInterface fun closeApp() { runOnUiThread { moveTaskToBack(true) } }
    }
    private fun askModels() {
        if(downloading || models.ready())return
        val size=models.manifest.getLong("bytes")/1_000_000
        AlertDialog.Builder(this).setTitle("Lokales Sprachpaket laden")
            .setMessage("Einmalig ca. $size MB von GitHub herunterladen, am besten über WLAN. Danach arbeiten Lehrer-Stimmen und Erkennung offline. Benötigt etwa 900 MB freien Speicher während des Downloads. Es gelten die unter Einstellungen → Lizenzen angezeigten Modellbedingungen.")
            .setNegativeButton("Abbrechen",null).setPositiveButton("Laden") { _,_ ->
                downloading=true; emit("modelProgress",JSONObject().put("done",0).put("total",models.manifest.getLong("bytes")))
                io.execute {
                    try { models.install { done,total -> emit("modelProgress",JSONObject().put("done",done).put("total",total)) }; emit("modelsReady",capabilities()) }
                    catch(e:Exception) { emit("modelError",JSONObject().put("message",e.message?:"Sprachpaket konnte nicht geladen werden.")) }
                    finally { downloading=false }
                }
            }.show()
    }
    private fun checkUpdate(testChannel:Boolean=false) {
        if(downloading)return
        availableUpdate=null; readyApk=null
        downloading=true; emit("updateChecking",JSONObject().put("test",testChannel))
        io.execute {
            try { availableUpdate=updates.check(testChannel); emit(if(availableUpdate==null)"updateCurrent" else "updateAvailable",(availableUpdate?:JSONObject()).put("test",testChannel)) }
            catch(e:Exception) { emit("updateError",JSONObject().put("message","Updates derzeit nicht erreichbar. Bitte später erneut versuchen.")) }
            finally { downloading=false }
        }
    }
    private fun installUpdate() {
        if(readyApk!=null) { launchInstaller(); return }
        val info=availableUpdate?:return
        if(downloading)return
        downloading=true; emit("updateProgress",JSONObject().put("done",0).put("total",info.getLong("bytes")))
        io.execute {
            try { readyApk=updates.download(info) { done,total -> emit("updateProgress",JSONObject().put("done",done).put("total",total)) }
                runOnUiThread { launchInstaller() }
            } catch(e:Exception) { emit("updateError",JSONObject().put("message",e.message?:"Update fehlgeschlagen.")) }
            finally { downloading=false }
        }
    }
    private fun launchInstaller() {
        val file=readyApk?:return
        if(!packageManager.canRequestPackageInstalls()) {
            AlertDialog.Builder(this).setTitle("Update erlauben")
                .setMessage("Android benötigt deine Freigabe für Updates aus dieser App. Erlaube sie in den folgenden Einstellungen und tippe danach erneut auf „Update installieren“.")
                .setNegativeButton("Später",null).setPositiveButton("Einstellungen") { _,_ ->
                    startActivity(Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,Uri.parse("package:$packageName")))
                }.show()
            emit("updateReady"); return
        }
        val uri=FileProvider.getUriForFile(this,"$packageName.files",file)
        startActivity(Intent(Intent.ACTION_VIEW).setDataAndType(uri,"application/vnd.android.package-archive")
            .addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION))
        emit("updateReady")
    }
    override fun onRequestPermissionsResult(requestCode:Int,permissions:Array<out String>,grantResults:IntArray) {
        super.onRequestPermissionsResult(requestCode,permissions,grantResults)
        val request=pendingRecording; pendingRecording=null
        if(requestCode==10 && request!=null) {
            if(grantResults.firstOrNull()==PackageManager.PERMISSION_GRANTED)speech.startRecording(request,pendingShortKana)
            else emit("speechError",JSONObject().put("request",request).put("message","Mikrofonzugriff nicht erlaubt. Du kannst ihn in den Android-App-Einstellungen erlauben."))
        }
    }
    @Deprecated("Platform document picker callback")
    override fun onActivityResult(requestCode:Int,resultCode:Int,data:Intent?) {
        super.onActivityResult(requestCode,resultCode,data)
        if(resultCode!=RESULT_OK) { exportText=null; return }
        val uri=data?.data?:return
        try {
            when(requestCode) {
                20 -> { val text=exportText?:return; contentResolver.openOutputStream(uri,"wt")!!.bufferedWriter().use { it.write(text) }; message("Lernstand exportiert.") }
                21 -> { val bytes=contentResolver.openInputStream(uri)!!.use { ModelStore.readLimited(it,2_000_000) }
                    require(bytes.size<=2_000_000); emit("profileCandidate",JSONObject().put("json",String(bytes,Charsets.UTF_8).removePrefix("\uFEFF"))) }
            }
        } catch(e:Exception) { message("Die Datei konnte nicht gelesen oder gespeichert werden.") }
        finally { exportText=null }
    }
    override fun onStop() { super.onStop(); pendingRecording=null; speech.stopAll(); emit("audioCancelled") }
    override fun onDestroy() {
        closed=true; models.cancelled=true; speech.close(); io.shutdownNow()
        web.removeJavascriptInterface("AndroidTrainer"); web.destroy(); super.onDestroy()
    }
}
