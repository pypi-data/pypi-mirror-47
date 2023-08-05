
class DjangoRESTQLError(Exception):
    """Base class for exceptions in this module."""


class InvalidField(DjangoRESTQLError, TypeError):
    """Invalid Field"""


class FieldNotFound(DjangoRESTQLError, KeyError):
    """Field Not Found"""


class FormatError(DjangoRESTQLError):
    """Query Format Error"""
