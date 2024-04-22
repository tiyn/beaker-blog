import glob
import locale
import os
import pathlib
import urllib.parse
from datetime import datetime
from os import path

import markdown
from bs4 import BeautifulSoup
from gtts import gTTS, gTTSError

import config
import search

WEBSITE = config.WEBSITE
ENTRY_DIR = config.ENTRY_DIR
LANGUAGE = config.LANGUAGE
LOCAL = "de_DE.UTF-8" if LANGUAGE == "de-de" else "en_US.UTF-8"
TIMEZONE = config.TIMEZONE

locale.setlocale(locale.LC_TIME, LOCAL)


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
    contents = sorted(full_list, key=os.path.getmtime)
    content_string = ""
    last_month = ""
    for file in reversed(contents):
      curr_date = datetime.fromtimestamp(os.path.getmtime(file)).strftime("%Y-%m-%d")
      curr_month = datetime.fromtimestamp(os.path.getmtime(file)).strftime("%B %Y")
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
      content_string += "<a href=\"" + "/index.html#" + \
          filename + "\">" + curr_date + "</a> - "
      content_string += "<a href=\"" + "/entry/" + \
          pathlib.PurePath(file).name + "\"><b>" + title + "</b></a>"
      content_string += "<br>"
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
    contents = sorted(full_list, key=os.path.getmtime)
    for file in reversed(contents):
      filename = pathlib.PurePath(file)
      # purefile = filename
      title = open(filename).readline().rstrip("\n")
      text = open(filename).readlines()[1:]
      filename = filename.name
      if filename[0] != ".":
        filename = filename.split(".", 1)[0]
      content_string += "<div class=\"entry\">\n"
      content_string += "<h2 id=\"" + filename + "\">"
      content_string += "<a href=\"" + "/entry/" + \
          pathlib.PurePath(file).name + "\">" + \
          title + "</a>" +"</h2>\n"
      content_string += "<small>" + \
          datetime.fromtimestamp(os.path.getmtime(
              file)).strftime("%Y-%m-%d") + "</small><br><br>"
      if file.endswith(".html"):
        for line in text:
          content_string += line
      if file.endswith(".md"):
        content_string += gen_md_content(file, 2)
      content_string += "</div>"
      content_string = absolutize_html(content_string)
  return content_string


def absolutize_html(string):
  """
  Creates a html string from another string that only uses absolute links that use the full domain.

  Parameters:
  string: html-formatted string.

  Returns:
  string: html-formatted string with absolute linksn
  """
  soup = BeautifulSoup(string, "html.parser")
  for a_tag in soup.find_all("a"):
    href = str(a_tag.get("href"))
    if href.startswith("/") or href.startswith("."):
      a_tag["href"] = urllib.parse.urljoin(WEBSITE, href)
  for img_tag in soup.find_all("img"):
    src = str(img_tag.get("src"))
    if src.startswith("/") or src.startswith("."):
      img_tag["src"] = urllib.parse.urljoin(WEBSITE, src)
  return str(soup)


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
    curr_date = datetime.fromtimestamp(os.path.getmtime(filename)).strftime("%Y-%m-%d")
    filename_no_end = filename.split(".", 1)[0]
    filename_no_end = filename_no_end.split("/")[-1]
    content_string += "<h1>" + title + "</h1>\n"
    content_string += "<a href=\"" + "/index.html#" + \
        filename_no_end + "\">" + curr_date + "</a>"
    content_string += "<br><br>\n"
    if os.path.isfile("static/tmp/" + filename_no_end + ".mp3"):
      content_string += "<audio controls>\n"
      content_string += '<source src="/static/tmp/' + filename_no_end + '.mp3" type="audio/mp3">\n'
      content_string += "</audio>\n"
    content_string += "<br><br>\n"
    if filename.endswith(".html"):
      for line in text:
        content_string += line
    if filename.endswith(".md"):
      content_string += gen_md_content(filename, 1)
    content_string = absolutize_html(content_string)
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
    header = "#"
    for _ in range(depth):
      header += "#"
    header += " "
    markdown_lines = open(path_ex, "r").readlines()[1:]
    markdown_text = ""
    for line in markdown_lines:
      markdown_text += line.replace("# ", header)
    content_string = markdown.markdown(markdown_text, extensions=["fenced_code", "tables"])
  return content_string


