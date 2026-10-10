"""
test_latency_harness.py
Performance verification harness to stress-test and evaluate the round-trip 
latency of the local GCC http.server endpoints.
"""

import urllib.request
import time
import sys

def verify_endpoint_latency(endpoint_url: str, request_count: int = 100):
    print("=================================================================")
    print("   GCC Infrastructure Performance Testing Harness Initialized   ")
    print("=================================================================\n")
    print(f"[Target Endpoint]: {endpoint_url}")
    print(f"[Sample Footprint Pool]: Sending {request_count} sequential requests...")

    latency_records_ms = []
    dropped_packets = 0

    # Ensure the URL is wrapped correctly
    try:
        urllib.request.urlopen(endpoint_url).close()
    except Exception as e:
        print(f"\n[Fatal Network Exception]: Target server loopback unreachable. {e}", file=sys.stderr)
        print("Please ensure 'python gcc_narrative_engine.py' is running before firing the harness.")
        return

    # Execute the performance profiling sweep
    for i in range(1, request_count + 1):
        start_time = time.perf_counter()
        try:
            with urllib.request.urlopen(endpoint_url) as response:
                response.read()
                end_time = time.perf_counter()
                
                # Calculate processing delta in milliseconds
                delta_ms = (end_time - start_time) * 1000.0
                latency_records_ms.append(delta_ms)
                
                if i % 20 == 0 or i == request_count:
                    print(f"  -> Sample #{i:03d} Ingestion Pass: Latency = {delta_ms:.3f} ms")
        except Exception:
            dropped_packets += 1

    # Compile and format performance metric analytics
    if not latency_records_ms:
        print("\n[Analysis Breakdown Error]: No valid data packets were collected.")
        return

    total_samples = len(latency_records_ms)
    avg_latency = sum(latency_records_ms) / total_samples
    min_latency = min(latency_records_ms)
    max_latency = max(latency_records_ms)

    print("\n=================================================================")
    print("                 PERFORMANCE COMPILATION DATA REPORT             ")
    print("=================================================================")
    print(f"  - Total Transmitted Ingestions : {request_count}")
    print(f"  - Successfully Accounted Pass  : {total_samples}")
    print(f"  - Total Dropped/Fault Sockets  : {dropped_packets}")
    print(f"  - Minimum Network Latency Floor: {min_latency:.4f} ms")
    print(f"  - Maximum Peak Network Spikes  : {max_latency:.4f} ms")
    print(f"  - Compiled Average Baseline RTT: {avg_latency:.4f} ms")
    print("-----------------------------------------------------------------")
    
    # Assert benchmark ceiling thresholds for seamless real-time client streaming
    if avg_latency < 5.0:
        print("  [System Performance Status]: EXCELLENT. Sub-5ms loop latency verified.")
    elif avg_latency < 16.6:
        print("  [System Performance Status]: OPTIMIZED. Fit for single-frame client updates (60Hz).")
    else:
        print("  [System Performance Status]: CAUTION. Minor socket transmission lag detected.")
    print("=================================================================\n")

if __name__ == "__main__":
    TARGET_ENDPOINT = "http://localhost:8000/blueprint"
    verify_endpoint_latency(TARGET_ENDPOINT, request_count=100)
