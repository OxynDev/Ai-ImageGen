import discord
from discord.ext import commands
from discord import app_commands
import time, os, json, random, httpx, io

accounts = open("accounts.txt","r").read().splitlines()


import client

config = json.loads(open("config.json","r", encoding="utf8").read())

class Cooldown:
    def __init__(self, duration):

        self.duration = duration
        self.last_end_time = None

    def remaining_time(self):
        if self.last_end_time is None:
            return 0
        else:
            return max(self.last_end_time - time.time(), 0)
    def start(self):
        self.last_end_time = time.time() + self.duration
    def is_on_cooldown(self):
        return self.remaining_time() > 0


class Discord_Bot:

    bot = None

    def __init__(self) -> None:

        self.bot_prefix = config['bot_config']["prefix"]
        self.bot_token = config['bot_config']["token"]
        self.server_id = config['bot_config']["server_id"]

        self.cooldown = {}
        
        os.system("cls")
        self.run_bot()

    def commands(self):

        @self.bot.event
        async def on_ready():
            await self.tree.sync(guild=discord.Object(id=self.server_id))
            await self.bot.change_presence(activity=discord.Game(name=f"NIGGA.AI"))


        @self.tree.command(name="ai", description="[NIGGA.AI] Create ai image", guild=discord.Object(id=self.server_id))
        async def ai(interaction, prompt: str, count: int = 1):
            if count > 4:  
                await interaction.response.send_message(content="LIMIT: 4")
                return

            await interaction.response.send_message(content="Generating AI image...")

            try:
                cookie = json.loads(random.choice(accounts))
                _client = client.Account(cookies=cookie)
                res = _client.generate_image(count, prompt)
                print(res)
                for i, image_url in enumerate(res):

                    embed = discord.Embed(description="```NIGGA.AI```")
                    response = httpx.get(image_url)
                    content_binary = response.content
                    file = discord.File(io.BytesIO(content_binary), filename=f'niggaAI_{i}.jpg')
                    embed.set_image(url=f"attachment://niggaAI_{i}.jpg")
                    await interaction.followup.send(embed=embed, file=file)


            except Exception as e:
                print(e)
                error_message = "An error occurred while generating the AI image."
                await interaction.followup.send(content=error_message)


     

    def run_bot(self):

        self.bot = discord.Client(
            command_prefix=self.bot_prefix, 
            help_command=None, 
            intents=discord.Intents().all()
        )

        self.tree = app_commands.CommandTree(self.bot)
        self.commands()
        self.bot.run(self.bot_token)
        


if __name__ == "__main__":

    Discord_Bot()