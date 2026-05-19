from sentence_transformers import SentenceTransformer
from supabase import create_client
import os
import time
from dotenv import load_dotenv

model = SentenceTransformer('all-MiniLM-L6-v2')

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
client = create_client(url, key)

for i in range(0, 35499, 10):
    try:
        batch = client.table("plays").select("id", "description").is_("embedding", "null").range(i, i+9).execute().data
        if not batch:
            break
        descriptions = [row['description'] for row in batch]
        embeddings = model.encode(descriptions)

        updates = [{"id": row["id"], "embedding": emb.tolist()} for row, emb in zip(batch, embeddings)]
        client.table("plays").upsert(updates, on_conflict="id").execute()
        time.sleep(0.5)
        print(f"Batch {i}–{i+len(batch)-1}: embedded {len(batch)} rows")
    except Exception as e:
        print(f"Batch {i} failed: {e}")