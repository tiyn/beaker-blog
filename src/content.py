from datetime import datetime
import markdown
import os
from os import path
import pathlib

import config

ENTRY_DIR = "templates/entry"

def gen_arch_string():
    """
    Creates and returns a archive string of every file in ENTRY_DIR.

    Returns:
    string: html-formatted archive-string
    """
    path_ex = ENTRY_DIR
    if path.exists(path_ex):
        name_list = os.listdir(path_ex)
        full_list = [os.path.join(path_ex, i) for i in name_list]
        contents = sorted(full_list, key=os.path.getctime)
        content_string = ""
        last_month = ""
        for file in reversed(contents):
            curr_date = datetime.fromtimestamp(
                os.path.getctime(file)).strftime("%Y-%m-%d")
            curr_month = datetime.fromtimestamp(
                os.path.getctime(file)).strftime("%b %Y")
            if curr_month != last_month:
                if last_month != "":
                    content_string += "</ul>\n"
                content_string += "<h2>" + curr_month + "</h2>\n"
                content_string += "<ul>\n"
                last_month = curr_month
            filename = pathlib.PurePath(file)
            title = open(filename).readline().rstrip("\n")
            filename = filename.name
            if filename[0] != ".":
                filename = filename.split(".", 1)[0]
            content_string += "<li>"
            content_string += curr_date + " - "
            content_string += title + " ["
            content_string += "<a href=\"" + "/index.html#" + \
                filename + "\">" + "link" + "</a> - "
            content_string += "<a href=\"" + "/entry/" + \
                pathlib.PurePath(file).name + "\">" + "standalone" + "</a>"
            content_string += "] <br>"
            content_string += "</li>\n"
        content_string += "</ul>\n"
        return content_string


def gen_index_string():
    """
    Create and returns a string including every file in the ENTRY_DIR as an index.

    Returns:
    string: html-formatted index string
    """
    path_ex = ENTRY_DIR
    content_string = ""
    if path.exists(path_ex):
        name_list = os.listdir(path_ex)
        full_list = [os.path.join(path_ex, i) for i in name_list]
        contents = sorted(full_list, key=os.path.getctime)
        for file in reversed(contents):
            filename = pathlib.PurePath(file)
            purefile = filename
            title = open(filename).readline().rstrip("\n")
            text = open(filename).readlines()[1:]
            filename = filename.name
            if filename[0] != ".":
                filename = filename.split(".", 1)[0]
            content_string += "<div class=\"entry\">\n"
            content_string += "<h2 id=\"" + filename + "\">" + title + "</h2>\n"
            content_string += "[<a href=\"" + "/entry/" + \
                pathlib.PurePath(file).name + "\">" + \
                "standalone" + "</a>]<br>\n"
            if file.endswith(".html"):
                for line in text:
                    content_string += line
                content_string += "<br>"
            if file.endswith(".md"):
                content_string += gen_md_content(file, 2)
            content_string += "<small>" + \
                datetime.fromtimestamp(os.path.getctime(
                    file)).strftime("%Y-%m-%d") + "</small>"
            content_string += "</div>"
    return content_string


def gen_stand_string(path_ex):
    """
    Creates a html-string for a file.
    If the file is markdown it will convert it.
    This functions ensures upscaling for future formats.

    Parameters:
    path_ex: path to a file.

    Returns:
    string: html-formatted string string equivalent to the file
    """
    filename = os.path.join(ENTRY_DIR, path_ex)
    content_string = ""
    if path.exists(filename):
        title = open(filename).readline().rstrip("\n")
        text = open(filename).readlines()[1:]
        filename_no_end = filename.split(".", 1)[0]
        filename_no_end = filename_no_end.split("/")[-1]
        content_string += "<h1>" + title + "</h1>\n"
        content_string += "["
        content_string += "<a href=\"" + "/index.html#" + \
            filename_no_end + "\">" + "link" + "</a>"
        content_string += "]<br>\n"
        if filename.endswith(".html"):
            for line in text:
                content_string += line
            content_string += "<br>"
        if filename.endswith(".md"):
            content_string += gen_md_content(filename, 1)
    return content_string


def gen_md_content(path_ex, depth):
    """
    Convert a markdown file to a html string.

    Parameters:
    path_ex (string): path to the markdown file
    depth (int): starting depth for markdown headings

    Returns:
    string: html-formatted string string equivalent to the markdown file
    """
    content_string = ""
    if path.exists(path_ex):
        filename = path_ex.split(".", 1)
        fileend = filename[len(filename) - 1]
        header = "#"
        for i in range(depth):
            header += "#"
        header += " "
        markdown_lines = open(path_ex, "r").readlines()[1:]
        markdown_text = ""
        for line in markdown_lines:
            markdown_text += line.replace("# ", header)
        content_string = markdown.markdown(
            markdown_text, extensions=["fenced_code", "tables"]
        )
    return content_string


def get_rss_string():
    """
    Create a rss-string of the blog and return it.

    Returns:
    string: rss-string of everything that is in the ENTRY_DIR.
    """
    path_ex = ENTRY_DIR
    if path.exists(path_ex):
        name_list = os.listdir(path_ex)
        full_list = [os.path.join(path_ex, i) for i in name_list]
        contents = sorted(full_list, key=os.path.getctime)
        content_string = ""
        for file in reversed(contents):
            filename = pathlib.PurePath(file)
            title = open(filename).readline().rstrip("\n")
            text = open(filename).readlines()[1:]
            filename = filename.name
            if filename[0] != ".":
                filename = filename.split(".", 1)[0]
            content_string += "<item>\n"
            content_string += "<title>" + title + "</title>\n"
            content_string += "<guid>" + config.WEBSITE + \
                "/index.html#" + filename + "</guid>\n"
            content_string += "<pubDate>" + \
                datetime.fromtimestamp(os.path.getctime(file)).strftime(
                    "%Y-%m-%d") + "</pubDate>\n"
            content_string += "<description>"
            for line in text:
                content_string += line
            content_string += "</description>\n"
            content_string += "</item>\n"
    return content_string
