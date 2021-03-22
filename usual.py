import discord
import os
from discord.ext.commands import has_permissions, MissingPermissions

client  = discord.Client()
Thistle	= 0xD8BFD8	

class Utils:
    def __init__(self, icon_url, client, token=None):
        self.TOKEN    = token
        self.icon_url = icon_url
        self.client   = client


    def write_json(self, file, description, encoding="utf-8"):
        """
        create and/or write in a .json file
        file:          file name
        description:   the value to be saved in the file
        encoding:      encoding wich will be used
        """
        import json

        if not ".json" in file:
            file += ".json"

        with open(file, "w", encoding=encoding) as json_file2:
            json.dump(description, json_file2, indent=4)


    def open_json(self, file, encoding="utf-8"):
        """
        open a .json file
        file:     file name 
        encoding: encoding wich will be used
        return returns a variable with the contents of the file
        """
        import json

        if not ".json" in file:
            file += ".json"

        content = {}
        if os.path.exists(file): 
            with open(file, "r", encoding=encoding) as f:
                content = json.load(f)
        return content

    def ins_prefix(self, prefix, command):
        """
        inserts the prefix in each alias of a command
        prefix:     inserts the prefix in each alias of a command
        command:    command alias list
        return alias list with the prefix
        """
        aliases = []
        for aliase in command:
            aliase = prefix + aliase
            aliases.append(aliase)
        aliases = tuple(aliases)
        return aliases

    
    def set_language(self, prefix, guild):  #message
        """
        search the defined language for the guild
        prefix:      guild prefix
        guild:       guild id of the message
        """

        usu          = Utils(self.icon_url, client)

        português_BR = usu.open_json("languages/pt-br")
        english      = usu.open_json("languages/en.json")
        languages    = {"pt-br":português_BR, "en":english}

        confgs       = usu.get_guild_configs(guild)
        lang         = languages[confgs["language"]]

        return lang

    
    def get_permissions(self, member, requeriments):
        """"""
        perms = member.guild_permissions
        level = requeriments.Requeriments()
        
        if perms.administrator:
            level.admin  = True
            level.mod    = True
            level.member = True

        elif perms.ban_members:
            level.admin  = False
            level.mod    = True
            level.member = True

        elif perms.send_messages:
            level.admin  = False
            level.mod    = False
            level.member = True

        return level
    

    def permission_error(self, permission, lang):
        embed = discord.Embed(title=lang["PERMISSION_ERROR_TITLE"])
        embed.set_author(name=lang["PERMISSION_ERROR_AUTHOR_NAME"], icon_url=self.icon_url)
        embed.add_field(name=lang["PERMISSION_ERROR_FIELD_NAME"], value=permission, inline=True)

        return embed
    

    def bot_permission_error(self, permission, lang):
        embed = discord.Embed(title=lang["BOT_PERM_ERROR_TITLE"])
        embed.set_author(name=lang["BOT_PERM_ERROR_AUTHOR_NAME"], icon_url=self.icon_url)
        embed.add_field(name=lang["BOT_PERM_ERROR_FIELD_NAME"], value=permission, inline=True)

        return embed


    def guild_confgs_model(self):
        model = {
            "language":"pt-br",
            "prefix":"h!",
            "locked_commands":[],
            "nsfw":True
        }

        return model

    
    def get_guild_configs(self, guild):
        usu     = Utils(self.icon_url, self.client)
        arq     = "configs/guilds configs/" + str(guild.id)
        configs = usu.open_json(arq)

        return configs

    def change_guild_config(self, guild, new_config, confg_key):
        usu     = Utils(self.icon_url, self.client)
        arq     = "configs/guilds configs/" + str(guild.id)
        configs = usu.open_json(arq)

        configs[confg_key] = new_config
        usu.write_json(arq, configs)


    def get_prefix(self, guild_id):
        from os import path

        usu  = Utils(self.icon_url, self.client)

        file = "configs/guilds configs/" + str(guild_id)  + ".json"

        if not path.exists(file):
            model = usu.guild_confgs_model()
            model["prefix"] = "h!"
            usu.write_json(file, model)
            return "h!"
 
        else:
            f = usu.open_json(file)
            prefix = f["prefix"]
            return prefix


    def embed_model(self, lang, prefixo, colors, ex_value, aliases, extra1=False, extra2=False, howToUse=False):
        embed = discord.Embed(title=lang["TITLE"], description=lang["DESCRIPTION"], color=colors.Thistle)
        embed.set_author(name=lang["AUTHOR_NAME1"] + f" {prefixo}help " + lang["AUTHOR_NAME2"], icon_url=self.icon_url)

        if howToUse:
            embed.add_field(name=lang["USE_NAME"], value="```" + prefixo + lang["USE_VALUE"] + "```", inline=True)
        if extra1:
            embed.add_field(name=lang["EXTRA1_NAME"], value=lang["EXTRA1_VALUE"], inline=True)
        if extra2:
            embed.add_field(name=lang["EXTRA2_NAME"], value=lang["EXTRA2_VALUE"], inline=True)

        embed.add_field(name=lang["EXAMPLE_NAME"], value=ex_value, inline=True)

        _aliases = "```"
        for n, alias in enumerate(aliases):
            if n + 1 == len(aliases):
                _aliases = _aliases + alias + "```"
                break
            _aliases = _aliases + alias + ", " 

        embed.add_field(name=lang["ALIASES_NAME"], value=_aliases, inline=True)

        return embed


    @client.event
    async def command_gif(self, message, mentions, lang, lang_key, client, _help, gifs, help_request, reply=False):
        from random import choice
        lang  = lang[lang_key]
        error = False

        if len(message.content.split()) > 1:

            users = [message.author]
            user  = message.content.split()[1] 

            try:
                users.append(client.get_user(int(user)))
                users[1].id = users[1].id
            except (ValueError, AttributeError):
                try:
                    users.append(mentions[0])
                except IndexError:
                    error = True
                    await message.channel.send(lang["USER_NOT_FOUND_ERROR"] + "`" + user + "`")  # send a message error for user not found

            interp = lang["MADE"]
            if reply:
                u0 = users[0]
                u1 = users[1]
                users = [u1, u0]
                interp = lang["REPLY"]

            if not error:
                embed = discord.Embed(description=users[0].mention + " " + interp + " " + users[1].mention, color=Thistle)
                embed.set_author(name=message.author.name + "#" + message.author.discriminator, icon_url=message.author.avatar_url)
                url   = choice(gifs)
                embed.set_image(url=url)
                await message.reply(embed=embed)
        else:
            await _help.help(request=help_request)


    @client.event
    async def get_user(self, content, mentions, message, _lang):
        user = None
        try:
            user    = self.client.get_user(int(content))
            user.id = user.id
        except (ValueError, AttributeError) as erro:
            print(erro)
            try:
                user = mentions[0]
            except IndexError as erro:
                print(erro)
                user = None
                await message.reply(_lang["USER_NOT_FOUND_ERROR"] + "`" + content + "`")
        return user


    @client.event
    async def get_member(self, content, mentions, message, _lang):
        member = None
        try:
            member    = message.guild.get_member(int(content))
            erro = member.id
        except (ValueError, AttributeError) as erro:
            try:
                member = mentions[0]
            except IndexError as erro:
                member = None
                await message.reply(_lang["USER_NOT_FOUND_ERROR"] + "`" + content + "`")
        return member