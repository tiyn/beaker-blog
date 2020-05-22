from flask import Flask, flash, make_response, render_template, request, redirect
import datetime
from datetime import datetime
import os
from os import path
import pathlib


app = Flask(__name__)

website = 'localhost:5000'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', title='Error 404', errorcode='404'), 404


@app.route('/')
@app.route('/index.html')
def index():
    content = gen_index_string()
    print('content is: ', content)
    return render_template('index.html', title='Blog', content_string=content)


@app.route('/archive')
@app.route('/archive.html')
def blog_archive():
    content = gen_arch_string()
    return render_template('archive.html', title='Blog Archive', content_string=content)


@app.route('/feed.xml')
@app.route('/rss.xml')
def feed():
    content = get_rss_string()
    rss_xml = render_template('rss.xml', content_string=content)
    response = make_response(rss_xml)
    response.headers['Content-Type'] = 'application/rss+xml'
    return response


def gen_arch_string():
    path_ex = 'templates/entry'
    if path.exists(path_ex):
        name_list = os.listdir(path_ex)
        full_list = [os.path.join(path_ex,i) for i in name_list]
        contents = sorted(full_list, key=os.path.getctime)
        content_string = ''
        for file in contents:
            filename = pathlib.PurePath(file)
            title = open(filename).readline().rstrip('\n')
            filename = filename.name
            if filename[0] != '.':
                filename = filename.split('.',1)[0]
            content_string += '<a href="' + '/index.html#' + filename + '">' + title + '</a><br>\n'
        return content_string

def gen_index_string():
    path_ex = 'templates/entry'
    content_string = ''
    if path.exists(path_ex):
        name_list = os.listdir(path_ex)
        full_list = [os.path.join(path_ex,i) for i in name_list]
        contents = sorted(full_list, key=os.path.getctime)
        for file in contents:
            filename = pathlib.PurePath(file)
            title = open(filename).readline().rstrip('\n')
            text = open(filename).readlines()[1:]
            filename = filename.name
            if filename[0] != '.':
                filename = filename.split('.',1)[0]
            content_string += '<div class=\'entry\'>\n'
            content_string += '<h2 id=\'' + filename + '\'>' + title + '</h2>\n'
            for line in text:
                content_string += line
            content_string += '<br><small>' + datetime.fromtimestamp(os.path.getctime(file)).strftime('%Y-%m-%d') + '</small>'
            content_string += '</div>'
    return content_string

def get_rss_string():
    path_ex = 'templates/entry'
    if path.exists(path_ex):
        name_list = os.listdir(path_ex)
        full_list = [os.path.join(path_ex,i) for i in name_list]
        contents = sorted(full_list, key=os.path.getctime)
        content_string = ''
        for file in contents:
            filename = pathlib.PurePath(file)
            title = open(filename).readline().rstrip('\n')
            text = open(filename).readlines()[1:]
            filename = filename.name
            if filename[0] != '.':
                filename = filename.split('.',1)[0]
            content_string += '<item>\n'
            content_string += '<title>' + title + '</title>\n'
            content_string += '<guid>' + '/index.html#' + filename + '</guid>\n'
            content_string += '<pubDate>' + datetime.fromtimestamp(os.path.getctime(file)).strftime('%Y-%m-%d') + '</pubDate>\n'
            content_string += '<description>'
            for line in text:
                content_string += line
            content_string += '</description>\n'
            content_string += '</item>\n'
    return content_string


if __name__ == '__main__':
    app.run(host='0.0.0.0')
