from discord import Client, Message


class DibugCommand:
    aliases: list[str]

    def __init__(self, client: Client) -> None:
        self._client = client

    async def execute(self, msg: Message, args: str) -> None:
        raise NotImplementedError
