# cisco_mock_cli
Create a mock CLI based on your logs.  Obviously read only.

# Usage
1. Get your switch logs - make sure they're in a text format and not gzipped.
2. Run the script with your filename as the arg
3. Profit.

# Example

```
micheal.taylor@bubdev ~/Cisco/2016_10_18 $ ./cisco_mock_cli.py Switch-A.log

        +==========================================================================================================+
        | Welcome to the Cisco mock CLI!  If youre completely unfamiliar with the available commands, please type  |
        | list_commands for a list of all possible commands.  If you'd like to filter commands, type list_commands |
        | with the search string immediately after, e.g.:                                                          |
        |                                                                                                          |
        | This will show you a list of all commands:                                                               |
        | list_commands                                                                                            |
        |                                                                                                          |
        | This would show you all commands that have the string "show zoneset active" in them:                     |
        | list_commands show zoneset active                                                                        |
        |                                                                                                          |
        | The CLI commands are based on the logfile listed below:                                                  |
        | LOGFILE = Switch-A.log                                                                                   |
        ===========================================================================================================+


Switch-A$ show switchname
Switch-A

Switch-A$ help

For a list of available commands, please type "list_commands"

Switch-A$ exit
Exiting
```
