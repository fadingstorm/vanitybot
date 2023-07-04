import discord
import random
import lists
from APIs import cats, dogs, ducks, nekos, coffees, waifu_stuff
from discord import app_commands

class InteractionCommands(app_commands.Group):
    
    @app_commands.command(name='slap', description='Slaps another user!')
    @app_commands.describe(user='The user you want to slap.')
    async def slap(self, interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(
            color=discord.Color.og_blurple(),
            description=f"**{interaction.user.mention} slapped {user.mention}!**"
        )
        embed.set_image(url=random.choice(lists.slap_gifs))
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='kiss', description='Kisses another user!')
    @app_commands.describe(user='The user you want to kiss~')
    async def kiss(self, interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(
            color=discord.Color.magenta(),
            description=f"**{interaction.user.mention} kissed {user.mention}** :heart:"
        )
        embed.set_image(url=random.choice(lists.kiss_gifs))
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='bully', description='Bully another user!')
    @app_commands.describe(user='The user you want to bully!')
    async def bully(self, interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(
            color=discord.Color.red(),
            description=f"**{interaction.user.mention} is bullying {user.mention}!**"
        )
        embed.set_image(url=waifu_stuff.get_the_img('bully'))
        embed.set_footer(text='How mean!')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='lick', description='Lick another user!')
    @app_commands.describe(user='The user you want to lick!')
    async def lick(self, interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(
            color=discord.Color.pink(),
            description=f"**{interaction.user.mention} licked {user.mention} :stuck_out_tongue:**"
        )
        embed.set_image(url=waifu_stuff.get_the_img('lick'))
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='highfive', description='High five another user!')
    @app_commands.describe(user='The user you want to high five!')
    async def highfive(self, interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(
            color=discord.Color.light_embed(),
            description=f"**{interaction.user.mention} high fived {user.mention} :hand_splayed:**"
        )
        embed.set_image(url=waifu_stuff.get_the_img('highfive'))
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='poke', description='Poke another user!')
    @app_commands.describe(user='Who do you want to poke?')
    async def poke(self, interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(
            color=discord.Color.random(),
            description=f"**{interaction.user.mention} :point_right: {user.mention}**"
        )
        embed.set_image(url=waifu_stuff.get_the_img('poke'))
        embed.set_footer(text='poke poke poke')
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    bot.tree.add_command(InteractionCommands(name='interact'))