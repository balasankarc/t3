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

import urllib
import re
from StringIO import StringIO
import gzip
import os
import sys

inputfile = open('nexttorrent')
filecontent = inputfile.read().strip().split('#')
season = filecontent[0][-(filecontent[0][::-1].index(':')):]
episode = filecontent[1][-(filecontent[1][::-1].index(':')):]
inputfile.close()
try:
    page = urllib.urlopen(
        'https://torrentz.in/search?q=big+bang+theory+s' + season + 'e' + episode)
    pagecontenthtml = page.read()
    page.close()
    torrentline = re.findall('<dt><a href=.*?</dt>', pagecontenthtml)
    linktag = torrentline[3]
    firstquotes = linktag.index('"')
    lastquotes = linktag.index('"', firstquotes + 1)
    resulturl = linktag[firstquotes + 1:lastquotes]
    newurl = 'https://torrentz.in' + resulturl
    page = urllib.urlopen(newurl)
    pagecontenthtml = page.read()
    page.close()
    kickassline = re.findall('https://kickass.to/.*?"', pagecontenthtml)
    kickassurl = kickassline[0][:-1]
    print kickassurl
    page = urllib.urlopen(str(kickassurl))
    buf = StringIO(page.read())
    f = gzip.GzipFile(fileobj=buf)
    page.close()
    pagecontenthtml = f.read()
    torcacheline = re.findall('magnet:.*?"', pagecontenthtml)
    torrenturl = torcacheline[0][:-1]
    print torrenturl
    print "Adding Torrent"
    os.system("deluge-console add -p /home/balasankarc '" + torrenturl + "'")
    if int(episode) == 24:
        nextepisode = "01"
        nextseason = str("%02d" % (int(season) + 1))
    else:
        nextepisode = "%02d" % (int(episode) + 1)
        nextseason = season
    outfile = open('nexttorrent', 'w')
    outfile.write('season:'+nextseason+"#"+'episode:'+nextepisode)
    outfile.close()
except:
    sys.exit(0)
