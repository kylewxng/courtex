from groq import Groq
import os
from .retriever import retrieve_similar_plays, retrieve_shot_chart_plays
from .prompt import build_prompt

client = Groq(api_key=os.environ["GROQ_API_KEY"])

def query_plays(query: str) -> tuple[str, list[dict]]:
    rag_plays = retrieve_similar_plays(query)
    viz_plays = retrieve_shot_chart_plays(query)
    prompt = build_prompt(query, rag_plays)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content, viz_plays

if __name__ == "__main__":
    answer, _ = query_plays("mid range jumpers in the fourth quarter")
    print(answer)