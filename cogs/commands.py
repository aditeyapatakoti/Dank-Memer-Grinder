import asyncio
import json
import random
import time

from discord.ext import commands, tasks

with open("config.json", "r") as config_file:
    config_dict = json.load(config_file)


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.commands.start()

    @tasks.loop(seconds=config_dict["global"]["min_commands_delay"] / 1000)
    async def commands(self):
        if not self.bot.state:
            await asyncio.sleep(1)
            return

        shuffled_commands = list(self.bot.commands_dict)[:]
        random.shuffle(shuffled_commands)

        for command in shuffled_commands:
            if self.bot.pause_commands:
                if time.time() - self.bot.pause_commands_timestamp > 60:
                    self.bot.pause_commands = False
                else:
                    await asyncio.sleep(1)
                    return

            if (
                time.time() - self.bot.last_ran[command]
                < self.bot.config_dict["commands"][command]["delay"]
                or not self.bot.config_dict["commands"][command]["state"]
                or not self.bot.state
            ):
                await asyncio.sleep(0.1)
                continue
            self.bot.last_ran[command] = time.time() + 2
            if command == "dep_all":
                await asyncio.sleep(random.randint(2, 4))
                await self.bot.send(self.bot.commands_dict[command], amount="max")
                continue
            elif command == "work":
                await asyncio.sleep(random.randint(2, 4))
                await self.bot.sub_send(self.bot.commands_dict[command], "shift")
                continue
            elif command == "pet":
                self.bot.pause_commands = True
                self.bot.pause_commands_timestamp = time.time()
                await asyncio.sleep(random.randint(2, 4))
                await self.bot.sub_send(self.bot.commands_dict[command], "care")
                continue
            elif command == "adventure":
                self.bot.pause_commands = True
                self.bot.pause_commands_timestamp = time.time()
                await asyncio.sleep(random.randint(2, 4))
                await self.bot.send(self.bot.commands_dict[command])
                continue
            await asyncio.sleep(random.randint(2, 4))
            await self.bot.send(self.bot.commands_dict[command])
            continue


async def setup(bot):
    await bot.add_cog(Commands(bot))
