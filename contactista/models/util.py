from sqlalchemy.util import OrderedDict
from sqlalchemy.orm.collections import MappedCollection
from werkzeug.datastructures import OrderedMultiDict


# http://docs.sqlalchemy.org/en/latest/orm/collections.html#custom-dictionary-based-collections
class CategoryMap(OrderedMultiDict, MappedCollection):
    """
    Holds objects keyed by the 'category' attribute
    with insert order maintained.
    """

    def __init__(self, *args, **kw):
        MappedCollection.__init__(self, keyfunc=lambda obj: obj.category)
        OrderedMultiDict.__init__(self, *args, **kw)
