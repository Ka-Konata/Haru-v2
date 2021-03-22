# --coding with python 3.8.8--

import discord
import asyncio
import json
from scripts           import colors
from scripts.bot_token import token
from scripts           import requeriments
from scripts           import aliases
from usual             import Utils


intents = discord.Intents.default()
intents.members = True

client  = discord.Client(intents=intents)
TOKEN   = token.get_token()  # Make your file with your token
invite  = "https://discord.com/oauth2/authorize?client_id=823255952069361715&scope=bot&permissions=85261377"
prefixo = "h!"
guilds_security_coding = ["788518735752724480"]  # "796451246864203816" "803997027733471242"


@client.event
async def on_ready():
    channel = client.get_channel(788785603105259574)
    embed_msg = discord.Embed(title="BOT ONLINE - HELLO WORLD", color=colors.ciano, description=f"**Bot UserName:**  {client.user.name} \n**Bot UserID:**  {client.user.id} \n**Channel:**  {channel.mention}")
    await channel.send(embed=embed_msg)
    print("BOT ONLINE - HELLO WORLD")
    print(client.user.name)
    print(client.user.id)
    print("-------------------------")

@client.event
async def on_message(message):

    utils   = Utils(message.author.avatar_url, client)
    channel = message.channel

    arq = "pt-br.json"
    lang = {}
    with open(arq, "r", encoding="utf-8") as f:
        lang = json.load(f)

    # Security Guild Coding edit
    if message.author.id == 502687173099913216:

        if message.content.lower().startswith(f"h!addguildtocodingtests"):
            guilds_security_coding.append(str(message.guild.id))
            await message.add_reaction("✅")
            print(guilds_security_coding)

        elif message.content.lower().startswith(f"h!removeguildfromcodingtests") and str(message.guild.id) in guilds_security_coding:
            guilds_security_coding.remove(str(message.guild.id))
            await message.add_reaction("✅")
            print(guilds_security_coding)
 
    if message.author.bot == False and str(message.guild.id) in guilds_security_coding:

            member_perms = utils.get_permissions(message.author, requeriments)
            bot_perms    = message.guild.get_member(808100198899384352).guild_permissions


            # Importanto os comandos
            from cogs.privilegies          import Cmd_privilegies

            help    = None
            privil  = Cmd_privilegies(message, lang, colors, member_perms, bot_perms, utils, help, prefixo, aliases)

            # Comando Test, para testar se o bot está online
            if message.content.lower().startswith(utils.ins_prefix(prefixo, aliases.test)):
                print(utils.ins_prefix(prefixo, aliases.test))
                await channel.send("Hello world, I'm alive.")


            # Comando Stop Running, restrição: bot onwer
            if message.content.lower().startswith(utils.ins_prefix(prefixo, aliases.stoprunning)):
                if message.author.id == 502687173099913216:
                    await channel.send(lang["FINAL_MESSAGE_EXECUTING"])
                    print("Encerrando o script...")
                    exit()
                else:
                    embed_error = utils.permission_error("bot owner", lang)
                    await channel.send(embed=embed_error)

            # ---------- PRIVILEGES ----------

            # Comando Move Me 
            if message.content.lower().startswith(utils.ins_prefix(prefixo, aliases.privilevies["moveme"])):
                await privil.moveme()

            # Comando Set Role
            if message.content.lower().startswith(utils.ins_prefix(prefixo, aliases.privilevies["setrole"])):
                await privil.setrole()

            # Comando Add Channel
            if message.content.lower().startswith(utils.ins_prefix(prefixo, aliases.privilevies["addchannel"])):
                await privil.addchannel()

            # Comando Remove Channel
            if message.content.lower().startswith(utils.ins_prefix(prefixo, aliases.privilevies["removechannel"])):
                await privil.removechannel()

            # Comando Channel List
            if message.content.lower().startswith(utils.ins_prefix(prefixo, aliases.privilevies["channellist"])):
                await privil.channellist()



client.run(TOKEN)