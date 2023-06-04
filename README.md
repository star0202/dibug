![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/star0202/dibug/release.yml?branch=stable&style=flat-square)
![GitHub](https://img.shields.io/github/license/star0202/dibug?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/dibug?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dibug?style=flat-square)

# dibug

Debugging Tool for discord.py

# Installation

Python 3.10+ is required

```sh
pip install dibug
```

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

### Default Prefix: `!dbg`

- `<prefix> eval | e | python | py <code>`: Evaluate python code
- `<prefix> shell | sh <code>`: Execute shell command
