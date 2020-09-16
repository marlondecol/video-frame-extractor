from itertools import cycle

from os import name, system

from sys import stdin, stdout

from threading import current_thread

from time import sleep

from typing import Optional

from modules.formatter.formatter import Formatter as F

from modules.utils.constants import (DEFAULT_MARGIN_H as def_h,
                                     DEFAULT_MARGIN_V as def_v, ERASE_LINE)

from modules.utils.settings import MESSAGE_FORMATTER as message


def _l(string: str = '', left: int = def_h) -> str:
    """
    Format a string with a margin of `left` chars to the left.

    ---
    Arguments
    ---

        string (str, '')
    Some string to format.

        left (int, def_h)
    A number of chars for the left margin.

    ---
    Returns
    ---

        str
    The string with the margin.
    """

    # Return the formatted string.
    return _lt(string, left, 0)


def _lt(string: str = '', left: int = def_h, top: int = def_v) -> str:
    """
    Format a string with a margin of `left` characters to the left and `top`
    lines above.

    ---
    Arguments
    ---

        string (str, '')
    Some string to format.

        left (int, def_h)
    A number of chars for the left margin.

        top (int, def_v)
    A number of lines for the top margin.

    ---
    Returns
    ---

        str
    The string with the margins.
    """

    # Return the formatted string.
    return _ltb(string, left, top, 0)


def _ltb(string: str = '',
         left: int = def_h,
         top: int = def_v,
         bottom: int = def_v) -> str:
    """
    Format a string with a margin of `left` characters to the left, `top` lines
    above and `bottom` lines below.

    ---
    Arguments
    ---

        string (str, '')
    Some string to format.

        left (int, def_h)
    A number of chars for the left margin.

        top (int, def_v)
    A number of lines for the top margin.

        bottom (int, def_v)
    A number of lines for the bottom margin.

    ---
    Returns
    ---

        str
    The string with the margins.
    """

    # Set the margins.
    left = abs(int(left)) + len(str(string))
    top = '\n' * abs(int(top))
    bottom = '\n' * abs(int(bottom))

    # Return the formatted string.
    return '{top}{:>{left}}{bottom}'.format(str(string),
                                            left=left,
                                            top=top,
                                            bottom=bottom)


def clear() -> None:
    """
    Clean the terminal screen.
    """

    try:

        # Run the command corresponding to the current operating system.
        system('cls' if name == 'nt' else 'clear')

    # Ctrl+C pressed.
    except (EOFError, KeyboardInterrupt):
        pass


def ellipsis(string: str = '',
             formatter: F = None,
             max_points: int = 3,
             freq: float = 2.0) -> None:
    """
    Show a ellipsis feedback animation while a process is running.

    ---
    Arguments
    ---

        string (str, '')
    Some string to print before the ellipsis.

        formatter (Formatter, None)
    A Formatter for the final printed string.

        max_points (int, 3)
    Maximum number of points for the ellipsis.

        freq (float, 2.0)
    Frequency of the animation cycle.
    """

    # Get the current thread.
    thread = current_thread()

    # The threads start alive.
    thread.alive = True

    # If a Formatter was not provided,...
    if formatter is None:

        # ... instantiate a new one.
        formatter = F()

    # List the animation pieces.
    chars = ['.' * i for i in range(1, max_points + 1)]

    # The animation cycles through the elements of the pieces list.
    for char in cycle(chars):

        # If the thread has stopped,...
        if not thread.alive:

            # ... then stop the animation.
            break

        # Print the string followed by the current piece.
        stdout.write('\r{}{}'.format(formatter.erase(string + char),
                                     ERASE_LINE))
        stdout.flush()

        # Pause for a period.
        sleep(1 / freq)


def error(string: str) -> F:
    """
    Show a formatted error message.

    ---
    Arguments
    ---

        string (str)
    Some string for the error message.

    ---
    Returns
    ---

        Formatter
    The formatted string.
    """

    # Return the formatted string.
    return message.erase().red(string)


def flush_input() -> None:
    """
    Flush the input buffer.

    Taken from:
    https://rosettacode.org/wiki/Keyboard_input/Flush_the_keyboard_buffer#Python
    """

    try:

        # Try to flush with the module for Windows.
        import msvcrt

        while msvcrt.kbhit():
            msvcrt.getch()

    # If it is unable to import,...
    except ImportError:

        # ... try the module for Linux.
        import termios

        termios.tcflush(stdin, termios.TCIOFLUSH)


