import sys
import os
import unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../model')
from graphpy import GPNode


class MyNode(GPNode):
    node_data = {
        'name': '',
        'last_name': '',
    }


class MyNode2(GPNode):
    pass


class TestNode(unittest.TestCase):

    def test_create_node(self):
        node = MyNode(id=123, name='Foo')
        node.get_name()

    def test_get_node_data(self):
        node = MyNode(id=123, name='Foo')
        self.assertEquals(node.get_id(), 123)
        self.assertEquals(node.get('name'), 'Foo')
        self.assertEquals(node.get('last_name'), None)
        self.assertEquals(node.get('bar'), None)

        self.assertEquals(node.getx('last_name'), None)
        self.assertEquals(node.getx('last_name', 'Doe'), 'Doe')
        with self.assertRaises(Exception):
            node.getx('bar')

    def test_set_node_data(self):
        node = MyNode()
        node.set('name', 'Mike').set('random', 123)
        self.assertEquals(node.get('name'), 'Mike')
        self.assertEquals(node.get('last_name'), None)
        self.assertEquals(node.get('random'), 123)

        node.setx('name', 'Other')
        with self.assertRaises(Exception):
            node.setx('random', '456')

    def test_magic_set(self):
        node = MyNode()
        node.set_name('Mike')
        with self.assertRaises(Exception):
            node.set_foo('Mike')

    def test_magic_get(self):
        node = MyNode(name='Mike')
        self.assertEquals(node.get_name(), 'Mike')
        self.assertEquals(node.get_name(), 'Mike')
        self.assertEquals(node.get_name(), 'Mike')
        self.assertEquals(node.get_last_name(), None)
        with self.assertRaises(Exception):
            node.get_foo()

    def test_save(self):
        node = MyNode(name='Mike')
        node.save().save()
        node_from_db = MyNode.get_by_id(node.get_id())
        self.assertEquals(node_from_db.get_name(), 'Mike')
        self.assertEquals(MyNode2.get_by_id(node.get_id()), None)
        GPNode.node_cache = {}
        node_from_db = MyNode.get_by_id(node.get_id())
        self.assertEquals(node_from_db.get_name(), 'Mike')
        self.assertEquals(MyNode2.get_by_id(node.get_id()), None)


if __name__ == '__main__':
    unittest.main()
