﻿import discord
from .nodes.permission_data import get_all_perms, generate_cmd_data
from sigma.core.utilities.role_processing import matching_role


async def unpermitrole(cmd, message, args):
    if args:
        if len(args) >= 2:
            if not message.author.permissions_in(message.channel).manage_guild:
                response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
            else:
                target_name = args[1]
                target = matching_role(message.guild, target_name)
                if target:
                    error_response = discord.Embed(color=0xBE1931, title='❗ Bad Input')
                    try:
                        perm_mode, cmd_name = args[0].split(':')
                    except Exception:
                        await message.channel.send(embed=error_response)
                        return
                    cmd_name = cmd_name.lower()
                    perm_mode = perm_mode.lower()
                    if perm_mode == 'c':
                        exception_group = 'CommandExceptions'
                        check_group = cmd.bot.modules.commands
                        check_alts = True
                    elif perm_mode == 'm':
                        exception_group = 'ModuleExceptions'
                        check_group = cmd.bot.modules.categories
                        check_alts = False
                    else:
                        await message.channel.send(embed=error_response)
                        return
                    if check_alts:
                        if cmd_name in cmd.bot.modules.alts:
                            cmd_name = cmd.bot.modules.alts[cmd_name]
                    if cmd_name in check_group:
                        perms = get_all_perms(cmd.db, message)
                        cmd_exc = perms[exception_group]
                        if cmd_name in perms[exception_group]:
                            inner_exc = cmd_exc[cmd_name]
                        else:
                            inner_exc = generate_cmd_data(cmd_name)[cmd_name]
                        exc_usrs = inner_exc['Roles']
                        if target.id in exc_usrs:
                            exc_usrs.remove(target.id)
                            inner_exc.update({'Roles': exc_usrs})
                            cmd_exc.update({cmd_name: inner_exc})
                            perms.update({exception_group: cmd_exc})
                            cmd.db[cmd.db.db_cfg.database].Permissions.update_one({'ServerID': message.guild.id},
                                                                                  {'$set': perms})
                            response = discord.Embed(color=0x77B255,
                                                     title=f'✅ `{target.name}` can no longer use `{cmd_name}`.')
                        else:
                            response = discord.Embed(color=0xFFCC4D,
                                                     title=f'⚠ {target.name} is not able to use `{cmd_name}`')
                    else:
                        response = discord.Embed(color=0x696969, title='🔍 Command/Module Not Found')
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 No {target_name} Role Found')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Not Enough Arguments')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Not Arguments Given')
    await message.channel.send(embed=response)
