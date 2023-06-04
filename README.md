# dibug

Debugging Tool for discord.py

# Usage

```py
from discord import Client, Intents, Message

from dibug import Dibugger

owners = [798690702635827200]


class Bot(Client):
    def __init__(self) -> None:
        intents = Intents.default()
        intents.message_content = True  # dibug requires message content intent
        super().__init__(intents=intents)

        self.dibugger = Dibugger(self, lambda id: id in owners)

    async def on_message(self, msg: Message) -> None:
        await self.dibugger.handle_msg(msg)


bot = Bot()

bot.run("token")
```

# Commands

### Default Prefix: `!dbg `

- `<prefix>eval <code>`: Evaluate code
