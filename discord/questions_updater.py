import sys
import os
from mods import moderators
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(f"{parent_directory}/common")
from logprint import custom_print
from database import database

# Reddit fetch routine handled by questionFinder class
class questionFinder:
  def __init__(self, client, reddit):  # Takes the Discord Client and Reddit objects as part of initialisation
    self.__client = client  # Defining client
    self.__reddit = reddit  # Defining Reddit object
    self.__my_subreddit = "catgirlcoin"  # Subreddit
    self.__my_role = "<@&985268742227369984>"  # Reddit Helpers role in Discord
    self.__my_channel = 985268124070858832  # Channel where questions are posted
    self.__hot = '🔥'  # Emoji for New question
    self.__resolved = '✅'  # Emoji for resolved question
    self.db = database('database.db')

  async def question_updater(self):
    channel = self.__client.get_channel(self.__my_channel)  # Fetch channel from client object
    subreddit = await self.__reddit.subreddit(self.__my_subreddit)  # Fetch subreddit from reddit object
    async for comment in subreddit.stream.comments(skip_existing=True):  # Fetch sr comments to find a question
      submission = await self.__reddit.submission(str(comment.link_id)[3:])  # Get submission of the current comment
      title = str(submission.title)  # Get title of the submission
      username = str(submission.author)  # Get username of the comment
      url = "https://reddit.com" + "/".join(str(submission.permalink).split('/')[:-2])  # URL to sub as string
      #custom_print(f"New comment from {comment.author} in {url}: {comment.body}")
      if str(submission.id) in str(comment.body):  # If comment in submission's ID, TITM bot found a question
        if str(comment.author) != 'this_is_the_mae':  # Only continue if the comment is made by the bot
          pass
        message = f"New question on the subreddit. {self.__my_role}, Mae give us a paw answering, nya? \n- Author: u/{username}\n- Question: {title}\n- URL: {url}"  # Generate string for message to post on the Discord Channel
        msg = await channel.send(message)  # Post the message
        self.db.find("questions")[str(submission.id)] = msg.id  # Update the database with the message's ID and the Submission's ID as key
        react = await channel.fetch_message(self.db.find("questions")[str(submission.id)])  # Create a "hot" reaction for new submission
        await react.add_reaction(self.__hot)  # Add reaction
        custom_print(message)  # Log the message in the log
        pass
      elif "!thankyou" in str(comment.body): # If the message is the !thankyou command
        whitelist = list(moderators)  # Create a whitelist of commenters with the moderators
        whitelist.append(str(submission.author))  # Add the author of the question to the whitelist
        if str(comment.author) not in whitelist:  # If the comment is not made by OP or mod, ignore
          pass
        if not str(submission.id) in list(self.db.find("questions").keys()):  # If submission is not in the database, ignore
          pass
        react = await channel.fetch_message(self.db.find("questions")[str(submission.id)])  # Otherwise, mark the submission as responded
        await react.clear_reaction(self.__hot)  # Remove the "hot" reaction
        await react.add_reaction(self.__resolved)  # Add "resolved" reaction
        custom_print(f"https://reddit.com{'/'.join(str(submission.permalink).split('/')[:-1])}: resolved")#Add to log
      pass