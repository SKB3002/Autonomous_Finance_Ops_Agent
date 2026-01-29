import requests
import time

HEADERS = {
    "User-Agent": "FinanceOps-Agent/1.0"
}

def web_search(query: str, max_results: int = 3):
    """
    Fetches live data from the internet.
    Returns content + sources.
    """
    results = []

    try:
        # DuckDuckGo instant answer API (lightweight, no key)
        response = requests.get(
            "https://api.duckduckgo.com/",
            params={
                "q": query,
                "format": "json",
                "no_redirect": 1,
                "no_html": 1
            },
            headers=HEADERS,
            timeout=10
        )

        data = response.json()

        if data.get("AbstractText"):
            results.append({
                "content": data["AbstractText"],
                "source": data.get("AbstractURL", "duckduckgo")
            })

        # Fallback: related topics
        for topic in data.get("RelatedTopics", [])[:max_results]:
            if isinstance(topic, dict) and "Text" in topic:
                results.append({
                    "content": topic["Text"],
                    "source": topic.get("FirstURL", "duckduckgo")
                })

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "results": []
        }

    return {
        "status": "success",
        "timestamp": time.time(),
        "query": query,
        "results": results
    }

