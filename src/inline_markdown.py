from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result_list.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError('Invalid markdown, formatted section not closed')
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        result_list.extend(split_nodes)
    return result_list

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    result_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result_list.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            result_list.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2 :
                raise ValueError("Invalid markdown, image section not closed.")
            if sections[0] != "":
                result_list.append(TextNode(sections[0], TextType.TEXT))
            original_text = sections[1]
            if original_text != "":
                result_list.append(TextNode(original_text, TextType.TEXT))
            result_list.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
        if original_text != "":
            result_list.append(TextNode(original_text, TextType.TEXT))
    return result_list


def split_nodes_link(old_nodes):
    result_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result_list.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            result_list.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed.")
            if sections[0] != "":
                result_list.append(TextNode(sections[0], TextType.TEXT))
            result_list.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
            if original_text != "":
                result_list.append(TextNode(original_text, TextType.TEXT))
    return result_list
