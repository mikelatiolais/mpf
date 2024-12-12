"""Contains the code for the bluetooth virtual switch platform

"""
import asyncio
import logging

from typing import Dict, List, Optional  # pylint: disable-msg=cyclic-import,unused-import

from mpf.core.utility_functions import Util
from mpf.platforms.interfaces.switch_platform_interface import SwitchPlatformInterface
