"""Benchmark for HydraDB memory recall — improved version."""
import json
import time
from dataclasses import dataclass, field
from typing import Any
from .hydradb import HydraDB

@dataclass
class BenchmarkQuestion:
    question_id: str
    question: str
    expected_answer: str
    question_type: str  # factual|multi_hop|contradiction|temporal|negative
    ground_truth_refs: list[str]
    difficulty: str = "medium"

@dataclass
class BenchmarkResult:
    question_id: str
    mode: str
    answer: str
    correct: bool
    latency_ms: float
    sources_used: list[str] = field(default_factory=list)

@dataclass
class BenchmarkReport:
    total_questions: int
    fast_accuracy: float
    thinking_accuracy: float
    fast_median_latency: float
    thinking_median_latency: float
    failure_breakdown: dict = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)

class BenchmarkSuite:
    def __init__(self, hydradb: HydraDB):
        self.hydradb = hydradb

    def generate_questions(self, ground_truth: list[dict]) -> list[BenchmarkQuestion]:
        """Auto-generate questions from ground truth."""
        questions = []
        for i, item in enumerate(ground_truth):
            # Factual questions
            questions.append(BenchmarkQuestion(
                question_id=f"Q{i:03d}_factual",
                question=f"What is the title of {item.get('id', '')}?",
                expected_answer=item.get("title", ""),
                question_type="factual",
                ground_truth_refs=[item.get("id", "")],
            ))
            # Negative questions (should NOT find)
            questions.append(BenchmarkQuestion(
                question_id=f"Q{i:03d}_negative",
                question=f"Does {item.get('id', '')} exist in the corpus?",
                expected_answer="yes" if item.get("id") else "no",
                question_type="negative",
                ground_truth_refs=[],
            ))
        return questions[:50]  # Cap at 50

    def evaluate(self, questions: list[BenchmarkQuestion], mode: str = "fast") -> list[BenchmarkResult]:
        """Evaluate questions against HydraDB."""
        results = []
        for q in questions:
            start = time.time()
            try:
                response = self.hydradb.query(q.question, mode=mode)
                latency = (time.time() - start) * 1000
                answer = response.get("result", {}).get("content", "")
                correct = q.expected_answer.lower() in answer.lower() if answer else False
                results.append(BenchmarkResult(
                    question_id=q.question_id, mode=mode,
                    answer=answer, correct=correct,
                    latency_ms=latency,
                ))
            except Exception as e:
                results.append(BenchmarkResult(
                    question_id=q.question_id, mode=mode,
                    answer=f"ERROR: {e}", correct=False,
                    latency_ms=(time.time() - start) * 1000,
                ))
        return results

    def compare_modes(self, questions: list[BenchmarkQuestion]) -> BenchmarkReport:
        """Compare fast vs thinking modes."""
        fast = self.evaluate(questions, "fast")
        thinking = self.evaluate(questions, "thinking")

        fast_acc = sum(r.correct for r in fast) / len(fast) if fast else 0
        think_acc = sum(r.correct for r in thinking) / len(thinking) if thinking else 0
        fast_lat = sorted([r.latency_ms for r in fast])[len(fast)//2] if fast else 0
        think_lat = sorted([r.latency_ms for r in thinking])[len(thinking)//2] if thinking else 0

        # Failure breakdown
        failures = {}
        for r in fast + thinking:
            if not r.correct:
                failures[r.question_id] = "incorrect"

        return BenchmarkReport(
            total_questions=len(questions),
            fast_accuracy=fast_acc,
            thinking_accuracy=think_acc,
            fast_median_latency=fast_lat,
            thinking_median_latency=think_lat,
            failure_breakdown=failures,
            recommendations=[
                f"Fast mode achieves {fast_acc:.1%} accuracy" if fast_acc < 0.8 else "Fast mode performs well",
                f"Thinking mode achieves {think_acc:.1%} accuracy" if think_acc < 0.9 else "Thinking mode performs well",
                f"Thinking is {think_lat/fast_lat:.1f}x slower" if fast_lat > 0 else "",
            ],
        )
