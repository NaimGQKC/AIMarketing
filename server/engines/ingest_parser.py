"""
VisiMind — Ingestion Parser
Parses pre-collected probe data files (.txt, .md, .json) into structured records.
Handles the consistent format: Query: → response → --- SOURCE LINKS --- → links.
"""
import re
import json
from typing import Optional


# --- French Detection Heuristics ---

_FRENCH_INDICATORS = [
    # Common French words that rarely appear in English text
    "meilleur", "montréal", "québec", "chaussures", "manteau", "boutique",
    "livraison", "marque", "canadienne", "durables", "résultat", "détails",
    "également", "disponible", "trouvez", "recherche", "spécialisé",
    "fermé", "ouvert", "magasin", "achat", "offre", "réduction",
    # French articles / prepositions
    "d'", "l'", "n'", "c'est", "qu'", "j'ai", "aujourd'hui",
    # French accented patterns
    "é", "è", "ê", "ë", "à", "â", "ù", "û", "ç", "ô", "î",
]

_FRENCH_STRONG_INDICATORS = [
    "meilleur", "québec", "montréal", "chaussures", "manteau",
    "livraison", "marque", "canadienne", "fermé", "résultat",
    "je ne", "je recommande", "voici", "trouvez",
]


def detect_language(query: str, response_text: str = "") -> str:
    """
    Detect whether the probe is French or English.
    Uses the query as primary signal, response as secondary.
    """
    combined = (query + " " + response_text).lower()

    # Strong indicator check (single match is enough)
    for indicator in _FRENCH_STRONG_INDICATORS:
        if indicator in combined:
            return "FR"

    # Weak indicator accumulation
    score = 0
    for indicator in _FRENCH_INDICATORS:
        if indicator in combined:
            score += 1

    return "FR" if score >= 3 else "EN"


# --- Brand Detection ---

# Known brands from the current DB + common luxury brands to auto-detect
_KNOWN_BRANDS = {
    "mackage": "Mackage",
    "ssense": "SSENSE",
    "aldo": "Aldo",
    "holt renfrew": "Holt Renfrew",
    "royalmount": "Royalmount",
    "canada goose": "Canada Goose",
    "aritzia": "Aritzia",
    "la maison simons": "La Maison Simons",
    "simons": "Simons",
    "browns": "Browns",
    "ogilvy": "Ogilvy",
    "nordstrom": "Nordstrom",
    "groupe dynamite": "Groupe Dynamite",
    "frank and oak": "Frank And Oak",
    "lululemon": "Lululemon",
    "roots": "Roots",
}


def detect_brands(response_text: str, query: str = "") -> list[dict]:
    """
    Detect all brands mentioned in the response text with their positions.
    Returns list of {name, position, mentioned} dicts.
    """
    combined = response_text.lower()
    lines = response_text.split("\n")
    results = []

    for key, name in _KNOWN_BRANDS.items():
        if key in combined or key in query.lower():
            # Find position — look for the brand in recommendation listings
            position = _find_brand_position(lines, key)
            results.append({
                "name": name,
                "slug": key.replace(" ", "-"),
                "position": position,
                "mentioned": True,
            })

    return results


def _find_brand_position(lines: list[str], brand_key: str) -> Optional[int]:
    """
    Try to find the position/rank of a brand in the recommendation list.
    Looks for numbered entries, header-like lines, etc.
    """
    position = 0
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Check if this looks like a recommendation entry
        # (contains a name, rating, or is a section header)
        is_entry = bool(re.match(r'^[\d.]+[.)\s]', stripped)) or \
                   bool(re.match(r'^[A-Z]', stripped) and '|' in stripped) or \
                   bool(re.search(r'\d+\.\d+\s*\(', stripped))  # Rating pattern like "4.2 (1.3K)"

        if is_entry:
            position += 1
            if brand_key in stripped.lower():
                return position

    # If not found in structured entries, just check if mentioned at all
    for i, line in enumerate(lines):
        if brand_key in line.lower():
            return i + 1

    return None


