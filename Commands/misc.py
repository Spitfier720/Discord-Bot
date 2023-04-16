import discord
import random
import threading
import time
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "8ball")
    @commands.guild_only()
    async def _ball(self, ctx, *, question:str = ""):
        '''
        Ask a question and the virtual and totally not based off of a true 8-Ball will give you an answer!
        Also with Mecha-Jimmy's comments!
        '''

        if not question:
            await ctx.send("{} Come on, you need to ask a question for the 8-Ball to make its response.".format(ctx.author.mention))
            return

        ball8Answers = [
            "As I see it, yes. I think.",
            "Ask again later. Busy getting reworked.",
            "Better not tell you now. The future holds...interesting things.",
            "Cannot predict now. The 8-ball is wonky.",
            "Concentrate and ask again. But open your eyes when you type.",
            "Don't count on it. This billiard ball only gives me an 8.",
            "It is certain. To a certain degree.",
            "It is decidedly so. I did not decide this.",
            "Most likely. More or less.",
            "My reply is no. Thats the only word I can make out on this stupid ball.",
            "My sources say no. Of course, when my source is a 'sentinent' ball, I wouldn't count on it.",
            "Outlook not so good. Maybe pray for a bit for better odds.",
            "Outlook good. Hopefully that's 100%.",
            "Reply hazy, try again. Stupid 8-ball.",
            "Signs point to yes. Even though the 8-ball doesn't point to anything.",
            "Very doubtful. The fact that you rely on a 6 ounce ball makes me doubt it as well.",
            "Without a doubt, as long as you don't have any.",
            "Yes. The ~~coin~~ **8ball** said so.",
            "Yes - definitely. It seems confident, so I guess I'm confident about this too.",
            "You may rely on it. Yeah, go ahead - rely on the 8ball to choose your life."
        ]

        await ctx.send("{} {}".format(ctx.author.mention, ball8Answers[random.randint(0, 19)]))

    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, user = None):
        '''
        Nice avatar you got there, be a shame if someone were to steal that
        '''

        try:
            if not user:
                user = ctx.author

            else:
                user = await commands.MemberConverter().convert(ctx, user)

        except commands.errors.MemberNotFound:
            await ctx.send("{} Well, since you didn't give me a valid user, I've decided to take it a step further and just not give an avatar at all.".format(ctx.author.mention))
            return

        e = discord.Embed(color = discord.Color.random(), description = "**{}'s avatar**\n\n".format(user.display_name))
        e.set_author(name = "So {}, you want to 'take a look' at {}'s avatar?".format(ctx.author.display_name, user.display_name), icon_url = ctx.author.avatar_url)
        e.set_image(url = user.avatar_url)
        await ctx.send(embed = e)

    @commands.command()
    @commands.guild_only()
    async def getrandom(self, ctx, min:str = "", max:str = ""):
        '''
        For when you lack the creativity and willpower to do it yourself
        '''

        if(not min or not max):
            await ctx.send("{} Did you really just ask me to give a random number without giving me anything?".format(ctx.author.mention))
            return

        try:
            min = int(min)
            max = int(max)
        except ValueError:
            await ctx.send("{} Either you typed too fast, or are just plain stupid, but either way, you need to give numbers, not some code you made up.".format(ctx.author.mention))
            return
        
        if(min > max):
            await ctx.send("{} Under what circumstances did you think that {} is greater than {}?".format(ctx.author.mention, min, max))
            return
        
        await ctx.send("{} Your random number is: **{}**".format(ctx.author.mention, random.randint(min, max)))

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
        '''
        Shows how fast the bot is
        Is he speed? Is he sloth? We must know
        '''
        latency = self.bot.latency
        await ctx.send("Your ping is: **{}** ms".format(round(latency * 1000, 2)))
        if(latency < 0.02):
            await ctx.send("I'm gaming so well with this ping but of course no one has any idea")
        
        elif(latency >= 0.02 and latency < 0.05):
            await ctx.send("I'm at a pretty good level of ping. I'll probably respond faster than a discord mod lol")
        
        elif(latency >= 0.05 and latency < 0.1):
            await ctx.send("I'm at an average level of ping, glad to see people actually use me")
        
        elif(latency >= 0.1 and latency < 0.15):
            await ctx.send("I'm at a slow-ish level of ping, so using me would be like jumping onto an shaky boat")
        
        else:
            await ctx.send("I'm experiencing some problems right now. Now look at what you've done.")
        
    @commands.command(aliases = ["say"])
    @commands.guild_only()
    async def quote(self, ctx, *message):
        '''
        Why are you even looking at this the bot just says whatever you say
        '''

        if not message:
            await ctx.send("{} has no words.".format(ctx.user.name))
        
        else:
            await ctx.send("\"{}\"\n\n - {}".format(" ".join(message), ctx.author.mention))
    
    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx):
        '''
        Wow look at all this cool stuff the server has
        '''

        e = discord.Embed(color = discord.Color.random(), description = "**{}**\n\n".format(ctx.message.guild.name))
        e.set_author(name = "So {}, you want to see the inner workings of the server?".format(ctx.author.display_name), icon_url = ctx.author.avatar_url)
        e.set_thumbnail(url = ctx.guild.icon_url)

        humans = 0
        bots = 0

        #fetch_members() takes less time, since it divides the task of getting all members in chunks.
        #Requesting for all members at once can slow down the API, especially when members reach the max limit.
        async for m in ctx.guild.fetch_members(limit = None):
            if not m.bot:
                humans += 1
            
            else:
                bots += 1

        notificationLevel = ""

        if(ctx.guild.default_notifications == discord.NotificationLevel.all_messages):
            notificationLevel = "All Messages"
        
        elif(ctx.guild.default_notifications == discord.NotificationLevel.only_mentions):
            notificationLevel = "Only Mentions"
        
        else:
            notificationLevel = "Nothing"
        
        rulesChannel = ctx.guild.rules_channel
        announcementChannel = ctx.guild.public_updates_channel

        if rulesChannel is not None:
            rulesChannel = rulesChannel.mention
        
        if announcementChannel is not None:
            announcementChannel = announcementChannel.mention

        emojiLimit = ctx.guild.emoji_limit
        level = "0"

        if(emojiLimit == 100):
            level = "1"
        
        if(emojiLimit == 150):
            level = "2"
        
        if(emojiLimit == 250):
            level = "3"
        
        afkChannel = ctx.guild.afk_channel

        if afkChannel is not None:
            afkChannel = afkChannel.mention
        
        e.add_field(name = "Member Info:", value = "Members: **{}**\nHumans: **{}**\nBots: **{}**".format(ctx.guild.member_count, humans, bots))
        e.add_field(name = "Owner:", value = ctx.guild.owner.mention)
        e.add_field(name = "Creation Date:", value = ctx.guild.created_at.strftime("%A, %B %d, %Y, at %I:%M:%S%p"))		
        e.add_field(name = "Channels Info:", value = "Number of Text Channels: **{}**\nNumber of Voice Channels: **{}**\nTotal Number of Channels: **{}**\nNumber of Categories: **{}**".format(len(ctx.guild.text_channels), len(ctx.guild.voice_channels), len(ctx.guild.text_channels) + len(ctx.guild.voice_channels), len(ctx.guild.categories)))
        e.add_field(name = "Number of Roles:", value = len(ctx.guild.roles))
        e.add_field(name = "Number of emojis:", value = len(ctx.guild.emojis))
        e.add_field(name = "Boost Level:", value = "Level {}".format(level))
        e.add_field(name = "Banner:", value = ctx.guild.banner)
        e.add_field(name = "Special Channels:", value = "Rules Channel: {}\nAnnouncement Channels: {}".format(rulesChannel, announcementChannel))
        e.add_field(name = "Notification Settings:", value = notificationLevel)
        e.add_field(name = "Verification Level:", value = ctx.guild.verification_level)
        e.add_field(name = "Default Role:", value = ctx.guild.default_role)
        e.add_field(name = "Description:", value = ctx.guild.description)
        e.add_field(name = "ID:", value = ctx.guild.id)
        e.add_field(name = "AFK Settings:", value = "AFK Channel: {}\nAFK Timeout: {}s".format(afkChannel, ctx.guild.afk_timeout))
        
        e.set_footer(text = "Now you know totally top-secret information lol")
        await ctx.send(embed = e)

    @commands.command(aliases = ["wheel"])
    @commands.guild_only()
    async def spin(self, ctx, *choices):
        '''
        Spin the wheel! Take a shot! Who wins? Who loses? Like I'd tell you!
        '''
        loadingMessage = await ctx.send("{} Choosing...".format(ctx.author.mention))
        time.sleep(1)
        
        if(len(choices) == 1):
            await loadingMessage.edit(content = "{} Well isn't that special, you've chosen {}, which also happens to be the only option. What a surpise.".format(ctx.author.mention, random.choice(choices)))
                
        elif(choices):
            await loadingMessage.edit(content = "{} has chosen {}, isn't that lucky".format(ctx.author.mention, random.choice(choices)))

        else:
            await loadingMessage.edit(content = "{} Oh wait! I can't choose, not when I have nothing to choose from!".format(ctx.author.mention))

    
    @commands.command(aliases = ["tias"], hidden = True)
    @commands.guild_only()
    async def thisisaserver(self, ctx):
        '''
        For the fools who seem to think that trolling in a random server is normal
        '''

        #I might work on this more, since right now it's just a copypasta
        await ctx.message.delete()
        await ctx.send("This is a :sparkles: server :sparkles:\nServers have :sparkles: rules :sparkles:\nIf you don't follow the rules\nThere are :sparkles: consequences :sparkles:")
    
    @commands.command(aliases = ["whois"])
    @commands.guild_only()
    async def userinfo(self, ctx, user = None):
        '''
        They say the best defense is a good offense, which is to learn everything about your opponent and to use it against them
        '''

        try:
            if not user:
                user = ctx.author

            else:
                user = await commands.MemberConverter().convert(ctx, user)

        except commands.errors.MemberNotFound:
            await ctx.send("{} Hey there buddy, energetic as you are, I can only doxx people who I know exist IN THE SERVER".format(ctx.author.mention))
            return

        e = discord.Embed(color = discord.Color.random(), description = "**All About {}**\n\n".format(user.mention))
        e.set_author(name = "So {}, you want to know all about {}?".format(ctx.author.name, user.name if user is not ctx.author else "yourself"), icon_url = ctx.author.avatar_url)
        e.set_thumbnail(url = user.avatar_url)

        activities = []
        for x in user.activities:
            activityType = ""
            
            if(x.type == discord.ActivityType.playing): activityType = "Playing "
            if(x.type == discord.ActivityType.streaming): activityType = "Streaming "
            if(x.type == discord.ActivityType.listening): activityType = "Listening to "
            if(x.type == discord.ActivityType.watching): activityType = "Watching "
            if(x.type == discord.ActivityType.custom): activityType = "Status: "
            if(x.type == discord.ActivityType.competing): activityType = "Competing in "
                
            activities.append(activityType + x.name)

        e.add_field(name = "Created Account at:", value = user.created_at.strftime("%A, %B %d, %Y, at %I:%M:%S%p"))
        e.add_field(name = "Joined Server at:", value = user.joined_at.strftime("%A, %B %d, %Y, at %I:%M:%S%p"))
        e.add_field(name = "Roles:", value = "".join([user.roles[x].mention for x in range(len(user.roles) - 1, 0, -1)]))
        e.add_field(name = "Color:", value = user.color)
        e.add_field(name = "ID:", value = user.id)
        e.add_field(name = "Activities:", value = "\n".join(activities))
        e.add_field(name = "Permissions:", value = ", ".join(u for u in dict(user.guild_permissions) if dict(user.guild_permissions)[u]))
        e.add_field(name = "Status:", value = user.raw_status)
        e.add_field(name = "Has Boosted:", value = "Yea nice I guess" if user.premium_since != None else "No lmao")

        e.set_footer(text = "Boom, now you know everything about them")

        await ctx.send(embed = e)

def setup(bot):
    bot.add_cog(Misc(bot))
