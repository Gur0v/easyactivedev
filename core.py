#!/usr/bin/env python3

import discord
from discord.ext import commands
import asyncio
import os
import signal
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import getpass
import secrets
import stat

def log(level, msg):
    print(f"[{level}] {msg}")

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_data(data, password):
    salt = secrets.token_bytes(16)
    key = derive_key(password, salt)
    return base64.urlsafe_b64encode(salt + Fernet(key).encrypt(data.encode())).decode()

def decrypt_data(encrypted_data, password):
    try:
        decoded = base64.urlsafe_b64decode(encrypted_data.encode())
        salt, encrypted = decoded[:16], decoded[16:]
        key = derive_key(password, salt)
        return Fernet(key).decrypt(encrypted).decode()
    except Exception:
        raise ValueError("Invalid token or password")

def secure_write(filename, data):
    with open(filename, 'w') as f:
        f.write(data)
    os.chmod(filename, stat.S_IRUSR | stat.S_IWUSR)

def secure_read(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def get_master_key():
    keyfile = '.master'
    if os.path.exists(keyfile):
        return secure_read(keyfile)
    
    key = secrets.token_urlsafe(32)
    secure_write(keyfile, key)
    os.chmod(keyfile, stat.S_IRUSR)
    return key

def validate_token(token):
    if not token or len(token) < 50 or not token.replace('.', '').replace('-', '').replace('_', '').isalnum():
        raise ValueError("Invalid token format")
    return token

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(
    command_prefix='/',
    intents=intents,
    help_command=None,
    case_insensitive=False
)

shutdown = asyncio.Event()

@bot.event
async def on_ready():
    log("OK", f"Authenticated as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        log("OK", f"Synced {len(synced)} slash commands")
    except discord.HTTPException as e:
        log("ERROR", f"Failed to sync commands: {e}")

@bot.event
async def on_error(event, *args, **kwargs):
    log("ERROR", f"Discord event error in {event}")

@bot.tree.command(name="init", description="Initialize Discord Active Developer Badge")
async def init_dev(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("❌ This command must be used in a server.", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🏆 Active Developer Badge",
        description="✅ **Command executed successfully!**\n\n"
                   "**Next Steps:**\n"
                   "🕐 Wait 24-48 hours\n"
                   "🌐 Visit: https://discord.com/developers/active-developer\n"
                   "🎖️ Claim your badge\n\n"
                   "⚠️ **Reminder:** Execute monthly to maintain badge status",
        color=0x5865F2,
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(text="Bot created using https://github.com/Gur0v/easyactivedev", icon_url=bot.user.display_avatar.url)
    
    try:
        await interaction.response.send_message(embed=embed, ephemeral=True)
        log("INFO", f"Badge command executed for {interaction.user} in {interaction.guild}")
    except discord.HTTPException as e:
        log("ERROR", f"Failed to respond to interaction: {e}")

async def graceful_shutdown():
    log("INFO", "Initiating graceful shutdown...")
    
    if not bot.is_closed():
        await bot.close()
    
    tasks = [t for t in asyncio.all_tasks() if t != asyncio.current_task()]
    if tasks:
        log("INFO", f"Cancelling {len(tasks)} remaining tasks...")
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
    
    log("OK", "Shutdown complete")

def handle_shutdown():
    log("WARN", "Shutdown signal received")
    shutdown.set()

async def setup_authentication():
    token_file = '.token'
    stored_token = secure_read(token_file)
    master_key = get_master_key()
    
    if not stored_token:
        log("INFO", "First-time setup - token required")
        while True:
            try:
                raw_token = getpass.getpass("Discord Bot Token: ").strip()
                validate_token(raw_token)
                encrypted = encrypt_data(raw_token, master_key)
                secure_write(token_file, encrypted)
                log("OK", "Token encrypted and stored securely")
                return raw_token
            except ValueError as e:
                log("ERROR", str(e))
                continue
    
    try:
        return decrypt_data(stored_token, master_key)
    except ValueError:
        log("ERROR", "Token decryption failed - corrupted data")
        os.remove(token_file)
        return await setup_authentication()

async def run_bot():
    try:
        token = await setup_authentication()
        
        loop = asyncio.get_running_loop()
        if hasattr(signal, 'SIGINT'):
            loop.add_signal_handler(signal.SIGINT, handle_shutdown)
        if hasattr(signal, 'SIGTERM'):
            loop.add_signal_handler(signal.SIGTERM, handle_shutdown)
        
        log("INFO", "Starting bot (stage 2)...")
        
        bot_task = asyncio.create_task(bot.start(token))
        shutdown_task = asyncio.create_task(shutdown.wait())
        
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
            if task.exception():
                exc = task.exception()
                if isinstance(exc, discord.LoginFailure):
                    log("ERROR", "Authentication failed - invalid token")
                    if os.path.exists('.token'):
                        os.remove('.token')
                elif not isinstance(exc, asyncio.CancelledError):
                    log("ERROR", f"Bot runtime error: {exc}")
                    
    except Exception as e:
        log("ERROR", f"Critical error: {e}")
    finally:
        await graceful_shutdown()

def main():
    try:
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        log("WARN", "Keyboard interrupt")
    except Exception as e:
        log("ERROR", f"Fatal error: {e}")
    finally:
        log("OK", "Application terminated")
        sys.exit(0)

if __name__ == "__main__":
    main()
