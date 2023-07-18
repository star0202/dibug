from discord import Message


class DibugCommand:
    def __init__(self, aliases: list[str]) -> None:
        self.aliases = aliases

    async def execute(self, msg: Message, args: str) -> None:
        raise NotImplementedError
