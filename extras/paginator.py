import discord
from typing import List
from collections import deque

class Paginator(discord.ui.View):
    def __init__(self, embeds: List[discord.Embed]) -> None:
        super().__init__(timeout=180)

        self._embeds = embeds
        self._queue = deque(embeds)
        self._initial = embeds[0]
        self._len = len(embeds)
        self._current_page = 1
        self.children[0].disabled = True
        self.children[1].disabled = True
        if self._len == 1:
            self.children[0].disabled = True
            self.children[1].disabled = True
            self.children[2].disabled = True
            self.children[3].disabled = True
        self._queue[0].set_footer(text=f'Page {self._current_page} of {self._len}')


    async def update_buttons(self, interaction: discord.Interaction) -> None:
        for i in self._queue:
            i.set_footer(text=f'Page {self._current_page} of {self._len}')
        if self._current_page == self._len:
            self.children[2].disabled = True
            self.children[3].disabled = True
        else:
            self.children[2].disabled = False
            self.children[3].disabled = False

        if self._current_page == 1:
            self.children[1].disabled = True
            self.children[0].disabled = True
        else:
            self.children[1].disabled = False
            self.children[0].disabled = False
        
        await interaction.message.edit(view=self)

    @discord.ui.button(label='◄◄', style=discord.ButtonStyle.primary)
    async def first(self, interaction: discord.Interaction, _):
        self._queue.rotate(-self._current_page + 1)
        embed = self._queue[0]
        self._current_page -= self._current_page - 1
        await self.update_buttons(interaction)
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label='◄', style=discord.ButtonStyle.primary)
    async def previous(self, interaction: discord.Interaction, _):
        self._queue.rotate(-1)
        embed = self._queue[0]
        self._current_page -= 1
        await self.update_buttons(interaction)
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label='►', style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, _):
        self._queue.rotate(1)
        embed = self._queue[0]
        self._current_page += 1
        await self.update_buttons(interaction)
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label='►►', style=discord.ButtonStyle.primary)
    async def last(self, interaction: discord.Interaction, _):
        self._queue.rotate(len(self._queue) - self._current_page)
        embed = self._queue[0]
        self._current_page += len(self._queue) - self._current_page
        await self.update_buttons(interaction)
        await interaction.response.edit_message(embed=embed)
    
    @property
    def initial(self) -> discord.Embed:
        return self._initial