import test from 'node:test';
import assert from 'node:assert/strict';
import {coachState} from '../web/characters.mjs';
test('The coach follows actual playback and recording states, never a requested playback alone',()=>{
 assert.equal(coachState({audio:{}})[0],'preparing');assert.equal(coachState({audio:{started:true}})[0],'speaking');
 for(const [recording,expected] of [['requesting','preparing'],['recording','listening'],['recognizing','thinking']])assert.equal(coachState({recording,audio:{started:true}})[0],expected);
 assert.equal(coachState({mood:'praise'})[0],'happy');assert.equal(coachState()[0],'ready');
});
