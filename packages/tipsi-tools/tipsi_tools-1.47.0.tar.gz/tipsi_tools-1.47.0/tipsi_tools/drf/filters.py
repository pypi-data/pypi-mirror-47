import logging
from functools import reduce

import django_filters
from django.db.models import Q


class EnumFilter(django_filters.CharFilter):
    def __init__(self, enum, *args, **kwargs):
        self._enum = enum
        super().__init__(*args, **kwargs)

    def filter(self, qs, name):
        # In django filters 2.0 `name` is renamed to `field_name`
        self_name = getattr(self, 'name', None) or getattr(self, 'field_name')
        try:
            q_objects = []
            if isinstance(name, str):
                names = name.split(',')
                for n in names:
                    if hasattr(self._enum, n):
                        value = getattr(self._enum, n)
                        q = Q(**{'{}__exact'.format(self_name): value})
                        q_objects.append(q)
                    elif n == 'null':
                        q_objects.append(Q(**{'{}__isnull'.format(self_name): True}))
            elif name is None:
                q_objects.append(Q(**{'{}__isnull'.format(self_name): True}))
            else:
                raise AttributeError
            if q_objects:
                return self.get_method(qs)(reduce(lambda q1, q2: q1 | q2, q_objects))
            else:
                return qs

        except Exception:
            logging.exception('Failed to convert value: {} {}'.format(self_name, name))
            return super(EnumFilter, self).filter(qs, None)
