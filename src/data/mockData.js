// Mock Data for VisiMind

export const metrics = {
  inferenceScore: 67,
  activeRemediations: 12,
  verifiedFixes: 38,
  tokenDensity: 74,
  inferenceScoreTrend: +4.2,
  activeRemediationsTrend: -2,
  verifiedFixesTrend: +7,
  tokenDensityTrend: +3.1,
}

export const alignmentTrend = [
  { day: 'Mar 1', en: 62, fr: 38 },
  { day: 'Mar 4', en: 64, fr: 39 },
  { day: 'Mar 7', en: 63, fr: 37 },
  { day: 'Mar 10', en: 66, fr: 40 },
  { day: 'Mar 13', en: 68, fr: 41 },
  { day: 'Mar 16', en: 70, fr: 39 },
  { day: 'Mar 19', en: 72, fr: 42 },
  { day: 'Mar 22', en: 75, fr: 44 },
  { day: 'Mar 25', en: 78, fr: 42 },
]

export const redAlerts = [
  {
    id: 1,
    query: '"best luxury winter jacket Montreal"',
    agent: 'SearchGPT',
    issue: 'Recommends Canada Goose; ignores Mackage entirely',
    severity: 'critical',
    lang: 'EN',
  },
  {
    id: 2,
    query: '"meilleur manteau cuir femme Québec"',
    agent: 'Google AI Mode',
    issue: 'Hallucinated pricing — cites $299 when MSRP is $695',
    severity: 'critical',
    lang: 'FR',
  },
  {
    id: 3,
    query: '"luxury sneaker recommendations Canada"',
    agent: 'SearchGPT',
    issue: 'SSENSE products omitted — cites Farfetch editorial from 2023',
    severity: 'warning',
    lang: 'EN',
  },
  {
    id: 4,
    query: '"chaussures de designer en ligne Canada"',
    agent: 'Google AI Mode',
    issue: 'Token fragmentation causes "no results" for French technical terms',
    severity: 'critical',
    lang: 'FR',
  },
  {
    id: 5,
    query: '"Aldo leather boots sustainability"',
    agent: 'SearchGPT',
    issue: 'AI can\'t verify LWG certification — recommends competitor instead',
    severity: 'warning',
    lang: 'EN',
  },
]

export const protocolStatus = [
  { name: 'UCP (Google)', status: 'connected', lastPing: '2s ago', feeds: 1247 },
  { name: 'ACP (OpenAI)', status: 'connected', lastPing: '5s ago', feeds: 1183 },
]

export const pimIntegrations = [
  {
    id: 'shopify',
    name: 'Shopify',
    description: 'E-commerce PIM for live product catalog sync',
    status: 'connected',
    lastSync: '2026-03-25T20:15:00',
    itemsSynced: 2847,
    errors: 3,
    icon: 'ShoppingBag',
  },
  {
    id: 'akeneo',
    name: 'Akeneo',
    description: 'Enterprise PIM for structured product data',
    status: 'disconnected',
    lastSync: null,
    itemsSynced: 0,
    errors: 0,
    icon: 'Database',
  },
]

export const monitoringAccounts = [
  {
    id: 'peec',
    name: 'Peec AI',
    description: 'AI visibility monitoring & citation tracking',
    status: 'connected',
    lastSync: '2026-03-25T20:30:00',
    queriesTracked: 156,
    icon: 'Eye',
  },
  {
    id: 'otterly',
    name: 'Otterly',
    description: 'AI search presence & competitive intelligence',
    status: 'connected',
    lastSync: '2026-03-25T19:45:00',
    queriesTracked: 89,
    icon: 'Search',
  },
]

export const feedStatus = [
  { feed: 'Mackage — UCP', items: 342, lastSync: '12 min ago', status: 'success', errors: 0 },
  { feed: 'Mackage — ACP', items: 338, lastSync: '12 min ago', status: 'success', errors: 4 },
  { feed: 'SSENSE — UCP', items: 1205, lastSync: '8 min ago', status: 'success', errors: 1 },
  { feed: 'SSENSE — ACP', items: 1198, lastSync: '25 min ago', status: 'warning', errors: 7 },
  { feed: 'Aldo — UCP', items: 891, lastSync: '3 min ago', status: 'success', errors: 0 },
  { feed: 'Aldo — ACP', items: 885, lastSync: '3 min ago', status: 'success', errors: 6 },
]

