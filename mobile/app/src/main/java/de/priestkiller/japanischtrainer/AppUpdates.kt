package de.priestkiller.japanischtrainer

import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.security.MessageDigest

class AppUpdates(private val context: Context) {
    private fun json(url:String):String {
        val c=ModelStore.connection(url)
        return try { c.inputStream.use { input ->
            String(ModelStore.readLimited(input,2_000_000),Charsets.UTF_8)
        } } finally { c.disconnect() }
    }
    fun check():JSONObject? {
        val releases=JSONArray(json("https://api.github.com/repos/Priestkiller/JapanischTrainer/releases?per_page=30"))
        var newest:JSONObject?=null
        for(i in 0 until releases.length()) {
            val release=releases.getJSONObject(i)
            if(release.optBoolean("draft") || !release.getString("tag_name").startsWith("android-v"))continue
            val assets=release.getJSONArray("assets")
            for(j in 0 until assets.length()) {
                val asset=assets.getJSONObject(j)
                if(asset.getString("name")!="android-update.json")continue
                val info=JSONObject(json(asset.getString("browser_download_url")))
                require(info.getString("package")=="de.priestkiller.japanischtrainer")
                require(info.getString("url").startsWith("https://github.com/Priestkiller/JapanischTrainer/releases/download/android-v"))
                if(info.getInt("code")>BuildConfig.VERSION_CODE && (newest==null || info.getInt("code")>newest!!.getInt("code")))newest=info
            }
        }
        return newest
    }
    fun download(info:JSONObject,progress:(Long,Long)->Unit):File {
        val dir=File(context.cacheDir,"updates").apply { mkdirs() }
        val temp=File(dir,"next.apk.part"); val target=File(dir,"next.apk")
        try {
            ModelStore.download(info.getString("url"),temp,info.getLong("bytes"),info.getString("sha256"),{false},progress)
            verifyPackage(temp,info.getLong("code"))
            if(target.exists())target.delete()
            check(temp.renameTo(target))
            return target
        } finally { temp.delete() }
    }
    @Suppress("DEPRECATION")
    fun verifyPackage(file:File,expected:Long) {
        val pm=context.packageManager
        val candidate=pm.getPackageArchiveInfo(file.absolutePath,PackageManager.GET_SIGNING_CERTIFICATES) ?: error("Ungültige Android-App.")
        val current=pm.getPackageInfo(context.packageName,PackageManager.GET_SIGNING_CERTIFICATES)
        require(candidate.packageName==context.packageName && candidate.longVersionCode==expected && expected>current.longVersionCode) {
            "Das Update passt nicht zu dieser App." }
        fun signatures(info:android.content.pm.PackageInfo)=info.signingInfo!!.apkContentsSigners.map {
            MessageDigest.getInstance("SHA-256").digest(it.toByteArray()).toList()
        }.toSet()
        require(signatures(candidate)==signatures(current)) { "Das Update stammt nicht vom selben Herausgeber." }
    }
}
