# bot.py
import os
import pandas as pd
import utils, data

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()
TOKEN=os.getenv('DISCORD_TOKEN')
GUILD =os.getenv('DISCORD_GUILD')
CREATOR=os.getenv('CREATOR_ID')

print('token:',TOKEN)

bot = Bot(command_prefix='$', case_insensitive=True)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_member_join(member):
    pass
    """await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )"""

#https://discordpy.readthedocs.io/en/latest/api.html?highlight=on_raw_reaction_add#discord.RawReactionActionEvent
@bot.event
async def on_raw_reaction_add(payload):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if message.author.id != bot.user.id :
        return
    if not message.embeds :
        return
    footer_text = message.embeds[0].footer.text
    if footer_text[0] == '@' : #language
        msg_num = footer_text[1:]
        flag = payload.emoji.name
        role_name = data.get_role_name(msg_num,flag)
        if role_name :
            role = discord.utils.get(channel.guild.roles, name=role_name)
            #print('author', payload.member)
            #print('role', role)
            await payload.member.add_roles(role)
    elif footer_text[0] == '#' : #collection
        cid = footer_text[1:]
        uid = payload.user_id
        emoji = payload.emoji.name
        if emoji == '✅' :
            data.in_collection(cid,uid)
        elif emoji == '📮' :
            data.in_swap(cid,uid)

@bot.event
async def on_raw_reaction_remove(payload):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if message.author.id != bot.user.id :
        return
    if not message.embeds :
        return
    footer_text = message.embeds[0].footer.text
    print(footer_text)
    if footer_text[0] == '@' : #language
        msg_num = footer_text[1:]
        flag = payload.emoji.name
        role_name = data.get_role_name(msg_num,flag)
        print(role_name)
        if role_name :
            role = discord.utils.get(channel.guild.roles, name=role_name)
            await payload.member.remove_roles(role)
    elif footer_text[0] == '#' : #collection
        cid = footer_text[1:]
        uid = payload.user_id
        emoji = payload.emoji.name
        if emoji == '✅' :
            data.out_collection(cid,uid)
        elif emoji == '📮' :
            data.out_swap(cid,uid)


@bot.command()
async def swap(ctx, user: discord.User) :
    uid1 = ctx.message.author.id
    uid2 = user.id
    if bot.user.id == uid2 :
        msg = 'You cannot swap coins with the bot.'
        await ctx.send(msg)
        return
    if uid1 == uid2 :
        return
    await ctx.message.add_reaction('🇪🇺')
    msg = ''
    for (u_sender, u_receiver) in [(uid1,uid2), (uid2,uid1)] :
        es = data.compute_swap_list(u_sender, u_receiver)
        if es :
            msg += '<@{u}> sends:\n'.format(u=u_sender)
            msg += ', '.join(es)
            msg += '\n'
        else :
            msg += '<@{u}> has nothing to send.\n'.format(u=u_sender)
    await ctx.send(msg)

@bot.command()
async def ping(ctx) :
    await ctx.message.add_reaction('🇪🇺')
    await ctx.send('Pong')