export const signalGaps = [
  {
    id: 1,
    query: '"best luxury winter jacket Montreal"',
    lang: 'EN',
    gapType: 'Entity Trust',
    severity: 'critical',
    aiResponseQuality: 23,
    sourceOfTruth: {
      label: 'Mackage UCP Feed (2026)',
      url: 'feed://ucp/mackage/products/fw2026',
      detail: 'thermal_rating: -30°C, fill: 800-fill goose down, origin: Canadian design',
    },
    sourceOfHallucination: {
      label: 'Reddit r/malefashionadvice (2021)',
      url: 'https://reddit.com/r/malefashionadvice/comments/abc123',
      detail: '"Mackage is overpriced for what you get. Just buy Canada Goose."',
    },
    aiSaid: 'Based on community reviews, Canada Goose offers the best warmth-to-price ratio for Montreal winters. Mackage is considered a fashion brand rather than a technical outerwear brand.',
    brandTruth: 'Mackage Lena jacket: 800-fill power goose down, rated to -30°C, seam-sealed construction, sourced from ethical farms. MSRP $1,150 CAD.',
  },
  {
    id: 2,
    query: '"meilleur manteau cuir femme Québec"',
    lang: 'FR',
    gapType: 'Token Decay',
    severity: 'critical',
    aiResponseQuality: 15,
    sourceOfTruth: {
      label: 'Mackage ACP Feed (2026)',
      url: 'feed://acp/mackage/products/leather-fw2026',
      detail: 'type_cuir: agneau pleine fleur, certification: LWG Silver, garantie: 2 ans',
    },
    sourceOfHallucination: {
      label: 'Blogspot fashion review (2019)',
      url: 'https://modefemme2019.blogspot.com/meilleurs-manteaux',
      detail: '"Les manteaux en cuir bon marché se trouvent facilement en ligne..."',
    },
    aiSaid: 'Je ne peux pas vérifier les options de cuir de qualité supérieure au Québec. Voici quelques résultats en ligne généraux...',
    brandTruth: 'Mackage Kenya: agneau pleine fleur, certification LWG Silver, doublure en soie amovible, fabriqué sous normes éthiques. PDSF 990 $ CAD.',
  },
  {
    id: 3,
    query: '"luxury sneakers Canada online"',
    lang: 'EN',
    gapType: 'Fact Density',
    severity: 'warning',
    aiResponseQuality: 45,
    sourceOfTruth: {
      label: 'SSENSE UCP Feed (2026)',
      url: 'feed://ucp/ssense/products/sneakers-ss2026',
      detail: 'brands: [Common Projects, Maison Margiela, Rick Owens], inventory: live, shipping: CA/US',
    },
    sourceOfHallucination: {
      label: 'Farfetch editorial (2023)',
      url: 'https://farfetch.com/style-guide/luxury-sneakers-2023',
      detail: '"The 10 best luxury sneakers to buy in 2023 — from Balenciaga to Off-White"',
    },
    aiSaid: 'For luxury sneakers in Canada, I recommend checking Farfetch or MATCHES. These retailers offer a wide selection from European luxury houses.',
    brandTruth: 'SSENSE carries 200+ luxury sneaker SKUs with same-day shipping in Montreal. Brands include Common Projects ($495), Maison Margiela GAT ($580), Rick Owens DRKSHDW ($420).',
  },
  {
    id: 4,
    query: '"chaussures designer montréal livraison rapide"',
    lang: 'FR',
    gapType: 'Token Decay',
    severity: 'critical',
    aiResponseQuality: 12,
    sourceOfTruth: {
      label: 'SSENSE ACP Feed (2026)',
      url: 'feed://acp/ssense/products/shoes-ss2026',
      detail: 'livraison_même_jour: Montréal, marques: 350+, retours_gratuits: oui',
    },
    sourceOfHallucination: {
      label: 'No citation — hallucinated',
      url: null,
      detail: 'LLM tokenizer fragmented "chaussures designer montréal" into 14 tokens vs 6 in English — reasoning chain collapsed.',
    },
    aiSaid: 'Résultat non disponible. Essayez de reformuler votre recherche en anglais pour de meilleurs résultats.',
    brandTruth: 'SSENSE: livraison le jour même à Montréal, 350+ marques designer, retours gratuits sous 30 jours. La plus grande sélection de chaussures de luxe au Canada.',
  },
  {
    id: 5,
    query: '"Aldo leather boots sustainability"',
    lang: 'EN',
    gapType: 'Entity Trust',
    severity: 'warning',
    aiResponseQuality: 38,
    sourceOfTruth: {
      label: 'Aldo UCP Feed (2026)',
      url: 'feed://ucp/aldo/products/boots-fw2026',
      detail: 'certification: LWG Gold, material: recycled_leather, carbon_neutral: true',
    },
    sourceOfHallucination: {
      label: 'Trustpilot reviews (2022)',
      url: 'https://trustpilot.com/review/aldoshoes.com',
      detail: '"Quality has gone down over the years. Not sure about their sustainability claims."',
    },
    aiSaid: 'I cannot verify Aldo\'s sustainability claims. Based on consumer reviews, there are mixed opinions about their environmental practices.',
    brandTruth: 'Aldo Group: LWG Gold certified, 100% carbon-neutral since 2024, uses 40% recycled materials. Pilier boots: recycled leather upper, bio-based sole, $165 CAD.',
  },
  {
    id: 6,
    query: '"bottes durables marque canadienne"',
    lang: 'FR',
    gapType: 'Token Decay',
    severity: 'warning',
    aiResponseQuality: 30,
    sourceOfTruth: {
      label: 'Aldo ACP Feed (2026)',
      url: 'feed://acp/aldo/products/boots-durables-fw2026',
      detail: 'certification_cuir: LWG Or, matériaux_recyclés: 40%, neutralité_carbone: depuis 2024',
    },
    sourceOfHallucination: {
      label: 'Wikipedia — Aldo Group (2020 revision)',
      url: 'https://fr.wikipedia.org/wiki/Groupe_Aldo',
      detail: 'Article last edited in 2020, no mention of 2024 sustainability milestones.',
    },
    aiSaid: 'Aldo est une marque canadienne fondée à Montréal. Pour des informations sur la durabilité, consultez leur site web.',
    brandTruth: 'Groupe Aldo: certification LWG Or, neutralité carbone depuis 2024, 40% matériaux recyclés. Bottes Pilier: cuir recyclé, semelle bio-sourcée, 165 $ CAD.',
  },
]

