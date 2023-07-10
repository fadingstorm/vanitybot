import lists
import settings
import discord
import typing
from paginator import Paginator
from discord.ext import commands
from discord import app_commands
from APIs import anime_quotes, lorem_ipsum, quotes
from webscraping import anime_news, stock_check, songlyrics


logger = settings.logging.getLogger("bot")

INVITE_LINK = "https://discord.com/api/oauth2/authorize?client_id=1124264065221541988&permissions=534723819584&scope=bot"


# this is literally only for the help command
def help_list(thing):
    string = ''
    for i in thing:
        string += str(f'`{i}`, ')
    string = string[:-2]
    return string


def run():

    intents = discord.Intents.all()

    # the bot doesn't actually use prefixes
    bot = commands.Bot(command_prefix='v!', intents=intents)
    bot.remove_command('help') # remove the default help command

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        print('The bot should be up and running.')

        await bot.load_extension("COGs.images")
        await bot.load_extension("COGs.interactions")
        await bot.load_extension("COGs.information")
        await bot.load_extension("COGs.text_commands")
        await bot.load_extension("COGs.fun")
        await bot.load_extension("COGs.manipulate")
        await bot.tree.sync(guild=None)

   # Here are all the commands for the bot
    @bot.tree.command(name='help', description='Provides a list of all commands.')
    async def help(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.dark_purple(),
            description=f'A list of all commands available in this bot.\n*Keep in mind that this bot ONLY uses [slash commands](https://support.discord.com/hc/en-us/articles/1500000368501-Slash-Commands-FAQ).*',
            title=f'{bot.user.name}\'s Commands'
        )
        embed.add_field(name='', value=f'[Invite Me!]({INVITE_LINK})', inline=False)
        embed.add_field(name='', value='`/updates` to see the latest changes.')
        embed.add_field(name='Info Commands', value=lists.infoOfInfo + '\n' + help_list(lists.info_commands), inline=False)
        embed.add_field(name='Miscellaneous Commands', value=lists.misc_info + '\n' + help_list(lists.misc_commands), inline=False)
        embed.add_field(name='Image Commands', value=lists.image_info + '\n' + help_list(lists.image), inline=False)
        embed.add_field(name='Fun Commands', value=lists.fun_info + '\n' + help_list(lists.fun), inline=False)
        embed.add_field(name='Interaction Commands', value=lists.interactions_info + '\n' + help_list(lists.interactions), inline=False)
        embed.add_field(name='Text Commands', value=lists.text_info + '\n' + help_list(lists.textCmds), inline=False)
        embed.add_field(name='Anime Commands', value=help_list(lists.anime), inline=False)
        embed.add_field(name='Image Manipulation Commands', value=lists.manip_info + '\n' + help_list(lists.manipCmds), inline=False)

        # embed.set_footer(text='This bot was created by @fadingstorm')

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
        info = quotes.get_quote()
        embed = discord.Embed(
            color=discord.Color.darker_grey(),
            title=f'*{info[0]}*',
        )
        embed.set_footer(text=f'—{info[1]}')
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='stockinfo', description='Get info on your favorite stock!')
    @app_commands.describe(symbol='The ticker symbol of the stock.')
    async def stockinfo(interaction: discord.Interaction, symbol: str):
        stock = stock_check.get_stock(symbol)
        if stock is False:
            embed = discord.Embed(
                color=discord.Color.brand_red(),
                title="Sorry, I'm not familiar with that stock.",
                description="*Make sure to enter the symbol correctly.*"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            name = stock[0]
            price = stock[1]
            changePrice = stock[2]
            changePercent = stock[3]
            if changePrice[0] == '+':
                goodbad = ':green_circle:'
            else:
                goodbad = ':red_circle:'
            embed = discord.Embed(
                color=discord.Color.light_grey(),
                title=f'{symbol.upper()} ({name})',
            )
            embed.set_footer(text="Data may be slightly delayed.")
            embed.add_field(name="Current Price:", value=price, inline=False)
            embed.add_field(name=f"Today's Change: {goodbad}", value=f"{changePrice} | {changePercent}", inline=False)
            await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='lipsum', description='Generates placeholder text for you!')
    @app_commands.describe(amount='The number of paragraphs generated.', length='The length of each paragraph.')
    async def lipsum(
        interaction : discord.Interaction,
        amount : typing.Literal[
            '1',
            '2',
            '3',
        ],
        length : typing.Literal[
            'short',
            'medium',
            'long'
        ]
    ):
        info = lorem_ipsum.get_lipsum(amount, length)
        embed = discord.Embed(
            color=discord.Color.light_grey(),
            title=info[0],
            description=info[1]
        )
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='lyrics', description='Find the lyrics to your favorite song!')
    @app_commands.describe(song='The name of the song. Include the artist for more accuracy.')
    async def lyrics(interaction: discord.Interaction, song: str):
        info = songlyrics.get_lyrics(song)
        if info != 'Sorry, I couldn\'t find that song!':
            embeds = []
            for s in info[2]:
                embed = discord.Embed(title=info[0], description=f'By: {info[1]}', color=discord.Color.purple())
                embed.add_field(name='Lyrics', value=s)

                embeds.append(embed)
            
            view = Paginator(embeds)
            await interaction.response.send_message(embed=view.initial, view=view)
        
        else:
            embed = discord.Embed(
                title=info
            )
            embed.set_footer(text='Make sure to type the name correctly.')
            await interaction.response.send_message(embed=embed)
    
    @bot.tree.command(name='createembed', description='Create your own embed!')
    @app_commands.describe(
        title='The title of your embed.',
        description='The description (text) of your embed.',
        imageurl='The url of the image displayed in your embed.',
        thumbnailurl='The url of the thumbnail (the picture in the top right)',
        footer='The text displayed in the footer of your embed.'
        )
    async def createembed(
        interaction: discord.Interaction,
        title: str,
        description: str='',
        imageurl: str='',
        thumbnailurl: str='',
        footer: str=''
        ):
        embed = discord.Embed(
            title=title,
            description=description
        )
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
        embed.set_footer(text=footer)
        embed.set_image(url=imageurl)
        embed.set_thumbnail(url=thumbnailurl)

        try:
            await interaction.response.send_message(embed=embed)
        except:
            embed = discord.Embed(color=discord.Color.brand_red(), title='There was an error loading your embed!')
            embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name='avatar', description='Get the avatar of a user.')
    @app_commands.describe(user='The user who\'s avatar you want to grab.')
    async def avatar(interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(
            color=discord.Color.blue(),
            title=user.name
        )
        embed.set_image(url=user.avatar.url)
        embed.set_footer(text=f'Requested by {interaction.user.mention}')
        await interaction.response.send_message(embed=embed)  

    @bot.tree.command(name='animenews', description='Read up on the latest anime headlines!')
    async def animenews(interaction: discord.Interaction):
        stuff = anime_news.get_anime_news()

        # for the button (read more button)
        view = discord.ui.View()
        button = discord.ui.Button(label="Read More", url=stuff[2], style=discord.ButtonStyle.red)
        view.add_item(button)

        # for the actual embed content
        TITLE = stuff[0]
        DESC = stuff[1]
        embed = discord.Embed(
            color=discord.Color.dark_magenta(),
            title=TITLE,
            description=DESC
        )
        await interaction.response.send_message(embed=embed, view=view)

    @bot.tree.command(name='animequote', description='Sends a random anime quote!')
    async def animequote(interaction: discord.Interaction):
        QUOTE = anime_quotes.get_anime_quote()
        CHARACTER = QUOTE[0]
        TEXT = QUOTE[1]
        ANIME = QUOTE[2]
        embed = discord.Embed(
            color=discord.Color.dark_purple(),
            title=CHARACTER,
            description=f'*{TEXT}*'
        )
        embed.set_footer(text=f'{CHARACTER} | {ANIME}')
        await interaction.response.send_message(embed=embed)  

    @bot.tree.command(name='updates', description='See the latest updates to the bot.')
    async def updates(interaction: discord.Interaction):
        if lists.updates_field is None:
            embed = discord.Embed(
                color=discord.Color.dark_red(),
                title='Looks like no recent changes have been added...'
            )
        else:
            embed = discord.Embed(
                color=discord.Color.dark_purple(),
                title=lists.updates_title
            )
            embed.add_field(name="Organized Commands", value="Most commands now fall under their own category save for the `misc` and `anime` ones.", inline=False)
            embed.add_field(name="Added New Command", value="Added new command, `createuser` under the `/fun` category.", inline=False)
            embed.add_field(name='Added Command Category', value="Added command category `manip`, which allows you to have some fun with different users' avatars.", inline=False)

        
        embed.set_author(name='fadingstorm', icon_url='https://images-ext-2.discordapp.net/external/4qN_SFZi-An4N0kexMHUCLzTm-hX_irO3eegZvj3GWI/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/766147685035933737/46ea45397f8014f9c01a06ee55bf3370.png?width=343&height=343')
        
        await interaction.response.send_message(embed=embed)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()