def get_rss_string():
  """
  Create a rss-string of the blog and return it.

  Returns:
  string: rss-string of everything that is in the ENTRY_DIR.
  """
  path_ex = ENTRY_DIR
  content_string = ""
  if path.exists(path_ex):
    name_list = os.listdir(path_ex)
    full_list = [os.path.join(path_ex, i) for i in name_list]
    contents = sorted(full_list, key=os.path.getmtime)
    for file in reversed(contents):
      filename = pathlib.PurePath(file)
      title = open(filename).readline().rstrip("\n")
      text = open(filename).readlines()[1:]
      filename = filename.name
      if filename[0] != ".":
        filename = filename.split(".", 1)[0]
      content_string += "<item>\n"
      content_string += "<title>" + title + "</title>\n"
      content_string += "<guid>" + WEBSITE + \
          "/index.html#" + filename + "</guid>\n"
      locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
      content_string += "<pubDate>" + \
          datetime.fromtimestamp(os.path.getmtime(file)).strftime(
              "%a, %d %b %Y %H:%M:%S") + " " + TIMEZONE + "</pubDate>\n"
      locale.setlocale(locale.LC_TIME, LOCAL)
      content_string += "<description>\n<![CDATA[<html>\n<head>\n</head>\n<body>\n"
      html_string = ""
      for line in text:
        html_string += line
      content_string += absolutize_html(html_string)
      content_string += "\n</body></html>\n]]>\n</description>\n"
      content_string += "</item>\n"
  return content_string


def gen_query_res_string(query_str):
  """
  Return the results of a query.

  Parameters:
  query_str (string): term to search

  Returns:
  string: html-formated search result
  """
  src_results = search.search(query_str)
  res_string = ""
  for result in src_results:
    title = result["title"]
    path = result["path"]
    filename = pathlib.PurePath(path)
    filename = filename.name
    if filename[0] != ".":
      filename = filename.split(".", 1)[0]
    curr_date = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d")
    is_markdown = path.endswith(".md")
    preview = create_preview(path, is_markdown)
    path = "/entry/" + path.split("/", 2)[2]
    res_string += "<div class=\"entry\">"
    res_string += "<a href=\"" + path + "\"><h2>" + title + "</h2></a>"
    res_string += "<small>"
    res_string += "<a href=\"" + "/index.html#" + \
        filename + "\">" + curr_date + "</a>"
    res_string += "</small><br><br>"
    res_string += preview + "</div>"
  return res_string


def create_preview(path, is_markdown):
  """
  Create a preview of a given article and return it.

  Parameters:
  path (string): path to the article

  Returns:
  string: html-formated preview
  """
  file = open(path, "r", encoding="utf-8")
  lines = file.read()
  if is_markdown:
    lines += markdown.markdown(lines)
  preview = ""
  first_p = BeautifulSoup(lines).find('p')
  if first_p is not None:
    preview = "\n<p>" + first_p.text + "</p>\n"
  preview += "...<br>"
  return preview


def get_text_only(filename):
  """
  Convert a file to text only to use in tts

  Parameters:
  path (string): path to the article

  Returns:
  string: unformatted string containing the contents of the file
  """
  # filename = os.path.join(ENTRY_DIR, path)
  clean_text = ""
  if path.exists(filename):
    title = open(filename).readline().rstrip("\n")
    text = open(filename).readlines()[1:]
    filename_no_end = filename.split(".", 1)[0]
    filename_no_end = filename_no_end.split("/")[-1]
    content_string = ""
    if filename.endswith(".html"):
      for line in text:
        content_string += line
    if filename.endswith(".md"):
      content_string += gen_md_content(filename, 1)
    content_string = absolutize_html(content_string)
    soup = BeautifulSoup(content_string, "html.parser")
    tag_to_remove = soup.find("figure")
    if tag_to_remove:
      tag_to_remove.decompose()
    clean_text = soup.get_text(separator=" ")
    clean_text = title + "\n\n" + clean_text
  return clean_text


def prepare_tts():
  files = glob.glob('static/tmp/*')
  for f in files:
    os.remove(f)
  files = glob.glob('templates/entry/*')
  clean_text = ""
  for f in files:
    clean_text = get_text_only(f)
    _, tail = os.path.split(f)
    new_filename = "static/tmp/" + os.path.splitext(tail)[0] + ".mp3"
    try:
      tts = gTTS(clean_text, lang=LANGUAGE.split("-")[0])
      tts.save(new_filename)
    except gTTSError as e:
      print("Too many request to the google servers. Try it again later.")
      os.remove(new_filename)
      return e
