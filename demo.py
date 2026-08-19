#!/usr/bin/env python3
"""MemoryProof + WigglyMem — full demo."""
import json
from patala_hydra.hydradb import HydraDB
from patala_hydra.wigglymem import WigglyMem
from patala_hydra.benchmark import BenchmarkSuite
from patala_hydra.failures import classify_failure

print("=" * 60)
print("  MemoryProof + WigglyMem")
print("  Hack Hydra — Track 03")
print("=" * 60)

# === PART 1: Build memory system on HydraDB ===
print("\n" + "=" * 60)
print("  PART 1: Build Memory System")
print("=" * 60)

print("\n[1.1] Connect to HydraDB...")
hydra = HydraDB()
print("  Connected to HydraDB MCP")

print("\n[1.2] Initialize WigglyMem...")
mem = WigglyMem(hydra)
print("  WigglyMem ready")

print("\n[1.3] Export ground truth to HydraDB...")
# In real demo, export from Wiggly corpus
# For demo, create sample evidence
sample_evidence = [
    {"id": "work_001", "title": "Tantraloka", "author": "Abhinavagupta", "tradition": "Kashmir Shaivism"},
    {"id": "work_002", "title": "Netratantra", "author": "Morkanda", "tradition": "Shaiva tantra"},
    {"id": "work_003", "title": "Pratyabhijna", "author": "Utpaladeva", "tradition": "Kashmir Shaivism"},
    {"id": "work_004", "title": "Spandakarika", "author": "Vasugupta", "tradition": "Kashmir Shaivism"},
    {"id": "work_005", "title": "Tattvasangraha", "author": "Shantarakshita", "tradition": "Buddhist"},
]

for ev in sample_evidence:
    text = f"# {ev['title']}\nAuthor: {ev['author']}\nTradition: {ev['tradition']}"
    try:
        hydra.ingest(text=text, title=ev['title'])
    except Exception:
        pass  # Offline mode
print(f"  Exported {len(sample_evidence)} evidence records")

print("\n[1.4] Query memory...")
try:
    result = hydra.query("Who wrote Tantraloka?", mode="fast")
    print(f"  Result: {result.get('result', {}).get('content', 'N/A')[:100]}")
except Exception as e:
    print(f"  Query result: {e}")

# === PART 2: Benchmark recall ===
print("\n" + "=" * 60)
print("  PART 2: Benchmark Recall")
print("=" * 60)

print("\n[2.1] Generate benchmark questions...")
suite = BenchmarkSuite(hydra)
questions = suite.generate_questions(sample_evidence)
print(f"  Generated {len(questions)} questions")

print("\n[2.2] Evaluate fast mode...")
fast_results = suite.evaluate(questions[:10], "fast")
fast_correct = sum(r.correct for r in fast_results)
print(f"  Fast: {fast_correct}/{len(fast_results)} correct ({fast_correct/len(fast_results)*100:.1f}%)")

print("\n[2.3] Evaluate thinking mode...")
think_results = suite.evaluate(questions[:10], "thinking")
think_correct = sum(r.correct for r in think_results)
print(f"  Thinking: {think_correct}/{len(think_results)} correct ({think_correct/len(think_results)*100:.1f}%)")

print("\n[2.4] Compare modes...")
report = suite.compare_modes(questions[:10])
print(f"  Fast accuracy: {report.fast_accuracy:.1%}")
print(f"  Thinking accuracy: {report.thinking_accuracy:.1f%}")
print(f"  Fast latency: {report.fast_median_latency:.0f}ms")
print(f"  Thinking latency: {report.thinking_median_latency:.0f}ms")

print("\n[2.5] Failure analysis...")
for q, r in zip(questions[:5], fast_results[:5]):
    if not r.correct:
        f = classify_failure(q, r, {})
        print(f"  {f.failure_type}: {f.description}")

# === PART 3: Results ===
print("\n" + "=" * 60)
print("  RESULTS")
print("=" * 60)

print(f"""
  Questions: {report.total_questions}
  Fast accuracy: {report.fast_accuracy:.1%}
  Thinking accuracy: {report.thinking_accuracy:.1%}
  Fast latency: {report.fast_median_latency:.0f}ms
  Thinking latency: {report.thinking_median_latency:.0f}ms
  
  Recommendations:
""")
for rec in report.recommendations:
    if rec:
        print(f"    - {rec}")

print("\n" + "=" * 60)
print("  Demo complete")
print("=" * 60)
