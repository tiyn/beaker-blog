from flask import Flask, make_response, render_template, abort

import content as con_gen
import config


app = Flask(__name__)

TITLE = config.TITLE
STITLE = config.STITLE
STYLE = config.STYLE
LANGUAGE = config.LANGUAGE
DESCRIPTION = config.DESCRIPTION
WEBSITE = config.WEBSITE
MAIL = config.MAIL

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", title=STITLE, errorcode="404", style=STYLE, language=LANGUAGE), 404


@app.route("/")
@app.route("/index.html")
def index():
    content = con_gen.gen_index_string()
    return render_template("index.html", title=STITLE, content_string=content, style=STYLE, language=LANGUAGE)

@app.route("/imprint")
@app.route("/imprint.html")
def imprint():
    return render_template("imprint.html", title=STITLE, mail=MAIL, style=STYLE, language=LANGUAGE)

@app.route("/archive")
@app.route("/archive.html")
def archive():
    content = con_gen.gen_arch_string()
    return render_template("archive.html", title=STITLE, content_string=content, style=STYLE, language=LANGUAGE)


@app.route("/entry/<path>")
def entry(path):
    content = con_gen.gen_stand_string(path)
    if content != "":
        return render_template("standalone.html", title=STITLE, content_string=content, style=STYLE, language=LANGUAGE)
    abort(404)


@app.route("/feed.xml")
@app.route("/rss.xml")
def feed():
    content = con_gen.get_rss_string()
    rss_xml = render_template("rss.xml", content_string=content, title=TITLE,
                              description=DESCRIPTION, website=WEBSITE)
    response = make_response(rss_xml)
    response.headers["Content-Type"] = "application/rss+xml"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
