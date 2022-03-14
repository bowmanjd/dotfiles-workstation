#!/usr/bin/env python
"""Interactions with libinput touchpad."""
import json
import subprocess  # noqa: S404


def dwt_enabled() -> bool:
    """Test if touchpad disable-when-typing is enabled.

    Returns:
        True if dwt is enabled
    """
    raw_inputs = subprocess.check_output(  # noqa: S603
        ["/usr/bin/swaymsg", "-r", "-t", "get_inputs"], text=True
    )
    inputs = json.loads(raw_inputs)
    touchpad = next(i for i in inputs if i["type"] == "touchpad")
    return touchpad["libinput"]["dwt"] == "enabled"


def dwt_toggle() -> bool:
    """Toggle touchpad disable-when-typing.

    Returns:
        True if dwt is enabled
    """
    enabled = dwt_enabled()
    if enabled:
        flag = "disable"
    else:
        flag = "enable"
    subprocess.check_output(  # noqa: S603
        ["/usr/bin/swaymsg", "input", "type:touchpad", "dwt", flag], text=True
    )
    return not enabled


def waybar() -> str:
    """Output custom icon for waybar.

    Returns:
        relevant icon
    """
    enabled = dwt_enabled()
    if enabled:
        output = ""
    else:
        output = "ﳶ"
    return output


def run() -> None:
    """Command runner."""
    import sys
    if sys.argv[1] == 'waybar':
        print(waybar())
    elif sys.argv[1] == 'status':
        print(dwt_enabled())
    elif sys.argv[1] == 'toggle':
        print(dwt_toggle())


if __name__ == "__main__":
    run()
