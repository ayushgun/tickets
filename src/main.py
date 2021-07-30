# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# Imports
import discord_components
import datetime
import mystbin
import discord
import asyncio
import os

from discord.ext import commands

# Bot Config
TOKEN = ""

# Role Config
# Note: Sample Values are Added
ADMIN_ROLE_NAME = "Owner"
SUPPORT_ROLE_NAME = "Staff"

# Ticket Config
# Note: Sample Values are Added
TICKET_CATEGORY_NAME = ""
TICKET_CHANNEL = 857967093516075059
SERVER_ID = 706932908190859284
LOG_CHANNEL = 706932908866142244
BTC_EMOTE_ID = 863070328765546526
ETH_EMOTE_ID = 863070328463687742
LTC_EMOTE_ID = 863070328787042314

# Intents
intents = discord.Intents.all()

# Define Client
client = commands.Bot(
    command_prefix="+",
    help_command=None,
    chunk_guilds_at_startup=False,
    case_insensitive=True,
    intents=intents,
)

# Variables
color = 0xF92246

# Extra Functions
def get_channel_id():
    """
    Get ticket channel ID
    """

    with open("ticket_id.cfg", "r") as backend:
        channel_id = backend.readline().strip()

    return client.get_channel(int(channel_id))


# Instantiate
# Note: Logs are pasted to Mystbin
mystbin_client = mystbin.Client()
discord_components.DiscordComponents(client)

# Events
async def change_status():
    """
    Rotate the client status
    every 10 seconds
    """

    while True:
        # Watching
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Ticket Bot via https://github.com/ayushgun",
            )
        )

        # Delay
        await asyncio.sleep(7)

        # Watching
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.playing, name="+help")
        )

        # Delay
        await asyncio.sleep(7)


@client.event
async def on_ready():
    """
    Fired on connect to the Discord API
    """

    # Print Startup
    os.system("cls||clear")  # Linux Friendly
    print(f"Connected to Discord API as {str(client.user)}")

    # Start Loop
    client.loop.create_task(change_status())


@client.event
async def on_command_error(ctx, error):
    """
    Fired when an error
    occurs
    """

    if isinstance(
        error,
        (
            discord.ext.commands.MissingRole,
            discord.ext.commands.MissingAnyRole,
        ),
    ):
        await ctx.reply(
            embed=discord.Embed(
                title="Error",
                color=color,
                description="You are not authorized to use this command.",
            )
        )


@client.event
async def on_button_click(interaction: discord_components.Interaction):
    """
    Event powering ticket panel
    """

    if interaction.channel == get_channel_id():
        # Constants
        guild = client.get_guild(SERVER_ID)
        ticket_category = discord.utils.get(guild.channels, name=TICKET_CATEGORY_NAME)
        support_role = discord.utils.get(guild.roles, name=SUPPORT_ROLE_NAME)

        # Get Emojis
        btc_emote = client.get_emoji(BTC_EMOTE_ID)
        eth_emote = client.get_emoji(ETH_EMOTE_ID)
        ltc_emote = client.get_emoji(LTC_EMOTE_ID)

        # Make Channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            support_role: discord.PermissionOverwrite(
                send_messages=False, read_messages=True
            ),
            interaction.user: discord.PermissionOverwrite(
                send_messages=False, read_messages=True
            ),
        }

        ticket_channel = await guild.create_text_channel(
            f"ticket-{interaction.user.name}",
            category=ticket_category,
            overwrites=overwrites,
        )

        # Add Embed in Ticket Channel
        embed = discord.Embed(
            title="Payment Method",
            description="Please select with your payment method. You have 5 minutes or your ticket will be closed.",
            color=color,
        )

        payment_message = await ticket_channel.send(
            interaction.user.mention,
            embed=embed,
            components=[
                [
                    discord_components.Button(label="BTC", emoji=btc_emote),
                    discord_components.Button(label="ETH", emoji=eth_emote),
                    discord_components.Button(label="LTC", emoji=ltc_emote),
                    discord_components.Button(label="Close", emoji="🔒"),
                ],
            ],
        )

        # Respond to Button
        await interaction.respond(
            type=4, content=f"Your ticket has been created: {ticket_channel.mention}"
        )

        # Wait for Event
        def payment_method_check(selection):
            return (
                selection.channel == ticket_channel
                and selection.user == interaction.user
            )

        try:
            selection = await client.wait_for(
                "button_click", check=payment_method_check, timeout=300.0
            )
        except asyncio.TimeoutError:
            await ticket_channel.delete()
            return await interaction.user.send(
                embed=discord.Embed(
                    title="Ticket Error",
                    description="You did not select a payment method, so your ticket has been closed.",
                    color=color,
                )
            )

        # Adjust Selection
        if selection.component.label == "BTC":
            await payment_message.delete()
            await ticket_channel.send(
                support_role.mention,
                embed=discord.Embed(
                    title="BTC Payment",
                    color=color,
                    description="""
```ADD BTC ADDRESS HERE```
📋 **Sample Text Here.**
✏️ Other Sample Text.
                """,
                ),
            )

            # Change Channel
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                support_role: discord.PermissionOverwrite(
                    send_messages=True, read_messages=True
                ),
                interaction.user: discord.PermissionOverwrite(
                    send_messages=True, read_messages=True
                ),
            }

            await ticket_channel.edit(
                name=f"order-{interaction.user.name}", overwrites=overwrites
            )

        elif selection.component.label == "ETH":
            await payment_message.delete()
            await ticket_channel.send(
                support_role.mention,
                embed=discord.Embed(
                    title="ETH Payment",
                    color=color,
                    description="""
```ADD ETH ADDRESS HERE```
📋 **Sample Text Here.**
✏️ Other Sample Text.
                """,
                ),
            )

            # Change Channel
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                support_role: discord.PermissionOverwrite(
                    send_messages=True, read_messages=True
                ),
                interaction.user: discord.PermissionOverwrite(
                    send_messages=True, read_messages=True
                ),
            }

            await ticket_channel.edit(
                name=f"order-{interaction.user.name}", overwrites=overwrites
            )

        elif selection.component.label == "LTC":
            await payment_message.delete()
            await ticket_channel.send(
                support_role.mention,
                embed=discord.Embed(
                    title="LTC Payment",
                    color=color,
                    description="""
```ADD LTC ADDRESS HERE```
📋 **Sample Text Here.**
✏️ Other Sample Text.
                """,
                ),
            )

            # Change Channel
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                support_role: discord.PermissionOverwrite(
                    send_messages=True, read_messages=True
                ),
                interaction.user: discord.PermissionOverwrite(
                    send_messages=True, read_messages=True
                ),
            }

            await ticket_channel.edit(
                name=f"order-{interaction.user.name}", overwrites=overwrites
            )

        elif selection.component.label == "Close":
            await ticket_channel.delete()


