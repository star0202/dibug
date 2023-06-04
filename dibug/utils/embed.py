from discord import Embed

from .chunk import chunk_string


def eval_embed(input: str, color: int) -> Embed:
    return Embed(
        title="Eval",
        color=color,
    ).add_field(
        name="Input",
        value=f"```py\n{input}```",
        inline=False,
    )


def shell_embed(input: str, color: int) -> Embed:
    return Embed(
        title="Shell",
        color=color,
    ).add_field(
        name="Input",
        value=f"```sh\n{input}```",
        inline=False,
    )


def chunked_fields(embed: Embed, name: str, lang: str, input: str, limit: int) -> None:
    chunked = chunk_string(input, limit)
    for idx in range(len(chunked)):
        embed.add_field(
            name=f"{name} {idx + 1}/{len(chunked)}",
            value=f"```{lang}\n{chunked[idx]}```",
            inline=False,
        )