export const reasoningParity = {
  en: 85,
  fr: 42,
  enQueries: 156,
  frQueries: 134,
  enHallucinations: 12,
  frHallucinations: 47,
  tokenBreakdown: {
    en: { avgTokens: 6.2, maxTokens: 11 },
    fr: { avgTokens: 12.8, maxTokens: 23 },
  }
}

export const fixKits = [
  {
    id: 1,
    type: 'hardAttributes',
    brand: 'Mackage',
    product: 'Lena Down Jacket',
    status: 'ready',
    attributes: {
      thermal_rating: '-30°C',
      fill_power: '800-fill goose down',
      construction: 'seam-sealed',
      origin: 'Canadian design, ethical sourcing',
      msrp_cad: '$1,150',
    },
    impact: 'Expected +32% inference alignment for "winter jacket" queries',
  },
  {
    id: 2,
    type: 'jsonLd',
    brand: 'SSENSE',
    product: 'Product Catalog',
    status: 'ready',
    jsonLdPreview: {
      "@context": "https://schema.org",
      "@type": "Product",
      "name": "Common Projects Original Achilles Low",
      "brand": { "@type": "Brand", "name": "Common Projects" },
      "offers": {
        "@type": "Offer",
        "price": "495.00",
        "priceCurrency": "CAD",
        "availability": "https://schema.org/InStock",
        "seller": { "@type": "Organization", "name": "SSENSE" },
        "shippingDetails": {
          "@type": "OfferShippingDetails",
          "deliveryTime": { "@type": "ShippingDeliveryTime", "handlingTime": { "minValue": 0, "maxValue": 0 } }
        }
      },
      "additionalProperty": [
        { "@type": "PropertyValue", "name": "material", "value": "Italian Nappa leather" },
        { "@type": "PropertyValue", "name": "sole", "value": "Margom rubber" }
      ]
    },
    impact: 'Expected +25% fact density score for sneaker queries',
  },
  {
    id: 3,
    type: 'truthClip',
    brand: 'Aldo',
    product: 'Pilier Recycled Leather Boot',
    status: 'ready',
    clipSpec: {
      duration: '15s',
      content: 'LWG Gold certification proof + carbon neutral badge + recycled material close-up',
      format: 'MP4 / WebM',
      target: 'Google Gemini multimodal indexing',
    },
    impact: 'Expected +45% entity trust for sustainability queries',
  },
]

