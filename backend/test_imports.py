
import time
print("Starting imports...")

start = time.time()
import os
print(f"Imported os in {time.time()-start:.4f}s")

start = time.time()
from dotenv import load_dotenv
print(f"Imported dotenv in {time.time()-start:.4f}s")

start = time.time()
from fastapi import FastAPI
print(f"Imported fastapi in {time.time()-start:.4f}s")

start = time.time()
import psycopg2
print(f"Imported psycopg2 in {time.time()-start:.4f}s")

start = time.time()
from qdrant_client import QdrantClient
print(f"Imported qdrant_client in {time.time()-start:.4f}s")

start = time.time()
print("Importing sentence_transformers...")
from sentence_transformers import SentenceTransformer
print(f"Imported sentence_transformers in {time.time()-start:.4f}s")

start = time.time()
import cohere
print(f"Imported cohere in {time.time()-start:.4f}s")

print("All imports done.")
