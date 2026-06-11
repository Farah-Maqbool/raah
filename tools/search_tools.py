import os
from dotenv import load_dotenv
from exa_py import Exa
from tavily import TavilyClient
from typing import List, Dict, Any

load_dotenv()

exa = Exa(api_key=os.getenv("EXA_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))




def search_business_problems(query: str) -> List[Dict[str, Any]]:
    results = []

    try:
        exa_results = exa.search(
            query,
            num_results=3
        )

        for r in exa_results.results:
            results.append({
                "source": "exa",
                "title": getattr(r, "title", ""),
                "url": getattr(r, "url", ""),
                "text": getattr(r, "text", "")[:500],
                "published_date": getattr(r, "published_date", None),
            })

    except Exception as e:
        print(f"Exa error: {e}")

    try:
        tavily_results = tavily.search(
            query=query,
            max_results=5
        )

        for r in tavily_results.get("results", []):
            results.append({
                "source": "tavily",
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "text": r.get("content", "")[:500],
                "published_date": r.get("published_date"),
            })

    except Exception as e:
        print(f"Tavily error: {e}")

    return results