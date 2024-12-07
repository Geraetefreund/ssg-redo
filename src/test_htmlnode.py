import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_leafnode_no_tag(self):
        node = LeafNode(None, "Some value", {"class": "beer_class"})
        self.assertEqual(node.to_html(), f'{node.value}')


class TestParentNode(unittest.TestCase):
    def test_repr(self):
        node = ParentNode("p", [LeafNode("b", "Bold Text inside a paragraph")])
        self.assertEqual("ParentNode(p, [LeafNode(b, Bold Text inside a paragraph, None)], None)", node.__repr__())

    def test_no_tag(self):
        node = ParentNode(None,[LeafNode("b", "Bold Text inside a paragraph")])
        #self.assertRaises(ValueError, node.to_html)
        with self.assertRaises(ValueError) as error:
            node.to_html()
        self.assertEqual(str(error.exception), "Invalid HTML: no tag")

    def test_no_children(self):
        node = ParentNode("a", [])
        with self.assertRaises(ValueError) as error:
            node.to_html()
        self.assertEqual(str(error.exception), "ParentNode needs children")


    def test_ParentNode_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_props(self):
        node = ParentNode("a", [LeafNode("b", "Bold text within a link")],
                          props={'href': 'https://boot.dev'})
        self.assertEqual(node.to_html(),
                         '<a href="https://boot.dev"><b>Bold text within a link</b></a>')


if __name__ == "__main__":
    unittest.main()
