import secrets


async def currency_message(ev, message):
    if not message.author.bot:
        if message.guild:
            prefix = ev.bot.get_prefix(message)
            if not message.content.startswith(prefix):
                if not ev.bot.cooldown.on_cooldown(ev.name, message.author):
                    points = secrets.randbelow(3)
                    ev.db.add_currency(message.author, message.guild, points)
                    ev.bot.cooldown.set_cooldown(ev.name, message.author, 60)
