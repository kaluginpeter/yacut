import re
from string import ascii_letters, digits

ORIGINAL_LINK_LENGTH = 2048
SHORT_LENGTH = 16
VALID_SIMBOLS_RANGE = ascii_letters + digits
REGEX_SHORT_VALIDATION = f'^[{re.escape(VALID_SIMBOLS_RANGE)}]{{1,16}}$'
ATTEMPS_TO_COLLISION_COUNT = 100
SHORT_GENERATION_LENGTH = 6
REDIRECT_SHORT_FUNCTION_NAME = 'redirect_from_short'
