import os
from exa_py import Exa
from tavily import TavilyClient

exa = Exa(api_key=os.getenv("EXA_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_business_problems(query: str):
    results = []

    try:
        exa_results = exa.search_and_contents(
            query=query,
            num_results=10
        )

        for r in exa_results.results:
            results.append({
                "source": "exa",
                "title": getattr(r, "title", ""),
                "url": getattr(r, "url", ""),
                "text": getattr(r, "text", "")
            })

    except Exception as e:
        print(f"Exa error: {e}")

    try:
        tavily_results = tavily.search(
            query=query,
            max_results=10
        )

        for r in tavily_results.get("results", []):
            results.append({
                "source": "tavily",
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "text": r.get("content", "")
            })

    except Exception as e:
        print(f"Tavily error: {e}")

    return results