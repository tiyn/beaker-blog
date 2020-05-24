from flask import Flask, flash, make_response, render_template, request, redirect

import content as con_gen


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', title='Error 404', errorcode='404'), 404


@app.route('/')
@app.route('/index.html')
def index():
    content = con_gen.gen_index_string()
    return render_template('index.html', title='Blog', content_string=content)


@app.route('/archive')
@app.route('/archive.html')
def blog_archive():
    content = con_gen.gen_arch_string()
    return render_template('archive.html', title='Blog Archive', content_string=content)


@app.route('/feed.xml')
@app.route('/rss.xml')
def feed():
    content = con_gen.get_rss_string()
    rss_xml = render_template('rss.xml', content_string=content)
    response = make_response(rss_xml)
    response.headers['Content-Type'] = 'application/rss+xml'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
