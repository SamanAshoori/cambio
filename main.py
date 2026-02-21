import time
import sys

# Import C++ version
from cambio import Cambio as CambioCpp

# Import Python version
from dry_run_python import Cambio as CambioPython


def benchmark_cpp(num_games=100, turns_per_game=50):
    """Benchmark the C++ implementation"""
    times = []
    for _ in range(num_games):
        c = CambioCpp()
        start = time.perf_counter()
        for _ in range(turns_per_game):
            c.step()
        end = time.perf_counter()
        times.append(end - start)
    
    return times


def benchmark_python(num_games=100, turns_per_game=50):
    """Benchmark the Python implementation"""
    times = []
    for _ in range(num_games):
        c = CambioPython()
        start = time.perf_counter()
        for _ in range(turns_per_game):
            c.step()
        end = time.perf_counter()
        times.append(end - start)
    
    return times


def format_time(seconds):
    """Format time in appropriate units"""
    if seconds < 1e-3:
        return f"{seconds * 1e6:.2f} µs"
    elif seconds < 1:
        return f"{seconds * 1e3:.2f} ms"
    else:
        return f"{seconds:.2f} s"


def run_benchmark(num_games=100, turns_per_game=50):
    """Run both benchmarks and compare"""
    print(f"=" * 60)
    print(f"CAMIGO BENCHMARK")
    print(f"=" * 60)
    print(f"Games per version: {num_games}")
    print(f"Turns per game: {turns_per_game}")
    print(f"Total operations: {num_games * turns_per_game}")
    print(f"=" * 60)
    
    print(f"\nRunning C++ benchmark...")
    cpp_times = benchmark_cpp(num_games, turns_per_game)
    
    print(f"Running Python benchmark...")
    python_times = benchmark_python(num_games, turns_per_game)
    
    # Calculate statistics
    cpp_total = sum(cpp_times)
    cpp_avg = cpp_total / len(cpp_times)
    cpp_min = min(cpp_times)
    cpp_max = max(cpp_times)
    
    python_total = sum(python_times)
    python_avg = python_total / len(python_times)
    python_min = min(python_times)
    python_max = max(python_times)
    
    cpp_speedup = cpp_total / python_total if python_total > 0 else 0
    
    print(f"\n{'Metric':<25} {'C++':<20} {'Python':<20}")
    print("-" * 65)
    print(f"{'Total Time':<25} {format_time(cpp_total):<20} {format_time(python_total):<20}")
    print(f"{'Average per Game':<25} {format_time(cpp_avg):<20} {format_time(python_avg):<20}")
    print(f"{'Min Time':<25} {format_time(cpp_min):<20} {format_time(python_min):<20}")
    print(f"{'Max Time':<25} {format_time(cpp_max):<20} {format_time(python_max):<20}")
    print(f"{'Ops/Second':<25} {int(num_games * turns_per_game / cpp_total):<20,} {int(num_games * turns_per_game / python_total):<20,}")
    
    print(f"\n{'=' * 60}")
    print(f"SPEEDUP: C++ is {cpp_speedup:.2f}x {'slower' if cpp_speedup < 1 else 'faster'} than Python")
    print(f"{'=' * 60}")
    
    return {
        'cpp': {'total': cpp_total, 'avg': cpp_avg, 'min': cpp_min, 'max': cpp_max},
        'python': {'total': python_total, 'avg': python_avg, 'min': python_min, 'max': python_max},
        'speedup': cpp_speedup
    }


if __name__ == "__main__":
    num_games = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    turns_per_game = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    
    run_benchmark(num_games, turns_per_game)
