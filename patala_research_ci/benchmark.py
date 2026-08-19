"""Benchmark for HydraDB memory recall."""
import json
from typing import Any
from .hydradb import HydraDB
from .model import TrackedClaim, Dependency

@dataclass
class BenchmarkQuestion:
    question_id: str
    question: str
    expected_answer: str
    question_type: str  # factual|multi_hop|contradiction|temporal|negative
    ground_truth_refs: list[str]

@dataclass
class BenchmarkResult:
    question_id: str
    mode: str
    answer: str
    correct: bool
    latency_ms: float
    sources_used: list[str]

class BenchmarkSuite:
    def __init__(self, hydradb: HydraDB):
        self.hydradb = hydradb

    def generate_questions(self, ground_truth: list[dict]) -> list[BenchmarkQuestion]:
        """Auto-generate questions from ground truth."""
        questions = []
        for i, item in enumerate(ground_truth[:50]):
            questions.append(BenchmarkQuestion(
                question_id=f"Q{i:03d}",
                question=f"What is the title of item {item.get('id', '')}?",
                expected_answer=item.get("title", ""),
                question_type="factual",
                ground_truth_refs=[item.get("id", "")],
            ))
        return questions

    def evaluate(self, questions: list[BenchmarkQuestion], mode: str = "fast") -> list[BenchmarkResult]:
        """Evaluate questions against HydraDB."""
        results = []
        for q in questions:
            import time
            start = time.time()
            response = self.hydradb.query(q.question, mode=mode)
            latency = (time.time() - start) * 1000

            answer = response.get("result", {}).get("content", "")
            correct = q.expected_answer.lower() in answer.lower() if answer else False

            results.append(BenchmarkResult(
                question_id=q.question_id, mode=mode,
                answer=answer, correct=correct,
                latency_ms=latency, sources_used=[],
            ))
        return results

    def compare_modes(self, questions: list[BenchmarkQuestion]) -> dict:
        """Compare fast vs thinking modes."""
        fast = self.evaluate(questions, "fast")
        thinking = self.evaluate(questions, "thinking")

        return {
            "fast": {
                "accuracy": sum(r.correct for r in fast) / len(fast) if fast else 0,
                "median_latency_ms": sorted([r.latency_ms for r in fast])[len(fast)//2] if fast else 0,
            },
            "thinking": {
                "accuracy": sum(r.correct for r in thinking) / len(thinking) if thinking else 0,
                "median_latency_ms": sorted([r.latency_ms for r in thinking])[len(thinking)//2] if thinking else 0,
            },
        }
