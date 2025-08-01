#!/usr/bin/env python3

import discord
from discord.ext import commands
import asyncio
import os
import signal
import sys
from cryptography.fernet import Fernet
import base64
import getpass

def print_step(msg):
    print(f"[INFO] {msg}")

def print_success(msg):
    print(f"[OK] {msg}")

def print_error(msg):
    print(f"[ERROR] {msg}")

def generate_key(password):
    return base64.urlsafe_b64encode(password.encode().ljust(32)[:32])

def encrypt_token(token, password):
    key = generate_key(password)
    fernet = Fernet(key)
    return fernet.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token, password):
    key = generate_key(password)
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_token.encode()).decode()

def save_token(encrypted_token):
    with open('.token', 'w') as f:
        f.write(encrypted_token)

def load_token():
    try:
        with open('.token', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def get_password():
    if os.path.exists('.pass'):
        with open('.pass', 'r') as f:
            return f.read().strip()
    password = os.urandom(32).hex()
    with open('.pass', 'w') as f:
        f.write(password)
    return password

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)
shutdown_event = asyncio.Event()

@bot.event
async def on_ready():
    print_success(f"Bot ready: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print_success(f"Synced {len(synced)} commands")
    except Exception as e:
        print_error(f"Failed to sync: {e}")

@bot.tree.command(name="init", description="Initialize active developer status")
async def init(interaction):
    embed = discord.Embed(
        title="Active Developer Badge",
        description="✅ Command executed successfully!\n\n"
                   "**Next steps:**\n"
                   "• Wait 2 days from now\n"
                   "• Visit https://discord.com/developers/active-developer\n"
                   "• Claim your badge\n\n"
                   "**Important:** Run this command once every month to keep your badge active!",
        color=0x5865F2
    )
    embed.set_footer(text="Bot created using https://github.com/Gur0v/easyactivedev")
    await interaction.response.send_message(embed=embed)

async def cleanup():
    print_step("Cleaning up...")
    if not bot.is_closed():
        await bot.close()
    
    tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
    if tasks:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
    
    print_success("Cleanup complete")

def signal_handler():
    print_step("Interrupt received, shutting down...")
    shutdown_event.set()

async def setup_token():
    encrypted_token = load_token()
    
    if encrypted_token is None:
        print_step("Token setup required")
        token = getpass.getpass("Enter Discord bot token: ")
        password = get_password()
        encrypted_token = encrypt_token(token, password)
        save_token(encrypted_token)
        print_success("Token saved")
    
    password = get_password()
    return decrypt_token(encrypted_token, password)

async def run_bot(token):
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, signal_handler)
    loop.add_signal_handler(signal.SIGTERM, signal_handler)
    
    print_step("Starting bot (stage 2)...")
    
    try:
        bot_task = asyncio.create_task(bot.start(token))
        shutdown_task = asyncio.create_task(shutdown_event.wait())
        
        done, pending = await asyncio.wait(
            [bot_task, shutdown_task],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        for task in done:
            if task.exception() and not isinstance(task.exception(), asyncio.CancelledError):
                raise task.exception()
                
    except KeyboardInterrupt:
        print_step("Keyboard interrupt")
    except Exception as e:
        print_error(f"Bot error: {e}")
    finally:
        await cleanup()

async def main():
    token = await setup_token()
    await run_bot(token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        print_success("Bot stopped")
        sys.exit(0)
