from flask import Flask, flash, make_response, render_template, request, redirect, abort

import content as con_gen
import config


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', title=config.TITLE, errorcode='404', style=config.STYLE), 404


@app.route('/')
@app.route('/index.html')
def index():
    content = con_gen.gen_index_string()
    return render_template('index.html', title=config.TITLE, content_string=content, style=config.STYLE)


@app.route('/archive')
@app.route('/archive.html')
def blog_archive():
    content = con_gen.gen_arch_string()
    return render_template('archive.html', title=config.TITLE, content_string=content, style=config.STYLE)


@app.route('/entry/<path>')
def entry(path):
    content = con_gen.gen_stand_string(path)
    if content != '':
        return render_template('standalone.html', title=config.TITLE, content_string=content, style=config.STYLE)
    abort(404)


@app.route('/feed.xml')
@app.route('/rss.xml')
def feed():
    content = con_gen.get_rss_string()
    rss_xml = render_template('rss.xml', content_string=content, title=config.TITLE,
                              description=config.DESCRIPTION, website=config.WEBSITE)
    response = make_response(rss_xml)
    response.headers['Content-Type'] = 'application/rss+xml'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
