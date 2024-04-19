from flask import Flask, abort, make_response, render_template, request
from flask_font_awesome import FontAwesome

import config
import content as con_gen
from forms import SearchForm, register_csrf

TITLE = config.TITLE
STITLE = config.STITLE
STYLE = config.STYLE
LANGUAGE = config.LANGUAGE
DESCRIPTION = config.DESCRIPTION
WEBSITE = config.WEBSITE
MAIL = config.MAIL

app = Flask(__name__)
register_csrf(app)
font_awesome = FontAwesome(app)


@app.errorhandler(404)
def page_not_found(e):
  return render_template("error.html",
                         title=TITLE,
                         stitle=STITLE,
                         errorcode="404",
                         style=STYLE,
                         language=LANGUAGE), 404


@app.route("/")
@app.route("/index.html")
def index():
  content = con_gen.gen_index_string()
  return render_template("index.html",
                         title=TITLE,
                         stitle=STITLE,
                         content_string=content,
                         style=STYLE,
                         language=LANGUAGE)


@app.route("/search", methods=["GET", "POST"])
@app.route("/search.html", methods=["GET", "POST"])
def search():
  form = SearchForm()
  if request.method == "POST":
    query_str = request.form["query_str"]
    content = con_gen.gen_query_res_string(query_str)
    return render_template("search.html",
                           title=TITLE,
                           stitle=STITLE,
                           style=STYLE,
                           form=form,
                           content=content,
                           language=LANGUAGE), 200
  return render_template("search.html",
                         title=TITLE,
                         stitle=STITLE,
                         style=STYLE,
                         form=form,
                         content="",
                         language=LANGUAGE), 200


@app.route("/imprint")
@app.route("/imprint.html")
def imprint():
  return render_template("imprint.html",
                         title=TITLE,
                         stitle=STITLE,
                         mail=MAIL,
                         style=STYLE,
                         language=LANGUAGE)


@app.route("/archive")
@app.route("/archive.html")
def archive():
  content = con_gen.gen_arch_string()
  return render_template("archive.html",
                         title=TITLE,
                         stitle=STITLE,
                         content_string=content,
                         style=STYLE,
                         language=LANGUAGE)


@app.route("/entry/<path>")
def entry(path):
  content = con_gen.gen_stand_string(path)
  if content != "":
    return render_template("standalone.html",
                           title=TITLE,
                           stitle=STITLE,
                           content_string=content,
                           style=STYLE,
                           language=LANGUAGE)
  abort(404)


@app.route("/feed.xml")
@app.route("/rss.xml")
def feed():
  content = con_gen.get_rss_string()
  rss_xml = render_template("rss.xml",
                            content_string=content,
                            title=TITLE,
                            description=DESCRIPTION,
                            website=WEBSITE)
  response = make_response(rss_xml)
  response.headers["Content-Type"] = "application/rss+xml"
  return response


if __name__ == "__main__":
  app.run(host="0.0.0.0")
