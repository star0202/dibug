from discord import Embed


def eval_embed(input: str, color: int) -> Embed:
    return Embed(
        title="Eval",
        color=color,
    ).add_field(
        name="Input",
        value=f"```py\n{input}```",
        inline=False,
    )
