import discord
import os
import requests
import random
from discord import app_commands
from extras.textify import textify_image
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw

def wrap_text(text, line_width):
    words = text.split()
    lines = []
    current_line = ''

    for word in words:
        if len(word) > line_width:  # Check if word exceeds line_width
            return None

        if current_line:
            if len(current_line) + len(word) + 1 <= line_width:
                current_line += ' ' + word  # Append word with a space
            else:
                lines.append(current_line)
                current_line = word
        else:
            current_line += word  # First word in the line

    if current_line:
        lines.append(current_line)

    return '\n'.join(lines) if lines else None

def truncate_string(text, mmm):
    if len(text) > mmm:
        truncated_text = text[:mmm-2].strip() + "..."
    else:
        truncated_text = text
    
    return truncated_text

def make_random_date():
    month = random.choice((
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sept",
        "Oct",
        "Nov",
        "Dec"
    ))
    if month != "Feb":
        if month not in ("Jan", "Mar", "May", "Jul", "Aug", "Oct", "Dec"):
            date = random.randint(1, 30)
        else:
            date = random.randint(1, 31)
    else:
        date = random.randint(1, 28)
    
    year = random.randint(2006, 2023)
    
    return (year, month, date)
    

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
        wanted = Image.open("images/wanted.jpg")
        asset = user.avatar.with_size(256)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((1317, 1317))
        wanted.paste(pfp, (337, 800))
        wanted.save(name)
        file = discord.File(name)
        embed = discord.Embed(description=f'**Looking for {user.mention} :cowboy:**')
        embed.set_image(url=f"attachment://{name}")

        await interaction.response.send_message(file=file, embed=embed)
        os.remove(name)
    
    @app_commands.command(name='textify', description='Draws a low quality avatar with symbols!')
    @app_commands.describe(user='The user who\'s avatar you want to textify (quality is terrible...)', size='Size of the output. Default is 31, which is the max.')
    async def textify(self, interaction: discord.Interaction, user: discord.User, size: int = 31):
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
    
    @app_commands.command(name='tweet', description='Tweet something!')
    @app_commands.describe(user='Blue bird app user', text="What they tweeted!")
    async def tweet(self, interaction: discord.Interaction, user: discord.User, text: str):
        if len(text) < 60 and wrap_text(text, 32) != None:
            dateinfo = make_random_date()
            text = wrap_text(text, 32)
            displayname = truncate_string(user.display_name, 12)
            if user.bot is False:
                username = truncate_string(user.global_name, 10)
            else:
                username = truncate_string(user.display_name, 10)

            name = 'tweet.png'
            circle = Image.open("images/transparent_circle.png").resize((256, 256)).convert("RGBA")
            asset = user.avatar.with_size(256)
            data = BytesIO(await asset.read())
            pfp = Image.open(data).convert("RGBA")
            pfp.alpha_composite(circle, (0, 0))

            # making the background transparent
            rgba = pfp.convert("RGBA")
            datas = rgba.getdata()
            newData = []
            for item in datas:
                if item[0] == 0 and item[1] == 0 and item[2] == 0:  # finding black colour by its RGB value
                    # storing a transparent value when we find a black colour
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)  # other colours remain unchanged
            
            rgba.putdata(newData)
            tweetTemp = Image.open("images/tweet_template.png")
            white = Image.open("images/white.jpg").resize((2000, 396))
            rgba = rgba.resize((140, 140))
            tweetTemp.paste(white, (0, -100))
            tweet = tweetTemp.convert("RGBA")
            tweet.alpha_composite(rgba, (50, 70))
            tweet.save(name, 'PNG')

            draw = ImageDraw.Draw(tweet)
            
            font = ImageFont.truetype("IBM_Plex_Sans/IBMPlexSans-Regular.ttf", 50)
            draw.text((225, 150), text, (0, 0, 0), font=font)
            font = ImageFont.truetype("IBM_Plex_Sans/IBMPlexSans-Regular.ttf", 40)
            draw.text((500, 70), f'@{username} • {dateinfo[1]} {dateinfo[2]}, {dateinfo[0]}', (127, 127, 127), font=font)
            font = ImageFont.truetype("IBM_Plex_Sans/IBMPlexSans-Bold.ttf", 40)
            draw.text((225,70), displayname, (0, 0, 0), font=font)

            tweet.save(name, 'PNG')
            file = discord.File(name)
            
            embed = discord.Embed(
                description=f'{user.mention} tweeted something!'
            )
            embed.set_image(url=f"attachment://{name}")

            await interaction.response.send_message(file=file, embed=embed)
            os.remove(name)
        else:
            embed = discord.Embed(
                color=discord.Color.brand_red(),
                title="Sorry, your text is too long!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    bot.tree.add_command(ManipCmds(bot))