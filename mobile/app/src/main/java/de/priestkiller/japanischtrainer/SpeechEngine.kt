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
    private var recognizerShort=false
    private var recognizerKind=""
    var alternatives:Map<String,ModelStore> = emptyMap()
    @Volatile var selectedRecognizer="sensevoice"
    private val captureGeneration=AtomicLong()
    @Volatile private var captureBusy=false
    private val generation=AtomicLong()
    @Volatile private var playback: AudioTrack? = null
    @Volatile private var recording=false
    @Volatile private var cancelRecording=false
    @Volatile private var decoding=false
    @Volatile private var destroyed=false
    private var recorder: AudioRecord? = null
    @Volatile private var ownRecording: Pair<String,FloatArray>? = null

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
    @JvmOverloads private fun asr(shortKana:Boolean=false,kind:String=selectedRecognizer): OfflineRecognizer {
        check(models.ready()) { "Das lokale Sprachpaket fehlt." }
        if(recognizer!=null && (recognizerShort!=shortKana||recognizerKind!=kind)) { recognizer?.release();recognizer=null }
        if(recognizer==null) {
            tts?.release(); tts=null
            val extra=alternatives[kind]
            if(kind!="sensevoice")check(extra?.ready()==true) { "Das gewählte Testmodell fehlt. Wähle SenseVoice oder lade das Testmodell vollständig." }
            val model=when(kind) {
                "reazonspeech" -> OfflineModelConfig(transducer=OfflineTransducerModelConfig(
                    encoder=extra!!.path("encoder-epoch-99-avg-1.int8.onnx"),decoder=extra.path("decoder-epoch-99-avg-1.int8.onnx"),joiner=extra.path("joiner-epoch-99-avg-1.int8.onnx")),tokens=extra.path("tokens.txt"),numThreads=2)
                "qwen3" -> OfflineModelConfig(qwen3Asr=OfflineQwen3AsrModelConfig(convFrontend=extra!!.path("conv_frontend.onnx"),encoder=extra.path("encoder.int8.onnx"),decoder=extra.path("decoder.int8.onnx"),tokenizer=extra.path("tokenizer"),maxNewTokens=80),numThreads=2)
                else -> OfflineModelConfig(
                senseVoice=OfflineSenseVoiceModelConfig(model=models.path("sensevoice/model.int8.onnx"),language="ja",useInverseTextNormalization=!shortKana),
                tokens=models.path("sensevoice/tokens.txt"),numThreads=2)
            }
            recognizer=OfflineRecognizer(config=OfflineRecognizerConfig(featConfig=FeatureConfig(featureDim=if(kind=="qwen3")128 else 80),modelConfig=model))
            recognizerShort=shortKana
            recognizerKind=kind
        }
        return recognizer!!
    }
    fun speak(text:String, sid:Int, speed:Float, request:String) {
        if(recording || decoding || captureBusy) { event("audioError",mapOf("request" to request,"message" to "Bitte die Aufnahme zuerst beenden.")); return }
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
    /** Only the latest explicitly identified recording, in RAM, can be replayed. */
    fun playRecording(original:String, request:String) {
        val own=ownRecording
        if(recording || decoding || captureBusy || own==null || own.first!=original) {
            event("audioError",mapOf("request" to request,"message" to "Diese Aufnahme ist nicht mehr verfügbar.")); return
        }
        stopPlayback(); val id=generation.get(); val samples=own.second
        worker.execute {
            try {
                if(destroyed || id!=generation.get())return@execute
                val track=AudioTrack.Builder().setAudioAttributes(AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH).build())
                    .setAudioFormat(AudioFormat.Builder().setEncoding(AudioFormat.ENCODING_PCM_FLOAT).setSampleRate(16000)
                        .setChannelMask(AudioFormat.CHANNEL_OUT_MONO).build())
                    .setTransferMode(AudioTrack.MODE_STREAM).setBufferSizeInBytes(maxOf(16384,
                        AudioTrack.getMinBufferSize(16000,AudioFormat.CHANNEL_OUT_MONO,AudioFormat.ENCODING_PCM_FLOAT))).build()
                playback=track
                try {
                    track.play();event("audioStarted",mapOf("request" to request));var offset=0
                    while(offset<samples.size && id==generation.get() && !destroyed) {
                        val n=track.write(samples,offset,minOf(4096,samples.size-offset),AudioTrack.WRITE_BLOCKING)
                        check(n>0) { "Wiedergabe fehlgeschlagen." };offset+=n
                    }
                    while(id==generation.get()&&!destroyed&&track.playbackHeadPosition<offset)Thread.sleep(20)
                    if(id==generation.get()&&!destroyed)event("audioDone",mapOf("request" to request))
                } finally { playback=null;runCatching { track.stop() };track.release() }
            } catch(e:Exception) { if(id==generation.get()&&!destroyed)event("audioError",mapOf("request" to request,"message" to (e.message?:"Wiedergabe fehlgeschlagen."))) }
        }
    }
    @Suppress("MissingPermission")
    @Synchronized fun startRecording(request:String,shortKana:Boolean=false,comparison:Boolean=false) {
        if(destroyed)return
        if(recording||decoding||captureBusy) {
            event("speechError",mapOf("request" to request,"message" to "Die vorherige Aufnahme wird noch beendet. Bitte gleich erneut versuchen."))
            return
        }
        stopPlayback()
        if(!models.ready()) { event("speechError",mapOf("request" to request,"message" to "Bitte zuerst das Sprachpaket laden.")); return }
        ownRecording=null; cancelRecording=false; recording=true;captureBusy=true
        val capture=captureGeneration.incrementAndGet()
        Thread({
            val chunks=ArrayList<FloatArray>(); var count=0;var lastSound=0;var soundFrames=0;var dispatched=false
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
                        chunks.add(chunk); count+=n
                        val rms=sqrt(chunk.sumOf { (it*it).toDouble() }/chunk.size)
                        if(rms>.0015) { lastSound=count;soundFrames++ }
                        event("speechLevel",mapOf("request" to request,"level" to minOf(1.0,rms*15),"seconds" to count/16000.0))
                        // Kana need only a short utterance. Leave a generous tail; manual stop remains.
                        if(shortKana && soundFrames>=1 && count-lastSound>=16000 && count>=16000)recording=false
                    }
                } finally { runCatching { mic.stop() }; mic.release(); recorder=null; recording=false }
                if(cancelRecording||destroyed||capture!=captureGeneration.get())return@Thread
                val samples=FloatArray(count); var pos=0
                chunks.forEach { it.copyInto(samples,pos); pos+=it.size }
                ownRecording=request to samples
                decoding=true; event("recognizing",mapOf("request" to request))
                worker.execute {
                    try {
                        if(cancelRecording||destroyed||capture!=captureGeneration.get())return@execute
                        val prepared=SpeechInput.prepare(samples,shortKana)
                        if(!detectSpeech(prepared.samples,shortKana)) {
                            event("speechError",mapOf("request" to request,"reason" to "no_voice","message" to "Keine sichere Stimme erkannt. Bei der Stilleprobe ist das erwartbar."));return@execute
                        }
                        val results=ArrayList<Map<String,Any>>()
                        val kinds=if(comparison) listOf("sensevoice")+alternatives.filterValues { it.ready() }.keys else listOf(selectedRecognizer)
                        for(kind in kinds) {
                            if(cancelRecording||destroyed||capture!=captureGeneration.get())return@execute
                            try {results.add(decodeOne(prepared.samples,shortKana,kind))}
                            catch(e:Exception){if(!comparison)throw e;results.add(mapOf("model" to kind,"text" to "","error" to (e.message?:"Modellfehler")))}
                        }
                        val text=results.first()["text"] as String
                        if(!cancelRecording&&!destroyed&&capture==captureGeneration.get()) {
                            if(!comparison&&!shortKana)check(text.isNotBlank()) { "Keine verständliche Sprache erkannt. Bitte erneut versuchen." }
                            event("speechResult",mapOf("request" to request,"text" to text,"results" to results,"comparison" to comparison,"audioQualified" to true,"shortKana" to shortKana,
                                "gain" to prepared.gain,"activeMs" to prepared.activeMs))
                        }
                    } catch(e:Exception) { if(!cancelRecording&&!destroyed&&capture==captureGeneration.get())event("speechError",mapOf("request" to request,"reason" to (if(e is SpeechInput.NoVoice)"no_voice" else "technical"),"message" to (e.message?:"Erkennung fehlgeschlagen."))) }
                    finally { decoding=false;captureBusy=false }
                }
                dispatched=true
            } catch(e:Exception) { recording=false; if(!cancelRecording&&!destroyed&&capture==captureGeneration.get())event("speechError",mapOf("request" to request,"message" to (e.message?:"Mikrofon nicht verfügbar."))) }
            finally { if(!dispatched){captureBusy=false;decoding=false} }
        },"JapaneseMicrophone").start()
    }
    private fun detectSpeech(samples:FloatArray,shortKana:Boolean):Boolean {
        val vad=Vad(assetManager=models.assets,config=VadModelConfig(sileroVadModelConfig=SileroVadModelConfig(
            model="speech/silero_vad.onnx",threshold=.5f,minSpeechDuration=if(shortKana).064f else .128f,minSilenceDuration=.3f)))
        return try { var offset=0
            while(offset+512<=samples.size){vad.acceptWaveform(samples.copyOfRange(offset,offset+512));offset+=512}
            if(offset<samples.size)vad.acceptWaveform(FloatArray(512).also { samples.copyInto(it,0,offset) })
            vad.flush();!vad.empty()
        } finally { vad.release() }
    }
    fun stopRecording(cancel:Boolean=false) { cancelRecording=cancel; recording=false; if(cancel){captureGeneration.incrementAndGet();ownRecording=null}; runCatching { recorder?.stop() } }
    fun stopAll() { stopPlayback(); stopRecording(true) }
    fun close() { destroyed=true; stopAll(); worker.execute { tts?.release(); recognizer?.release() }; worker.shutdown() }
    private fun decodeOne(samples:FloatArray,shortKana:Boolean,kind:String):Map<String,Any> {
        val started=System.nanoTime();val engine=asr(shortKana,kind);val loaded=System.nanoTime();val stream=engine.createStream()
        val text=try {
            if(kind=="qwen3")stream.setOption("language","Japanese")
            stream.acceptWaveform(SpeechInput.padded(samples),16000);engine.decode(stream);engine.getResult(stream).text.trim()
        } finally {stream.release()}
        return mapOf("model" to kind,"text" to text,"loadMs" to (loaded-started)/1_000_000,"decodeMs" to (System.nanoTime()-loaded)/1_000_000)
    }
    // Test fixtures are generated locally. This does not access the microphone.
    fun modelComparisonDiagnostic(kind:String):Map<String,Any> {
        val a=tts().generateWithConfig("みずをのみます。",GenerationConfig(sid=2,speed=.95f,extra=mapOf("lang" to "ja")))
        val raw=FloatArray(a.samples.size*16000/a.sampleRate) { i ->
            val at=i.toDouble()*a.sampleRate/16000;val lo=at.toInt().coerceAtMost(a.samples.lastIndex);val hi=minOf(lo+1,a.samples.lastIndex)
            (a.samples[lo]+(a.samples[hi]-a.samples[lo])*(at-lo)).toFloat()
        }
        val prepared=SpeechInput.prepare(raw,false);check(detectSpeech(prepared.samples,false))
        return decodeOne(prepared.samples,false,kind)
    }
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
