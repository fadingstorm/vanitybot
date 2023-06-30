import random
import lists
import settings
import discord
from discord.ext import commands
from discord import app_commands
from APIs import cats, dogs, quotes

logger = settings.logging.getLogger("bot")

# this is literally only for the help command
def help_list(thing):
    string = ''
    for i in thing:
        string += str(f'`/{i}` ')
    return string


def run():
    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix='v!', intents=intents)
    bot.remove_command('help') # remove the default help command, it's ugly

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        logger.info(f"Guild ID: {bot.guilds[0].id}")
        #bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        print('The bot should be up and running.')
        await bot.tree.sync(guild=None)
    

   # Here are all the commands for the bot
    @bot.tree.command(name='help', description='Provides a list of all commands.')
    async def help(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.blue(),
            description='This bot has many fun commands for you to use!\n*Keep in mind that this bot uses slash commands.*',
            title=f'{bot.user.name}\'s commands!'
        )
        embed.add_field(name='Helpful Commands', value=help_list(lists.random_commands), inline=False)
        embed.add_field(name='Random Commands', value=help_list(lists.random_commands), inline=False)
        embed.add_field(name='Fun Commands', value=help_list(lists.fun), inline=False)
        embed.add_field(name='Image Commands', value=help_list(lists.image), inline=False)
        await interaction.response.send_message(embed=embed)
    
    @bot.tree.command(name='ping', description='Sends pong!')
    async def ping(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.blurple(),
            description=f"{round(bot.latency * 100000) / 100}ms {interaction.user.mention}",
            title="Pong!"
        )
        await interaction.response.send_message(embed=embed)
    
    @bot.tree.command(name='quote', description='Sends a random quote!')
    async def quote(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.darker_grey(),
            description=f'*{quotes.get_quote()[0]}*'
        )
        embed.set_footer(text=f'—{quotes.get_quote()[1]}')
        await interaction.response.send_message(embed=embed)
    
    @bot.tree.command(name='fate', description='Ask a yes or no question!')
    @app_commands.describe(question='Your yes or no question.')
    async def fate(interaction: discord.Interaction, question: str):
        embed = discord.Embed(
            color=discord.Color.random(),
            title=random.choice(lists.eight_ball_responses)
        )
        await interaction.response.send_message(embed=embed)
    
    @bot.tree.command(name='dog', description='Sends a photo of a dog!')
    async def dog(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.dark_gold(),
            title="What a cute dog :dog:"
        )
        embed.set_image(url=dogs.get_dog_url())
        await interaction.response.send_message(embed=embed)
    
    @bot.tree.command(name='cat', description='Sends a photo of a cat!')
    async def cat(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.dark_gold(),
            title="What a cute cat :cat:"
        )
        embed.set_image(url=cats.get_cat_url())
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='slap', description='Slaps another user!')
    @app_commands.describe(user='The user you want to slap.')
    async def slap(interaction: discord.Interaction, user: discord.User):
        await interaction.response.send_message(f"{interaction.user.mention} slapped {user.mention}!")

    @bot.tree.command(name='punch', description='Punches another user!')
    @app_commands.describe(user='The user you want to punch.')
    async def punch(interaction: discord.Interaction, user: discord.User):
        await interaction.response.send_message(f"{interaction.user.mention} punched {user.mention}!")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()