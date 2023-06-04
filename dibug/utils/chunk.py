def chunk_string(value: str, limit: int) -> list[str]:
    chunks: list[str] = []
    start = 0

    while start < len(value):
        end = start + limit

        if end >= len(value):
            chunks.append(value[start:])
            break

        last_newline = value.rfind("\n", start, end)
        if last_newline != -1 and last_newline > start:
            end = last_newline

        chunks.append(value[start:end])
        start = end + 1

    return chunks
