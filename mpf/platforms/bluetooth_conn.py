"""Contains the code for the bluetooth virtual switch platform

   This functionality is useful for local communication with secondary controllers and other pinball machines.
   It presents 10 virtual switches

"""
import asyncio
import logging

from typing import Dict, List, Optional  # pylint: disable-msg=cyclic-import,unused-import

from mpf.core.utility_functions import Util
from mpf.platforms.interfaces.switch_platform_interface import SwitchPlatformInterface
