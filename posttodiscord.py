import discord
from discord.ext import commands
import asyncio
from config import config
import requests


class posttodiscord:
    def createpost(comments):
        user_token = config["discord_authtoken"]
        channel_id = config["channel_id"]

        # User's Token
        header = {
            "authorization": user_token,
        }

        # File
        files = {
            "file": (
                "dailychart.png",
                open("dailychart.png", "rb"),
            )  # The picture that we want to send in binary
        }

        # Optional message to send with the picture
        payload = {"content": comments}

        r = requests.post(
            f"https://discord.com/api/v9/channels/{channel_id}/messages",
            data=payload,
            headers=header,
            files=files,
        )

        print(r)
