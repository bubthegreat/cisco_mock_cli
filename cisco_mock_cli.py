#!/usr/bin/python
""" A simple mock CLI that will parse a cisco log file and let you view the results."""

import argparse
from collections import defaultdict


def cisco_mock_cli(logfile):
    """ Open the log file and loop command input until user exits."""
    with open(logfile, 'rt') as raw_log:
        command_dict = get_command_dict(raw_log)
        exit = False
        name = command_dict.get('show switchname')[0]
        while not exit:
            user_input = input("\n{}$ ".format(name))
            if user_input in ['quit', 'exit', 'q']:
                print('Exiting')
                break
            if user_input in ['help', '?', '-h', '--help']:
                print('\nFor a list of available commands, please type "list_commands"')
                continue
            elif "list_commands" in user_input.lower():
                search_string = ' '.join(user_input.split()[1:])
                if search_string:
                    filtered_commands = set()
                    for command in sorted(command_dict.keys()):
                        if search_string in command:
                            filtered_commands.add(command)
                    print("\nHere are commands with '{}' in them:\n".format(search_string))
                    for command in sorted(filtered_commands):
                        print(command)
                            
                else:
                    print("\nNo search string provided - showing all commands:\n")
                    for key in sorted(command_dict.keys()):
                        print(key)
                        continue
            else:
                command_results = command_dict.get(user_input)
                if not command_results:
                    print('\n\tCould not find that command.  For available commands please type "list_commands"')
                    
                    search_string = ' '.join(user_input.split()[1:])
                    if search_string:
                        filtered_commands = set()
                        for command in sorted(command_dict.keys()):
                            if search_string in command:
                                filtered_commands.add(command)
                        print("\n\tHere are commands with '{}' in them:\n".format(search_string))
                        for command in sorted(filtered_commands):
                            print(command)
                else:
                    for line in command_results:
                        print(line)


def get_command_dict(raw_log):
    """Get a dict of commands from the logfileself.
    Arguments:
        raw_log (FileObj): Cisco logfile to mock CLI fromself.
    Returns:
        command_dict (dict): Cisco commands for keys with list of command result lines for values.
    """
    command_dict = defaultdict(list)
    command = None
    for line in (raw_log):
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
    parser = argparse.ArgumentParser(description='Mock up the Cisco switch CLI for easier log navigation.')
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
