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
    iterations: int = Field(default=50, ge=1, le=200)


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
