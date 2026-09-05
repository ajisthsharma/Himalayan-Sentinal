import type { Telemetry } from '../risk';

export type DatasetPoint = Telemetry & {
  id: string;
  latitude: number;
  longitude: number;
  temperature: number;
  humidity: number;
  discharge: number;
  waterLevel: number;
  elevation: number;
  landCover: string;
  soilType: string;
  historicalFloods: number;
  floodOccurredLabel: number;
};

// Exact observations selected from flood_risk_dataset_india.csv. No target label
// is used by the frontend risk calculation, preventing outcome leakage.
export const providedIndiaPoints: Record<'baseline'|'rainfall'|'cascade', DatasetPoint> = {
  baseline: { id:'IND-R-001', latitude:31.6332521277, longitude:81.279372802, rainfall:46.5179164237, soil:55.9532470549, water:7.295373958, slope:78.9902787403, susceptibility:0, confidence:94, temperature:22.7458489997, humidity:55.9532470549, discharge:121.1294230569, waterLevel:0.7295373958, elevation:7899.0278740289, landCover:'Urban', soilType:'Silt', historicalFloods:0, floodOccurredLabel:1 },
  rainfall: { id:'IND-R-157', latitude:28.3720384356, longitude:79.5406386298, rainfall:106.2197585381, soil:87.6358350667, water:7.304030444, slope:48.4809307307, susceptibility:100, confidence:94, temperature:25.3170960175, humidity:87.6358350667, discharge:3161.4185032063, waterLevel:0.7304030444, elevation:4848.0930739684, landCover:'Desert', soilType:'Silt', historicalFloods:1, floodOccurredLabel:1 },
  cascade: { id:'IND-R-313', latitude:32.6913237746, longitude:78.3048515384, rainfall:252.1219966691, soil:72.3321088607, water:88.152358085, slope:29.0847020178, susceptibility:100, confidence:94, temperature:26.689425239, humidity:72.3321088607, discharge:4372.6199282057, waterLevel:8.8152358085, elevation:2908.4702017808, landCover:'Forest', soilType:'Peat', historicalFloods:1, floodOccurredLabel:0 },
};

export const datasetFacts = {
  indiaRecords: 10000,
  indiaBounds: '8.00–36.99°N · 68.00–97.00°E',
  modisRecords: 1025801,
  modisRange: '2003-12-10 to 2015-02-05',
  modisCoverage: 'Paling, Indonesia (not local Himalayan monitoring)',
};
