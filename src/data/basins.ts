export type BasinCoverage = 'data-supported' | 'historical-reference' | 'unavailable';

export type BasinRecord = {
  id: string;
  river: string;
  basin: string;
  region: string;
  coverage: BasinCoverage;
  caseStudy?: {
    when: string;
    mechanism: string;
    evidence: string;
  };
  dataNotes: string;
};

// Names and case-study context derive from the supplied group guide. Coverage is
// deliberately conservative: the supplied environmental point CSV is national,
// untimestamped, and does not identify a named river basin.
export const basinRegistry: BasinRecord[] = [
  {
    id: 'mandakini-kedarnath',
    river: 'Mandakini',
    basin: 'Kedarnath / Mandakini valley',
    region: 'Uttarakhand',
    coverage: 'historical-reference',
    caseStudy: {
      when: '15–17 June 2013',
      mechanism: 'Extreme rainfall, rapid snow/ice melt, catchment saturation, landslides/debris and Chorabari lake-system outburst.',
      evidence: 'Supplied group guide citing World Bank and NHP/NRSC material.',
    },
    dataNotes: 'Historical case-study context available; no basin-specific live stream supplied.',
  },
  {
    id: 'rishiganga-dhauliganga',
    river: 'Rishiganga–Dhauliganga',
    basin: 'Raunthi Garh / Chamoli valley',
    region: 'Uttarakhand',
    coverage: 'historical-reference',
    caseStudy: {
      when: '7 February 2021',
      mechanism: 'Snow/ice/rock avalanche transformed into debris flow and flash flood.',
      evidence: 'Supplied group guide citing PIB/GSI reporting.',
    },
    dataNotes: 'Historical case-study context available; rainfall-only signals are insufficient for this event class.',
  },
  {
    id: 'teesta-south-lhonak',
    river: 'Teesta',
    basin: 'South Lhonak Lake / Teesta basin',
    region: 'Sikkim',
    coverage: 'historical-reference',
    caseStudy: {
      when: '28 September–4 October 2023',
      mechanism: 'Glacial lake drainage / GLOF with downstream flood-wave risk.',
      evidence: 'Supplied group guide citing ISRO/NRSC satellite comparison.',
    },
    dataNotes: 'Historical satellite case-study context available; no local telemetry supplied.',
  },
  {
    id: 'india-point-records',
    river: 'Unassigned',
    basin: 'Provided India flood-risk point records',
    region: 'India-wide',
    coverage: 'data-supported',
    dataNotes: '10,000 untimestamped point records with latitude/longitude and environmental attributes; they are not assigned to named river basins.',
  },
];
