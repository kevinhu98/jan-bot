from discord.ext import commands
import praw
import os
import discord


def add_embed_field(submission, embed) -> None:
    embed_value_name = "{score}- {title}".format(score=submission.score, title=submission.title)
    embed_value_link = submission.url
    embed.add_field(name='\u200b',
                    value="[{name}]({link})".format(name=embed_value_name, link=embed_value_link),
                    inline=False)


class Stocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.subreddits = ['wallstreetbets', 'pennystocks', 'options']

        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent="my user agent"
        )

    @commands.command(name="dd")
    async def grab_dd(self, ctx, count=100):
        if count == 100:
            await ctx.send("Grabbing DD...")
        elif count > 500:
            await ctx.send("Don't break janbot pls")
            return
        else:
            await ctx.send("Grabbing DD from latest {count} posts".format(count=count))
        for subreddit in self.subreddits:
            e = discord.Embed(title="DD time", url="https://reddit.com/r/{sub}".format(sub=subreddit),
                              description="Daily DD's from r/{sub}".format(sub=subreddit),
                              color=0xE37D30)
            e.set_thumbnail(url="https://i.ebayimg.com/images/g/4qAAAOSweWldK-h8/s-l400.png")
            for submission in self.reddit.subreddit(subreddit).hot(limit=count):
                if submission.score > 100 and submission.link_flair_text in ["DD", "DD :DD:"]:
                    add_embed_field(submission, e)
                elif submission.score > 5 and "dd" in submission.title.lower().split() and subreddit in ['options']:  # grabbing from r/options, since no flairs
                    add_embed_field(submission, e)
            await ctx.send(embed=e)

    @commands.command(name="ddnew")
    async def grab_dd_new(self, ctx, count=100):
        if count == 100:
            await ctx.send("Grabbing DD...")
        elif count > 500:
            await ctx.send("Don't break janbot pls")
            return
        else:
            await ctx.send("Grabbing DD from latest {count} posts".format(count=count))
        for subreddit in self.subreddits:
            e = discord.Embed(title="DD time", url="https://reddit.com/r/{sub}".format(sub=subreddit),
                              description="Daily DD's from r/{sub}".format(sub=subreddit),
                              color=0xE37D30)
            e.set_thumbnail(url="https://i.ebayimg.com/images/g/4qAAAOSweWldK-h8/s-l400.png")
            for submission in self.reddit.subreddit(subreddit).new(limit=count):
                if submission.score > 0 and submission.link_flair_text in ["DD", "DD :DD:"]:
                    add_embed_field(submission, e)
                elif submission.score > 30 and "dd" in submission.title.lower().split() and subreddit in ['options']:  # grabbing from r/options, since no flairs
                    add_embed_field(submission, e)
            await ctx.send(embed=e)
