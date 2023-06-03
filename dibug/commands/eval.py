from traceback import format_exception

from discord import Client, Embed, Message

from ..abc import DibugCommand
from ..utils import chunk_string, eval_embed, inspect


class EvalCommand(DibugCommand):
    def __init__(self, client: Client) -> None:
        self.name = "eval"
        self.client = client

    async def execute(self, msg: Message, args: str) -> None:
        if not args:
            await msg.channel.send("No codes")
            return

        if args.startswith("```py") and args.endswith("```"):
            args = args[5:-3]

        client = self.client  # shortcut

        try:
            result = eval(args)

            embed = eval_embed(args, 0x2B2D31)

            chunked = chunk_string(
                "\n".join(inspect(result, 0)),
                1024 - 10,
            )
            for idx in range(len(chunked)):
                embed.add_field(
                    name=f"Output (Verbose) {idx + 1}/{len(chunked)}",
                    value=f"```py\n{chunked[idx]}```",
                    inline=False,
                )

            chunked = chunk_string(str(result), 1024 - 10)
            for idx in range(len(chunked)):
                embed.add_field(
                    name=f"Output (Compact) {idx + 1}/{len(chunked)}",
                    value=f"```py\n{chunked[idx]}```",
                    inline=False,
                )

            await msg.reply(embed=embed)

        except Exception as e:
            embed = eval_embed(args, 0xFF0000).add_field(
                name="Error",
                value=f"```py\n{''.join(format_exception(e))}```",
                inline=False,
            )

            await msg.reply(embed=embed)
