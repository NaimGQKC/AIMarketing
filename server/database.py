"""
VisiMind — SQLite Database Layer
"""
import aiosqlite
from pathlib import Path
from config import DB_PATH

DATABASE = DB_PATH


async def get_db():
    """Yield an async database connection."""
    db = await aiosqlite.connect(DATABASE)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()


async def init_db():
    """Create all tables if they don't exist."""
    async with aiosqlite.connect(DATABASE) as db:
        await db.executescript(SCHEMA)
        await db.commit()


SCHEMA = """
-- Brands
CREATE TABLE IF NOT EXISTS brands (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products (Ground Truth PIM)
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    brand_id TEXT NOT NULL REFERENCES brands(id),
    name_en TEXT NOT NULL,
    name_fr TEXT,
    category TEXT,
    description_en TEXT,
    description_fr TEXT,
    price_cad REAL,
    thermal_rating TEXT,
    fill_power TEXT,
    material TEXT,
    certifications TEXT,  -- JSON array
    bilingual_mapping TEXT,  -- JSON: {en_term: fr_term, ...}
    attributes TEXT,  -- JSON: additional key-value pairs
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Signal Gaps (Diagnose)
CREATE TABLE IF NOT EXISTS signal_gaps (
    id TEXT PRIMARY KEY,
    brand_id TEXT REFERENCES brands(id),
    product_id TEXT REFERENCES products(id),
    query TEXT NOT NULL,
    lang TEXT NOT NULL DEFAULT 'EN',
    gap_type TEXT NOT NULL,  -- 'Entity Trust' | 'Fact Density' | 'Tokenization Premium' (legacy: 'Token Decay')
    severity TEXT NOT NULL DEFAULT 'warning',
    ai_response_quality INTEGER DEFAULT 0,
    source_of_truth_label TEXT,
    source_of_truth_url TEXT,
    source_of_truth_detail TEXT,
    source_of_hallucination_label TEXT,
    source_of_hallucination_url TEXT,
    source_of_hallucination_detail TEXT,
    ai_said TEXT,
    brand_truth TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Probe Results (Inference Lab raw data)
CREATE TABLE IF NOT EXISTS probe_results (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    query TEXT NOT NULL,
    lang TEXT NOT NULL,
    iteration INTEGER NOT NULL,
    model TEXT NOT NULL,
    response_text TEXT,
    citations TEXT,  -- JSON array of cited URLs
    brand_mentioned INTEGER DEFAULT 0,
    brand_mention_logprob REAL,  -- token-level certainty
    recommendation_position INTEGER,  -- rank in recommendations list
    response_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Async Tasks (polling pattern)
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,  -- 'probe' | 'audit' | 'deploy'
    status TEXT NOT NULL DEFAULT 'pending',  -- pending | running | completed | failed
    progress INTEGER DEFAULT 0,
    total INTEGER DEFAULT 0,
    result TEXT,  -- JSON result payload
    error TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fix Kits (Remediation Factory)
CREATE TABLE IF NOT EXISTS fix_kits (
    id TEXT PRIMARY KEY,
    brand_id TEXT REFERENCES brands(id),
    product_id TEXT REFERENCES products(id),
    type TEXT NOT NULL,  -- 'hardAttributes' | 'jsonLd' | 'truthClip'
    status TEXT NOT NULL DEFAULT 'ready',  -- ready | deploying | deployed
    payload TEXT,  -- JSON: the fix data
    impact TEXT,
    deployed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit Runs (Verification Loop)
CREATE TABLE IF NOT EXISTS audit_runs (
    id TEXT PRIMARY KEY,
    brand_id TEXT REFERENCES brands(id),
    fix_kit_id TEXT REFERENCES fix_kits(id),
    query TEXT,
    day_number INTEGER,
    scheduled_date TEXT,
    status TEXT NOT NULL DEFAULT 'scheduled',  -- scheduled | running | passed | failed | pending
    label TEXT,
    detail TEXT,
    score_technical_accuracy REAL,
    score_citation_fidelity REAL,
    score_linguistic_parity REAL,
    score_overall REAL,
    before_response TEXT,
    after_response TEXT,
    before_citations TEXT,  -- JSON
    after_citations TEXT,  -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PIM Connections
CREATE TABLE IF NOT EXISTS pim_connections (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,  -- 'pim' | 'monitoring'
    provider TEXT NOT NULL,  -- 'shopify' | 'akeneo' | 'peec' | 'otterly'
    status TEXT NOT NULL DEFAULT 'disconnected',
    last_sync TIMESTAMP,
    items_synced INTEGER DEFAULT 0,
    queries_tracked INTEGER DEFAULT 0,
    errors INTEGER DEFAULT 0,
    config TEXT  -- JSON config blob
);

-- Reasoning Parity Stats
CREATE TABLE IF NOT EXISTS parity_stats (
    id TEXT PRIMARY KEY,
    en_visibility REAL NOT NULL,
    fr_visibility REAL NOT NULL,
    en_queries INTEGER DEFAULT 0,
    fr_queries INTEGER DEFAULT 0,
    en_hallucinations INTEGER DEFAULT 0,
    fr_hallucinations INTEGER DEFAULT 0,
    en_avg_tokens REAL,
    en_max_tokens INTEGER,
    fr_avg_tokens REAL,
    fr_max_tokens INTEGER,
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alignment Trend (daily snapshots)
CREATE TABLE IF NOT EXISTS alignment_trend (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT NOT NULL,
    en_score REAL,
    fr_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Side-by-Side Reasoning snapshots
CREATE TABLE IF NOT EXISTS reasoning_snapshots (
    id TEXT PRIMARY KEY,
    brand_id TEXT REFERENCES brands(id),
    query TEXT NOT NULL,
    before_verdict TEXT,
    before_reasoning TEXT,
    before_citations TEXT,  -- JSON array
    before_confidence TEXT,
    after_verdict TEXT,
    after_reasoning TEXT,
    after_citations TEXT,  -- JSON array
    after_confidence TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Knowledge Graph Entities
CREATE TABLE IF NOT EXISTS kg_entities (
    id TEXT PRIMARY KEY,
    brand_id TEXT NOT NULL REFERENCES brands(id),
    entity_type TEXT NOT NULL,  -- 'Brand' | 'Product' | 'Organization' | 'Certification'
    label TEXT NOT NULL,
    label_fr TEXT,
    metadata TEXT,  -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Knowledge Graph Triples
CREATE TABLE IF NOT EXISTS kg_triples (
    id TEXT PRIMARY KEY,
    brand_id TEXT NOT NULL REFERENCES brands(id),
    subject TEXT NOT NULL,
    predicate TEXT NOT NULL,
    object TEXT NOT NULL,
    confidence REAL NOT NULL DEFAULT 1.0,
    source TEXT DEFAULT 'pim',  -- 'pim' | 'certification_body' | 'bilingual_bridge'
    lang TEXT DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RAFT (Retrieval-Augmented Fine-Tuning) Schedule
CREATE TABLE IF NOT EXISTS raft_schedule (
    id TEXT PRIMARY KEY,
    brand_id TEXT NOT NULL REFERENCES brands(id),
    cycle INTEGER NOT NULL,
    scheduled_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled',  -- scheduled | running | completed | failed
    e_score_before REAL,
    e_score_after REAL,
    delta_e REAL,
    e1_errors_purged INTEGER DEFAULT 0,
    detail TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Syndication Nodes (EEE Semantic Saturation)
CREATE TABLE IF NOT EXISTS syndication_nodes (
    id TEXT PRIMARY KEY,
    brand_id TEXT NOT NULL REFERENCES brands(id),
    node_type TEXT NOT NULL,
    tier TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'planned',  -- planned | active | deployed | stale
    authority_weight REAL DEFAULT 0,
    last_touched TIMESTAMP,
    uri TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Freshness Cycles (EEE External RAFT)
CREATE TABLE IF NOT EXISTS freshness_cycles (
    id TEXT PRIMARY KEY,
    brand_id TEXT NOT NULL REFERENCES brands(id),
    cycle_number INTEGER NOT NULL,
    executed_at TIMESTAMP,
    freshness_score REAL,
    e_score_before REAL,
    e_score_after REAL,
    nodes_touched INTEGER DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'scheduled',  -- scheduled | running | completed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crawler Visits (AI bot detection logging)
CREATE TABLE IF NOT EXISTS crawler_visits (
    id TEXT PRIMARY KEY,
    timestamp TEXT,
    crawler_name TEXT,
    user_agent TEXT,
    path TEXT,
    brand_id TEXT,
    response_code INTEGER,
    response_time_ms REAL
);

-- E-Score History (tracks 0.6 → 1.4+ path)
CREATE TABLE IF NOT EXISTS e_score_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_id TEXT REFERENCES brands(id),
    e_score REAL NOT NULL,
    s_in REAL,
    s_out REAL,
    delta REAL,
    status TEXT,  -- critical_failure | sub_threshold | marginal | strong | optimal
    trigger TEXT,  -- 'audit' | 'raft_cycle' | 'kit_deployment' | 'manual'
    detail TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
