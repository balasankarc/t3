import sleekxmpp
import os


class SendMsgBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, recipient, msg):
        super(SendMsgBot, self).__init__(jid, password)
        self.recipient = recipient
        self.msg = msg
        self.add_event_handler('session_start', self.start)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.send_message(mto=self.recipient, mbody=self.msg)
        self.disconnect(wait=True)


def getcredential():
    credential = {}
    for ln in open(os.environ['HOME'] + '/.xsend').readlines():
        key, val = ln.strip().split('=', 1)
        credential[key.lower()] = val
    return credential


def sendmsg(recipient, msg):
    credential = getcredential()
    con = SendMsgBot(credential["jid"], credential["password"], recipient, msg)
    if con.connect():
        con.process(block=True)
