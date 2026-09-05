export type Severity = 'NORMAL' | 'WATCH' | 'WARNING' | 'CRITICAL';
export type Telemetry = { rainfall:number; soil:number; water:number; slope:number; susceptibility:number; confidence:number };
export type RiskResult = { score:number; severity:Severity; action:string; contributions: Record<string,number> };
const clamp=(n:number)=>Math.max(0,Math.min(100,n));
export function calculateRisk(t:Telemetry):RiskResult {
 const c={ rainfall:clamp(t.rainfall/1.2)*.25, soil:clamp(t.soil)*.20, water:clamp(t.water)*.22, slope:clamp(t.slope)*.16, susceptibility:clamp(t.susceptibility)*.17 };
 const score=Math.round(Object.values(c).reduce((a,b)=>a+b,0)*t.confidence/100);
 const severity:Severity=score>=75?'CRITICAL':score>=55?'WARNING':score>=30?'WATCH':'NORMAL';
 const action=severity==='CRITICAL'?'Activate sirens; evacuate marked households to Ridge Shelter.':severity==='WARNING'?'Dispatch ward volunteers; prepare route clearance and evacuation.':severity==='WATCH'?'Verify upstream nodes and alert control-room operators.':'Continue edge monitoring and 15-minute health checks.';
 return {score,severity,action,contributions:c};
}
