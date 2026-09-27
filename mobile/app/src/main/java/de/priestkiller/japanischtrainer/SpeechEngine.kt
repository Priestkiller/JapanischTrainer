package de.priestkiller.japanischtrainer

import android.media.*
import com.k2fsa.sherpa.onnx.*
import java.util.concurrent.Executors
import java.util.concurrent.atomic.AtomicLong
import kotlin.math.abs
import kotlin.math.sqrt

/** Audio stays in memory; never uploaded and never written to a recording file. */
class SpeechEngine(private val models: ModelStore, private val event: (String, Map<String, Any>) -> Unit) {
    private val worker = Executors.newSingleThreadExecutor()
    private var tts: OfflineTts? = null
    private var recognizer: OfflineRecognizer? = null
    private val generation=AtomicLong()
    @Volatile private var playback: AudioTrack? = null
    @Volatile private var recording=false
    @Volatile private var cancelRecording=false
    @Volatile private var decoding=false
    @Volatile private var destroyed=false
    private var recorder: AudioRecord? = null

    private fun tts(): OfflineTts {
        check(models.ready()) { "Bitte zuerst das Sprachpaket unter Einstellungen laden." }
        if(tts==null) {
            recognizer?.release(); recognizer=null // Bound mobile RAM: one large model at a time.
            fun p(n:String)=models.path("supertonic/$n")
            tts=OfflineTts(config=OfflineTtsConfig(model=OfflineTtsModelConfig(
                supertonic=OfflineTtsSupertonicModelConfig(
                    durationPredictor=p("duration_predictor.int8.onnx"),textEncoder=p("text_encoder.int8.onnx"),
                    vectorEstimator=p("vector_estimator.int8.onnx"),vocoder=p("vocoder.int8.onnx"),
                    ttsJson=p("tts.json"),unicodeIndexer=p("unicode_indexer.bin"),voiceStyle=p("voice.bin")),numThreads=2)))
        }
        return tts!!
    }
    private fun asr(): OfflineRecognizer {
        check(models.ready()) { "Das lokale Sprachpaket fehlt." }
        if(recognizer==null) {
            tts?.release(); tts=null
            recognizer=OfflineRecognizer(config=OfflineRecognizerConfig(modelConfig=OfflineModelConfig(
                senseVoice=OfflineSenseVoiceModelConfig(model=models.path("sensevoice/model.int8.onnx"),language="ja",useInverseTextNormalization=true),
                tokens=models.path("sensevoice/tokens.txt"),numThreads=2)))
        }
        return recognizer!!
    }
    fun speak(text:String, sid:Int, speed:Float, request:String) {
        if(recording || decoding) { event("audioError",mapOf("request" to request,"message" to "Bitte die Aufnahme zuerst beenden.")); return }
        stopPlayback()
        val id=generation.get()
        worker.execute {
            try {
                if(destroyed || id!=generation.get())return@execute
                event("audioLoading",mapOf("request" to request))
                val audio=tts().generateWithConfig(text,GenerationConfig(sid=sid,speed=speed,extra=mapOf("lang" to "ja")))
                if(destroyed || id!=generation.get())return@execute
                val track=AudioTrack.Builder().setAudioAttributes(AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH).build())
                    .setAudioFormat(AudioFormat.Builder().setEncoding(AudioFormat.ENCODING_PCM_FLOAT)
                        .setSampleRate(audio.sampleRate).setChannelMask(AudioFormat.CHANNEL_OUT_MONO).build())
                    .setTransferMode(AudioTrack.MODE_STREAM).setBufferSizeInBytes(maxOf(16384,
                        AudioTrack.getMinBufferSize(audio.sampleRate,AudioFormat.CHANNEL_OUT_MONO,AudioFormat.ENCODING_PCM_FLOAT))).build()
                playback=track
                try {
                    track.play(); event("audioStarted",mapOf("request" to request))
                    var offset=0
                    while(offset<audio.samples.size && id==generation.get() && !destroyed) {
                        val n=track.write(audio.samples,offset,minOf(4096,audio.samples.size-offset),AudioTrack.WRITE_BLOCKING)
                        check(n>0) { "Audiowiedergabe fehlgeschlagen." }; offset+=n
                    }
                    while(id==generation.get() && !destroyed && track.playbackHeadPosition<offset) Thread.sleep(20)
                    if(id==generation.get() && !destroyed)event("audioDone",mapOf("request" to request))
                } finally { playback=null; runCatching { track.stop() }; track.release() }
            } catch(e:Exception) { if(id==generation.get()&&!destroyed)event("audioError",mapOf("request" to request,"message" to (e.message?:"Stimme nicht verfügbar."))) }
        }
    }
    fun stopPlayback() { generation.incrementAndGet(); runCatching { playback?.pause(); playback?.flush() } }
    @Suppress("MissingPermission")
    fun startRecording(request:String) {
        if(recording||decoding||destroyed)return
        stopPlayback()
        if(!models.ready()) { event("speechError",mapOf("request" to request,"message" to "Bitte zuerst das Sprachpaket laden.")); return }
        cancelRecording=false; recording=true
        Thread({
            val chunks=ArrayList<FloatArray>(); var count=0; var peak=0f; var sum=0.0; var voiced=0
            try {
                val size=maxOf(4096,AudioRecord.getMinBufferSize(16000,AudioFormat.CHANNEL_IN_MONO,AudioFormat.ENCODING_PCM_16BIT))
                val mic=AudioRecord(MediaRecorder.AudioSource.VOICE_RECOGNITION,16000,AudioFormat.CHANNEL_IN_MONO,AudioFormat.ENCODING_PCM_16BIT,size)
                recorder=mic
                check(mic.state==AudioRecord.STATE_INITIALIZED) { "Mikrofon konnte nicht gestartet werden." }
                try {
                    if(cancelRecording || destroyed)return@Thread
                    mic.startRecording(); event("recording",mapOf("request" to request))
                    val buffer=ShortArray(1600)
                    while(recording&&!cancelRecording&&count<16000*15) {
                        val n=mic.read(buffer,0,buffer.size)
                        if(n<0) { if(!recording)break; error("Mikrofon wurde unterbrochen.") }
                        if(n==0)continue
                        val chunk=FloatArray(n) { buffer[it]/32768f }
                        chunk.forEach { peak=maxOf(peak,abs(it)); sum+=it*it; if(abs(it)>.015f)voiced++ }
                        chunks.add(chunk); count+=n
                    }
                } finally { runCatching { mic.stop() }; mic.release(); recorder=null; recording=false }
                if(cancelRecording||destroyed)return@Thread
                check(count>=6400 && peak>.012 && sqrt(sum/maxOf(1,count))>.002 && voiced>600) {
                    "Zu wenig Sprache erkannt. Bitte etwas näher ans Mikrofon sprechen und erneut versuchen." }
                val samples=FloatArray(count); var pos=0
                chunks.forEach { it.copyInto(samples,pos); pos+=it.size }
                decoding=true; event("recognizing",mapOf("request" to request))
                worker.execute {
                    try {
                        if(cancelRecording||destroyed)return@execute
                        val engine=asr(); val stream=engine.createStream()
                        val text=try { stream.acceptWaveform(samples,16000); engine.decode(stream); engine.getResult(stream).text.trim() } finally { stream.release() }
                        if(!cancelRecording&&!destroyed) {
                            check(text.isNotBlank()) { "Keine verständliche Sprache erkannt. Bitte erneut versuchen." }
                            event("speechResult",mapOf("request" to request,"text" to text))
                        }
                    } catch(e:Exception) { if(!cancelRecording&&!destroyed)event("speechError",mapOf("request" to request,"message" to (e.message?:"Erkennung fehlgeschlagen."))) }
                    finally { decoding=false }
                }
            } catch(e:Exception) { recording=false; if(!cancelRecording&&!destroyed)event("speechError",mapOf("request" to request,"message" to (e.message?:"Mikrofon nicht verfügbar."))) }
        },"JapaneseMicrophone").start()
    }
    fun stopRecording(cancel:Boolean=false) { cancelRecording=cancel; recording=false; runCatching { recorder?.stop() } }
    fun stopAll() { stopPlayback(); stopRecording(true) }
    fun close() { destroyed=true; stopAll(); worker.execute { tts?.release(); recognizer?.release() }; worker.shutdown() }
    // Instrumented test: real synthesis and recognition, no microphone or speaker involved.
    fun diagnostic(): String {
        var first:GeneratedAudio?=null
        val speakers=intArrayOf(2,0,6,9,1,3,7,4)
        val speeds=floatArrayOf(.95f,.90f,.93f,1.03f,.87f,1.05f,.94f,.99f)
        for(i in speakers.indices) {
            val normal=tts().generateWithConfig("ありがとうございます。",GenerationConfig(sid=speakers[i],speed=speeds[i],extra=mapOf("lang" to "ja")))
            val slow=tts().generateWithConfig("ありがとうございます。",GenerationConfig(sid=speakers[i],speed=speeds[i]*.72f,extra=mapOf("lang" to "ja")))
            check(normal.samples.size>1000 && slow.samples.size>normal.samples.size)
            if(first==null)first=normal
        }
        val audio=first!!
        val engine=asr(); val stream=engine.createStream()
        return try { stream.acceptWaveform(audio.samples,audio.sampleRate); engine.decode(stream); engine.getResult(stream).text } finally { stream.release() }
    }
}
