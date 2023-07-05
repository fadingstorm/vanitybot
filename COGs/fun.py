import discord
import random
import asyncio
import lists
from discord import app_commands
from APIs import trivias, dadjokes, user

class FunCmds(app_commands.Group):
    def __init__(self, bot):
        super().__init__(name='fun')
        self.bot = bot
    
    @app_commands.command(name='trivia', description='Asks a random trivia question!')
    async def trivia(self, interaction: discord.Interaction):
        channel = interaction.channel
        info = trivias.get_trivia()
        all_choices = [info['correct_answer']] + info['incorrect_answers']
        random.shuffle(all_choices)
        question_type = info['type']

        # matches each choice to ABCD (if it is a multiple choice)
        if question_type != 'boolean':
            choices_dict = {
                'A':all_choices[0],
                'B':all_choices[1],
                'C':all_choices[2],
                'D':all_choices[3],
            }

        # Creating the actual embed to ask the question
        embed = discord.Embed(
            color=discord.Color.blue(),
            description='Type the letter of the correct answer or true/false!'
        )
        embed.add_field(name='Category', value=info['category'])
        embed.add_field(name='Difficulty', value=info['difficulty'].upper())
        embed.add_field(name='Question', value=info['question'], inline=False)

        # I dont wanna type this out again
        correct_letter = list(choices_dict.keys())[list(choices_dict.values()).index(info['correct_answer'])]

        # if the question is a multiple choice, or a true/false, the bot will take answers differently
        # prolly could have made this more efficient but whatever
        if question_type == 'boolean':
            embed.add_field(name='True or False?', value='')
            await interaction.response.send_message(embed=embed)
            
            # now waiting for a response
            def check(m):
                return (m.content.capitalize() in ('True', 'False')) and m.channel == channel
            try:
                answer = await self.bot.wait_for('message', check=check, timeout=12)

                # when the answer is right
                if answer.content.capitalize() == info['correct_answer']:
                    embed.color = discord.Color.brand_green()
                    embed.description = f'{answer.author.mention} got it first!'
                    embed.add_field(name='Correct Answer\n', value=info['correct_answer'], inline=False)
                    embed.set_footer(text='Nice job!')
                    await interaction.edit_original_response(embed=embed)
                else: # when the answer is wrong
                    embed.color = discord.Color.brand_red()
                    embed.description = f'{answer.author.mention} got it wrong!'
                    embed.add_field(name='Correct Answer\n', value=info['correct_answer'], inline=False)
                    embed.set_footer(text=f'You chose: {answer.content.capitalize()}')
                    await interaction.edit_original_response(embed=embed)
            except asyncio.TimeoutError: # when the time is up
                embed.color = discord.Color.brand_red()
                embed.description = 'Time\'s up!'
                embed.add_field(name='Correct Answer\n', value=info['correct_answer'], inline=False)
                embed.set_footer(text='You get 12 seconds to answer.')
                await interaction.edit_original_response(embed=embed)       
        else:
            embed.add_field(
                name='Choices',
                value=f'**A)** {all_choices[0]}\n**B)** {all_choices[1]}\n**C)** {all_choices[2]}\n**D)** {all_choices[3]}'
            )
            await interaction.response.send_message(embed=embed)
        
            # now waiting for a response
            def check(m):
                return (m.content.capitalize() in ('A', 'B', 'C', 'D')) and m.channel == channel
            try:
                answer = await self.bot.wait_for('message', check=check, timeout=12)

                # when the answer is right
                if choices_dict[answer.content.capitalize()] == info['correct_answer']:
                    embed.color = discord.Color.brand_green()
                    embed.description = f'{answer.author.mention} got it first!'
                    embed.add_field(name='Correct Answer\n', value=correct_letter + '\n' + info['correct_answer'], inline=False)
                    embed.set_footer(text='Nice job!')
                    await interaction.edit_original_response(embed=embed)
                else: # when the answer is wrong
                    embed.color = discord.Color.brand_red()
                    embed.description = f'{answer.author.mention} got it wrong!'
                    embed.add_field(name='Correct Answer', value=correct_letter + '\n' + info['correct_answer'], inline=False)
                    embed.set_footer(text=f'You chose: {choices_dict[answer.content.capitalize()]}')
                    await interaction.edit_original_response(embed=embed)
            except asyncio.TimeoutError: # when the time is up
                embed.color = discord.Color.brand_red()
                embed.description = 'Time\'s up!'
                embed.add_field(name='Correct Answer', value=correct_letter + '\n' + info['correct_answer'], inline=False)
                embed.set_footer(text='You get 12 seconds to answer.')
                await interaction.edit_original_response(embed=embed)

    @app_commands.command(name='8ball', description='Ask a yes or no question!')
    @app_commands.describe(question='Your yes or no question.')
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        embed = discord.Embed(
            color=discord.Color.random(),
            description=random.choice(lists.eight_ball_responses),
        )
        embed.set_author(name=question)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='dadjoke', description='Get a random dad joke!')
    async def dadjoke(self, interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.random(),
            title=dadjokes.get_dadjoke(),
        )
        await interaction.response.send_message(embed=embed)  
    
    @app_commands.command(name='createuser', description='Generate a random online user!')
    async def createuser(self, interaction: discord.Interaction):
        info = user.generate_user()
        embed = discord.Embed(
            color=discord.Color.blue(),
            title=info['firstname'] + ' ' + info['lastname'],
            description=info['username'],
        )
        embed.set_thumbnail(url=info['pic'])
        embed.add_field(name='Gender', value='`' + info['gender'] + '`')
        embed.add_field(name='Age', value='`' + str(info['age']) + '`')
        embed.add_field(name='Country', value='`' + info['country'] + '`')
        embed.add_field(name='City', value='`' + info['city'] + '`')
        embed.add_field(name='Email', value='`' + info['email'] + '`')

        embed.set_footer(text='Hi there!')

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    bot.tree.add_command(FunCmds(bot))