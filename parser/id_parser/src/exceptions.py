class ParserError(Exception):
    """Common parser exception"""

class HtmlElementNotFound(ParserError):
    """Throw if html element not found"""


class MaxRowErrorCount(ParserError):
    """Throw if some error raise in row"""


class NoGroupsToParse(ParserError):
    """throw if no groups to parse"""
