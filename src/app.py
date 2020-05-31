from flask import Flask, flash, make_response, render_template, request, redirect, abort

import content as con_gen
import config


app = Flask(__name__)

TITLE = config.TITLE
STYLE = config.STYLE
DESCRIPTION = config.DESCRIPTION
WEBSITE = config.WEBSITE

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', title=TITLE, errorcode='404', style=STYLE), 404


@app.route('/')
@app.route('/index.html')
def index():
    content = con_gen.gen_index_string()
    return render_template('index.html', title=TITLE, content_string=content, style=STYLE)


@app.route('/archive')
@app.route('/archive.html')
def blog_archive():
    content = con_gen.gen_arch_string()
    return render_template('archive.html', title=TITLE, content_string=content, style=STYLE)


@app.route('/entry/<path>')
def entry(path):
    content = con_gen.gen_stand_string(path)
    if content != '':
        return render_template('standalone.html', title=TITLE, content_string=content, style=STYLE)
    abort(404)


@app.route('/feed.xml')
@app.route('/rss.xml')
def feed():
    content = con_gen.get_rss_string()
    rss_xml = render_template('rss.xml', content_string=content, title=TITLE,
                              description=DESCRIPTION, website=WEBSITE)
    response = make_response(rss_xml)
    response.headers['Content-Type'] = 'application/rss+xml'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
