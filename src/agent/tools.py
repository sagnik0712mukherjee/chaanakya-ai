from typing import List

from duckduckgo_search import DDGS

from config import config


def legal_web_search(query: str) -> str:
    """
    Performs a controlled web search for legal queries.

    - Uses DuckDuckGo
    - Filters results to allowed legal domains
    - Returns a clean, readable summary for the agent
    """

    results: List[str] = []

    with DDGS() as ddgs:
        search_results = ddgs.text(
            query,
            max_results=config.SEARCH_RESULTS_LIMIT,
        )

        for result in search_results:
            url = result.get("href", "")
            body = result.get("body", "")
            title = result.get("title", "")

            if not url or not body:
                continue

            # Domain filtering
            if any(domain in url for domain in config.ALLOWED_LEGAL_DOMAINS):
                snippet = f"- {title}\n  {body}\n  Source: {url}"
                results.append(snippet)

    if not results:
        return (
            "No reliable legal sources were found for this query. "
            "The information may be unavailable, outdated, or jurisdiction-specific."
        )

    return "\n\n".join(results)
