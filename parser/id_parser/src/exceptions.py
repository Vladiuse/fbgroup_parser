from common.exceptions import ParserError

class HtmlElementNotFound(ParserError):
    """Throw if html element not found"""

class MaxRowErrorCount(ParserError):
    """Throw if some error raise in row"""

class NoGroupsToParse(ParserError):
    """throw if no groups to parse"""
