from discord import Embed, Message


def eval_embed(input: str, msg: Message, color: int) -> Embed:
    return (
        Embed(
            title="Eval",
            color=color,
        )
        .set_author(
            name=msg.author.display_name,
            icon_url=msg.author.avatar.url
            if msg.author.avatar
            else msg.author.default_avatar.url,
        )
        .add_field(
            name="Input",
            value=f"```py\n{input}```",
            inline=False,
        )
    )
