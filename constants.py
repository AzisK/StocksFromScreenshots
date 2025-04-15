import re

UPLOADED_SCREENSHOTS = "uploaded_screenshots"

# REGEX = r'(?P<action>Buy|Sell)\s+(?P<stock>[\w\d\.]{3,5})\s+(?P<price>[-+][$€][\d\s]+(,\s*\d{2})?)\s+(?P<shares>\d+,?\d*)\s+shares\s+-\s+(?P<share_price>[$€]\d+,\d{2})[\s\w):]+(?P<time>\d{2}:\d{2})'
# PATTERN = re.compile(r'(?P<action>Buy|Sell)\s+(?P<stock>[\w\d\.]{3,5})\s+(?P<price>[-+][$€][\d\s]+(,\s*\d{2})?)\s+(?P<shares>\d+,?\d*)\s+shares\s+-\s+(?P<share_price>[$€]\d+,\d{2})[\s\w):]+(?P<time>\d{2}:\d{2})', re.MULTILINE)
# Support for top up of Stocks account from the main one
REGEX = r'(?P<action>Buy|Sell|Main)[\s>]+(?P<stock>[\w\d\.]{3,5}|Stocks)\s+(?P<price>[-+][$€][\d\s]+(,\s*\d{2})?)(\s+(?P<shares>\d+,?\d*)\s+shares\s+[-+:]\s*(?P<share_price>[$€][\d\s]+[,.]\d{2}))?[\s\w):]+(?P<time>\d{2}:\d{2})'
PATTERN = re.compile(r'(?P<action>Buy|Sell|Main)[\s>]+(?P<stock>[\w\d\.]{3,5}|Stocks)\s+(?P<price>[-+][$€][\d\s]+(,\s*\d{2})?)(\s+(?P<shares>\d+,?\d*)\s+shares\s+[-+:]\s*(?P<share_price>[$€][\d\s]+[,.]\d{2}))?[\s\w):]+(?P<time>\d{2}:\d{2})', re.MULTILINE)

REGEX_GROUP = r'(?P<date>(\d{1,2}\s(January|February|March|April|May|June|July|August|September|October|November|December)(\s\d{4})?)|Yesterday)'
PATTERN_GROUP = re.compile(r'(?P<date>(\d{1,2}\s(January|February|March|April|May|June|July|August|September|October|November|December)(\s\d{4})?)|Yesterday)')

DB_PATH = "trades.duckdb"
