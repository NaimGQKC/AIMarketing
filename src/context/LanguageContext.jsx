import { createContext, useContext, useState, useCallback } from 'react'

const translations = {
  en: {
    // Nav
    dashboard: 'Dashboard',
    connect: 'Connect',
    diagnose: 'Diagnose',
    remediate: 'Remediate',
    verify: 'Verify',
    roadmap: 'Roadmap',
    outreach: 'Outreach',
    
    // Dashboard
    dashboardTitle: 'Command Center',
    dashboardSubtitle: 'Real-time inference alignment monitoring for your brand portfolio — measuring how accurately AI systems represent your brand, adapted from GEO visibility research (Princeton, 2024).',
    inferenceScore: 'Inference Alignment',
    activeRemediations: 'Active Remediations',
    verifiedFixes: 'Verified Fixes',
    tokenDensity: 'Token Density',
    redAlerts: 'Red Alert Queries',
    protocolStatus: 'Protocol Status',
    alignmentTrend: 'Alignment Trend (30d)',
    
    // Connect
    connectTitle: 'Connect Your Data',
    connectSubtitle: 'Sync your PIM and monitoring accounts to enable the remediation engine.',
    pimIntegrations: 'PIM Integrations',
    monitoringSync: 'Monitoring Sync',
    feedStatus: 'Feed Status',
    connected: 'Connected',
    disconnected: 'Disconnected',
    syncing: 'Syncing...',
    lastSync: 'Last Sync',
    itemsSynced: 'Items Synced',
    errors: 'Errors',
    connectNow: 'Connect',
    
    // Diagnose
    diagnoseTitle: 'Signal Gap Analysis',
    diagnoseSubtitle: 'Identify where AI agents are failing your brand — and why.',
    signalGapTable: 'Signal Gap Table',
    query: 'Query',
    language: 'Language',
    gapType: 'Gap Type',
    severity: 'Severity',
    sourceOfTruth: 'Source of Truth',
    sourceOfHallucination: 'Toxic Citation',
    aiResponse: 'AI Response Quality',
    reasoningParity: 'Reasoning Parity',
    enVisibility: 'English Visibility',
    frVisibility: 'French Visibility',
    parityMessage: 'Your English visibility is {en}%, but your French visibility is {fr}% because the LLM is Scrabble-tiling (tokenizing) your technical terms.',
    factDensity: 'Fact Density',
    entityTrust: 'Entity Trust',
    tokenDecay: 'Tokenization Premium',
    
    // Remediate
    remediateTitle: 'Deploy Fix Kits',
    remediateSubtitle: 'Remediate hallucinations with programmatic data injection.',
    fixKits: 'Available Fix Kits',
    hardAttributes: 'Hard Attributes',
    jsonLdInjection: 'JSON-LD Injection',
    truthClip: 'Truth Clip Generation',
    deployFix: 'Deploy Fix Kit',
    preview: 'Preview',
    beforeAfter: 'Before / After',
    deploying: 'Deploying...',
    deployed: 'Deployed',
    
    // Verify
    verifyTitle: 'Verification & Audit',
    verifySubtitle: 'Prove that your remediations shifted AI agent behavior.',
    autoAudit: 'Auto-Audit Schedule',
    auditTimeline: 'Audit Timeline',
    confidenceShift: 'Confidence Shift',
    sideBySide: 'Side-by-Side Reasoning',
    beforeFix: 'Before Fix',
    afterFix: 'After Fix',
    day: 'Day',
    passed: 'Passed',
    failed: 'Failed',
    pending: 'Pending',
    scheduleAudit: 'Schedule Audit',

    // Evaluation Rubric
    remediationEfficiency: 'Remediation Efficiency',
    remediationEfficiencyDesc: 'Live E = (S_out / S_in) · (1 − δ)',
    tokenFertilityTitle: 'Token Fertility',
    tokenFertilityDesc: 'Measures the tokenization cost premium of your French content vs. English. French typically shows a 1.1-1.5x premium over English for general content, with specialized vocabulary experiencing higher ratios. Research: Petrov et al. 2023, Lundin et al. 2025.',
    technicalDeepDive: 'Technical Deep Dive',
    evaluationRubric: 'Evaluation Rubric',
    semanticAlignment: 'Semantic Alignment',
    temporalAccuracy: 'Temporal Accuracy',
    linguisticDensity: 'Linguistic Density',
    discoverability: 'Discoverability',
    preFix: 'Pre-Fix',
    postFix: 'Post-Fix',
    tokenDecayFactor: 'Token Fertility Factor (δ)',
    semanticIn: 'Semantic In (S_in)',
    semanticOut: 'Semantic Out (S_out)',
    current: 'Current',
    target: 'Target',
    the9Standard: 'The 9/10 Standard',
    improvement: 'Improvement',
    fertilityScore: 'Fertility Score',

    // General
    search: 'Search...',
    notifications: 'Notifications',
    viewDetails: 'View Details',
    critical: 'Critical',
    warning: 'Warning',
    success: 'Success',
    info: 'Info',
  },
  fr: {
    // Nav
    dashboard: 'Tableau de bord',
    connect: 'Connecter',
    diagnose: 'Diagnostiquer',
    remediate: 'Remédier',
    verify: 'Vérifier',
    roadmap: 'Feuille de route',
    outreach: 'Prospection',
    
    // Dashboard
    dashboardTitle: 'Centre de commande',
    dashboardSubtitle: 'Surveillance en temps réel de l\'alignement d\'inférence pour votre portefeuille de marques — mesure la fidélité de représentation de votre marque par l\'IA, méthodologie adaptée de la recherche GEO (Princeton, 2024).',
    inferenceScore: 'Alignement d\'inférence',
    activeRemediations: 'Remédiations actives',
    verifiedFixes: 'Corrections vérifiées',
    tokenDensity: 'Densité de jetons',
    redAlerts: 'Alertes rouges',
    protocolStatus: 'Statut des protocoles',
    alignmentTrend: 'Tendance d\'alignement (30j)',
    
    // Connect
    connectTitle: 'Connecter vos données',
    connectSubtitle: 'Synchronisez votre PIM et vos comptes de surveillance pour activer le moteur de remédiation.',
    pimIntegrations: 'Intégrations PIM',
    monitoringSync: 'Synchronisation de surveillance',
    feedStatus: 'Statut des flux',
    connected: 'Connecté',
    disconnected: 'Déconnecté',
    syncing: 'Synchronisation...',
    lastSync: 'Dernière sync',
    itemsSynced: 'Éléments synchronisés',
    errors: 'Erreurs',
    connectNow: 'Connecter',
    
    // Diagnose
    diagnoseTitle: 'Analyse des écarts de signaux',
    diagnoseSubtitle: 'Identifiez où les agents IA échouent pour votre marque — et pourquoi.',
    signalGapTable: 'Tableau des écarts de signaux',
    query: 'Requête',
    language: 'Langue',
    gapType: 'Type d\'écart',
    severity: 'Sévérité',
    sourceOfTruth: 'Source de vérité',
    sourceOfHallucination: 'Citation toxique',
    aiResponse: 'Qualité de réponse IA',
    reasoningParity: 'Parité de raisonnement',
    enVisibility: 'Visibilité anglaise',
    frVisibility: 'Visibilité française',
    parityMessage: 'Votre visibilité en anglais est de {en}%, mais votre visibilité en français est de {fr}% car le LLM fragmente (tokenise) vos termes techniques.',
    factDensity: 'Densité de faits',
    entityTrust: 'Confiance d\'entité',
    tokenDecay: 'Prime de tokenisation',
    
    // Remediate
    remediateTitle: 'Déployer les kits de correction',
    remediateSubtitle: 'Remédiez les hallucinations avec une injection de données programmatique.',
    fixKits: 'Kits de correction disponibles',
    hardAttributes: 'Attributs rigides',
    jsonLdInjection: 'Injection JSON-LD',
    truthClip: 'Génération de clip vérité',
    deployFix: 'Déployer le kit',
    preview: 'Aperçu',
    beforeAfter: 'Avant / Après',
    deploying: 'Déploiement...',
    deployed: 'Déployé',
    
    // Verify
    verifyTitle: 'Vérification et audit',
    verifySubtitle: 'Prouvez que vos remédiations ont modifié le comportement des agents IA.',
    autoAudit: 'Planification d\'audit automatique',
    auditTimeline: 'Chronologie d\'audit',
    confidenceShift: 'Évolution de la confiance',
    sideBySide: 'Raisonnement côte à côte',
    beforeFix: 'Avant correction',
    afterFix: 'Après correction',
    day: 'Jour',
    passed: 'Réussi',
    failed: 'Échoué',
    pending: 'En attente',
    scheduleAudit: 'Planifier un audit',

    // Evaluation Rubric
    remediationEfficiency: 'Efficacité de remédiation',
    remediationEfficiencyDesc: 'E en direct = (S_out / S_in) · (1 − δ)',
    tokenFertilityTitle: 'Fertilité des jetons',
    tokenFertilityDesc: 'Mesure la prime de coût de tokenisation de votre contenu français vs. anglais. Le français montre typiquement une prime de 1,1-1,5x par rapport à l\'anglais pour le contenu général. Recherche : Petrov et al. 2023, Lundin et al. 2025.',
    technicalDeepDive: 'Analyse technique approfondie',
    evaluationRubric: 'Grille d\'évaluation',
    semanticAlignment: 'Alignement sémantique',
    temporalAccuracy: 'Précision temporelle',
    linguisticDensity: 'Densité linguistique',
    discoverability: 'Découvrabilité',
    preFix: 'Avant correction',
    postFix: 'Après correction',
    tokenDecayFactor: 'Facteur de fertilité des jetons (δ)',
    semanticIn: 'Sémantique entrée (S_in)',
    semanticOut: 'Sémantique sortie (S_out)',
    current: 'Actuel',
    target: 'Cible',
    the9Standard: 'Le standard 9/10',
    improvement: 'Amélioration',
    fertilityScore: 'Score de fertilité',

    // General
    search: 'Rechercher...',
    notifications: 'Notifications',
    viewDetails: 'Voir les détails',
    critical: 'Critique',
    warning: 'Avertissement',
    success: 'Succès',
    info: 'Info',
  }
}

const LanguageContext = createContext()

export function LanguageProvider({ children }) {
  const [lang, setLang] = useState('en')

  const t = useCallback((key, params = {}) => {
    let text = translations[lang]?.[key] || translations.en?.[key] || key
    Object.entries(params).forEach(([k, v]) => {
      text = text.replace(`{${k}}`, v)
    })
    return text
  }, [lang])

  const toggleLang = useCallback(() => {
    setLang(prev => prev === 'en' ? 'fr' : 'en')
  }, [])

  return (
    <LanguageContext.Provider value={{ lang, setLang, toggleLang, t }}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  const ctx = useContext(LanguageContext)
  if (!ctx) throw new Error('useLanguage must be used within LanguageProvider')
  return ctx
}
