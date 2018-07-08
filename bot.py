import discord
import os
import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix="!", owner_id=277981712989028353)

@bot.event
async def on_ready():
    print("Bot is online, and READY TO ROLL!")
    await bot.change_presence(game=discord.Game(name="!apply to apply for the clan."))
    
    
@bot.command()
async def apply(ctx):
    """Apply for the clan!"""
    await ctx.send("Thanks for showing interest in joining our clan! Please answer my questions so that you could get into the clan.")
    await asyncio.sleep(2)
    await ctx.send("Question 1: What's your age?")
    x = await bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
    try:
        age = int(x.content)
    except ValueError:
        return await ctx.send("Age isn't a valid number.")
    await ctx.send("What gender are you?")
    x = await bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
    gender = x.content.lower()
    if gender not in ("male", "female"):
        return await ctx.send("Invalid gender.")
    await ctx.send("Which country are you from?")
    x = await bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
    country = x.content
    await ctx.send("What Town Hall are you in COC?")
    x = await bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
    try:
        townhall = int(x.content)
    except ValueError:
        return await ctx.send("Invalid Town Hall.")
    if townhall not in (8,9,10,11,12):
        return await ctx.send("Sorry! But we're currently looking for Town Hall 8-12. Come back later :wink:")
    await ctx.send("Please submit your base and profile screenshots and wait for a Co Leader to validate them and accept you in!")
    x = await bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
    try:
        screenshot = x.attachments[0]
    except IndexError:
        return await ctx.send("No screenshot was submitted.")
    await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name="Applicant"))
    await ctx.send("You have been given the **Appplicant** role, which gives you access to the channel <#327167497369419787>. The Admins and Co-Leaders will ask you questions.")
    em = discord.Embed(color=ctx.author.color, title="New Applicant")
    em.add_field(name="Applicant Name", value=str(ctx.author), inline=False)
    em.add_field(name="Age", value=age, inline=False)
    em.add_field(name="Gender", value=gender, inline=False)
    em.add_field(name="Country", value=country, inline=False)
    em.add_field(name="Town Hall", value=townhall, inline=False)
    em.set_image(url=screenshot.url)
    admin = discord.utils.get(ctx.guild.roles, name='ADMIN').mention
    co = discord.utils.get(ctx.guild.roles, name='Co-Leader').mention
    await ctx.send(f"{admin} {co}", embed=em)
