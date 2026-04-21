#!/usr/bin/env python3
"""Mock deterministic scorer for the autoresearch test fixture.

Scores target/summarize.md against a 10-item checklist of features a good
summarization prompt tends to have. Returns a single number 0.0–1.0.

This is a MOCK: it scores structural properties of the prompt file, not
the quality of actual summaries. The purpose is to give the autoresearch
loop a deterministic, fast metric that responds to edits — so we can test
whether the loop is structured correctly, not whether it produces good
summaries. A real autoresearch run would use an LLM-based eval against
test cases.
"""
from pathlib import Path

PROMPT = Path(__file__).parent / "summarize.md"
text = PROMPT.read_text().lower()

checks = {
    "mentions_bullets":        "bullet" in text,
    "specifies_count":         any(s in text for s in ["3-5", "3 to 5", "3 bullets", "5 bullets", "three", "five"]),
    "specifies_length":        any(s in text for s in ["word", "under ", "max ", "no more than", "at most"]),
    "forbids_hallucination":   any(s in text for s in ["only include", "do not invent", "from the article", "do not add", "no facts not in", "faithful"]),
    "gives_example":           "example" in text or "for instance" in text,
    "specifies_order":         any(s in text for s in ["most important", "order of importance", "priority", "ranked"]),
    "forbids_filler":          any(s in text for s in ["no filler", "avoid phrases", "do not use", "no clichés", "no phrases like"]),
    "specifies_tone":          any(s in text for s in ["concise", "terse", "direct", "plain", "clear"]),
    "has_role":                any(s in text for s in ["you are", "you're a", "act as"]),
    "specifies_output_format": any(s in text for s in ["format:", "output:", "structure:", "return:", "respond with"]),
}

score = sum(checks.values()) / len(checks)
print(f"{score:.4f}")
