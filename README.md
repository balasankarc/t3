#TV Torrent Taker (T3)
T3 is a python script to download torrents of your favorite TV shows from the site eztv.ch. The list of the TV Shows that are supported are

1. The Big Bang Theory
2. Modern Family

WARNING : Downloading TV Shows without their respective owners' permission is deemed illegal in many countries. Use at your own risk.

##Requirements
1. Packages deluge, deluge-web, deluge-console
2. Python 2.7 - Porting to Python3 is going on. Will update once done.
3. Python modules - urllib2, lxml, argparse, xmpp, smtplib

##Installation
Either clone the repository  
`git clone https://gitlab.com/balasankarc/tbbt-downloader.git`  
`cd tbbt-downloader`  
`python t3.py 1 <show_id>`

##Usage
The basic usage of the script is as follows  
`python t3.py [options] show_id`  
where the show_id follows the list of shows supported above. 
####Options
The various options supported by T3 are  

Syntax  | Meaning  | Example
:-------------:|:-------------:|:----------:
-h  | View the help  | python t3.py -h
--email \<EMAIL>  | Send email notifications | python t3.py --email test@example.com 1
--xmpp \<JID>  | Send XMPP notifications | python t3.py --xmpp test@example.com 1

Note : For the notifications to work, the files .xsend and .xemail should be present inside the $HOME directory. The content of these files are  


**.xsend**  
JID=\<your jabber id - used as the sender>  
PASSWORD=\<password>



**.xemail (supports only GMail now)**  
USERNAME=\<your jabber id - used as the sender>  
PASSWORD=\<password>


WARNING : NOTIFICATIONS REQUIRE STORING PASSWORDS IN PLAIN TEXT AND HENCE SHOULD BE USED IN OWN RESPONSIBILITY.

##FAQ
**1. Does this support only eztv.ch?**  
Well, at first I followed a method of using [Torrentz](http://torrentz.eu) to find and download the first search hit. But then I was told about the website [EZTV](http://eztv.ch) which listed all the shows I needed then. If I need shows not listed in eztv.ch in future, I'll modify the script to get them.

**2. Can you add my favorite show too?**  
Why not?? Just file an issue. I'll see if I can get a consistent location to pull the latest torrents. To be frank, you may yourself add them and file a pull request. I beleive the code is actually simple enough to understand. I will add comments when I get time.

##Contributing
This script, as usual, was created just to solve developer's personal itch. So, it contains the quickest (which surely will be ugly) method of solving the problem. Anyone is welcome to modify the script and file pull requests and I am more than happy to merge them. 

##License
The software is licensed under GPLv3 and hence is free software.
