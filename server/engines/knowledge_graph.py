"""
VisiMind — Engine 5: Neuro-Symbolic Knowledge Graph
Deterministic entity binding using fuzzy logic to constrain LLM generative output.

Implements:
  - KGQA Scoring: S_KGQA_out = {(e, Score(e)) : e in E}
  - Fuzzy Union:  T(v?) = I - prod_{1<=i<=K}(I - T(v_i))
  - Entity-Attribute-Relationship triple store
  - Constraint boundary computation for DPO integration
"""
import json
import uuid
import math
from datetime import datetime
from typing import Optional


# =============================================================================
# Knowledge Graph Core — Triple Store
# =============================================================================

class KGTriple:
    """A single (subject, predicate, object) triple with confidence score."""
    __slots__ = ("subject", "predicate", "obj", "confidence", "source", "lang", "created_at")

    def __init__(self, subject: str, predicate: str, obj: str,
                 confidence: float = 1.0, source: str = "pim", lang: str = "en"):
        self.subject = subject
        self.predicate = predicate
        self.obj = obj
        self.confidence = max(0.0, min(1.0, confidence))
        self.source = source
        self.lang = lang
        self.created_at = datetime.utcnow().isoformat()


class KnowledgeGraph:
    """
    In-memory Knowledge Graph with fuzzy logic scoring.
    Designed to bind LLM generative output to explicit relational truth.
    """

    def __init__(self):
        self.triples: list[KGTriple] = []
        self.entities: dict[str, dict] = {}  # entity_id -> metadata
        self._index_by_subject: dict[str, list[int]] = {}
        self._index_by_object: dict[str, list[int]] = {}

    def add_entity(self, entity_id: str, entity_type: str, label: str,
                   label_fr: str = "", metadata: dict = None):
        """Register an entity node."""
        self.entities[entity_id] = {
            "id": entity_id,
            "type": entity_type,
            "label": label,
            "label_fr": label_fr,
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat(),
        }

    def add_triple(self, subject: str, predicate: str, obj: str,
                   confidence: float = 1.0, source: str = "pim", lang: str = "en"):
        """Add a (subject, predicate, object) relationship with confidence."""
        triple = KGTriple(subject, predicate, obj, confidence, source, lang)
        idx = len(self.triples)
        self.triples.append(triple)

        self._index_by_subject.setdefault(subject, []).append(idx)
        self._index_by_object.setdefault(obj, []).append(idx)

    def query_entity(self, entity_id: str) -> list[dict]:
        """Get all triples where entity is subject."""
        indices = self._index_by_subject.get(entity_id, [])
        return [self._triple_to_dict(self.triples[i]) for i in indices]

    def query_attribute(self, entity_id: str, predicate: str) -> Optional[dict]:
        """Get a specific attribute of an entity."""
        indices = self._index_by_subject.get(entity_id, [])
        for i in indices:
            t = self.triples[i]
            if t.predicate == predicate:
                return self._triple_to_dict(t)
        return None

    def _triple_to_dict(self, t: KGTriple) -> dict:
        return {
            "subject": t.subject,
            "predicate": t.predicate,
            "object": t.obj,
            "confidence": t.confidence,
            "source": t.source,
            "lang": t.lang,
        }

    # =========================================================================
    # KGQA Scoring — S_KGQA_out = {(e, Score(e)) : e in E}
    # =========================================================================

    def kgqa_score(self, query_entities: list[str]) -> dict:
        """
        Knowledge Graph Question Answering score.
        For each entity in the query set, compute an aggregate confidence score
        based on all triples involving that entity.

        Returns:
            S_KGQA_out = {(e, Score(e)) : e in E}
        """
        scores = {}
        for entity_id in query_entities:
            indices = self._index_by_subject.get(entity_id, [])
            if not indices:
                scores[entity_id] = 0.0
                continue

            # Score = geometric mean of triple confidences (rewards consistent high confidence)
            confidences = [self.triples[i].confidence for i in indices]
            product = 1.0
            for c in confidences:
                product *= c
            geo_mean = product ** (1.0 / len(confidences))

            # Density bonus: more triples = more grounded entity
            density_factor = min(len(confidences) / 10.0, 1.0)

            scores[entity_id] = round(geo_mean * (0.7 + 0.3 * density_factor), 4)

        return {"S_KGQA_out": scores}

    # =========================================================================
    # Fuzzy Union — T(v?) = I - prod_{1<=i<=K}(I - T(v_i))
    # =========================================================================

    def fuzzy_union(self, child_scores: list[float]) -> float:
        """
        Compute fuzzy union of child node truth values.
        T(v?) = I - prod_{1<=i<=K}(I - T(v_i))

        This ensures the LLM cannot hallucinate beyond defined boundaries:
        the union of all child truths creates an upper bound on what the
        generative output can claim.

        Args:
            child_scores: List of truth values T(v_i) in [0, 1]

        Returns:
            T(v?): The fuzzy union truth value
        """
        if not child_scores:
            return 0.0

        product = 1.0
        for t_vi in child_scores:
            clamped = max(0.0, min(1.0, t_vi))
            product *= (1.0 - clamped)

        return round(1.0 - product, 6)

    # =========================================================================
    # Constraint Boundary Computation — for DPO Hard Attributes
    # =========================================================================

    def compute_constraint_boundary(self, entity_id: str) -> dict:
        """
        Compute the hard constraint boundary for an entity.
        Returns the set of attributes that MUST be respected (confidence >= 0.9)
        and the fuzzy boundary score for the entity as a whole.

        Used by the DPO framework to set P(contradictory_token) = 0.
        """
        indices = self._index_by_subject.get(entity_id, [])
        if not indices:
            return {"entity": entity_id, "hard_constraints": [], "boundary_score": 0.0}

        hard_constraints = []
        all_confidences = []

        for i in indices:
            t = self.triples[i]
            all_confidences.append(t.confidence)

            if t.confidence >= 0.9:
                hard_constraints.append({
                    "predicate": t.predicate,
                    "value": t.obj,
                    "confidence": t.confidence,
                    "source": t.source,
                    "constraint_type": "hard",
                    "dpo_action": "P(contradiction) = 0",
                })

        # Fuzzy boundary = union of all attribute confidences
        boundary_score = self.fuzzy_union(all_confidences)

        return {
            "entity": entity_id,
            "entity_meta": self.entities.get(entity_id, {}),
            "hard_constraints": hard_constraints,
            "soft_attributes": [
                self._triple_to_dict(self.triples[i])
                for i in indices
                if self.triples[i].confidence < 0.9
            ],
            "boundary_score": boundary_score,
            "total_triples": len(indices),
            "hard_count": len(hard_constraints),
        }

    # =========================================================================
    # Graph Export — for @graph JSON-LD integration
    # =========================================================================

    def export_jsonld_graph(self, entity_ids: list[str] = None) -> dict:
        """
        Export the KG as a JSON-LD @graph with deterministic IDs.
        This creates a unified, disambiguated entity graph that overrides
        heuristic text-generation-inference parsers.
        """
        if entity_ids is None:
            entity_ids = list(self.entities.keys())

        graph_nodes = []

        for eid in entity_ids:
            meta = self.entities.get(eid, {})
            triples = self.query_entity(eid)

            node = {
                "@id": f"urn:visimind:entity:{eid}",
                "@type": meta.get("type", "Thing"),
                "name": meta.get("label", eid),
            }

            if meta.get("label_fr"):
                node["alternateName"] = meta["label_fr"]

            # Add all attributes from triples
            properties = {}
            for t in triples:
                pred = t["predicate"]
                if pred not in properties:
                    properties[pred] = []
                properties[pred].append({
                    "@value": t["object"],
                    "confidence": t["confidence"],
                    "source": t["source"],
                })

            # Flatten single-value properties
            for pred, values in properties.items():
                if len(values) == 1:
                    node[pred] = values[0]["@value"]
                else:
                    node[pred] = [v["@value"] for v in values]

            graph_nodes.append(node)

        return {
            "@context": {
                "@vocab": "https://schema.org/",
                "visimind": "https://visimind.ai/ontology/",
                "confidence": "visimind:confidence",
                "kgqa_score": "visimind:kgqaScore",
            },
            "@graph": graph_nodes,
        }

    # =========================================================================
    # Serialization
    # =========================================================================

    def to_dict(self) -> dict:
        """Serialize the entire KG for storage."""
        return {
            "entities": self.entities,
            "triples": [self._triple_to_dict(t) for t in self.triples],
            "stats": {
                "entity_count": len(self.entities),
                "triple_count": len(self.triples),
                "avg_confidence": round(
                    sum(t.confidence for t in self.triples) / max(len(self.triples), 1), 3
                ),
            },
        }


