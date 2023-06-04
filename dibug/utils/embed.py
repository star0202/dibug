from discord import Embed

from .chunk import chunk_string


class DibugEmbed(Embed):
    def __init__(
        self,
        title: str,
        error: bool = False,
    ):
        super().__init__(title=title, color=0xFF0000 if error else 0x2B2D31)

    def chunked_fields(self, name: str, value: str, lang: str) -> "DibugEmbed":
        chunked = chunk_string(value, 1024 - 10)
        for idx in range(len(chunked)):
            self.add_field(
                name=f"{name} ({idx + 1}/{len(chunked)})",
                value=f"```{lang}\n{chunked[idx]}```",
                inline=False,
            )

        return self
