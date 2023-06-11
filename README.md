[![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/star0202/dibug/release.yml?branch=stable&style=flat-square)](https://github.com/star0202/dibug/actions/workflows/release.yml)
[![GitHub](https://img.shields.io/github/license/star0202/dibug?style=flat-square)](https://github.com/star0202/dibug/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/dibug?style=flat-square)](https://pypi.org/project/dibug)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dibug?style=flat-square)](https://pypi.org/project/dibug)

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

owners = [1234567890]  # owners id


async def user_has_perm(msg: Message) -> bool:
    return msg.author.id in owners


class Bot(Client):
    def __init__(self) -> None:
        intents = Intents.default()
        intents.message_content = True  # dibug requires message content intent
        super().__init__(intents=intents)


bot = Bot()

dibugger = Dibugger(bot, user_has_perm)

bot.run("token")
```

# Commands

### Default Prefix: `!dbg`

- `<prefix>` | `<prefix> info | i`: Show bot info

- `<prefix> eval | e | python | py <code>`: Evaluate python code
- `<prefix> kill | k | shutdown`: Kill bot process
- `<prefix> shell | sh <code>`: Execute shell command
