from traceback import format_exception

from async_eval import eval
from discord import Message

from dibug.classes.command import DibugCommand
from dibug.classes.embed import DibugEmbed
from dibug.utils.object import inspect


class EvalCommand(DibugCommand):
    aliases = ["eval", "e", "python", "py"]

    async def execute(self, msg: Message, args: str) -> None:
        if not args:
            await msg.reply("Missing code")
            return

        res = await msg.reply("Running...")

        if args.startswith("```py") and args.endswith("```"):
            args = args[6:-3]

        try:
            result = eval(args, {"client": self._client, "msg": msg})

            embed = (
                DibugEmbed("Eval")
                .chunked_fields(
                    "Input",
                    args,
                    "py",
                )
                .chunked_fields(
                    "Output (Verbose)",
                    "\n".join(inspect(result, 0)),
                    "py",
                )
                .chunked_fields(
                    "Output (Compact)",
                    str(result),
                    "py",
                )
            )

            await res.edit(content=None, embed=embed)

        except Exception as e:
            embed = (
                DibugEmbed("Eval", True)
                .chunked_fields(
                    "Input",
                    args,
                    "py",
                )
                .chunked_fields(
                    "Error",
                    "\n".join(format_exception(e)),
                    "py",
                )
            )

            await res.edit(content=None, embed=embed)
