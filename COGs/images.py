import discord
from APIs import cats, dogs, ducks, nekos, coffees, waifu_stuff
from discord import app_commands


class ImageCommands(app_commands.Group):
    @app_commands.command(name='cat', description='Sends a photo of a cat!')
    async def cat(self, interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.dark_gold(),
            title="Meow Meow! :cat:"
        )
        embed.set_image(url=cats.get_cat_url())
        embed.set_footer(text='Dogs or cats?')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='dog', description='Sends a photo of a dog!')
    async def dog(self, interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.dark_gold(),
            title="Woof Woof! :dog:"
        )
        embed.set_image(url=dogs.get_dog_url())
        embed.set_footer(text='Man\'s best friend')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='duck', description='Sends an image of a duck!')
    async def duck(self, interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.dark_gold(),
            title="Quack! :duck:"
        )
        embed.set_image(url=ducks.get_duck_img()[0])
        embed.set_footer(text=f'{ducks.get_duck_img()[1]}')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='neko', description='Sends an image of a neko!')
    async def neko(self, interaction: discord.Interaction):
        info = nekos.get_neko_img()
        embed = discord.Embed(
            color=discord.Color.pink(),
            title="Neko~"
        )
        embed.set_image(url=info[0])
        embed.set_footer(text=f'Artist: {info[1]}')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='coffee', description='Sends a random photo of coffee!')
    async def coffee(self, interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.dark_orange(),
            title="Coffee. :coffee:"
        )
        embed.set_image(url=coffees.get_coffee_img())
        embed.set_footer(text='Everyone needs it.')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='megumin', description='Sends a random photo of Megumin!')
    async def megumin(self, interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.orange(),
            title="爆裂 :boom:"
        )
        embed.set_image(url=waifu_stuff.get_the_img('megumin'))
        embed.set_footer(text='Megumin')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='smug', description=':smirk:')
    async def smirk(self, interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.dark_teal(),
            title=':smirk:'
        )
        embed.set_image(url=waifu_stuff.get_the_img('smirk'))
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='nom', description='nom nom nom')
    async def nom(self, interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.yellow(),
            title='nom nom nom'
        )
        embed.set_image(url=waifu_stuff.get_the_img('nom'))
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='cringe', description='Cringe at something!')
    async def cringe(self, interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.random(),
            description=f'{interaction.user.mention} is cringing...'
        )
        embed.set_image(url=waifu_stuff.get_the_img('cringe'))
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    bot.tree.add_command(ImageCommands(name='image'))