# --- File Parsing ---

def parse_probe_file(file_content: str) -> list[dict]:
    """
    Parse a probe data file into structured records.

    Expected format per block:
    ```
    Query: <query text>

    <AI response text...>

    --- SOURCE LINKS ---
    <source 1>
    <source 2>
    ...
    ```

    Multiple blocks can exist in one file, separated by blank lines
    and a new "Query:" header.
    """
    blocks = _split_into_blocks(file_content)
    results = []

    for block in blocks:
        parsed = _parse_single_block(block)
        if parsed:
            results.append(parsed)

    return results


def _split_into_blocks(content: str) -> list[str]:
    """
    Split file content into individual probe blocks.
    Each block starts with 'Query:'.
    """
    # Split on "Query:" while keeping the delimiter
    parts = re.split(r'(?=^Query:\s)', content, flags=re.MULTILINE)
    blocks = [p.strip() for p in parts if p.strip() and p.strip().startswith("Query:")]

    if not blocks and content.strip():
        # Maybe the file has a single block without "Query:" prefix
        # Try to treat the entire file as one block
        blocks = [content.strip()]

    return blocks


def _parse_single_block(block: str) -> Optional[dict]:
    """
    Parse a single probe block into a structured record.
    """
    # Extract query
    query_match = re.match(r'^Query:\s*(.+?)(?:\n|$)', block, re.IGNORECASE)
    if query_match:
        query = query_match.group(1).strip()
        rest = block[query_match.end():]
    else:
        # No "Query:" header — skip or try to infer
        return None

    # Split on source links delimiter
    source_delimiter = re.split(r'---\s*SOURCE\s*LINKS\s*---', rest, flags=re.IGNORECASE)

    response_text = source_delimiter[0].strip()
    source_links = []

    if len(source_delimiter) > 1:
        links_section = source_delimiter[1].strip()
        # Each non-empty line is a source
        for line in links_section.split("\n"):
            line = line.strip()
            if line and line != "---":
                source_links.append(line)

    # Detect language
    lang = detect_language(query, response_text)

    # Detect brands
    brands = detect_brands(response_text, query)

    return {
        "query": query,
        "lang": lang,
        "response_text": response_text,
        "source_links": source_links,
        "brands_detected": brands,
    }


# --- Source Classification ---

_TOXIC_PATTERNS = [
    "reddit.com", "reddit ", "r/", "trustpilot", "blogspot",
    "blog", "quora", "yahoo answers", "youtube review",
    "forum", "wordpress", "medium.com",
]

_AUTHORITATIVE_PATTERNS = [
    "ucp", "acp", "feed://", ".gov", ".gc.ca",
    "official", "brand site", "manufacturer",
    "schema.org", "certification", "registry",
]

_STALE_YEAR_THRESHOLD = 2023  # Sources older than this are considered stale


def classify_source(source: str) -> dict:
    """
    Classify a source link/label as toxic, authoritative, or neutral.
    Returns: {label, classification, is_toxic, is_stale}
    """
    source_lower = source.lower()

    is_toxic = any(p in source_lower for p in _TOXIC_PATTERNS)
    is_authoritative = any(p in source_lower for p in _AUTHORITATIVE_PATTERNS)

    # Check for staleness (year detection)
    year_match = re.search(r'\b(20\d{2})\b', source)
    is_stale = False
    if year_match:
        year = int(year_match.group(1))
        if year < _STALE_YEAR_THRESHOLD:
            is_stale = True

    if is_toxic:
        classification = "toxic"
    elif is_authoritative:
        classification = "authoritative"
    elif is_stale:
        classification = "stale"
    else:
        classification = "neutral"

    return {
        "label": source,
        "classification": classification,
        "is_toxic": is_toxic or is_stale,
        "is_stale": is_stale,
    }


def classify_sources(sources: list[str]) -> list[dict]:
    """Classify a list of source strings."""
    return [classify_source(s) for s in sources]
