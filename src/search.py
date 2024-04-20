import os

from whoosh import scoring
from whoosh.fields import ID, TEXT, Schema
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser

import config

INDEX_DIR = "indexdir"
DEF_TOPN = 10
ENTRY_DIR = config.ENTRY_DIR


def createSearchableData(root):
  """
  Schema definition: title(name of file), path(as ID), content(indexed but not stored), textdata (stored text content)
  source:
  https://appliedmachinelearning.blog/2018/07/31/developing-a-fast-indexing-and-full-text-search-engine-with-whoosh-a-pure-pythhon-library/
  """
  schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
  if not os.path.exists(INDEX_DIR):
    os.mkdir(INDEX_DIR)
  ix = create_in(INDEX_DIR, schema)
  writer = ix.writer()
  for r, _, f in os.walk(root):
    for file in f:
      path = os.path.join(r, file)
      fp = open(path, encoding="utf-8")
      title = fp.readline()
      text = title + fp.read()
      writer.add_document(title=title, path=path, content=text)
      fp.close()
  writer.commit()


def search_times(query_str, topN):
  """
  Search for a given term and returns a specific amount of results.

  Parameters:
  query_str (string): term to search for
  topN (int): number of results to return

  Returns:
  string: html-formatted string including the hits of the search
  """
  ix = open_dir(INDEX_DIR)
  results = []
  with ix.searcher(weighting=scoring.BM25F) as s:
    query = QueryParser("content", ix.schema).parse(query_str)
    matches = s.search(query, limit=topN)
    for match in matches:
      results.append({"title": match["title"], "path": match["path"], "match": match.score})
  return results


def search(query_str):
  """
  Search for a given term and show the predefined amount of results.

  Parameters:
  query_str (string): term to search for

  Returns:
  string: html-formatted string including the hits of the search
  """
  return search_times(query_str, DEF_TOPN)


createSearchableData(ENTRY_DIR)
