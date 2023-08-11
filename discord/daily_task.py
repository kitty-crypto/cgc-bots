import sys
import os
from datetime import datetime
import discord

current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(f"{parent_directory}/common")
from database import database
from logprint import custom_print

class daily_task:
    def __init__(self, client, title='Catgirl Coin Daily Task!', foot='Thank you for all your support!', schedule=14400) -> None:
        self.client = client
        self.title = title
        self.foot = foot
        self.schedule = schedule
        self.db = database('database.db')
        self.msgThr = 10

        # Check and schedule the next_msg timestamp to the next allowed time
        next_msg_timestamp = self.db['daily_task']['next_msg']
        next_msg_timestamp = self.__get_next_allowed_timestamp(next_msg_timestamp)
        dt_db = self.db['daily_task']
        dt_db['next_msg'] = next_msg_timestamp
        self.db['daily_task'] = dt_db

    async def __send_daily_task(self, title: str, foot: str, task_channel: int, task_message: int, main_channel: int):
        task_channel = await self.client.fetch_channel(task_channel)
        task_message = await task_channel.fetch_message(task_message)
        main_channel = await self.client.fetch_channel(main_channel)
        embed = discord.Embed(title=f"{title}", colour=discord.Colour(0xffb3c9))
        embed.add_field(name=f"{str(datetime.now().date())}", value=f"{task_message.content}")
        embed.set_footer(text=f"{foot}")
        await main_channel.send(embed=embed)
        return True

    def __get_next_allowed_timestamp(self, timestamp):
        allowed_hours = [0, 4, 8, 12, 16, 20]
        next_allowed_hour = (timestamp // 3600 + 1) % 24
        while next_allowed_hour not in allowed_hours:
            timestamp += 3600  # Add an hour until we get to the next allowed hour
            next_allowed_hour = (timestamp // 3600 + 1) % 24
        return round(timestamp, -2)  # Round to the nearest minute 0 and second 0

    async def schedule_daily_task(self, msgSinceLast, main_channel=845739075835002930):
        now = int(datetime.now().timestamp())
        next_msg_timestamp = self.db['daily_task']['next_msg']
        next_msg_timestamp = self.__get_next_allowed_timestamp(next_msg_timestamp)

        if now < next_msg_timestamp:
            return False

        dt_db = self.db['daily_task']
        dt_db['next_msg'] = next_msg_timestamp + self.schedule
        self.db['daily_task'] = dt_db

        if msgSinceLast >= self.msgThr:
            await self.__send_daily_task(self.title, self.foot, self.db['daily_task']['channel'], self.db['daily_task']['message'], main_channel)
            custom_print(f'Daily task sent at: {datetime.now()}')
            dt_db["last_msg"] = 0
            self.db["daily_task"] = dt_db
            return True

        custom_print(f'Daily task skipped for chat inactivity: {datetime.now()}')
        return False