# =============================================================================
# KG Builder — constructs a KG from product/brand data
# =============================================================================

def build_brand_kg(brand: dict, products: list[dict]) -> KnowledgeGraph:
    """
    Build a comprehensive Knowledge Graph for a brand and its products.
    This creates the deterministic relational structure that binds LLM output.
    """
    kg = KnowledgeGraph()

    brand_id = brand.get("id", brand.get("slug", "unknown"))
    brand_name = brand.get("name", brand_id)

    # Brand entity
    kg.add_entity(brand_id, "Brand", brand_name, metadata={
        "description": brand.get("description", ""),
        "domain": "luxury_retail",
        "market": "CA",
    })

    # Organization entity (parent)
    org_id = f"{brand_id}-org"
    kg.add_entity(org_id, "Organization", brand_name)
    kg.add_triple(org_id, "brand", brand_id, confidence=1.0, source="pim")

    for product in products:
        pid = product.get("id", str(uuid.uuid4()))
        name_en = product.get("name_en", "")
        name_fr = product.get("name_fr", "")

        # Product entity
        kg.add_entity(pid, "Product", name_en, label_fr=name_fr, metadata={
            "category": product.get("category", ""),
            "price_cad": product.get("price_cad"),
        })

        # Brand → Product relationship
        kg.add_triple(brand_id, "hasProduct", pid, confidence=1.0, source="pim")
        kg.add_triple(pid, "brand", brand_id, confidence=1.0, source="pim")

        # Hard attributes (confidence 1.0 — these are DPO constraints)
        if product.get("thermal_rating"):
            kg.add_triple(pid, "thermalRating", product["thermal_rating"],
                          confidence=1.0, source="pim")
            if name_fr:
                kg.add_triple(pid, "thermalRating", product["thermal_rating"],
                              confidence=1.0, source="pim", lang="fr")

        if product.get("fill_power"):
            kg.add_triple(pid, "fillPower", product["fill_power"],
                          confidence=1.0, source="pim")

        if product.get("material"):
            kg.add_triple(pid, "material", product["material"],
                          confidence=1.0, source="pim")

        # Certifications (high confidence — verified by third party)
        certs = product.get("certifications", "[]")
        if isinstance(certs, str):
            try:
                certs = json.loads(certs)
            except json.JSONDecodeError:
                certs = []
        for cert in certs:
            kg.add_triple(pid, "certification", cert, confidence=0.95, source="certification_body")

        # Pricing (moderate confidence — changes frequently)
        if product.get("price_cad"):
            kg.add_triple(pid, "price", f"{product['price_cad']} CAD",
                          confidence=0.8, source="pim")

        # Bilingual mapping triples
        bilingual = product.get("bilingual_mapping", "{}")
        if isinstance(bilingual, str):
            try:
                bilingual = json.loads(bilingual)
            except json.JSONDecodeError:
                bilingual = {}
        for en_term, fr_term in bilingual.items():
            mapping_id = f"{pid}-map-{en_term[:20].replace(' ', '_')}"
            kg.add_triple(pid, "bilingualTerm", f"{en_term}|{fr_term}",
                          confidence=1.0, source="bilingual_bridge", lang="fr")

    return kg


