from dotenv import load_dotenv
import os
import logging
import discord
from discord.ext import tasks, commands
from discord import app_commands
from screenshot import take_screenshot
from selenium.common.exceptions import WebDriverException, TimeoutException
import typing
from pixeldiff import pixeldiff

logging.basicConfig(filename="pixie.log", encoding="utf-8")
interval = 600

load_dotenv(".env", override=True)
owner_id = int(os.environ["OWNER_ID"])
channel_id = int(os.environ["CHANNEL_ID"])
guild_id = int(os.environ["GUILD_ID"])

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="%", intents=intents)


@bot.event
async def on_ready():
    print("Pixiebot initiated!")
    post_screenshot.start()


@bot.tree.command(
    name="pixiefreq",
    description="Change how often pixiebot posts an update.",
)
@app_commands.describe(
    frequency="The number of seconds to wait before posting an update to the channel. Minimum 600."
)
async def pixie_freq(
    interaction: discord.Interaction, frequency: typing.Optional[int] = 0
):
    global interval
    if frequency:
        if frequency < 600:
            await interaction.response.send_message(
                "That is too low of an interval. The minimum is 10 minutes."
            )
        elif frequency > 7 * 24 * 60 * 60:
            await interaction.response.send_message(
                "That is too high of an interval. The maximum is 1 week."
            )
        else:
            interval = frequency
            post_screenshot.change_interval(seconds=interval)
            await interaction.response.send_message(
                f"Interval successfully changed to {interval} seconds."
            )
    else:
        await interaction.response.send_message(
            f"Current interval is {interval} seconds."
        )


@bot.command(name="pixiesync")
async def sync(ctx: commands.Context):
    if ctx.author.id != owner_id:
        await ctx.send("This is an owner-only command.")
    else:
        await bot.tree.sync()
        await ctx.send("Tree successfully synced")


@tasks.loop(seconds=interval)
async def post_screenshot():
    channel = bot.get_channel(channel_id)
    try:
        this_ss = await take_screenshot()
        await channel.send(file=discord.File(f"screenshots/{this_ss}"))

        screenshot_list = sorted(os.listdir("screenshots"))
        if len(screenshot_list) > 1:
            last_ss = screenshot_list[-2]

            pixels_changed = pixeldiff(last_ss, this_ss)
            if pixels_changed == 1:
                await channel.send(
                    f"{pixels_changed} pixel has been changed on the canvas since the last time I checked!"
                )
            else:
                await channel.send(
                    f"{pixels_changed} pixels have been changed on the canvas since the last time I checked!"
                )

    except (WebDriverException, TimeoutException) as e:
        logging.error(e)


bot.run(os.environ["BOT_TOKEN"])
