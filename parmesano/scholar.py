import os
import math
from serpapi import GoogleSearch


def search_scholar(query, api_key, max_results=10, year_from=None, year_to=None,
                   sort_by="relevance"):
    params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": api_key,
        "num": min(max_results, 20),
    }

    if sort_by == "date":
        params["scisbd"] = 2
    else:
        params["scisbd"] = 0

    if year_from is not None:
        params["as_ylo"] = str(year_from)
    if year_to is not None:
        params["as_yhi"] = str(year_to)

    results = []
    pages_needed = math.ceil(max_results / 20)
    total_results = None

    for page in range(pages_needed):
        params["start"] = page * 20

        search = GoogleSearch(params)
        data = search.get_dict()

        if "error" in data:
            raise RuntimeError(f"SerpAPI error: {data['error']}")

        organic = data.get("organic_results", [])
        for item in organic:
            result = {
                "position": item.get("position"),
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet"),
                "type": item.get("type"),
                "result_id": item.get("result_id"),
            }

            pub_info = item.get("publication_info", {})
            if pub_info:
                result["publication_summary"] = pub_info.get("summary")
                authors = pub_info.get("authors", [])
                result["authors"] = [a.get("name") for a in authors if a.get("name")]

            inline = item.get("inline_links", {})
            cited_by = inline.get("cited_by", {})
            if cited_by:
                result["cited_by"] = cited_by.get("total")

            resources = item.get("resources", [])
            if resources:
                result["resources"] = [
                    {"title": r.get("title"), "link": r.get("link"),
                     "file_format": r.get("file_format")}
                    for r in resources
                ]

            results.append(result)

        if total_results is None:
            search_info = data.get("search_information", {})
            total_results = search_info.get("total_results")

        if len(organic) == 0:
            break

        if page == pages_needed - 1:
            break

    return {
        "query": query,
        "total_results": total_results,
        "results_fetched": len(results),
        "results": results,
    }


def search_scholar_batch(queries, api_key, max_results=10, year_from=None,
                         year_to=None, sort_by="relevance"):
    all_results = []
    for i, query in enumerate(queries):
        try:
            result = search_scholar(
                query, api_key,
                max_results=max_results,
                year_from=year_from,
                year_to=year_to,
                sort_by=sort_by,
            )
            all_results.append(result)
        except Exception as exc:
            all_results.append({
                "query": query,
                "error": str(exc),
                "results": [],
            })
    return all_results
