import { describe, expect, it } from 'vitest';
import { calculateRisk } from './risk';
describe('risk engine',()=>{
 it('escalates high multi-source evidence',()=>expect(calculateRisk({rainfall:110,soil:94,water:95,slope:75,susceptibility:80,confidence:95}).severity).toBe('CRITICAL'));
 it('keeps quiet readings normal',()=>expect(calculateRisk({rainfall:4,soil:16,water:11,slope:5,susceptibility:20,confidence:95}).severity).toBe('NORMAL'));
 it('reduces score when node confidence is weak',()=>expect(calculateRisk({rainfall:100,soil:90,water:92,slope:70,susceptibility:80,confidence:35}).score).toBeLessThan(40));
});
