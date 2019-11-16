import json
import os
import sys
from configparser import ConfigParser

from fbchat import Client, log
from fbchat.models import *

import display


def config(filename=sys.path[0] + '/config.ini', section='facebook credentials'):
    # create a parser 
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section
    creds = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            creds[param[0]] = param[1]
    elif os.environ['EMAIL']: 
        creds['email'] = os.environ['EMAIL']
        creds['password'] = os.environ['PASSWORD']
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))
    return creds


class CursedBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        super(CursedBot, self).onMessage(author_id, message_object, thread_id, thread_type, **kwargs)


def startupClient(email, password):
    try:
        with open("session.txt", "r") as session:
            session_cookies = json.loads(session.read())
    except FileNotFoundError:
        session_cookies = None

    client = CursedBot(email, password, session_cookies=session_cookies)
    with open("session.txt", "w") as session:
        session.write(json.dumps(client.getSession()))
    return client




### Reving up the engines ###
if __name__ == '__main__':
    creds = config()
    print(creds)
    client = startupClient(creds['email'], creds['password'])
    client.listen()
