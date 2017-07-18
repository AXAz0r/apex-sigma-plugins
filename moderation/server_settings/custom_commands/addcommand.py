import discord


async def addcommand(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            if len(args) >= 2:
                trigger = args[0].lower()
                if trigger not in cmd.bot.modules.commands and trigger not in cmd.bot.modules.alts:
                    content = ' '.join(args[1:])
                    custom_commands = cmd.db.get_guild_settings(message.guild.id, 'CustomCommands')
                    if custom_commands is None:
                        custom_commands = {}
                    if trigger in custom_commands:
                        res_text = 'updated'
                    else:
                        res_text = 'added'
                    custom_commands.update({trigger: content})
                    cmd.db.set_guild_settings(message.guild.id, 'CustomCommands', custom_commands)
                    response = discord.Embed(title=f'✅ {trigger} has been {res_text}', color=0x66CC66)
                else:
                    response = discord.Embed(title='❗ Can\'t replace an existing core command', color=0xDB0000)
            else:
                response = discord.Embed(title='❗ Missing Message To Send', color=0xDB0000)
        else:
            response = discord.Embed(title='❗ Nothing Was Inputted', color=0xDB0000)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)
