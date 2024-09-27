from common.exceptions import ParserError

class EmptyPayload(ParserError):
    """Throw if fblib response have no payload data"""