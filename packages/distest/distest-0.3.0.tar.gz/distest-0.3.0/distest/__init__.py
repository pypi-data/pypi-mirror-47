""" Distest is a small library designed to allow you to make discord bots to test other bots.

    This is the main file, and contains the code that is directly involved in running the bot
    and interacting with the command line, including the classes for bot types and the two interfaces.
"""

import argparse
import sys

from .bot import DiscordInteractiveInterface, DiscordCliInterface
from .collector import TestCollector


def run_dtest_bot(sysargs, test_collector: TestCollector, timeout=5):
    from distest.validate_discord_token import token_arg

    all_run_options = ["all"]
    for i in test_collector._tests:
        all_run_options.append(i.name)

    parser = argparse.ArgumentParser(
        description="A small library used to write automated unit tests for Discord bots. "
        "Has 2 modes, Interactive and CLI. "
        "If you include -c, the bot will expect to be used in CLI mode. "
        "See the github wiki for more info"
    )
    required = parser.add_argument_group("Always Required Arguments")
    required.add_argument(
        "bot_target",
        metavar="target_bot_user",
        type=str,
        nargs=1,
        help="The username of the target bot (not this bot). "
        "Remove the discriminant (#1234) so it is just the account's name.",
    )
    required.add_argument(
        "bot_token",
        metavar="tester_bot_token",
        type=token_arg,
        nargs=1,
        help="The bot token for the testing bot (this bot).",
    )
    cli_only = parser.add_argument_group("CLI Only")
    cli_only.add_argument(
        "--channel",
        "-c",
        metavar="channel",
        type=int,
        nargs=1,
        help="The channel ID that the tests should be occurring in (CLI) "
        "or the ID to send the awake message to (Interactive)",
        dest="channel",
    )
    run_stats_group = cli_only.add_mutually_exclusive_group()
    run_stats_group.add_argument(
        "--run",
        "-r",
        type=str,
        choices=all_run_options,
        help="Runs the bot in run mode, equivalent to ::run <option>. "
        "Options are listed, they are the tests declared in the bot and the three default options."
        "Required for the bot to be run in CLI mode, if using in Interactive mode, don't specify this",
    )
    run_stats_group.add_argument(
        "--stats",
        "-s",
        action="store_true",
        help="Runs the bot in stats mode, outputting the last runs stats. "
        "Equivalent to ::stats",
    )
    parser.add_argument(
        "--timeout",
        "-t",
        type=int,
        nargs=1,
        help="Changes the timeout (in seconds) on tests before they are assumed to have failed. "
        "Default is 5 sec.",
    )

    sysargs.pop(0)  # Pops off the first arg (the filename that is being run)
    clean_args = vars(parser.parse_args(sysargs))

    # Makes the changing of the timeout optional
    if clean_args.get("timeout") is not None:
        timeout = clean_args.get("timeout")[0]

    # Controls whether or not the bot is run in CLI mode based on the parameters present
    if clean_args["run"] is not None:
        # If --run is present, the bot should be in CLI mode
        print("In CLI mode")
        run_command_line_bot(
            clean_args.get("bot_target")[0],
            clean_args.get("bot_token")[0],
            clean_args.get("run"),
            clean_args.get("channel")[0],
            clean_args.get("stats"),
            test_collector,
            timeout,
        )
    else:
        print("Not in CLI mode")
        run_interactive_bot(
            clean_args.get("bot_target")[0],
            clean_args.get("bot_token")[0],
            test_collector,
            timeout,
        )


def run_interactive_bot(target_name, token, test_collector, timeout=5):
    bot = DiscordInteractiveInterface(target_name, test_collector)
    bot.run(token)  # Starts the bot


def run_command_line_bot(target, token, tests, channel_id, stats, collector, timeout):
    """ Start the bot in command-line mode. The program will exit 1 if any of the tests failed.

        :param str target: The display name of the bot we are testing.
        :param str token: The tester's token, used to log in.
        :param str tests: List of tests to run.
        :param int channel_id: The ID of the channel in which to run the tests.
        :param bool stats: Determines whether or not to display stats after run.
        :param TestCollector collector: The ``TestCollector`` that gathered our tests.
        :param int timeout: The amount of time to wait for responses before failing tests.
        :rtype: None
    """
    bot = DiscordCliInterface(target, collector, tests, channel_id, stats, timeout)
    failed = bot.run(token)  # returns True if a test failed
    sys.exit(1 if failed else 0)
