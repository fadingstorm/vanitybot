import random
import lists
import settings
import discord
from discord.ext import commands

logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix='v!', intents=intents)
    bot.remove_command('help') # remove the default help command, it's ugly

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        print('WOAH')
        logger.info(f"Guild ID: {bot.guilds[0].id}")
        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync(guild=settings.GUILDS_ID)
    

   # Here are all the commands for the bot
    @bot.tree.command()
    async def help(interaction: discord.Interaction):
        await interaction.response.send_message("This is the help page!")
    
    @bot.tree.command(name='ping', description='Sends pong!')
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(f"pong! {interaction.user.mention}")
    
    @bot.tree.command(name='fate', description='Ask a yes or no question!')
    async def fate(interaction: discord.Interaction, question: str):
        await interaction.response.send_message(random.choice(lists.eight_ball_responses))
    

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()