def plan(topic: str, memory):
    # Use lightweight rules + memory (no LLM needed)
    # Break the topic into fetchable subtasks.
    return [
        "Fetch official schedule & participant info",
        "Fetch official announcements / press releases (UNFCCC & host)",
        "Fetch top wire stories (Reuters/AP) about today/yesterday",
        "Fetch science side-events (IPCC) and note dates/rooms",
        "Filter out URLs we've already seen",
        "Rank by freshness + authority + novelty vs memory",
    ]
