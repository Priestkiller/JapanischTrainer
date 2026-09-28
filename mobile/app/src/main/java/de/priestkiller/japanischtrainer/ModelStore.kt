package de.priestkiller.japanischtrainer

import android.content.Context
import org.json.JSONObject
import java.io.File
import java.net.HttpURLConnection
import java.net.URL
import java.security.MessageDigest
import java.util.zip.ZipFile

/** Model identity is pinned inside the signed APK. No downloaded executable code. */
class ModelStore(private val context: Context) {
    val assets get() = context.assets
    val manifest = JSONObject(context.assets.open("model-pack.json").bufferedReader().use { it.readText() })
    val directory = File(context.filesDir, "models-${manifest.getInt("version")}")
    @Volatile var cancelled = false
    fun ready(): Boolean = File(directory, "verified.sha256").let {
        it.isFile && it.readText() == manifest.getString("sha256") &&
            (0 until manifest.getJSONArray("files").length()).all { i ->
                val item = manifest.getJSONArray("files").getJSONObject(i)
                File(directory, item.getString("path")).length() == item.getLong("size")
            }
    }
    fun path(name: String) = File(directory, name).absolutePath
    fun install(progress: (Long, Long) -> Unit) {
        if (ready()) return
        cancelled = false
        val archive = File(context.cacheDir, "speech.zip.part")
        val stage = File(context.filesDir, "models-staging")
        stage.deleteRecursively(); stage.mkdirs()
        try {
            download(manifest.getString("url"), archive, manifest.getLong("bytes"), manifest.getString("sha256"),
                { cancelled }, progress)
            ZipFile(archive).use { zip ->
                val records = manifest.getJSONArray("files")
                require(zip.size() == records.length()) { "Unerwarteter Paketinhalt." }
                for (i in 0 until records.length()) {
                    check(!cancelled) { "Download abgebrochen." }
                    val record = records.getJSONObject(i)
                    val name = record.getString("path")
                    val file = File(stage, name)
                    require(file.canonicalPath.startsWith(stage.canonicalPath + File.separator))
                    val entry = zip.getEntry(name) ?: error("Unvollständiges Sprachpaket.")
                    require(!entry.isDirectory && entry.size == record.getLong("size"))
                    file.parentFile!!.mkdirs()
                    zip.getInputStream(entry).use { input -> file.outputStream().use { output ->
                        val buffer = ByteArray(65536); var total = 0L
                        while (true) {
                            check(!cancelled) { "Download abgebrochen." }
                            val n = input.read(buffer); if (n < 0) break
                            total += n; require(total <= record.getLong("size"))
                            output.write(buffer, 0, n)
                        }
                        require(total == record.getLong("size"))
                    } }
                    require(hash(file) == record.getString("sha256")) { "Dateiprüfung fehlgeschlagen." }
                }
            }
            File(stage, "verified.sha256").writeText(manifest.getString("sha256"))
            if (directory.exists()) directory.deleteRecursively() // Only this app's incomplete model version.
            check(stage.renameTo(directory)) { "Sprachpaket konnte nicht gespeichert werden." }
        } finally { archive.delete(); stage.deleteRecursively() }
    }
    companion object {
        fun readLimited(input:java.io.InputStream,limit:Int):ByteArray {
            val output=java.io.ByteArrayOutputStream(); val buffer=ByteArray(8192)
            while(true) { val n=input.read(buffer); if(n<0)break; require(output.size()+n<=limit) { "Datei ist zu groß." }; output.write(buffer,0,n) }
            return output.toByteArray()
        }
        fun hash(file: File): String {
            val digest = MessageDigest.getInstance("SHA-256")
            file.inputStream().use { input -> val b = ByteArray(65536)
                while (true) { val n=input.read(b); if(n<0)break; digest.update(b,0,n) }
            }
            return digest.digest().joinToString("") { "%02x".format(it) }
        }
        fun connection(address: String): HttpURLConnection {
            var url = URL(address)
            repeat(6) {
                require(url.protocol == "https" && url.userInfo == null) { "Unsichere Download-Adresse." }
                val connection = url.openConnection() as HttpURLConnection
                connection.connectTimeout = 20000; connection.readTimeout = 30000
                connection.instanceFollowRedirects = false
                connection.setRequestProperty("User-Agent", "JapanischTrainer-Android/${BuildConfig.VERSION_NAME}")
                if (connection.responseCode in listOf(301,302,303,307,308)) {
                    val location=connection.getHeaderField("Location") ?: error("Download-Weiterleitung fehlt.")
                    connection.disconnect(); url=URL(url,location)
                } else { require(connection.responseCode == 200) { "Download nicht erreichbar (${connection.responseCode})." }; return connection }
            }
            error("Zu viele Weiterleitungen.")
        }
        fun download(url: String, target: File, size: Long, sha: String, cancel: () -> Boolean,
                     progress: (Long, Long) -> Unit) {
            require(size in 1..600_000_000L && sha.matches(Regex("[a-f0-9]{64}")))
            val connection=connection(url)
            try {
                connection.inputStream.use { input -> target.outputStream().use { output ->
                    val b=ByteArray(65536); var total=0L; var last=0L
                    while (true) {
                        check(!cancel()) { "Download abgebrochen." }
                        val n=input.read(b); if(n<0)break
                        total+=n; require(total<=size) { "Download ist größer als erwartet." }
                        output.write(b,0,n)
                        if(System.currentTimeMillis()-last>200) { progress(total,size); last=System.currentTimeMillis() }
                    }
                    require(total==size) { "Download ist unvollständig." }
                } }
                require(hash(target)==sha) { "Download-Prüfsumme stimmt nicht." }
                progress(size,size)
            } finally { connection.disconnect() }
        }
    }
}
