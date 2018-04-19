#!/usr/bin/python
""" A simple mock CLI that will parse a cisco log file and let you view the results."""

from __future__ import print_function

import argparse
from collections import defaultdict

# So we're python2/3 compatible, we'll make sure we're using the input that works:
try:
   input = raw_input
except NameError:
   pass


def cisco_mock_cli(logfile):
    """ Open the log file and loop command input until user exits."""
    with open(logfile, 'rt') as raw_log:
        command_dict = get_command_dict(raw_log)
        exit_cmd = False
        name = command_dict.get('show switchname')[0]
        if not name:
            print("Count not parse switchname.  Please check that the logs are formatted properly.")
            exit_cmd = True
        while not exit_cmd:
            # Get user input
            user_input = input("\n{}$ ".format(name))
            # Exit on these commands:
            if user_input in ['quit', 'exit', 'q']:
                print('Exiting')
                exit_cmd = True
                break
            # If someone didn't read the intro and types one of these, it'll give the big
            # help text we've got...
            if user_input in ['help', '?', '-h', '--help']:
                print('\nFor a list of available commands, please type "list_commands"')
                continue
            # if we type list_commands, either filter, or print them all.
            elif "list_commands" in user_input.lower():
                search_string = ' '.join(user_input.split()[1:])
                if search_string:
                    filtered_commands = filter_commands(command_dict, search_string)
                    print("\nHere are commands with '{}' in them:\n".format(search_string))
                    for command in sorted(filtered_commands):
                        print(command)
                else:
                    print("\nNo search string provided - showing all commands:\n")
                    for key in sorted(command_dict.keys()):
                        print(key)
                        continue
            # If it's not one of the above, we're trying to get a command.
            else:
                command_results = command_dict.get(user_input)
                # If we don't have any command key for that user input, filter and print out ones
                # that have that in it, or tell them we don't have any commands with that.
                if not command_results:
                    filtered_commands = filter_commands(command_dict, user_input)
                    print('\nERROR: Could not find that command. Type "help" for help.')
                    if filtered_commands:
                        print("\nDid you mean...\n")
                        for command in sorted(filtered_commands):
                            print(command)
                # If we have the command results, print them.
                else:
                    for line in command_results:
                        print(line)


def filter_commands(command_dict, search_string):
    """Filter command_Dict based on search_string."""
    if search_string:
        filtered_commands = set()
        for command in sorted(command_dict.keys()):
            if search_string in command:
                filtered_commands.add(command)
    return sorted(filtered_commands)


def get_command_dict(raw_log):
    """Get a dict of commands from the logfileself.
    Arguments:
        raw_log (FileObj): Cisco logfile to mock CLI fromself.
    Returns:
        command_dict (dict): Cisco commands for keys with list of command result lines for values.
    """
    command_dict = defaultdict(list)
    command = None
    for line in raw_log:
        if "`show" in line:
            # Some lines may have output from a previous line that doesn't have a newline
            # character, so we split on our command start/end backtick, and take the second
            # element - that should be our command.
            command = line.strip().split('`')[1]
            continue
        if command:
            command_dict[command].append(line.strip())
    return command_dict


def main():
    """Get filename and run CLI parser."""
    parser = argparse.ArgumentParser(description='Mock up the Cisco switch CLI for log navigation.')
    parser.add_argument('filepath', help='File path of the Cisco log file.')
    args = parser.parse_args()
    message = """
\t+==========================================================================================================+
\t| Welcome to the Cisco mock CLI!  If youre completely unfamiliar with the available commands, please type  |
\t| list_commands for a list of all possible commands.  If you'd like to filter commands, type list_commands |
\t| with the search string immediately after, e.g.:                                                          |
\t|                                                                                                          |
\t| This will show you a list of all commands:                                                               |
\t| list_commands                                                                                            |
\t|                                                                                                          |
\t| This would show you all commands that have the string "show zoneset active" in them:                     |
\t| list_commands show zoneset active                                                                        |
\t|                                                                                                          |
\t| The CLI commands are based on the logfile listed below:                                                  |
\t| LOGFILE = {}                                                                                             |
\t===========================================================================================================+
""".format(args.filepath)
    print(message)
    cisco_mock_cli(args.filepath)


if __name__ == '__main__':
    main()
