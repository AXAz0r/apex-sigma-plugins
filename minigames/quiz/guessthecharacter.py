import aiohttp
import discord
import secrets
import asyncio
from lxml import html as l

ongoing_list = []


async def guessthecharacter(cmd, message, args):
    if message.channel.id not in ongoing_list:
        if args:
            if args[0].lower() == 'hint':
                hint = True
            else:
                hint = False
        else:
            hint = False
        ongoing_list.append(message.channel.id)
        vn_url_list = []
        page_order = secrets.randbelow(3) + 1
        kud_reward = int((page_order * 0.85 * 15) + secrets.randbelow(10))
        vn_top_list_url = f'https://vndb.org/v/all?q=;fil=tagspoil-0;rfil=;o=d;s=pop;p={page_order}'
        async with aiohttp.ClientSession() as session:
            async with session.get(vn_top_list_url) as vn_top_list_session:
                vn_top_list_html = await vn_top_list_session.text()
        vn_top_list_data = l.fromstring(vn_top_list_html)
        list_items = vn_top_list_data.cssselect('.tc1')
        for list_item in list_items:
            if 'href' in list_item[0].attrib:
                vn_url = list_item[0].attrib['href']
                if vn_url.startswith('/v') and not vn_url.startswith('/v/'):
                    vn_url = f'https://vndb.org{vn_url}'
                    vn_url_list.append(vn_url)
        vn_url_choice = secrets.choice(vn_url_list)
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{vn_url_choice}/chars') as vn_details_page_session:
                vn_details_page_html = await vn_details_page_session.text()
        vn_details_page = l.fromstring(vn_details_page_html)
        vn_title = vn_details_page.cssselect('.stripe')[0][0][1].text_content().strip()
        vn_image = vn_details_page.cssselect('.vnimg')[0][0][0].attrib['src']
        character_objects = vn_details_page.cssselect('.chardetails')
        character = secrets.choice(character_objects)
        char_img = character[0][0].attrib['src']
        char_name = character[1][0][0][0][0].text.strip()
        question_embed = discord.Embed(color=0x225588)
        question_embed.set_image(url=char_img)
        question_embed.set_footer(text='You have 30 seconds to guess it.')
        if hint:
            scrambled_name = ''
            char_name_list = list(char_name)
            while char_name_list:
                char_choice = char_name_list.pop(secrets.randbelow(len(char_name_list)))
                scrambled_name += char_choice
            question_embed.set_author(name=scrambled_name, icon_url=vn_image, url=vn_url_choice)
        await message.channel.send(embed=question_embed)

        def check_answer(msg):
            if msg.content.lower() in char_name.lower().split():
                correct = True
            else:
                correct = False
            return correct

        try:
            answer_message = await cmd.bot.wait_for('message', check=check_answer, timeout=30)
            cmd.db.add_currency(answer_message.author, message.guild, kud_reward)
            author = answer_message.author.display_name
            currency = cmd.bot.cfg.pref.currency
            win_title = f'🎉 Correct, {author}, it was {char_name}. You won {kud_reward} {currency}!'
            win_embed = discord.Embed(color=0x77B255, title=win_title)
            await message.channel.send(embed=win_embed)
        except asyncio.TimeoutError:
            timeout_embed = discord.Embed(color=0x696969, title=f'🕙 Time\'s up! It was {char_name} from {vn_title}...')
            await message.channel.send(embed=timeout_embed)
        ongoing_list.remove(message.channel.id)
    else:
        ongoing_error = discord.Embed(color=0xBE1931, title='❗ There is one already ongoing.')
        await message.channel.send(embed=ongoing_error)