"""
VisiMind — Pydantic Models (Request/Response Schemas)
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# --- Dashboard ---
class MetricsResponse(BaseModel):
    inference_score: float
    active_remediations: int
    verified_fixes: int
    token_density: float
    inference_score_trend: float
    active_remediations_trend: float
    verified_fixes_trend: float
    token_density_trend: float


class RedAlert(BaseModel):
    id: str
    query: str
    agent: str
    issue: str
    severity: str
    lang: str


class ProtocolStatus(BaseModel):
    name: str
    status: str
    last_ping: str
    feeds: int


class AlignmentPoint(BaseModel):
    day: str
    en: float
    fr: float


# --- Connect ---
class PIMConnection(BaseModel):
    id: str
    name: str
    type: str
    provider: str
    status: str
    description: Optional[str] = None
    last_sync: Optional[str] = None
    items_synced: int = 0
    queries_tracked: int = 0
    errors: int = 0
    icon: Optional[str] = None


class FeedStatus(BaseModel):
    feed: str
    items: int
    last_sync: str
    status: str
    errors: int


# --- Diagnose ---
class SourceInfo(BaseModel):
    label: str
    url: Optional[str] = None
    detail: str


class SignalGap(BaseModel):
    id: str
    query: str
    lang: str
    gap_type: str
    severity: str
    ai_response_quality: int
    source_of_truth: SourceInfo
    source_of_hallucination: SourceInfo
    ai_said: str
    brand_truth: str


class ParityStats(BaseModel):
    en: float
    fr: float
    en_queries: int
    fr_queries: int
    en_hallucinations: int
    fr_hallucinations: int
    token_breakdown: dict


class ProbeRequest(BaseModel):
    query: str
    lang: str = "EN"
    iterations: int = Field(default=3, ge=1, le=10)
    use_golden_set: bool = Field(default=True, description="Generate 5 query variations instead of repeating one query")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class TaskStatus(BaseModel):
    id: str
    type: str
    status: str
    progress: int
    total: int
    result: Optional[dict] = None
    error: Optional[str] = None


# --- Remediate ---
class FixKit(BaseModel):
    id: str
    type: str
    brand: str
    product: str
    status: str
    payload: Optional[dict] = None
    impact: str


class DeployRequest(BaseModel):
    kit_id: str


class FeedComparison(BaseModel):
    before: dict
    after: dict


# --- Verify ---
class AuditScheduleItem(BaseModel):
    day: int
    date: str
    status: str
    label: str


class AuditEvent(BaseModel):
    id: str
    date: str
    label: str
    status: str
    detail: str
    score: Optional[float] = None


class ConfidencePoint(BaseModel):
    day: str
    mackage: Optional[float] = None
    ssense: Optional[float] = None
    aldo: Optional[float] = None


class ReasoningSide(BaseModel):
    verdict: str
    reasoning: str
    citations: list[str]
    confidence: str


class SideBySideReasoning(BaseModel):
    id: str
    brand: str
    query: str
    before: ReasoningSide
    after: ReasoningSide


class ScheduleAuditRequest(BaseModel):
    brand_id: str
    fix_kit_id: str
    days: list[int] = [3, 7, 14]


# --- UCP Manifest ---
class UCPManifest(BaseModel):
    schema_version: str = "1.0"
    organization: dict
    data_feeds: list[dict]
    capabilities: list[str]
    contact: dict


# --- Knowledge Graph ---
class KGEntityResponse(BaseModel):
    id: str
    entity_type: str
    label: str
    label_fr: str = ""
    triples: list[dict] = []
    kgqa_score: float = 0.0


class KGValidationRequest(BaseModel):
    entity_id: str
    claims: dict  # {attribute: claimed_value}


class KGValidationResponse(BaseModel):
    entity_id: str
    total_claims: int
    grounded: int
    violations: int
    unverifiable: int
    grounding_ratio: float
    kgqa_score: float
    boundary_score: float
    verdict: str
    results: list[dict]


# --- E-Score ---
class EScoreResponse(BaseModel):
    e_score: float
    s_in: float
    s_out: float
    delta: float
    delta_e: float
    status: str
    interpretation: str
    formula: str
    thresholds: dict
    path_to_optimal: list[dict]


# --- RAFT ---
class RAFTCadenceResponse(BaseModel):
    brand_id: str
    current_e_score: float
    target_e_score: float
    cadence_interval_days: int
    urgency: str
    total_cycles: int
    schedule: list[dict]
    methodology: dict


class RAFTCycleRequest(BaseModel):
    brand_id: str


# --- DPO Constraints ---
class DPOConstraintSet(BaseModel):
    product_id: str
    product_name: str
    brand: str
    constraints: list[dict]
    total_constraints: int
    contextual_success_rate: float
    kg_boundary_score: float
    dpo_config: dict


# --- EEE (External Environment Engineering) ---
class SyndicationNode(BaseModel):
    id: str
    type: str
    tier: str
    tier_label: str
    authority_weight: float
    status: str
    deployment: dict
    freshness_target: str


class CitationAuthority(BaseModel):
    brand_id: str
    authority_ratio: float
    total_citations_analyzed: int
    toxic_source_count: int
    clean_source_count: int
    countermeasures: list[dict]


class EEERoadmapPhase(BaseModel):
    phase: int
    name: str
    eee_vector: str
    duration: str
    projected_e: float
    actions: list[str]
    success_metric: str
    e_score_mechanism: str
