import json
import datetime
from datetime import datetime
import aiohttp
import discord
from discord.ext import commands
from mojang import MojangAPI
import requests

bot = commands.Bot(command_prefix = ".", case_insensitive=True, strip_after_prefix=True)
bot.launch_time = datetime.utcnow()

api_key = ""


@bot.command(name='ping')
async def ping(ctx: commands.Context) -> None:
  uptime = datetime.utcnow() - bot.launch_time
  embed = discord.Embed(description=f"Ping: `{round(bot.latency*1000):2f} ms`")
  await ctx.reply(embed=embed)

async def get_info(call):
  async with aiohttp.ClientSession() as session:
    res = await session.get(call)
    return await res.json()


@bot.command()
async def stats(ctx, username: str):
  uuid = MojangAPI.get_uuid(username)
  url = f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}"
  data = await get_info(url)
  losses = data["player"]["stats"]["Duels"].get("sumo_duel_losses")
  wins = data["player"]["stats"]["Duels"].get("sumo_duel_wins", 0)
  roundsplayed = data["player"]["stats"]["Duels"].get("sumo_duel_rounds_played", 0)
  wlr = wins if losses is None else round((wins/losses), 2)
  if losses is None:
    losses1 = f"**{username}** has __***0***__ sumo losses" + "\n"
  else:
    losses1 = f"**{username}** has __***{losses}***__ sumo losses" + "\n"
  wins1 = f"**{username}** has __***{wins}***__ sumo wins" + "\n"
  roundsplayed1 = f"**{username}** has played __***{roundsplayed}***__ games of sumo" + "\n"
  wlr1 = f"**{username}** has a __***{wlr}***__ WLR" + "\n"

  wlr_dangerous = 2
  if wlr > wlr_dangerous:
    color = 0xff0000
    danger = f":red_circle: **{username}** is a **dangerous** opponent!"
  else:
    color = 0x11fa00
    danger = f":green_circle: **{username}** is **not** a dangerous opponent!"
    
  embed = discord.Embed(title="``Stats:``", description=f"{losses1}{wins1}{roundsplayed1}{wlr1}\n{danger}", colour=color)
  await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(title="**Error**", description="Please provide a username when running the stats command!", colour=0xff0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/890893296421969960/964795016633520168/error.gif")
        await ctx.send(embed=embed)

bot.run("")

