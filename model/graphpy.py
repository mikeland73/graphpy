from abc import ABCMeta
import functools
import hashlib
import json
import MySQLdb


class GPNode(object):
    __metaclass__ = ABCMeta

    db = None
    node_cache = {}
    node_data = {}
    node_type = None

    def __init__(self, **data):
        self.data = data
        self.id = data.get('id')

    def get_id(self):
        return self.id

    def get(self, name, default=None):
        return self.data.get(name, default)

    def getx(self, name, default=None):
        if name in self.node_data:
            return self.get(name, default)
        raise Exception

    def set(self, name, val):
        self.data[name] = val
        return self

    def setx(self, name, val):
        if name in self.node_data:
            return self.set(name, val)
        raise Exception

    def save(self):
        db = GPNode.get_db()
        if (self.id):
            q = ("""UPDATE node SET data = %s WHERE id = %s""",
                 (json.dumps(self.data), self.id, ))
        else:
            q = ("""INSERT INTO node (type, data) VALUES (%s, %s)""",
                 (self.get_type(), json.dumps(self.data), ))
        cur = db.cursor()
        cur.execute(*q)
        self.id = cur.lastrowid if not self.id else self.id
        db.commit()
        cur.close()
        GPNode.node_cache[self.id] = self
        return self

    def __getattr__(self, name):
        print name
        method = None
        if name[:4] == 'get_':
            method = lambda self: self.getx(name[4:])
        if name[:4] == 'set_':
            method = lambda self, val: self.setx(name[4:], val)
        if method:
            setattr(self.__class__, name, method)
            return functools.partial(method, self)
        raise AttributeError

    @classmethod
    def get_type(cls):
        if not cls.node_type:
            m = hashlib.md5()
            m.update(cls.get_storage_key())
            cls.node_type = int(m.hexdigest()[17:], 16)
        return cls.node_type

    @classmethod
    def get_storage_key(cls):
        return cls.__name__

    @staticmethod
    def get_db():
        if not GPNode.db:
            GPNode.db = MySQLdb.connect(host="localhost",
                                        user="root",
                                        passwd="",
                                        db="graphpy")
        return GPNode.db

    @classmethod
    def get_by_id(cls, id):
        if id not in cls.node_cache:
            db = GPNode.get_db()
            cur = db.cursor()
            cur.execute(
                """SELECT data FROM node WHERE id = %s AND type = %s""",
                (id, cls.get_type()))
            try:
                obj = cls(**json.loads(cur.fetchone()[0]))
                obj.id = id
                cls.node_cache[id] = obj
            except TypeError:
                pass
        result = cls.node_cache.get(id)
        return result if type(result) is cls else None
