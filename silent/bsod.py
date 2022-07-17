# A Python script to generate a BSOD.
# This script is based on the following article:
# https://stackoverflow.com/questions/11254763/is-there-a-way-in-windows-to-throw-a-bsod-on-demand-from-python
# https://www.geeksforgeeks.org/how-to-create-a-countdown-timer-using-python/
import os
import sys
import time

if os.name != 'nt':
    print("This script is only for Windows.")
    sys.exit(1)


def bsod():
    """Generate a BSOD."""
    from ctypes import POINTER, byref, c_int, c_uint, c_ulong, windll

    nullptr = POINTER(c_int)()

    windll.ntdll.RtlAdjustPrivilege(
        c_uint(19),
        c_uint(1),
        c_uint(0),
        byref(c_int())
    )

    windll.ntdll.NtRaiseHardError(
        c_ulong(0xC000007B),
        c_ulong(0),
        nullptr,
        nullptr,
        c_uint(6),
        byref(c_uint())
    )


def countdown(t):
    """Countdown timer."""
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1


if __name__ == '__main__':
    # Check arguments
    if len(sys.argv) != 2:
        print("Usage: python3 bsod.py <seconds>")
        sys.exit(1)
    try:
        # Ask for confirmation, comment out if you don't want to ask
        '''
        print("This will generate a BSOD in {} seconds.".format(sys.argv[1]))
        print("Press Ctrl+C to cancel.")
        confirmMsg = "Yes, I want to generate a BSOD."
        confirmInput = input("Type \""+confirmMsg +
                             "\" and press Enter to continue: ")
        if confirmInput != confirmMsg:
            print("Aborted.")
            sys.exit(1)
        '''

        # Get seconds absolute value
        seconds = abs(int(sys.argv[1]))

        # Countdown
        countdown(seconds)

        # Generate BSOD
        bsod()
        print("\nBSOD generated.")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(1)
