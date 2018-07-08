import discord
import os
import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix="!", owner_id=277981712989028353)

@bot.event
async def on_ready():
    print("Bot is online, and READY TO ROLL!")
    await bot.change_presence(game=discord.Game(name="!apply to apply for the clan."))

@bot.event
async def on_member_join(member):
    await bot.get_channel(465511193897992192).send(f"Welcome to the server of CrYpT Nd RiPPeD, {member.mention}! To apply for the clan, use !apply and I'll get you started :wink:")
    
@bot.command()
async def apply(ctx):
    """Apply for the clan!"""
    chan = bot.get_channel(327167497369419787)
    await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name="Applicant"))
    await ctx.send("Thanks for showing interest in joining our clan! You have been given the **Applicant** role. Please move to <#327167497369419787> to answer the questions.")
    await asyncio.sleep(2)
    await chan.send("Question 1: What's your age?")
    x = await bot.wait_for("message", check=lambda x: x.channel == chan and x.author == ctx.author, timeout=60.0)
    try:
        age = int(x.content)
    except ValueError:
        return await chan.send("Age isn't a valid number.")
    await chan.send("What gender are you?")
    x = await bot.wait_for("message", check=lambda x: x.channel == chan and x.author == ctx.author, timeout=60.0)
    gender = x.content.lower()
    if gender not in ("male", "female"):
        return await chan.send("Invalid gender.")
    await chan.send("Which country are you from?")
    x = await bot.wait_for("message", check=lambda x: x.channel == chan and x.author == ctx.author, timeout=60.0)
    country = x.content
    await chan.send("What Town Hall are you in COC?")
    x = await bot.wait_for("message", check=lambda x: x.channel == chan and x.author == ctx.author, timeout=60.0)
    try:
        townhall = int(x.content)
    except ValueError:
        return await chan.send("Invalid Town Hall.")
    if townhall not in (8,9,10,11,12):
        return await chan.send("Sorry! But we're currently looking for Town Hall 8-12. Come back later :wink:")
    await chan.send("What strategies do you know?")
    x = await bot.wait_for("message", check=lambda x: x.channel == chan and x.author == ctx.author, timeout=60.0)
    strategies = x.content
    await chan.send("Please submit your base screenshot.")
    x = await bot.wait_for("message", check=lambda x: x.channel == chan and x.author == ctx.author, timeout=60.0)
    try:
        screenshot = x.attachments[0]
    except IndexError:
        return await ctx.send("No screenshot was submitted.")
    await chan.send("Please submit your profile screenshot.")
    x = await bot.wait_for("message", check=lambda x: x.channel == chan and x.author == ctx.author, timeout=60.0)
    try:
        profile = x.attachments[0]
    except IndexError:
        return await chan.send("No screenshot was submitted.")
    await asyncio.sleep(5)
    em = discord.Embed(color=ctx.author.color, title="New Applicant")
    em.add_field(name="Applicant Name", value=str(ctx.author), inline=False)
    em.add_field(name="Age", value=age, inline=False)
    em.add_field(name="Gender", value=gender, inline=False)
    em.add_field(name="Country", value=country, inline=False)
    em.add_field(name="Town Hall", value=townhall, inline=False)
    em.add_field(name="Known Strategies", value=strategies, inline=False)
    em.set_image(url=screenshot.url)
    admin = discord.utils.get(ctx.guild.roles, name='ADMIN').mention
    await chan.send(f"{admin}", embed=em)
    emb = discord.Embed(color=ctx.author.color, title="Base Screenshot")
    emb.set_image(url=screenshot.url)
    await chan.send(embed=emb)
    embed = discord.Embed(color=ctx.author.color, title="Profile Screenshot")
    embed.set_image(url=profile.url)
    await chan.send(embed=embed)

    
    
@bot.command()
async def accept(ctx, user: discord.Member):
    if not "ADMIN" in [x.name for x in ctx.author.roles] or not "Co-Leader" in [x.name for x in ctx.author.roles]:
        return await ctx.send("Only Co-Leaders/Admins can use this command!")
    await user.remove_roles(discord.utils.get(bot.get_guild(327158447399370753).roles, name="Applicant"))
    await user.add_roles(discord.utils.get(bot.get_guild(327158447399370753).roles, name="Member"))
    await user.send("Congo.. You are selected! Join the clan as soon as possible :wink:")
    await ctx.send("**{}**has been accepted in to the clan!".format(str(user))) 
    
    
@bot.command()
async def reject(ctx, user: discord.Member):
    if not "ADMIN" in [x.name for x in ctx.author.roles] or not "Co-Leader" in [x.name for x in ctx.author.roles]:
        return await ctx.send("Only Co-Leaders/Admins can use this command!")
    await user.remove_roles(discord.utils.get(bot.get_guild(327158447399370753).roles, name="Applicant"))
    await user.send("Sorry, your application was rejected. :cry:")
    await ctx.send("**{}**has been rejected from the clan.".format(str(user))) 
    
    
bot.run(os.environ.get("TOKEN"))
