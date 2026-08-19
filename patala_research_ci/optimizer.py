"""HydraDB config optimizer — evolutionary search for optimal recall settings."""
import random
from typing import Any
from .benchmark import BenchmarkSuite, BenchmarkQuestion

@dataclass
class HydraConfig:
    mode: str = "fast"
    max_results: int = 10
    recency_bias: float = 0.5
    graph_context: bool = True

@dataclass
class OptimizationResult:
    config: HydraConfig
    accuracy: float
    latency_ms: float

class HydraOptimizer:
    def __init__(self, suite: BenchmarkSuite):
        self.suite = suite

    def optimize(self, questions: list[BenchmarkQuestion],
                 population_size: int = 10, generations: int = 5) -> HydraConfig:
        """Evolutionary search for optimal HydraDB config."""
        # Generate initial population
        population = [self._random_config() for _ in range(population_size)]

        for gen in range(generations):
            # Evaluate each config
            results = []
            for config in population:
                # Patch HydraDB query params
                score = self._evaluate_config(config, questions)
                results.append((config, score))

            # Sort by accuracy (descending)
            results.sort(key=lambda x: -x[1])

            # Keep top 50%
            survivors = [c for c, _ in results[:population_size//2]]

            # Generate new candidates via mutation
            new_population = list(survivors)
            while len(new_population) < population_size:
                parent = random.choice(survivors)
                child = self._mutate(parent)
                new_population.append(child)

            population = new_population

        # Return best
        best = max(population, key=lambda c: self._evaluate_config(c, questions))
        return best

    def _random_config(self) -> HydraConfig:
        return HydraConfig(
            mode=random.choice(["fast", "thinking"]),
            max_results=random.choice([5, 10, 20, 50]),
            recency_bias=random.random(),
            graph_context=random.choice([True, False]),
        )

    def _mutate(self, config: HydraConfig) -> HydraConfig:
        c = HydraConfig(
            mode=config.mode,
            max_results=config.max_results,
            recency_bias=config.recency_bias,
            graph_context=config.graph_context,
        )
        if random.random() < 0.3:
            c.mode = "thinking" if c.mode == "fast" else "fast"
        if random.random() < 0.3:
            c.max_results = random.choice([5, 10, 20, 50])
        if random.random() < 0.3:
            c.recency_bias = random.random()
        if random.random() < 0.3:
            c.graph_context = not c.graph_context
        return c

    def _evaluate_config(self, config: HydraConfig, questions: list[BenchmarkQuestion]) -> float:
        """Evaluate a config against questions."""
        # In real implementation, would patch HydraDB query params
        results = self.suite.evaluate(questions[:10], config.mode)
        return sum(r.correct for r in results) / len(results) if results else 0