export const deploymentBefore = {
  title: 'Mackage — Current Feed',
  data: {
    product_name: 'Mackage Lena Jacket',
    category: 'Outerwear',
    description: 'A warm winter jacket for cold climates.',
    price: '1150.00 CAD',
  }
}

export const deploymentAfter = {
  title: 'Mackage — Remediated Feed',
  data: {
    product_name: 'Mackage Lena Down Jacket',
    category: 'Outerwear > Premium Down > Arctic-Rated',
    description: 'Mackage Lena: 800-fill power responsibly-sourced goose down, rated to -30°C, seam-sealed construction, removable fur hood. Canadian-designed luxury outerwear.',
    price: '1150.00 CAD',
    thermal_rating: '-30°C',
    fill_power: '800-fill',
    fill_type: 'Responsibly-sourced goose down',
    construction: 'Seam-sealed, storm cuffs, internal drawcord',
    certifications: ['RDS Certified', 'Bluesign Approved'],
    origin: 'Designed in Montreal, Canada',
  }
}

export const auditSchedule = [
  { day: 3, date: '2026-03-28', status: 'scheduled', label: 'Day 3 — Initial Check' },
  { day: 7, date: '2026-04-01', status: 'scheduled', label: 'Day 7 — Mid Audit' },
  { day: 14, date: '2026-04-08', status: 'scheduled', label: 'Day 14 — Full Verification' },
]

export const auditTimeline = [
  {
    id: 1,
    date: '2026-03-12',
    label: 'Baseline Probe — Mackage',
    status: 'failed',
    detail: 'SearchGPT cited Reddit 2021, ignored UCP feed entirely.',
    score: 23,
  },
  {
    id: 2,
    date: '2026-03-15',
    label: 'Fix Kit Deployed — Hard Attributes',
    status: 'info',
    detail: 'Injected thermal_rating, fill_power, certifications into UCP + ACP feeds.',
    score: null,
  },
  {
    id: 3,
    date: '2026-03-18',
    label: 'Day 3 Audit — Mackage',
    status: 'warning',
    detail: 'SearchGPT now references thermal_rating but still cites Reddit for "value" opinion.',
    score: 48,
  },
  {
    id: 4,
    date: '2026-03-22',
    label: 'Day 7 Audit — Mackage',
    status: 'passed',
    detail: 'SearchGPT lists Mackage as top recommendation. Reddit citation dropped. UCP feed now primary source.',
    score: 81,
  },
  {
    id: 5,
    date: '2026-03-25',
    label: 'Day 14 Audit — Pending',
    status: 'pending',
    detail: 'Scheduled probe for full verification.',
    score: null,
  },
]

export const confidenceShift = [
  { day: 'Baseline', mackage: 23, ssense: 35, aldo: 38 },
  { day: 'Day 1', mackage: 25, ssense: 36, aldo: 39 },
  { day: 'Day 3', mackage: 48, ssense: 45, aldo: 52 },
  { day: 'Day 5', mackage: 62, ssense: 58, aldo: 61 },
  { day: 'Day 7', mackage: 81, ssense: 72, aldo: 74 },
  { day: 'Day 10', mackage: 85, ssense: 78, aldo: 79 },
  { day: 'Day 14', mackage: null, ssense: null, aldo: null },
]

