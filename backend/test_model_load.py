
from sentence_transformers import SentenceTransformer
import time

print("Start loading model...", flush=True)
start = time.time()
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print(f"✅ Model loaded in {time.time() - start:.2f}s")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
