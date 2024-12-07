import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("a", "testlink", None, {"href": "https://www.google.com"})
        self.assertEqual(
            "HTMLNode(a, testlink, None, {'href': 'https://www.google.com'})", repr(node)
        )

    def test_props_to_html(self):
        node = HTMLNode("a", "testlink", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())

    def test_values(self):
        node = HTMLNode("div", "I wish I could read")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

class TestLeafNode(unittest.TestCase):
    def test_p_to_html(self):
        node = LeafNode('p', 'This is a paragraph of text.')
        self.assertEqual(node.to_html(), '<p>This is a paragraph of text.</p>')
        
    def test_a_to_html(self):
        node = LeafNode('a', 'Click me!', {"href": "https://www.google.com/"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com/">Click me!</a>')

    def test_leafnode_no_value(self):
        node = LeafNode('div', None)
        self.assertRaises(ValueError, node.to_html)

    def _test_leafnode_no_tag(self):
        node = LeafNode(None, "Some value", {"class": "beer_class"})
        self.assertEqual(node.to_html(), f'{node.value}')

if __name__ == "__main__":
    unittest.main()