# Commands
@commands.has_role(ADMIN_ROLE_NAME)
@client.command(name="build")
async def build(ctx):
    """
    Build the ticket system
    """

    # Get Channel
    ticket_channel = client.get_channel(TICKET_CHANNEL)

    embed = discord.Embed(
        title="Make a ticket",
        description="Have a question or want to purchase? Click the button below to make a ticket.",
        color=color,
    )

    # Send with Button
    await ticket_channel.send(
        embed=embed,
        components=[discord_components.Button(label="Create", emoji="🛒")],
    )

    # Confirm Success and Save
    await ctx.reply(
        embed=discord.Embed(
            title="Successfully Built",
            description=f"Built the ticket system in {ticket_channel.mention}. Please restart the bot to cleanly activate.",
            color=color,
        )
    )

    with open("ticket_id.cfg", "w") as backend:
        backend.write(str(ticket_channel.id))


@commands.has_any_role(ADMIN_ROLE_NAME, SUPPORT_ROLE_NAME)
@client.command(name="delete")
async def delete(ctx):
    """
    Delete a ticket
    """

    if (ctx.channel.name).startswith("order") or (ctx.channel.name).startswith(
        "ticket"
    ):
        await ctx.channel.delete()
    else:
        await ctx.send(
            embed=discord.Embed(
                title="Command Error",
                description="This is not a ticket channel",
                color=color,
            )
        )


@commands.has_any_role(ADMIN_ROLE_NAME, SUPPORT_ROLE_NAME)
@client.command(name="close")
async def close(ctx):
    """
    Delete a ticket and log messages
    """

    if (ctx.channel.name).startswith("order") or (ctx.channel.name).startswith(
        "ticket"
    ):
        message_history = await ctx.channel.history(limit=None).flatten()

        # Get Ticket Messages
        messages = "".join(
            f"{str(message.author)}: {message.content}\n"
            for message in message_history[::-1]
        )

        # Log to Mystbin
        paste = await mystbin_client.post(messages, syntax="text")

        # Send to Channel
        log_channel = client.get_channel(LOG_CHANNEL)

        await log_channel.send(
            embed=discord.Embed(
                title=f"#{ctx.channel.name} Log",
                color=color,
                description=f"""
                Author: {ctx.channel.name.split("-", 1)[1]}
                Channel: #{ctx.channel.name}

                Date of Deletion: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
                Message History: {paste.url}
                """,
            )
        )

        # Delete Channel
        await ctx.channel.delete()

    else:
        await ctx.send(
            embed=discord.Embed(
                title="Command Error",
                description="This is not a ticket channel",
                color=color,
            )
        )


@client.command(name="help")
async def help(ctx):
    """
    Display commands for the help menu
    """

    embed = discord.Embed(
        title="Command Help",
        color=color,
        description="""
**+help**
Displays this menu

**+build**
Builds the ticket system

**+close**
Close a ticket and log messages

**+delete**
Close a ticket without logging
        """,
    )

    embed.set_footer(text="https://github.com/ayushgun")
    await ctx.send(embed=embed)


@client.command(name="say")
async def say(ctx, *, text):
    """
    Send a message through the bot
    """

    await ctx.send(text)
    await ctx.message.delete()


@client.command(name="embed")
async def embed(ctx, *, text):
    """
    Send a message as an embed through the bot
    """

    await ctx.send(embed=discord.Embed(description=text, color=color))
    await ctx.message.delete()


if __name__ == "__main__":
    client.run(TOKEN)
