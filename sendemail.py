import smtplib
import os


def getcredential():
    credential = {}
    for ln in open(os.environ['HOME'] + '/.xemail').readlines():
        key, val = ln.strip().split('=', 1)
        credential[key.lower()] = val
    return credential


def sendmail(toaddrs, subject, text):
    credential = getcredential()
    msg = "\r\n".join([
                      "From: " + credential['username'],
                      "To: " + toaddrs,
                      "Subject: " + subject,
                      "",
                      text
                      ])
    username = credential['username']
    password = credential['password']
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(credential['username'], toaddrs, msg)
    server.quit()
