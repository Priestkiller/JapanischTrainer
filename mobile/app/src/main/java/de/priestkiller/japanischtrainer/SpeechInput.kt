package de.priestkiller.japanischtrainer

import kotlin.math.abs
import kotlin.math.sqrt

/** Target-independent signal preparation. Never manufactures an expected answer. */
object SpeechInput {
    class NoVoice:IllegalArgumentException("Noch keine ausreichend hörbare Stimme. Sprich nach dem Mikrofonsignal in normaler Lautstärke.")
    data class Prepared(val samples:FloatArray,val gain:Float,val activeMs:Int,val clippedPercent:Float)
    fun prepare(raw:FloatArray,shortKana:Boolean):Prepared {
        require(raw.isNotEmpty() && raw.size<=16000*16 && raw.all { it.isFinite() }) { "Keine gültige Aufnahme. Bitte erneut sprechen." }
        val mean=raw.sumOf { it.toDouble() }/raw.size
        val x=FloatArray(raw.size) { raw[it]-mean.toFloat() }
        val peak=x.maxOf { abs(it) }
        val clipped=raw.count { abs(it)>=.985f }*100f/raw.size
        require(clipped<8f) { "Die Aufnahme übersteuert. Halte etwas mehr Abstand zum Mikrofon." }
        val frame=320
        val energy=FloatArray((x.size+frame-1)/frame) { i ->
            val end=minOf(x.size,(i+1)*frame);var sum=0.0
            for(j in i*frame until end)sum+=x[j]*x[j]
            sqrt(sum/(end-i*frame)).toFloat()
        }
        val threshold=maxOf(.0006f,energy.maxOrNull()!!*.08f)
        val active=energy.indices.filter { energy[it]>=threshold }
        if(peak<.001f || active.size<(if(shortKana)4 else 8))throw NoVoice()
        // Keep consonant onsets and endings; silence padding happens only after VAD.
        val begin=maxOf(0,active.first()*frame-2400)
        val end=minOf(x.size,(active.last()+1)*frame+3200)
        val segment=x.copyOfRange(begin,end)
        val rms=sqrt(segment.sumOf { (it*it).toDouble() }/segment.size).toFloat()
        val gain=maxOf(1f,minOf(10f,.08f/maxOf(.0001f,rms),.9f/peak))
        return Prepared(FloatArray(segment.size) { segment[it]*gain },gain,active.size*20,clipped)
    }
    fun padded(samples:FloatArray):FloatArray = FloatArray(samples.size+6400).also { samples.copyInto(it,1600) }
}
