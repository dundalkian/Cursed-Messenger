#!/usr/bin/env python3

import io
import os
import sys
import curses
import curses.ascii
import argparse
import re
import time

from fbchat import Client, log
from fbchat.models import *

import listener



class CursedMessengerDisplay():
    def __init__(self, fbclient):
        self.fbclient = fbclient
        self.search_string = ""
        curses.wrapper(self.update_loop)
    
    def insert_filtered_elements(self):
        self.typing_window.move(0,0)
        self.typing_window.clrtoeol()
        #self.typing_window.insstr(0, 0, f"Search string: {self.search_string}")
        self.typing_window.insstr(0, 0, "Search string")
        self.typing_window.refresh()

    def update_loop(self, stdscr):
        curses.curs_set(0)
        self.stdscr = stdscr
        self.chat_window = curses.newwin(9*int(curses.LINES/10), curses.COLS, 0, 0)
        self.typing_window = curses.newwin(int(curses.LINES/10), curses.COLS, 9*int(curses.LINES/10), 0)
        time.sleep(1)
        print("hello")
        self.insert_filtered_elements()
        while True:
            #self.chat_window.insstr(1, 0, f"Cols: {curses.COLS} Lines: {curses.LINES}")
            char = self.typing_window.getch()
            if curses.ascii.isprint(char):
                self.search_string += chr(char)
                self.insert_filtered_elements()
            # actual ascii values as follows: (8, 127, {system dependent})
            elif char in (curses.ascii.BS, curses.ascii.DEL, curses.KEY_BACKSPACE):
                self.search_string = self.search_string[:-1]
                self.insert_filtered_elements()
            elif char == curses.ascii.NL:
                self.fbclient.send(Message(text=self.search_string), thread_id='2813871368632313', thread_type=ThreadType.GROUP)

def main():
    try:
        #prev_stdin = os.dup(0)
        #prev_stdout = os.dup(1)
        #stdin = open("/dev/tty")
        #stdout = open("/dev/tty", "w")
        #os.dup2(stdin.fileno(), 0)
        #os.dup2(stdout.fileno(), 1)
        creds = listener.config()
        print(creds)
        fbclient = listener.startupClient(creds['email'], creds['password'])
        mpick = CursedMessengerDisplay(fbclient)
    finally:
        pass
        #os.dup2(prev_stdin, 0)
        #os.dup2(prev_stdout, 1)

if __name__ == '__main__':
    main()
