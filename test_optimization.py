import time
from app.agent import generate_reading
import os

# Mock env if needed, but it should load from .env
# We need to ensure logic runs.

def benchmark():
    print("Starting benchmark...")
    
    dob, tob, pob, yob = "1990-01-01", "12:00", "New Delhi", "1990"
    
    print("First call (Uncached)...")
    start = time.time()
    try:
        generate_reading(dob, tob, pob, yob)
    except Exception as e:
        print(f"Error during API call: {e}")
        return
        
    duration1 = time.time() - start
    print(f"First call took: {duration1:.4f}s")
    
    print("Second call (Cached)...")
    start = time.time()
    generate_reading(dob, tob, pob, yob)
    duration2 = time.time() - start
    print(f"Second call took: {duration2:.4f}s")
    
    if duration2 < 0.1:
        print("SUCCESS: Caching is working!")
    else:
        print("FAILURE: Caching did not improve performance significantly.")

if __name__ == "__main__":
    benchmark()
