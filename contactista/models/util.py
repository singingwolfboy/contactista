from sqlalchemy.util import OrderedDict
from sqlalchemy.orm.collections import MappedCollection


# http://docs.sqlalchemy.org/en/latest/orm/collections.html#custom-dictionary-based-collections
class CategoryMap(OrderedDict, MappedCollection):
    """
    Holds objects keyed by the 'category' attribute
    with insert order maintained.
    """

    def __init__(self, *args, **kw):
        MappedCollection.__init__(self, keyfunc=lambda obj: obj.category)
        OrderedDict.__init__(self, *args, **kw)
