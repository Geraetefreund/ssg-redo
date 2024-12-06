import unittest

from htmlnode import HTMLNode


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
        self.assertEqual((node.props), None)

if __name__ == "__main__":
    unittest.main()
