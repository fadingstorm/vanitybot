import discord
import random
from discord import app_commands

def mock_txt(text):
    letters = text.lower()
    result = ''
    i = 0
    for _ in range(len(text)):
        letter = letters[i]
        if random.randint(0, 1) == 1:
            letter = letter.upper()
        i += 1
        result += letter
    return result

def emojify_txt(text):
    emoji_dict = {}
    result = ''
    for i in "abcdefghijklmnopqrstuvwxyz":
        emoji_dict[i] = f':regional_indicator_{i}:'
    for i in text:
        if i.lower().isalpha():
            result += emoji_dict[i] + ' '
        else:
            result += i + ' '
        
    return result

def pig_latin(text):
    vowels = ['a', 'e', 'i', 'o', 'u']
    words = text.lower().split()
    pig_latin_words = []

    for word in words:
        if word[0] in vowels:
            pig_latin_words.append(word + 'way')
        else:
            if (word.startswith('th')) or (word.startswith('sh')) or (word.startswith('gh')):
                pig_latin_words.append(word[2:] + word[0] + word[1] + 'ay')
            else:
                pig_latin_words.append(word[1:] + word[0] + 'ay')

    pig_latin_text = ' '.join(pig_latin_words)
    return pig_latin_text



class TextCmds(app_commands.Group):

    @app_commands.command(name='reverse', description='Reverse a given text.')
    @app_commands.describe(text='The text you want to reverse.')
    async def reverse(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message(text[::-1])
    
    @app_commands.command(name='mock', description='mOcK SomE TeXt')
    @app_commands.describe(text='tHe tExT yoU waNt tO MoCK')
    async def mock(self, interaction:discord.Interaction, text: str):
        await interaction.response.send_message(mock_txt(text))
    
    @app_commands.command(name='emojify', description='Emojify some text!')
    @app_commands.describe(text='The text you want to emojify.')
    async def emojify(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message(emojify_txt(text))

    @app_commands.command(name='piglatin', description='Convert text into Pig Latin.')
    @app_commands.describe(text='The text you want to convert.')
    async def piglatin(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message(pig_latin(text))

async def setup(bot):
    bot.tree.add_command(TextCmds(name='text'))