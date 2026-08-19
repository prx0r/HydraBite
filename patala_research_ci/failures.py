"""Failure taxonomy for memory recall."""
from dataclasses import dataclass

@dataclass
class FailureAnalysis:
    question_id: str
    failure_type: str
    description: str
    severity: str  # low|medium|high

FAILURE_TYPES = {
    "WRONG_ENTITY": "Recalled wrong entity",
    "STALE_FACT": "Recalled outdated information",
    "MISSING_EDGE": "Graph traversal missed a relation",
    "FALSE_EDGE": "Hallucinated a non-existent relation",
    "SOURCE_COLLAPSE": "Attributed to wrong source",
    "TEMPORAL_COLLAPSE": "Mixed time periods",
    "OVER_RETRIEVAL": "Retrieved too much irrelevant context",
    "UNDER_RETRIEVAL": "Missed relevant context",
    "UNSUPPORTED_SYNTHESIS": "Combined facts from incompatible sources",
}

def classify_failure(question: Any, result: Any, ground_truth: dict) -> FailureAnalysis:
    """Classify why a recall failed."""
    if not result.correct:
        if not result.answer:
            return FailureAnalysis(question.question_id, "UNDER_RETRIEVAL",
                "No answer returned", "high")
        if result.answer and ground_truth.get("expected", "").lower() not in result.answer.lower():
            return FailureAnalysis(question.question_id, "WRONG_ENTITY",
                f"Got: {result.answer[:50]}", "high")
    return FailureAnalysis(question.question_id, "CORRECT", "", "low")
