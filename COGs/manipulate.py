import discord
import os
import requests
from discord import app_commands
from textify import textify_image
from io import BytesIO
from PIL import Image

class ManipCmds(app_commands.Group):
    def __init__(self, bot):
        super().__init__(name='manip')
        self.bot = bot

    @app_commands.command(name='rip', description='rip someone')
    @app_commands.describe(user='Who\'s avatar')
    async def rip(self, interaction: discord.Interaction, user: discord.User):
        name = 'rip.png'
        rip = Image.open("images/tombstone.png")
        asset = user.avatar.with_size(256)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((200, 200))
        rip.paste(pfp, (140, 300))
        rip.save(name)
        file = discord.File(name)
        embed = discord.Embed(description=f'**rip {user.mention} :headstone:**')
        embed.set_image(url=f"attachment://{name}")

        await interaction.response.send_message(file=file, embed=embed)
        os.remove(name)
    
    @app_commands.command(name='everest', description='Climb mount everest')
    @app_commands.describe(user='Who\'s going to climb everest')
    async def everest(self, interaction: discord.Interaction, user: discord.User):
        name = 'everest.jpg'
        rip = Image.open("images/everest.jpg")
        asset = user.avatar.with_size(256)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((205, 205))
        rip.paste(pfp, (500, 100))
        rip.save(name)
        file = discord.File(name)
        embed = discord.Embed(description=f'**{user.mention} spotted at everest :mountain_snow:**')
        embed.set_image(url=f"attachment://{name}")

        await interaction.response.send_message(file=file, embed=embed)
        os.remove(name)
    
    @app_commands.command(name='wanted', description='Armed and dangerous.')
    @app_commands.describe(user='Who is on the run')
    async def wanted(self, interaction: discord.Interaction, user: discord.User):
        name = 'wanted.jpg'
        rip = Image.open("images/wanted.jpg")
        asset = user.avatar.with_size(256)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((1317, 1317))
        rip.paste(pfp, (337, 800))
        rip.save(name)
        file = discord.File(name)
        embed = discord.Embed(description=f'**Looking for {user.mention} :cowboy:**')
        embed.set_image(url=f"attachment://{name}")

        await interaction.response.send_message(file=file, embed=embed)
        os.remove(name)
    
    @app_commands.command(name='textify', description='Draws a low quality avatar with symbols!')
    @app_commands.describe(user='The user who\'s avatar you want to textify (quality is terrible...)', size='Size of the output. Default is 31, which is the max.')
    async def emojify(self, interaction: discord.Interaction, user: discord.User, size: int = 31):
        if size > 31:
            result = 'That size is too big!'
            await interaction.response.send_message(result, ephemeral=True)
        else:
            if user.avatar is None:
                result = 'That user does not have an avatar!'
                await interaction.response.send_message(result, ephemeral=True)
            else:
                url = user.avatar.with_size(256)

                def get_emojified_image():
                    r = requests.get(url, stream=True)
                    image = Image.open(r.raw).convert("RGB")
                    res = textify_image(image, size)

                    if size > 1:
                        res = f"```{res}```"
                    return res

                result = await self.bot.loop.run_in_executor(None, get_emojified_image)
                await interaction.response.send_message(result, ephemeral=False)

async def setup(bot):
    bot.tree.add_command(ManipCmds(bot))