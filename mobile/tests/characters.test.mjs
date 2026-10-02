import test from 'node:test';
import assert from 'node:assert/strict';
import {coachState,teacherPose} from '../web/characters.mjs';
test('The coach follows actual playback and recording states, never a requested playback alone',()=>{
 assert.equal(coachState({audio:{}})[0],'preparing');assert.equal(coachState({audio:{started:true}})[0],'speaking');
 for(const [recording,expected] of [['requesting','preparing'],['recording','listening'],['recognizing','thinking']])assert.equal(coachState({recording,audio:{started:true}})[0],expected);
 assert.equal(coachState({mood:'praise'})[0],'happy');assert.equal(coachState()[0],'ready');
});
test('Full-body pose rows match playback/listening/praise and reduced motion has a still pose',()=>{
 for(const [mode,row] of [['ready',0],['preparing',0],['speaking',1],['listening',2],['thinking',2],['happy',3]]){
  for(let step=0;step<24;step++)assert.equal(Math.floor(teacherPose(mode,step)/4),row);
  assert.equal(new Set(Array.from({length:24},(_,n)=>teacherPose(mode,n,false))).size,1);
 }
 assert.equal(new Set(Array.from({length:12},(_,n)=>teacherPose('speaking',n))).size,4);
});