# =============================================================================
# KGQA Validation — validate LLM output against KG
# =============================================================================

def validate_against_kg(kg: KnowledgeGraph, entity_id: str, llm_claims: dict) -> dict:
    """
    Validate LLM-generated claims against the Knowledge Graph.
    Returns a detailed report of which claims are grounded vs hallucinated.

    Args:
        kg: The Knowledge Graph
        entity_id: Entity being described
        llm_claims: dict of {attribute: claimed_value}

    Returns:
        Validation report with per-claim grounding status
    """
    boundary = kg.compute_constraint_boundary(entity_id)
    hard_map = {c["predicate"]: c["value"] for c in boundary["hard_constraints"]}

    results = []
    grounded_count = 0
    violated_count = 0
    unverifiable_count = 0

    for attr, claimed_value in llm_claims.items():
        kg_value = hard_map.get(attr)

        if kg_value is not None:
            # Hard constraint exists — check compliance
            is_match = str(claimed_value).lower().strip() == str(kg_value).lower().strip()
            if is_match:
                grounded_count += 1
                results.append({
                    "attribute": attr,
                    "claimed": claimed_value,
                    "kg_truth": kg_value,
                    "status": "grounded",
                    "constraint_type": "hard",
                })
            else:
                violated_count += 1
                results.append({
                    "attribute": attr,
                    "claimed": claimed_value,
                    "kg_truth": kg_value,
                    "status": "E1_semantic_override",
                    "constraint_type": "hard",
                    "dpo_action": "P(contradictory_token) → 0",
                })
        else:
            # No hard constraint — check soft attributes
            soft_match = None
            for soft in boundary["soft_attributes"]:
                if soft["predicate"] == attr:
                    soft_match = soft
                    break

            if soft_match:
                grounded_count += 1
                results.append({
                    "attribute": attr,
                    "claimed": claimed_value,
                    "kg_truth": soft_match["object"],
                    "status": "soft_grounded",
                    "confidence": soft_match["confidence"],
                })
            else:
                unverifiable_count += 1
                results.append({
                    "attribute": attr,
                    "claimed": claimed_value,
                    "kg_truth": None,
                    "status": "unverifiable",
                })

    total = len(llm_claims)
    grounding_ratio = grounded_count / max(total, 1)

    # Compute KGQA score for the entity
    kgqa = kg.kgqa_score([entity_id])
    entity_score = kgqa["S_KGQA_out"].get(entity_id, 0.0)

    return {
        "entity_id": entity_id,
        "total_claims": total,
        "grounded": grounded_count,
        "violations": violated_count,
        "unverifiable": unverifiable_count,
        "grounding_ratio": round(grounding_ratio, 3),
        "kgqa_score": entity_score,
        "boundary_score": boundary["boundary_score"],
        "results": results,
        "verdict": "PASS" if violated_count == 0 and grounding_ratio >= 0.7 else "FAIL",
    }


