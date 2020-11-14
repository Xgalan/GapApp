import operator
import collections
import datetime
import uuid


class ValuesMixin(object):
    """ Mixin to a model class to return a namedtuple from an object instance. """

    @property
    def as_values(self, attrgetter=operator.attrgetter, namedtuple=collections.namedtuple,
                  methodcaller=operator.methodcaller):

        def get_attribute(attr):
            a = getattr(self, attr)
            isoformat = methodcaller('isoformat')
            if isinstance(a, str):
                return a
            if isinstance(a, datetime.datetime):
                return isoformat(a)
            if isinstance(a, datetime.date):
                return isoformat(a)
            if isinstance(a, uuid.UUID):
                return a.hex
            return a

        if not hasattr(self, "_as_values"):
            Fields = namedtuple('Fields', [f.name for f in tuple(
                f for f in self._meta.get_fields() if not f.is_relation)])
            self._as_values = Fields._make(map(get_attribute, Fields._fields))
        return self._as_values