def header(margin: int = def_h, clear_screen: bool = True) -> str:
    """
    Return the app header string, with a margin around.

    ---
    Arguments
    ---

        margin (int, def_h)
    A number of chars for the margin, based on the left margin.

        clear_screen (bool, True)
    Set whether the header should be printed on a clean screen.

    ---
    Returns
    ---

        str
    The formatted header.
    """

    # Don't accept negative or odd margins.
    margin_h = abs(int(margin)) - int(margin) % 2

    # Vertical margins are half of the left margin.
    margin_v = margin_h / 2

    # Typography generated at:
    # http://patorjk.com/software/taag/#p=display&f=ANSI%20Shadow&t=VFEx
    #
    # There was an elongation of a line in the capital letters, only.
    lines = [
        '██╗   ██╗███████╗███████╗', '██║   ██║██╔════╝██╔════╝██╗  ██╗™',
        '██║   ██║█████╗  █████╗  ╚██╗██╔╝',
        '██║   ██║██╔══╝  ██╔══╝   ╚███╔╝', '╚██╗ ██╔╝██║     ██║      ██╔██╗',
        ' ╚████╔╝ ██║     ███████╗██╔╝ ██╗',
        '  ╚═══╝  ╚═╝     ╚══════╝╚═╝  ╚═╝', ''
    ]

    # Add the full app name.
    lines.append('{}\n\n'.format(F().background(
        None, ' {}ideo {}rame {}tractor ™ '.format(F().bold('V'),
                                                   F().bold('F'),
                                                   F().bold('Ex')))))

    # If the `clear_screen` flag is True,...
    if clear_screen:

        # ... clean the terminal screen before printing.
        clear()

    # Return the formatted joining of the lines list with a breakline.
    return _ltb('{:{margin}}'.format('\n', margin=margin_h + 1).join(lines),
                margin_h, margin_v, margin_v)


def humanize_duration(seconds: float, decimals: int = 3) -> str:
    """
    Convert time duration to human readable time string.

    ---
    Arguments
    ---

        seconds (float)
    Some time duration, in seconds, to convert.

    ---
    Returns
    ---

        str
    The human readable time string.
    """

    # Get hours.
    hours = int(seconds // 3600)
    seconds %= 3600

    # Get minutes.
    minutes = int(seconds // 60)
    seconds %= 60

    return '{:02d}:{:02d}:{:0{total_size}.{decimals}f}'.format(
        hours, minutes, seconds, total_size=decimals + 3, decimals=decimals)


def info(string: str) -> F:
    """
    Show a formatted information message.

    ---
    Arguments
    ---

        string (str)
    Some string for the information message.

    ---
    Returns
    ---

        Formatter
    The formatted string.
    """

    # Return the formatted string.
    return message.erase().blue(string)


def press_enter_to(action: str,
                   formatter: F = None,
                   enter_formatter: F = None,
                   wait: bool = True,
                   left: int = def_h) -> Optional[str]:
    """
    Show the message "Press [ENTER] to `action`...".

    ---
    Arguments
    ---

        action (str)
    Some action to use in the message.

        formatter (Formatter, None)
    A message Formatter.

        enter_formatter (Formatter, None)
    The "[ENTER]" string Formatter.

        wait (bool, True)
    Set whether the `input()` method should be used.

        left (int, def_h)
    A number of chars for the left margin.

    ---
    Returns
    ---

        Optional[str]
    The formatted message, if the `wait` flag is False.
    """

    # If a message formatter was not provided,...
    if formatter is None:

        # ... instantiate a new one.
        formatter = F()

    # If a "[ENTER]" string formatter was not provided,...
    if enter_formatter is None:

        # ... instantiate a new one.
        enter_formatter = F()

    # Save the output string in a variable.
    output = _lt(
        formatter.write('Press [').write(
            enter_formatter.write('ENTER')).write('] to ').write(F().write(
                str(action).lower())).write('...'), left)

    # If it should not wait,...
    if not wait:

        # ... just return the output string.
        return output

    try:

        # Flush some previous inputs.
        flush_input()

        # Wait for the user to press the ENTER key.
        input(output)

    # Ctrl+C pressed.
    except (EOFError, KeyboardInterrupt):
        print()

        pass


def success(string: str) -> F:
    """
    Show a formatted success message.

    ---
    Arguments
    ---

        string (str)
    Some string for the success message.

    ---
    Returns
    ---

        Formatter
    The formatted string.
    """

    # Return the formatted string.
    return message.erase().green(string)


def warning(string: str) -> F:
    """
    Show a formatted warning message.

    ---
    Arguments
    ---

        string (str)
    Some string for the warning message.

    ---
    Returns
    ---

        Formatter
    The formatted string.
    """

    # Return the formatted string.
    return message.erase().yellow(string)
