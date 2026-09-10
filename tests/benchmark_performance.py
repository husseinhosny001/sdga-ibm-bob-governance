import time
import statistics
from wrapper_api.schemas import BobProposalPayload
from sdga_kernel.expected_loss import SDGAExpectedLossEngine

def run_performance_benchmark(iterations: int = 1000):
    engine = SDGAExpectedLossEngine()
    payload = BobProposalPayload(
        proposal_id="BENCHMARK-001",
        repository="core",
        branch="main",
        files_changed_count=5,
        lines_added=100,
        lines_deleted=50,
        breaking_changes_detected=False,
        test_coverage_delta=0.05,
        confidence_score=0.90,
        proposed_diff_summary="Benchmark diff",
        security_sensitive_module=False
    )
    
    latencies = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        _ = engine.compute_decision(payload)
        latencies.append((time.perf_counter() - t0) * 1000)

    avg_lat = statistics.mean(latencies)
    print(f"Average Execution Latency: {avg_lat:.4f} ms")
    assert avg_lat < 50.0, "Latency SLA Violated"

if __name__ == "__main__":
    run_performance_benchmark()