@bot.command()
async def test(ctx):
    if ctx.message.author.id != CREATOR :
        return
    await ctx.message.add_reaction('🇪🇺')
    descr = ':flag_de: 75o anniversario della fondazione dello Stato della Città del Vaticano / :flag_gb: 75o anniversario della fondazione dello Stato della Città del Vaticano / :flag_fr: 75o anniversario della fondazione dello Stato della Città del Vaticano'
    embed=discord.Embed(title='2004', description=descr, color=0xf00000)
    embed.set_author(name='Eurasmus', url='https://eurasmus.eu', icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Euro_symbol.svg/584px-Euro_symbol.svg.png')
    embed.set_thumbnail(url='https://www.ecb.europa.eu/euro/coins/comm/shared/img/comm_2004_va.jpg')
    embed.set_footer(text='#1')
    msg = await ctx.send(embed=embed)
    for emoji in ['✅', '📮'] :
        await msg.add_reaction(emoji)

@bot.command()
async def clangs(ctx) :
    if ctx.message.author.id != CREATOR :
        return
    await ctx.message.add_reaction('🇪🇺')
    langch = discord.utils.get(ctx.guild.channels, name='identikit-🕵')

    def create_embed(title,descr,text) :
        embed=discord.Embed(title=title, description=descr, color=0xff6666)
        embed.set_author(name='Eurasmus', url='https://eurasmus.eu')
        embed.set_footer(text=text)
        return embed
    #send
    titles = ['Slawische Sprachen/Slavic languages/Langues slaves','Romanische Sprachen/Romance languages/Langues romanes','Germanische Sprachen/Germanic languages/Langues germaniques','Uralische Sprachen/Uralic languages/Langues ouraliennes','Andere/Others/Autres']
    descrs = ['🇧🇬 български\n🇨🇿 čeština\n🇭🇷 hrvatski\n🇵🇱 polski\n🇸🇰 slovenčina\n🇸🇮 slovenščina','💛 català\n🇪🇸 español\n🇫🇷 français\n🇮🇹 italiano\n🇵🇹 português\n🇷🇴 română','🇩🇰 dansk\n🇩🇪 deutsch\n🇬🇧 English\n🇳🇱 nederlands\n🇸🇪 svenska','🇪🇪 eesti\n🇭🇺 magyar\n🇫🇮 suomi','🇬🇷 ελληνικά\n💚 Esperanto\n🇮🇪 gaelige\n🇱🇻 latviešu\n🇱🇹 lietuvių\n🇲🇹 malti']
    assert(len(titles)==len(descrs))
    texts = ['@{}'.format(n+1) for n,_ in enumerate(titles)]
    for title,(descr,text) in zip(titles,zip(descrs,texts)) :
        embed = create_embed(title,descr,text)
        emojis = [e.split()[0] for e in descr.split('\n')]
        msg = await langch.send(embed=embed)
        for emoji in emojis :
            await msg.add_reaction(emoji)


@bot.command()
async def ccch(ctx): 
    if ctx.message.author.id != CREATOR :
        return
    await ctx.message.add_reaction('🇪🇺')
    ch_names = [cn for (_,cn)  in utils.fetch_channel_data()]
    ch_names.extend(['eu-{y}-🇪🇺'.format(y=y) for y in [2015,2012,2009,2007]])
    chs = [discord.utils.get(ctx.guild.channels, name=name) for name in ch_names]
    for ch in chs :
        mgs = [] #Empty list to put all the messages in the log
        async for x in ch.history(limit = 100):
            mgs.append(x)
        for mg in mgs :
            await mg.delete() 
        #await bot.delete_messages(mgs)

@bot.command()
async def uc(ctx) :
    if ctx.message.author.id != CREATOR :
        return
    await ctx.message.add_reaction('🇪🇺')

    #fetch data from CSVs
    coins = pd.read_csv ('coins.csv')
    ch_pairs = utils.fetch_channel_data()
    ch_dict = {code:discord.utils.get(ctx.guild.channels, name=name) for code,name in ch_pairs}

    outfile = open('processed.csv', 'w')
    for index, row in coins.iterrows():

        #read
        d = dict()
        attrs = ['ID', 'YEAR', 'COUNTRY', 'DESCR_DE', 'DESCR_EN', 'DESCR_FR', 'IMG', 'NOTE', 'MSG_ID']
        for attr in attrs :
            d[attr.lower()] = getattr(row, attr)

        if d['msg_id'] != 'None':
            continue

        if d['country'] == 'eu': #joint european issue
            assert(d['note'] != None)

            #send
            descr = ':flag_de: {descr_de} / :flag_gb: {descr_en} / :flag_fr: {descr_fr}'.format(**d)
            embed=discord.Embed(title='{year}—{note}'.format(**d), description=descr, color=0xf00000)
            embed.set_author(name='Eurasmus', url='https://eurasmus.eu', icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Euro_symbol.svg/584px-Euro_symbol.svg.png')
            embed.set_thumbnail(url='https://www.ecb.europa.eu/euro/coins/comm/shared/img/{img}'.format(**d))
            embed.set_footer(text='#{id}'.format(**d))
            channel_name = 'eu-{year}-🇪🇺'.format(**d)
            channel = discord.utils.get(ctx.guild.channels, name=channel_name)

        else : #national issue
            assert(d['country'] in ch_dict)

            #send
            descr = ':flag_de: {descr_de} / :flag_gb: {descr_en} / :flag_fr: {descr_fr}'.format(**d)
            embed=discord.Embed(title='{year}'.format(**d), description=descr, color=0xf00000)
            embed.set_author(name='Eurasmus', url='https://eurasmus.eu', icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Euro_symbol.svg/584px-Euro_symbol.svg.png')
            embed.set_thumbnail(url='https://www.ecb.europa.eu/euro/coins/comm/shared/img/{img}'.format(**d))
            embed.set_footer(text='#{id}'.format(**d))
            channel = ch_dict[d['country']]
        msg = await channel.send(embed=embed)
        for emoji in ['✅', '📮'] :
            await msg.add_reaction(emoji)
        print(msg.id)
        outfile.write('{},{}\n'.format(d['id'], msg.id))
    outfile.close()



if __name__ == '__main__' :
    bot.run(TOKEN)