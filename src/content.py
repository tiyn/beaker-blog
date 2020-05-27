import datetime
from datetime import datetime
import markdown
import os
from os import path
import pathlib

WEBSITE = 'localhost:5000'

ENTRY_DIR = 'templates/entry'


def gen_arch_string():
    path_ex = ENTRY_DIR
    if path.exists(path_ex):
        name_list = os.listdir(path_ex)
        full_list = [os.path.join(path_ex, i) for i in name_list]
        contents = sorted(full_list, key=os.path.getctime)
        content_string = ''
        last_month = ''
        for file in reversed(contents):
            curr_date = datetime.fromtimestamp(
                os.path.getctime(file)).strftime('%Y-%m-%d')
            curr_month = datetime.fromtimestamp(
                os.path.getctime(file)).strftime('%b %Y')
            if curr_month != last_month:
                if last_month != '':
                    content_string += '</ul>\n'
                content_string += '<h2>' + curr_month + '</h2>\n'
                content_string += '<ul>\n'
                last_month = curr_month
            filename = pathlib.PurePath(file)
            title = open(filename).readline().rstrip('\n')
            filename = filename.name
            if filename[0] != '.':
                filename = filename.split('.', 1)[0]
            content_string += '<li>'
            content_string += curr_date + ' - '
            content_string += '<a href="' + '/index.html#' + \
                filename + '">' + title + '</a><br>'
            content_string += '</li>\n'
        content_string += '</ul>\n'
        return content_string


def gen_index_string():
    path_ex = ENTRY_DIR
    content_string = ''
    if path.exists(path_ex):
        name_list = os.listdir(path_ex)
        full_list = [os.path.join(path_ex, i) for i in name_list]
        contents = sorted(full_list, key=os.path.getctime)
        for file in reversed(contents):
            filename = pathlib.PurePath(file)
            purefile = filename
            title = open(filename).readline().rstrip('\n')
            text = open(filename).readlines()[1:]
            filename = filename.name
            if filename[0] != '.':
                filename = filename.split('.', 1)[0]
            content_string += '<div class=\'entry\'>\n'
            content_string += '<h2 id=\'' + filename + '\'>' + title + '</h2>\n'
            if file.endswith('.html'):
                for line in text:
                    content_string += line
                content_string += '<br>'
            if file.endswith('.md'):
                content_string += gen_md_content(file)
            content_string += '<small>' + \
                datetime.fromtimestamp(os.path.getctime(
                    file)).strftime('%Y-%m-%d') + '</small>'
            content_string += '</div>'
    return content_string


def gen_md_content(path_ex):
    content_string = ''
    if path.exists(path_ex):
        filename = path_ex.split('.', 1)
        fileend = filename[len(filename) - 1]
        markdown_file = open(path_ex, "r")
        depth = 2
        header = '#'
        for i in range(depth):
            header += '#'
        header += ' '
        markdown_text = markdown_file.read().replace('# ', header)
        content_string = markdown.markdown(
            markdown_text, extensions=["fenced_code", "tables"]
        )
    return content_string


def get_rss_string():
    path_ex = ENTRY_DIR
    if path.exists(path_ex):
        name_list = os.listdir(path_ex)
        full_list = [os.path.join(path_ex, i) for i in name_list]
        contents = sorted(full_list, key=os.path.getctime)
        content_string = ''
        for file in reversed(contents):
            filename = pathlib.PurePath(file)
            title = open(filename).readline().rstrip('\n')
            text = open(filename).readlines()[1:]
            filename = filename.name
            if filename[0] != '.':
                filename = filename.split('.', 1)[0]
            content_string += '<item>\n'
            content_string += '<title>' + title + '</title>\n'
            content_string += '<guid>' + '/index.html#' + filename + '</guid>\n'
            content_string += '<pubDate>' + \
                datetime.fromtimestamp(os.path.getctime(file)).strftime(
                    '%Y-%m-%d') + '</pubDate>\n'
            content_string += '<description>'
            for line in text:
                content_string += line
            content_string += '</description>\n'
            content_string += '</item>\n'
    return content_string
