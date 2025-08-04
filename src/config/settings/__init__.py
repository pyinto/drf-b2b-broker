from enum import Enum
import sys
import os
from typing import Literal

from dotenv import load_dotenv

load_dotenv()


class SettingsEnv(str, Enum):
    DEV = "dev"
    PROD = "prod"
    TESTING = "testing"

    def __str__(self):
        return self.value


T_ENVS = Literal["dev", "prod", "testing"]
TESTING = "test" in sys.argv or "PYTEST_VERSION" in os.environ
if TESTING:
    os.environ["ENV"] = "testing"


ENV = os.environ.get("ENV", SettingsEnv.DEV)
match ENV:
    case SettingsEnv.DEV:
        from .dev import *  # noqa: F403
    case SettingsEnv.PROD:
        from .dev import *  # noqa: F403
    case SettingsEnv.TESTING:
        from .dev import *  # noqa: F403
    case _:
        raise Exception(f"Unknown 'ENV' value received! Got: '{ENV}'; choices: {[s.value for s in SettingsEnv]}.")
