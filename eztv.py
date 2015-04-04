#! /usr/bin/python
# Copyright 2015 Balasankar C <balasankarc@autistici.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import urllib2
import re
import os
from lxml import etree
import sys
import argparse
from argparse import RawTextHelpFormatter as rt


def getinfo(show_id, title):
    '''
    The episode details may be present in two forms : S##E## or #x#.
    This function parses them correctly.
    Need to be modified if more patterns arise.
    '''
    split_title = title.split('.')
    showname = show_list[show_id].split(' ')
    length = len(showname)
    splitinfo = split_title[length]
    if "x" in splitinfo:
        split_x = splitinfo.split('x')
        season = "%02d" % int(split_x[0])
        episode = "%02d" % int(split_x[1])
        info = (season, episode)
    elif "S" in splitinfo and "E" in splitinfo:
        pos_e = splitinfo.index("E")
        season = "%02d" % int(splitinfo[1:pos_e])
        episode = "%02d" % int(splitinfo[pos_e + 1:])
        info = (season, episode)
    return info
try:
    show_list = {1: 'The Big Bang Theory', 2: 'Modern Family'}
    show_link = {1: 'https://eztv.ch/shows/23/',
                 2: 'https://eztv.ch/shows/330/'}
    episode_count = {1: 24, 2: 24}
    parser = argparse.ArgumentParser(description='Download TV show torrents',
                                     formatter_class=rt)
    parser.add_argument(
        "show_id", help="Specify the show id\n" +
        "\n".join(str(show_list)[1:-1].split(', ')))
    args = parser.parse_args()
    inputfile = open('nexttorrent')
    '''
    The file nexttorrent contains details of next episode to be downloaded
    show_id season:<season number>#episode:<episode number>
    Both numbers in two digit form
    '''
    downloaded_list = {}
    with open("nexttorrent") as f:
        for line in f:
            (key, val) = line.split()
            downloaded_list[int(key)] = val
    f.close()
    filecontent = downloaded_list[int(args.show_id)].strip().split('#')
    season = "%02d" % int(filecontent[0][-(filecontent[0][::-1].index(':')):])
    episode = "%02d" % int(filecontent[1][-(filecontent[1][::-1].index(':')):])
    headers = {'User-Agent': 'Mozilla/5.0'}
    # Change user agent since eztv rejected default one.
    req = urllib2.Request(show_link[int(args.show_id)], None, headers)
    page = urllib2.urlopen(req)
    pagecontenthtml = page.read()
    tree = etree.HTML(pagecontenthtml)
    r = tree.xpath('//a[contains(@class, "magnet")]/@href')
    magnet_link = r[0]
    name = re.search('dn=.*?&', magnet_link)
    title = name.group(0)[3:-1]
    (latestseason, latestepisode) = getinfo(int(args.show_id), title)
    if latestseason == season and latestepisode == episode:
        os.system("deluge-console add '" + magnet_link + "'")
        if latestepisode == episode_count[int(args.show_id)]:
            nextseson = "%02d" % (int(season) + 1)
            nextepisode = "01"
        else:
            nextseason = season
            nextepisode = "%02d " % (int(episode) + 1)
        infostring = "season:" + nextseason + "#episode:" + nextepisode
        downloaded_list[int(args.show_id)] = infostring
        outfile = open('nexttorrent', 'w')
        for key in downloaded_list.keys():
            outfile.write(str(key) + " " + downloaded_list[key] + "\n")
        outfile.close()
except:
    sys.exit(0)