# =============================================================================
# DB Persistence — store/load KG from SQLite
# =============================================================================

async def store_kg(db, brand_id: str, kg: KnowledgeGraph):
    """Persist a Knowledge Graph to the kg_entities and kg_triples tables."""
    now = datetime.utcnow().isoformat()

    # Clear existing KG for this brand
    await db.execute("DELETE FROM kg_triples WHERE brand_id = ?", (brand_id,))
    await db.execute("DELETE FROM kg_entities WHERE brand_id = ?", (brand_id,))

    # Store entities
    for eid, meta in kg.entities.items():
        await db.execute(
            """INSERT INTO kg_entities (id, brand_id, entity_type, label, label_fr, metadata, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (eid, brand_id, meta.get("type", "Thing"), meta.get("label", ""),
             meta.get("label_fr", ""), json.dumps(meta.get("metadata", {})), now),
        )

    # Store triples
    for t in kg.triples:
        await db.execute(
            """INSERT INTO kg_triples (id, brand_id, subject, predicate, object, confidence, source, lang, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (str(uuid.uuid4()), brand_id, t.subject, t.predicate, t.obj,
             t.confidence, t.source, t.lang, now),
        )

    await db.commit()


async def load_kg(db, brand_id: str) -> KnowledgeGraph:
    """Load a Knowledge Graph from the database."""
    kg = KnowledgeGraph()

    # Load entities
    cursor = await db.execute(
        "SELECT * FROM kg_entities WHERE brand_id = ?", (brand_id,)
    )
    for row in await cursor.fetchall():
        metadata = {}
        if row["metadata"]:
            try:
                metadata = json.loads(row["metadata"])
            except json.JSONDecodeError:
                pass
        kg.add_entity(row["id"], row["entity_type"], row["label"],
                      label_fr=row["label_fr"] or "", metadata=metadata)

    # Load triples
    cursor = await db.execute(
        "SELECT * FROM kg_triples WHERE brand_id = ? ORDER BY created_at", (brand_id,)
    )
    for row in await cursor.fetchall():
        kg.add_triple(row["subject"], row["predicate"], row["object"],
                      confidence=row["confidence"], source=row["source"],
                      lang=row["lang"] or "en")

    return kg
