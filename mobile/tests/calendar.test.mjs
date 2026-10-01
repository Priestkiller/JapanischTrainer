import test from 'node:test';
import assert from 'node:assert/strict';
import {validDay,dayOffset,cleanDays,currentStreak,monthDays,shiftMonth} from '../web/calendar.mjs';
import {Store,cleanProfile} from '../web/core.mjs';

test('Civil dates reject impossible days, accept leap days and handle month/year/DST boundaries',()=>{
 for(const bad of ['2026-02-29','2026-04-31','2026-13-01','2026-01-00','x','1999-12-31'])assert.equal(validDay(bad),false,bad);
 assert.ok(validDay('2028-02-29'));assert.equal(dayOffset('2026-03-29',-1),'2026-03-28');assert.equal(dayOffset('2026-10-25',1),'2026-10-26');
 assert.equal(dayOffset('2026-01-01',-1),'2025-12-31');assert.equal(shiftMonth('2026-01',-1),'2025-12');
});
test('Opening/importing an old profile preserves its series and does not invent historic learning days',()=>{
 const old={xp:45,completed:['0:0'],streak:9,last_active:'2026-09-30',teacher_id:'yuki',last_lesson:{key:'0:1',card:1},course_revision:11};
 const s=new Store(old);assert.equal(s.data.streak,9);assert.equal(s.data.xp,45);assert.equal(s.data.teacher_id,'yuki');assert.deepEqual(s.data.completed,old.completed);
 assert.deepEqual(s.data.last_lesson,old.last_lesson);assert.deepEqual(s.data.learning_days,['2026-09-30']);assert.equal(s.data.learning_calendar_partial,true);
 assert.equal(currentStreak(s.data,'2026-10-01'),9);assert.equal(currentStreak(s.data,'2026-10-02'),0);assert.equal(s.data.streak,9);
});
test('A real learning event records one local day, repeats do not add days and a gap resets the series',()=>{
 const s=new Store({streak:3,last_active:'2026-09-30'});s.touch(new Date(2026,9,1,23,58));s.touch(new Date(2026,9,1,23,59));
 assert.equal(s.data.streak,4);assert.deepEqual(s.data.learning_days,['2026-09-30','2026-10-01']);
 s.touch(new Date(2026,9,2,0,1));assert.equal(s.data.streak,5);s.touch(new Date(2026,9,4));assert.equal(s.data.streak,1);
});
test('History survives export and import and rendering a month never changes progress or adds activity',()=>{
 const s=new Store({xp:20,completed:['0:0'],learning_days:['2026-09-30','2026-10-01'],last_active:'2026-10-01',streak:2,learning_calendar_since:'2026-09-30',learning_calendar_partial:false});
 const before=JSON.stringify(s.data);const cells=monthDays('2026-10','2026-10-01',s.data.learning_days);
 assert.equal(cells.length,35);assert.equal(cells[3].key,'2026-10-01');assert.ok(cells[3].learned&&cells[3].today);assert.equal(cells.filter(c=>c?.learned).length,1);
 assert.equal(JSON.stringify(s.data),before);assert.deepEqual(cleanProfile(JSON.parse(before),true),s.data);
});
test('Month layout uses Monday as its first column and covers leap years and six-week months',()=>{
 const feb=monthDays('2028-02');assert.equal(feb.filter(Boolean).length,29);const aug=monthDays('2026-08');assert.equal(aug.length,42);assert.equal(aug[5].day,1);
 assert.deepEqual(cleanDays(['2026-10-01','2026-02-30','2026-10-01','2026-09-30']),['2026-09-30','2026-10-01']);
});
