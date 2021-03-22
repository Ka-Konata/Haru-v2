import discord
import asyncio

client = discord.Client()

class Cmd_privilegies:
    def __init__(self, message, lang, colors, member_perms, bot_perms, utils, help, prefixo, aliases):
        self.message      = message
        self.lang         = lang
        self.colors       = colors
        self.member_perms = member_perms
        self.utils        = utils
        self.help         = help
        self.prefixo      = prefixo
        self.aliases      = aliases

        self.channels_id  = self.utils.open_json("channels.json")
        self.channels     = []
        for ch in self.channels_id.values():
            ch = self.message.guild.get_channel(ch)
            self.channels.append(ch)

        try:
            self.priv_role_id  = self.utils.open_json("privil_role.json")["role"]
        except:
            self.priv_role_id  = None
        self.privil_role = self.message.guild.get_role(self.priv_role_id)

    # Comando Move Me 
    @client.event
    async def moveme(self):
        content = self.message.content.split()

        if self.privil_role in self.message.author.roles:
            if len(content) > 1:
                try:
                    if content[1].isnumeric:
                        print(str(int(content[1])))
                        print(self.channels_id)
                        print(self.channels_id[str(int(content[1]) - 1)])
                        key = self.channels_id[str(int(content[1]) - 1)]
                        channel = self.message.guild.get_channel(key)
                        print(channel)
                        if not channel == None:
                            await self.message.author.move_to(channel)
                            await self.message.add_reaction("✅")
                        else:
                            await self.message.channel.send(f":x: Canal `{content[1]}` não encontrado")
                            await self.message.add_reaction("❌")
                    else:
                        await self.message.channel.send(f":x: Canal `{content[1]}` não encontrado")
                        await self.message.add_reaction("❌")
                except Exception as erro:
                    print(erro.__class__.__name__)
                    if erro.__class__.__name__ == "KeyError":
                        await self.message.channel.send(f":x: Canal `{content[1]}` não encontrado")
                    await self.message.add_reaction("❌")
        else:
            embed = self.utils.permission_error(f"{self.privil_role.name} role", self.lang)
            await self.message.channel.send(embed=embed)

    # Comando Set Role
    @client.event
    async def setrole(self):
        content = self.message.content.split()

        if self.member_perms.admin:
            if len(content) > 1:
                try:
                    await self.message.channel.send("`procurando o cargo...`")
                    role = self.message.guild.get_role(int(content[1]))
                    await self.message.channel.send("`verificando...`")

                    if role == None:
                        raise ValueError

                    self.priv_role_id = role.id
                    self.utils.write_json("privil_role.json", {"role":self.priv_role_id})
                    self.privil_role = self.message.guild.get_role(self.priv_role_id)
                    await self.message.channel.send(":white_check_mark: cargo setado com sucesso!")

                except Exception as erro:
                    print(erro)
                    await self.message.channel.send(f":x: Não foi possível setar o cargo `{content[1]}`. Lembre-se, você deve inserir o id de um cargo válido")
            else:
                await self.message.channel.send(f"Você escreveu o comando de forma errada \nsyntax:`h!setrole <roleID>` \nexemplo: `h!setrole 811674928994451476`")
        else:
            embed = self.utils.permission_error("administrator")
            await self.message.channel.send(embed=embed)

    # Comando Add Channel
    @client.event
    async def addchannel(self):
        content = self.message.content.split()

        if self.member_perms.admin:
            if len(content) > 2:

                try:
                    await self.message.channel.send("`procurando canal de voz...`")
                    channel = self.message.guild.get_channel(int(content[1]))
                    await self.message.channel.send("`verificando...`")

                    try:
                        position = int(content[2]) - 1
                        if position < 0:
                            raise Exception("Position Error")
                        if position > len(self.channels_id):
                            position = len(self.channels_id)
                            await self.message.channel.send(f"Posição alterada para: `{position + 1}`")
                    except Exception:
                        await self.message.channel.send(":x: Posição inválida!")
                        raise Exception("Position Error")

                    if int(content[1]) in self.channels_id.values():
                        raise Exception("Already added")

                    self.channels_id[str(position)] = channel.id
                    self.utils.write_json("channels.json", self.channels_id)
                    self.channels_id = get_channels()

                    voiceCl = await channel.connect()
                    await voiceCl.disconnect()
                    embed   = chs_embed(self.channels, self.privil_role)
                    await self.message.channel.send(":white_check_mark: canal adicionado com sucesso!")
                    await self.message.channel.send(embed=embed)
                except Exception as erro:
                    await self.message.channel.send(f":x: Não foi possível adicionar o canal de voz `{content[1]}`. Lembre-se, você deve inserir um id de um canal de voz válido")
                    print(erro)
            else:
                await self.message.channel.send(f"Você escreveu o comando de forma errada \nsyntax:`h!addchanel <channelID> [position]` \nexemplo: `h!addchannel 788518736457105411 1`")
        else:
            embed = self.utils.permission_error("administrator")
            await self.message.channel.send(embed=embed)


    # Comando Remove Channel
    @client.event
    async def removechannel(self):
        content = self.message.content.split()

        if self.member_perms.admin:
            if len(content) > 1:
                try:
                    await self.message.channel.send("`procurando canal de voz...`")
                    await self.message.channel.send("`verificando...`")

                    key = int(content[1]) -1

                    if not str(key) in self.channels_id.keys():
                        await self.message.channel.send(f":x: Canal de voz não encontrado")
                        raise Exception("not in channel_id list")

                    self.channels_id.pop(str(key))
                    self.utils.write_json("channels.json", self.channels_id)
                    self.channels_id = get_channels()
                    await self.message.channel.send(":white_check_mark: canal removido com sucesso!")

                except:
                    await self.message.channel.send(f":x: Não foi possível remover o canal de voz `{content[1]}`. Lembre-se, você deve inserir o número do canal de acordo com a lista")
            else:
                await self.message.channel.send(f"Você escreveu o comando de forma errada \nsyntax: `h!removechannel [position]` \nexemplo: `h!removechannel 1`")
        else:
            embed = self.utils.permission_error("administrator")
            await self.message.channel.send(embed=embed)


    # Comando Channel List
    @client.event
    async def channellist(self):
        if self.member_perms.member:
            embed = chs_embed(self.channels, self.privil_role)
            await self.message.channel.send(embed=embed)
        else: 
            embed = self.utils.permission_error("member")
            await self.message.channel.send(embed=embed)


def chs_embed(channels, role):
    desc = ""
    for num, ch in enumerate(channels):
        desc += f"{num + 1} - {ch.mention}" + "\n"
    desc += f"\nCargo setado: {role.mention}"

    embed = discord.Embed(title="Canais registrados:", description=desc, color=0xD8BFD8)
    return embed

def get_channels():
    import json
    arq = "channels.json"
    
    with open(arq, "r", encoding="utf-8") as f:
        content = json.load(f)
    return content