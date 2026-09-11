import {test} from 'node:test';
import assert from 'node:assert/strict';
import {prepareMessage} from '../lib/message.mjs';
test('message remains an unsent draft and preserves intended topic',()=>{
 const value=prepareMessage({name:' Test ',message:'Ik wil meer weten over coaching.',topic:'Online coaching'});
 assert.match(value,/Van: Test\n/);assert.match(value,/Onderwerp: Online coaching/);assert.match(value,/Het is niet verstuurd\./);
});
test('invalid inputs cannot create a draft',()=>{
 for(const input of [null,{name:' ',message:'Een geldige lange vraag'},{name:'Test',message:'         x'},{name:'Test',message:'Een geldige lange vraag',email:'ongeldig'},{name:'Test',message:'x'.repeat(2501)}])assert.throws(()=>prepareMessage(input));
});
