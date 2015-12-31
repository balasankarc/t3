#!/usr/bin/env python

from lxml import etree
import re
import json
try:
    import urllib.request
except:
    import urllib2
import sys
import os
import argparse
import sendemail
import sendxmpp


parser = argparse.ArgumentParser(description='Download TV show torrents')
parser.add_argument(
    "--email", help="Specify email address to send notification")
parser.add_argument(
    "--xmpp", help="Specify jabber address to send notification")
args = parser.parse_args()

# Reading the nextone file that specifies the next episode to be downloaded
nextonefile = open('nextone')
nextonecontent = nextonefile.read()
nextonefile.close()
try:
    tv_shows = json.loads(nextonecontent)
except:
    print("Incorrect input file")
    sys.exit(0)

# Setting request header to mimic Mozilla FIrefox
headers = {'User-Agent': 'Mozilla/5.0'}

for show in tv_shows:
    print(show)
    if not tv_shows[show]['nextseason'] or not tv_shows[show]['nextepisode']:
        print("No information found")
        continue

    # Generate the string SxxExx from input file
    nextitem = "S" + tv_shows[show]['nextseason'] + \
        "E" + tv_shows[show]['nextepisode']
    url = tv_shows[show]['url']

    # Get the source HTML from corresponding web page
    try:
        req = urllib.request.Request(url, None, headers)
        page = urllib.request.urlopen(req)
    except:
        req = urllib2.Request(url, None, headers)
        page = urllib2.urlopen(req)
    sourcecontent = page.read()
    out = {}
    tree = etree.HTML(sourcecontent)

    # Find all the rows with class 'forum_header_border'
    # (From analysing the page source, the links use this format'
    r = tree.xpath('//tr[contains(@class, "forum_header_border")]')
    for row in r:
        name = row.xpath('td/a/@title')[0]
        episode_regex = re.compile(r"S[0-9]*")
        regexes = [
            "S(?P<season>[0-9]*)E(?P<episode>[0-9]*)",  # SxxExx format
            "(?P<season>[0-9]*)x(?P<episode>[0-9]*)"    # NNxNN format
        ]
        for regex in regexes:
            match = re.search(regex, name)
            if match:
                break
        seasonepisodestring = match.group()
        season = match.group('season')
        episode = match.group('episode')
        magnet_link = row.xpath('td/a[contains(@class, "magnet")]/@href')

        # Get the size column of the row
        size = float(row.xpath('td/text()')[-2][:-3])

        # Populate the nested json object with seasonepisodestring
        # and size as keys
        if seasonepisodestring not in out:
            out[seasonepisodestring] = {}
        out[seasonepisodestring][size] = magnet_link
    if nextitem in out:
        min_size = min(out[nextitem])  # Find the link with smallest size
        print(min_size, ":", out[nextitem][min_size])
        os.system("deluge-console add '" + out[nextitem][min_size][0] + "'")
        if args.email:
            sendemail.sendmail(
                args.email, 'Torrent Added', name)
        if args.xmpp:
            sendxmpp.sendmsg(args.xmpp, 'Torrent Added : '+name)

        if tv_shows[show]['nextepisode'] == '24':
            # If the number of episodes in a season has exceeded,
            # increment the season count and initialize episode to 01.
            # 24 is the normal number of episodes in TV shows
            nextseason = "%02d" % (int(tv_shows[show]['nextseason']) + 1)
            nextepisode = "01"
        else:
            # Increment the episode count
            nextseason = tv_shows[show]['nextseason']
            nextepisode = "%02d" % (int(tv_shows[show]['nextepisode']) + 1)
        tv_shows[show]['nextseason'] = nextseason
        tv_shows[show]['nextepisode'] = nextepisode
    else:
        print("Torrent not here yet")

nextonefile = open('nextone', 'w')
nextonefile.write(json.dumps(tv_shows, indent=4))
nextonefile.close()
