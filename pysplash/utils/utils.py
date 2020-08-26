import os
import sys
from contextlib import contextmanager
import tempfile
import warnings


@contextmanager
def stdchannel_redirected(print_warnings=False, stdchannel=sys.stdout):
    """
    Redirect stdout from Fortran code into a temporary file, so to not clutter
    the terminal with unnecessary print statements.
    """

    # Create a temporary file to store stdout from Fortran code
    dest_file = tempfile.NamedTemporaryFile(mode='w')

    try:
        oldstdchannel = os.dup(stdchannel.fileno())

        # Redirect stdchannel messages into our temporary file
        os.dup2(dest_file.fileno(), stdchannel.fileno())

        # Allow Fortran code to run
        yield

    finally:
        if oldstdchannel is not None:
            os.dup2(oldstdchannel, stdchannel.fileno())
        if dest_file is not None:
            with open(dest_file.name, 'r') as f:
                # Check the output for errors
                stdchannel_check_errors(f, print_warnings=print_warnings)
            dest_file.close()


def stdchannel_check_errors(fileobject, print_warnings=False):
    """ Simple function to check a fileobject in read mode for any warnings or
    errors.
    """

    lines = fileobject.readlines()
    warning_messages = []
    error_messages = []
    for line in lines:
        if 'warning' in line.lower():
            warning_messages.append(line)
        elif 'error' in line.lower():
            error_messages.append(line)

    if len(warning_messages) > 0 and print_warnings:
        warnings.warn("The following warnings were encountered in SPLASH", RuntimeWarning)
        for warning in warning_messages:
            print(warning.strip())

    if len(error_messages) > 0:
        for error in error_messages:
            print(error.strip())
        raise RuntimeError("Errors encountered in SPLASH")
