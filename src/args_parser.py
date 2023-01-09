# -*- coding: utf-8 -*-
import argparse, sys, gettext

Args = [
    {
        'short_name': '-s',
        'long_name': '--session_name',
        'help': 'any name you want to give to your pyrogram.Client',
        'type': str
    },
    {
        'short_name': '-a',
        'long_name': '--author_id',
        'help': 'a userid classify to give to your pyrogram.Client',
        'type': int
    },
    {
        'short_name': '-m',
        'long_name': '--max_link',
        'help': 'max link for bots recording the stream',
        'type': int
    },
    {
        'short_name': '-t',
        'long_name': '--token',
        'help': 'if generating session is for a bot to pass bot_token',
        'type': str
    }
]

class ColoredArgumentParser(argparse.ArgumentParser):

    color_dict = {
        'RED' : '1;31',
        'GREEN' : '1;32',
        'YELLOW' : '1;33',
        'BLUE' : '1;36'
    }

    def print_usage(self, file = None):
        if file is None:
            file = sys.stdout
        self.msg(self.format_usage()[0].upper() + 
                            self.format_usage()[1:],
                            file, self.color_dict['YELLOW'])

    def print_help(self, file = None):
        if file is None:
            file = sys.stdout
        self.msg(
            self.format_help()[0].upper() + self.format_help()[1:],
            file,
            self.color_dict['BLUE']
        )

    def msg(self, message, file = None, color = None):
        if message:
            if file is None:
                file = sys.stderr
            if color is None:
                file.write(message)
            else:
                file.write('\x1b[' + color + 'm' + message.strip() + '\x1b[0m\n')

    def exit(self, status = 0, message = None):
        if message:
            self.msg(message, sys.stderr, self.color_dict['RED'])
        sys.exit(status)

    def error(self, message):
        self.print_usage(sys.stderr)
        args = {'prog' : self.prog, 'message': message}
        self.exit(2, gettext.gettext('%(prog)s: Error: %(message)s\n') % args)