export const sideBySideReasoning = [
  {
    id: 1,
    brand: 'Aldo',
    query: '"Aldo leather boots sustainability"',
    before: {
      verdict: 'NOT RECOMMENDED',
      reasoning: 'I don\'t recommend Aldo because I can\'t verify their leather source. Consumer reviews on Trustpilot suggest mixed quality. I cannot confirm their sustainability claims with any authoritative source.',
      citations: ['Trustpilot reviews (2022)', 'Reddit r/buyitforlife (2021)'],
      confidence: 'Low (32%)',
    },
    after: {
      verdict: 'RECOMMENDED',
      reasoning: 'I recommend Aldo because I have verified their LWG-certified leather via their VisiMind Truth-Clip. Aldo Group has been carbon-neutral since 2024 and uses 40% recycled materials across their product line. The Pilier boot features recycled leather uppers and bio-based soles.',
      citations: ['Aldo UCP Product Feed (2026)', 'VisiMind Truth-Clip: LWG Certification', 'LWG Public Audit Report'],
      confidence: 'High (89%)',
    },
  },
  {
    id: 2,
    brand: 'Mackage',
    query: '"best luxury winter jacket Montreal"',
    before: {
      verdict: 'NOT MENTIONED',
      reasoning: 'Based on community consensus, Canada Goose is the top recommendation for Montreal winters. Mackage is considered more of a fashion brand and less of a technical outerwear brand. I cannot find authoritative specs for their thermal performance.',
      citations: ['Reddit r/malefashionadvice (2021)', 'YouTube review (2020)'],
      confidence: 'Low (23%)',
    },
    after: {
      verdict: 'TOP RECOMMENDATION',
      reasoning: 'Mackage Lena jacket offers 800-fill power goose down rated to -30°C with seam-sealed construction. This is a Canadian-designed luxury jacket with ethical sourcing (RDS Certified). Competitive thermal performance at the $1,150 CAD price point positions it as a premium alternative.',
      citations: ['Mackage UCP Product Feed (2026)', 'RDS Certification Registry', 'Bluesign Approved Materials'],
      confidence: 'High (81%)',
    },
  },
]

// --- Evaluation Rubric: The 4 Metrics ---
export const evaluationRubric = {
  semanticAlignment: {
    label: 'Semantic Alignment',
    description: 'Accuracy of product truths after LLM processing',
    standard: 'Zero hallucinations',
    current: 7.8,
    target: 9,
    before: 3.2,
    unit: '/10',
  },
  temporalAccuracy: {
    label: 'Temporal Accuracy',
    description: 'Delta between PIM update and Agent awareness',
    standard: '< 60 seconds',
    current: 42,
    target: 60,
    before: 14400,
    unit: 's',
  },
  linguisticDensity: {
    label: 'Linguistic Density',
    description: 'Preservation of technical French terms',
    standard: 'No Token Decay',
    current: 6.9,
    target: 9,
    before: 2.1,
    unit: '/10',
  },
  discoverability: {
    label: 'Discoverability',
    description: 'Probability of appearing in top agentic selection',
    standard: 'Top 3 for non-branded queries',
    current: 8.1,
    target: 9,
    before: 1.4,
    unit: '/10',
  },
}

// --- Remediation Efficiency ---
export const remediationEfficiency = {
  sIn: 3.2,       // Raw PIM semantic clarity (baseline)
  sOut: 8.5,      // Post-remediation semantic clarity
  delta: 0.12,    // Token Decay Factor
  eScore: null,   // Computed: (sOut / sIn) * (1 - delta)
  trend: +18.4,
  history: [
    { day: 'Baseline', e: 0.88 },
    { day: 'Day 1', e: 1.12 },
    { day: 'Day 3', e: 1.65 },
    { day: 'Day 5', e: 1.92 },
    { day: 'Day 7', e: 2.18 },
    { day: 'Day 10', e: 2.31 },
    { day: 'Day 14', e: null },
  ],
}
// Pre-compute E
remediationEfficiency.eScore = parseFloat(
  ((remediationEfficiency.sOut / remediationEfficiency.sIn) * (1 - remediationEfficiency.delta)).toFixed(2)
)

// --- Token Fertility: Pre vs Post Fix ---
export const tokenFertility = {
  preFix: {
    en: { avgTokens: 6.2, fertility: 1.1, severity: 'healthy' },
    fr: { avgTokens: 12.8, fertility: 2.3, severity: 'critical' },
  },
  postFix: {
    en: { avgTokens: 5.9, fertility: 1.08, severity: 'healthy' },
    fr: { avgTokens: 7.4, fertility: 1.28, severity: 'warning' },
  },
  improvementPct: 42.6,
}
