def chunk_string(str: str, limit: int) -> list[str]:
    chunks = []
    start = 0

    while start < len(str):
        end = start + limit

        if end >= len(str):
            chunks.append(str[start:])
            break

        last_space = str.rfind("\n", start, end)
        if last_space != -1 and last_space > start:
            end = last_space

        chunks.append(str[start:end])
        start = end + 1

    return chunks
