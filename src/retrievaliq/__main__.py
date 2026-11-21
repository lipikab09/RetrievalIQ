from .evaluate import run_benchmark
if __name__ == "__main__":
    summary, _ = run_benchmark()
    print(summary)
