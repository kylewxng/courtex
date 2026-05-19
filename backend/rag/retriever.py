from sentence_transformers import SentenceTransformer
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_similar_plays(query: str, top_k: int = 5) -> list[dict]:
    query_embedding = model.encode(query).tolist()
    response = supabase.rpc("match_plays", {"query_embedding": query_embedding, "match_count": top_k}).execute()
    return response.data

def retrieve_shot_chart_plays(query: str, top_k: int = 10) -> list[dict]:
    made_embedding = model.encode(query + " made field goal").tolist()
    missed_embedding = model.encode(query + " missed field goal").tolist()
    made = supabase.rpc("match_plays", {"query_embedding": made_embedding, "match_count": top_k}).execute().data
    missed = supabase.rpc("match_plays", {"query_embedding": missed_embedding, "match_count": top_k}).execute().data
    return made + missed

if __name__ == "__main__":
    results = retrieve_similar_plays("Curry three pointer from the corner")
    for play in results:
        print(play)