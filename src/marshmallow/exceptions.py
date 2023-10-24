# -*- coding: utf-8 -*-
"""Exception classes for marshmallow-related errors."""
import warnings

from marshmallow.compat import basestring
from marshmallow.warnings import ChangedInMarshmallow3Warning
from marshmallow.warnings import RemovedInMarshmallow3Warning


class MarshmallowError(Exception):
    """Base class for all marshmallow-related errors."""
    pass


class ValidationError(MarshmallowError):
    """Raised when validation fails on a field. Validators and custom fields should
    raise this exception.

    :param message: An error message, list of error messages, or dict of
        error messages.
    :param list field_names: Field names to store the error on.
        If `None`, the error is stored in its default location.
    :param list fields: `Field` objects to which the error applies.
    """

    def __init__(self, message, field_name=None, field_names=None, fields=None, data=None, **kwargs):
        if fields is None and field_names is not None:
            warnings.warn(
                'Parameter field_names is deprecated. Use field_name in marshmallow 3.', ChangedInMarshmallow3Warning
            )
        if field_name is not None and not isinstance(field_name, str):
            warnings.warn('Parameter field_name must be a string in marshmallow 3.', ChangedInMarshmallow3Warning)

        if not isinstance(message, dict) and not isinstance(message, list):
            messages = [message]
        else:
            messages = message
        #: String, list, or dictionary of error messages.
        #: If a `dict`, the keys will be field names and the values will be lists of
        #: messages.
        self.messages = messages
        #: List of field objects which failed validation.
        self._fields = fields
        if isinstance(field_name, basestring):
            #: List of field_names which failed validation.
            self.field_names = [field_name]
        elif isinstance(field_names, basestring):
            #: List of field_names which failed validation.
            self.field_names = [field_names]
        else:  # fields is a list or None
            self.field_names = field_names or []
        # Store nested data
        self._data = data
        self.valid_data = data
        self.kwargs = kwargs
        MarshmallowError.__init__(self, message)

    @property
    def data(self):
        warnings.warn(
            'Property valid_data should be used instead of data on ValidationError in marshmallow 3.',
            ChangedInMarshmallow3Warning,
        )
        return self._data

    @property
    def fields(self):
        warnings.warn(
            'ValidationError no longer stores a list of Field instances associated with the validation errors.',
            RemovedInMarshmallow3Warning,
        )
        return self._fields

    def normalized_messages(self, no_field_name="_schema"):
        if isinstance(self.messages, dict):
            return self.messages
        if len(self.field_names) == 0:
            return {no_field_name: self.messages}
        return dict((name, self.messages) for name in self.field_names)

class RegistryError(NameError):
    """Raised when an invalid operation is performed on the serializer
    class registry.
    """
    pass
