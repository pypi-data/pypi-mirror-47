#
# This file is part of pyasn1 software.
#
# Copyright (c) 2005-2019, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/pyasn1/license.html
#


class PyAsn1Error(Exception):
    """Create pyasn1 exception object

    The `PyAsn1Error` exception represents generic, usually fatal, error.
    """


class PyAsn1StringError(PyAsn1Error, UnicodeError):
    """Create pyasn1 exception object

    The `PyAsn1StringError` exception is a base class for errors relating to
    string encoding/decoding and other related problems
    """
    def __init__(self, message, unicode_error=None):
        if isinstance(unicode_error, UnicodeError):
            UnicodeError.__init__(self, *unicode_error.args)
        PyAsn1Error.__init__(self, message)


class PyAsn1StringDecodeError(PyAsn1StringError, UnicodeDecodeError):
    """Create pyasn1 exception object

    The `PyAsn1StringDecodeError` exception represents a failure to decode
    underlying bytes values to a string
    """


class PyAsn1StringEncodeError(PyAsn1StringError, UnicodeEncodeError):
    """Create pyasn1 exception object

    The `PyAsn1StringEncodeError` exception represents a failure to encode
    underlying string value as bytes
    """


class ValueConstraintError(PyAsn1Error):
    """Create pyasn1 exception object

    The `ValueConstraintError` exception indicates an ASN.1 value
    constraint violation.
    """


class SubstrateUnderrunError(PyAsn1Error):
    """Create pyasn1 exception object

    The `SubstrateUnderrunError` exception indicates insufficient serialised
    data on input of a de-serialization routine.
    """
