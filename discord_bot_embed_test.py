import discord
import random
import bs4
import requests
from settings import users

TOKEN = 'NDkwMTIyNjY1MzM2NTA0MzIy.Dn0uGQ.uokwSV1FgO39Id7exalxEB2AvE0'

client = discord.Client()


def data_request(author, id):
    global casual
    global waifu
    global waifupicture
    global profileurl
    global username_web

    r = requests.get('https://r6stats.com/stats/{}/'.format(id)).text
    scrape = bs4.BeautifulSoup(r, 'html.parser')
    print(scrape)

    label = []
    count = []
    data = []
    cas_rank = []
    total = []

    for element in scrape.select('.stats-center'):
        for stats_type in element.select('.card__title'):
            if stats_type.get_text() == 'Casual Stats' or \
                    stats_type.get_text() == 'Ranked Stats':
                cas_rank.append(stats_type.get_text())
        for card in element.select('.card__content'):
            # print(card)
            for row in card.select('.desktop-only'):
                for text in row.select('.stat-label'):
                    label.append(text.get_text())

                for text in row.select('.stat-count'):
                    count.append(text.get_text())
            data.append(dict(zip(label, count)))

    for user in scrape.select('.username'):
        username_web = user.get_text()

    for mostplayed in scrape.select('.player-header__left-side'):
        waifu = str(mostplayed)
        waifupicture = str(waifu[waifu.find('src="')+5:waifu.find('"/><')])
        waifu = str(waifu[waifu.find('t="')+3:waifu.find('" src=')])

    for profile in scrape.select('.profile'):
        profile = str(profile)
        profileurl = str(profile[profile.find('src="')+5:profile.find('"/>')])

    total.append(dict(zip(cas_rank, data)))
    ranked = total[0]['Ranked Stats']
    casual = total[0]['Casual Stats']


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!insult'):
        msg = 'What the fuck is wrong with you {0.author.mention}?'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!stats'):
        msg = 'I checked your stats and honestly {0.author.mention}, they are so bad I don\'t want to print them...'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!test'):
        msg = 'Test message'
        await client.send_message(message.channel, msg)

    if message.content.startswith('!r6') or message.content.startswith('!R6'):
        print('>Stats check by ' + str(message.author))
        u = str(message.author)
        if u in users:
            username_local = users[u][0]
            id = users[u][2]
            data_request(username_local, id)
            if username_local.lower() == username_web.lower():
                embed=discord.Embed(title="R6 Stats", description="User {} has the following stats".format(username_local))
                embed.set_thumbnail(url=profileurl)
                embed.add_field(name="Time Played", value=casual['Time Played'], inline=False)
                embed.add_field(name="Kills", value=casual['Kills'], inline=False)
                embed.add_field(name="Deaths", value=casual['Deaths'], inline=False)
                embed.add_field(name="K/D Ratio", value=casual['K/D Ratio'], inline=False)
                embed.add_field(name="W/L Ratio", value=casual['W/L Ratio'], inline=False)
                embed.add_field(name="Waifu", value=waifu, inline=True)
                embed.set_image(url=waifupicture)
                await client.send_message(message.channel, embed=embed)
            else:
                msg = 'I can\'t access the R6Stats site right now so I\'ll just guess your K/D instead.'
                msg2 = 'User {} has a KD of {} on Rainbow 6: Siege'.format(author, round(random.uniform(1, 5), 3))
                return msg, msg2


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)