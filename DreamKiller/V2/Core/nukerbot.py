import discord
from discord.ext import commands
from discord import ui, Interaction
from colorama import Fore, init
import asyncio

# Initialize colorama
init(autoreset=True)

# Function to get the bot token in blue
def get_token():
    token = input(Fore.BLUE + "Please enter your Discord bot token: ")
    return token

# Create a class for interactive buttons
class HelpButtons(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Delete All Roles", style=discord.ButtonStyle.danger)
    async def delete_roles(self, interaction: Interaction, button: ui.Button):
        bot_roles = {role for member in interaction.guild.members if member.bot for role in member.roles}
        for role in interaction.guild.roles:
            if role.name != "@everyone" and role not in bot_roles:
                try:
                    await role.delete()
                except discord.Forbidden:
                    await interaction.response.send_message("Missing Permissions to delete roles.", ephemeral=True)
                    return
                except discord.HTTPException as e:
                    if e.code == 50028:
                        print(Fore.BLUE + f"Invalid Role: {role.name}")
                    else:
                        raise
        await interaction.response.send_message("All roles (except @everyone and bot roles) have been deleted.", ephemeral=True)

    @ui.button(label="Delete All Channels", style=discord.ButtonStyle.danger)
    async def delete_channels(self, interaction: Interaction, button: ui.Button):
        for channel in interaction.guild.channels:
            try:
                await channel.delete()
            except discord.Forbidden:
                await interaction.response.send_message("Missing Permissions to delete channels.", ephemeral=True)
                return
        await interaction.response.send_message("All channels have been deleted.", ephemeral=True)

    @ui.button(label="Create Channels", style=discord.ButtonStyle.primary)
    async def create_channels(self, interaction: Interaction, button: ui.Button):
        await interaction.response.send_message("Please enter the name for the new channels:")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            channel_name_msg = await bot.wait_for('message', check=check, timeout=60.0)
            channel_name = channel_name_msg.content
            await interaction.channel.send("Please enter the number of channels to create:")
            number_msg = await bot.wait_for('message', check=check, timeout=60.0)
            number = int(number_msg.content)
            for i in range(number):
                try:
                    await interaction.guild.create_text_channel(f"{channel_name} #{i+1}")
                except discord.Forbidden:
                    await interaction.channel.send("Missing Permissions to create channels.", delete_after=10)
                    return
            await interaction.channel.send(f"{number} channels have been created.", delete_after=10)
        except asyncio.TimeoutError:
            await interaction.channel.send("You took too long to respond.", delete_after=10)
        except ValueError:
            await interaction.channel.send("Invalid number provided.", delete_after=10)

    @ui.button(label="Create Roles", style=discord.ButtonStyle.primary)
    async def create_roles(self, interaction: Interaction, button: ui.Button):
        await interaction.response.send_message("Please enter the name for the new roles:")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            role_name_msg = await bot.wait_for('message', check=check, timeout=60.0)
            role_name = role_name_msg.content
            await interaction.channel.send("Please enter the number of roles to create:")
            number_msg = await bot.wait_for('message', check=check, timeout=60.0)
            number = int(number_msg.content)
            for i in range(number):
                try:
                    await interaction.guild.create_role(name=f"{role_name} #{i+1}")
                except discord.Forbidden:
                    await interaction.channel.send("Missing Permissions to create roles.", delete_after=10)
                    return
            await interaction.channel.send(f"{number} roles have been created.", delete_after=10)
        except asyncio.TimeoutError:
            await interaction.channel.send("You took too long to respond.", delete_after=10)
        except ValueError:
            await interaction.channel.send("Invalid number provided.", delete_after=10)

    @ui.button(label="DM All", style=discord.ButtonStyle.primary)
    async def dm_all(self, interaction: Interaction, button: ui.Button):
        await interaction.response.send_message("Please enter the message to send to all members:")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            message = await bot.wait_for('message', check=check, timeout=60.0)
            sent_count = 0
            failed_count = 0

            # DM the author of the DM All command
            try:
                await interaction.user.send(message.content)
                sent_count += 1
            except discord.Forbidden as e:
                print(Fore.BLUE + f"Failed to DM {interaction.user}: {e}")
                failed_count += 1

            # DM all other members
            for member in interaction.guild.members:
                if member != interaction.user and not member.bot:
                    try:
                        await member.send(message.content)
                        sent_count += 1
                    except discord.Forbidden as e:
                        print(Fore.BLUE + f"Failed to DM {member}: {e}")
                        failed_count += 1

            await interaction.channel.send(
                f"Message sent to {sent_count} members. Failed to send to {failed_count} members.",
                delete_after=10
            )
        except asyncio.TimeoutError:
            await interaction.channel.send("You took too long to respond.", delete_after=10)
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")
            await interaction.channel.send("An error occurred while processing your request.", delete_after=10)

    @ui.button(label="Admin All", style=discord.ButtonStyle.primary)
    async def admin_all(self, interaction: Interaction, button: ui.Button):
        await interaction.response.send_message("Creating and assigning 'Admin' role to all members...")

        try:
            # Create the "Admin" role
            role_name = "Admin"
            existing_role = discord.utils.get(interaction.guild.roles, name=role_name)
            if existing_role:
                await interaction.channel.send(f"Role '{role_name}' already exists. Assigning it to all members...")
                admin_role = existing_role
            else:
                admin_role = await interaction.guild.create_role(name=role_name, permissions=discord.Permissions.all())
                await interaction.channel.send(f"Role '{role_name}' created. Assigning it to all members...")

            # Assign the role to all members except bots
            for member in interaction.guild.members:
                if not member.bot:
                    try:
                        await member.add_roles(admin_role)
                    except discord.Forbidden:
                        print(Fore.BLUE + f"Failed to add role to {member}: Missing Permissions")
                    except discord.HTTPException as e:
                        print(Fore.RED + f"HTTPException occurred: {e}")

            await interaction.channel.send(f"Role '{role_name}' has been assigned to all members.", delete_after=10)
        
        except asyncio.TimeoutError:
            await interaction.channel.send("You took too long to respond.", delete_after=10)
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")
            await interaction.channel.send("An error occurred while processing your request.", delete_after=10)

    @ui.button(label="Kick All", style=discord.ButtonStyle.danger)
    async def kick_all(self, interaction: Interaction, button: ui.Button):
        await interaction.response.send_message("Kicking all members...")

        try:
            for member in interaction.guild.members:
                if not member.bot:
                    try:
                        await member.kick(reason="Kicked by bot command")
                    except discord.Forbidden as e:
                        print(Fore.BLUE + f"Failed to kick {member}: {e}")
                    except discord.HTTPException as e:
                        print(Fore.RED + f"HTTPException occurred: {e}")

            await interaction.channel.send("All members have been kicked.", delete_after=10)
        
        except asyncio.TimeoutError:
            await interaction.channel.send("You took too long to respond.", delete_after=10)
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")
            await interaction.channel.send("An error occurred while processing your request.", delete_after=10)

    @ui.button(label="Ban All", style=discord.ButtonStyle.danger)
    async def ban_all(self, interaction: Interaction, button: ui.Button):
        await interaction.response.send_message("Banning all members...")

        try:
            for member in interaction.guild.members:
                if not member.bot:
                    try:
                        await member.ban(reason="Banned by bot command")
                    except discord.Forbidden as e:
                        print(Fore.BLUE + f"Failed to ban {member}: {e}")
                    except discord.HTTPException as e:
                        print(Fore.RED + f"HTTPException occurred: {e}")

            await interaction.channel.send("All members have been banned.", delete_after=10)
        
        except asyncio.TimeoutError:
            await interaction.channel.send("You took too long to respond.", delete_after=10)
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")
            await interaction.channel.send("An error occurred while processing your request.", delete_after=10)

    @ui.button(label="Auto", style=discord.ButtonStyle.danger)
    async def auto_action(self, interaction: Interaction, button: ui.Button):
        # Send a message to confirm the auto action
        await interaction.response.send_message("Starting auto action. This will delete channels, roles, and ban members. Please wait...")

        try:
            # Delete all channels
            for channel in interaction.guild.channels:
                try:
                    await channel.delete()
                except discord.Forbidden:
                    await interaction.channel.send("Missing Permissions to delete channels.", delete_after=10)
                    return

            # Create a new channel for confirmation messages
            confirmation_channel = await interaction.guild.create_text_channel("bot-actions")
            await confirmation_channel.send("All channels have been deleted.")
            
            # Delete all roles except those belonging to bots and @everyone
            bot_roles = {role for member in interaction.guild.members if member.bot for role in member.roles}
            for role in interaction.guild.roles:
                if role.name != "@everyone" and role not in bot_roles:
                    try:
                        await role.delete()
                    except discord.Forbidden:
                        await confirmation_channel.send("Missing Permissions to delete roles.", delete_after=10)
                        return
                    except discord.HTTPException as e:
                        if e.code == 50028:
                            print(Fore.BLUE + f"Invalid Role: {role.name}")
                        else:
                            raise
            
            await confirmation_channel.send("All roles (except @everyone and bot roles) have been deleted.")

            # Ban all members
            for member in interaction.guild.members:
                if member != interaction.user and not member.guild_permissions.administrator:
                    try:
                        await member.ban(reason="Banned by auto command")
                    except discord.Forbidden as e:
                        print(Fore.BLUE + f"Failed to ban {member}: {e}")
                        await confirmation_channel.send(f"Missing Permissions to ban {member}.", delete_after=10)
                        return

            await confirmation_channel.send("All members have been banned.")
        
        except asyncio.TimeoutError:
            await interaction.channel.send("You took too long to respond.", delete_after=10)
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")
            await interaction.channel.send("An error occurred while processing your request.", delete_after=10)

# Create the bot with necessary intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.members = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    print(Fore.BLUE + f'Logged in as {bot.user}')

# Custom help command
@bot.command(name='bothelp')
async def bothelp_command(ctx):
    embed = discord.Embed(title="Bot Commands", description="Here are the available commands:")
    embed.add_field(name="Delete All Roles", value="Deletes all roles except @everyone and bot roles.", inline=False)
    embed.add_field(name="Delete All Channels", value="Deletes all channels.", inline=False)
    embed.add_field(name="Create Channels", value="Creates a specified number of channels with a given name.", inline=False)
    embed.add_field(name="Create Roles", value="Creates a specified number of roles with a given name.", inline=False)
    embed.add_field(name="DM All", value="Sends a DM to all members in the server.", inline=False)
    embed.add_field(name="Admin All", value="Creates an 'Admin' role and assigns it to all members.", inline=False)
    embed.add_field(name="Kick All", value="Kicks all members from the server.", inline=False)
    embed.add_field(name="Ban All", value="Bans all members from the server.", inline=False)
    embed.add_field(name="Auto", value="Deletes all channels, all roles (except @everyone and bot roles), and bans all members.", inline=False)
    await ctx.send(embed=embed, view=HelpButtons())

# Run the bot
bot.run(get_token())
