import discord
from dotenv import load_dotenv
import os
from message_db import store_message, init_db

load_dotenv()

class MultiChannelClient(discord.Client):
    async def on_ready(self):
        init_db()
        # Split channel IDs from environment variable
        self.target_channels = os.getenv('TARGET_CHANNEL_IDS', '').split(',')
        
        print(f'Logged in as {self.user}')
        print(f"Monitoring channels: {self.target_channels}")

        # Print accessible channels for verification
        for guild in self.guilds:
            print(f"\nGuild: {guild.name}")
            for channel in guild.channels:
                print(f"- {channel.name} (ID: {channel.id})")

    async def on_message(self, message):
        # Check if message is in target channels
        if str(message.channel.id) in self.target_channels:
            print(f"Message in monitored channel: {message.channel.name}")
            store_message(message)

# Configure intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

client = MultiChannelClient(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))