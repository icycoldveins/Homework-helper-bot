from discord.ext import commands, tasks
from datetime import datetime
import asyncio


class ReminderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = {}  # Store reminders by user ID
        self.check_reminders.start()  # Start the background task to check reminders

    @tasks.loop(seconds=30)
    async def check_reminders(self):
        now = datetime.now()
        for user_id, user_reminders in list(self.reminders.items()):
            for reminder in user_reminders[:]:
                if reminder['time'] <= now:
                    user = self.bot.get_user(user_id)
                    if user:
                        await user.send(f"Reminder: {reminder['description']}")
                        # Remove sent reminders
                        user_reminders.remove(reminder)

    @commands.command()
    async def setreminder(self, ctx, date: str, time: str, *, description: str):
        try:
            reminder_time = datetime.strptime(
                f"{date} {time}", "%d/%m/%Y %I:%M%p")
            reminder = {
                'id': len(self.reminders.get(ctx.author.id, [])) + 1,
                'time': reminder_time,
                'description': description
            }

            if ctx.author.id not in self.reminders:
                self.reminders[ctx.author.id] = []

            self.reminders[ctx.author.id].append(reminder)
            await ctx.send(f"Reminder set for {date} at {time} with description: {description}")
        except ValueError:
            await ctx.send("Invalid date or time format. Please use the format 'dd/mm/yyyy hh:mmAM/PM'.")

    @commands.command()
    async def getreminders(self, ctx):
        user_reminders = self.reminders.get(ctx.author.id, [])

        if not user_reminders:
            await ctx.send("You have no reminders set!")
            return

        reminder_list = []
        for reminder in user_reminders:
            reminder_list.append(
                f"ID: {reminder['id']} - {reminder['time'].strftime('%d/%m/%Y %I:%M%p')} - {reminder['description']}")

        await ctx.send("\n".join(reminder_list))

    @commands.command()
    async def deletereminder(self, ctx, reminder_id: int):
        user_reminders = self.reminders.get(ctx.author.id, [])

        if not user_reminders:
            await ctx.send("You have no reminders set!")
            return

        for reminder in user_reminders:
            if reminder['id'] == reminder_id:
                user_reminders.remove(reminder)
                await ctx.send(f"Reminder with ID {reminder_id} has been deleted!")
                return

        await ctx.send(f"No reminder found with ID {reminder_id}.")


async def setup(bot):
    await bot.add_cog(ReminderCog(bot))
