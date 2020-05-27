# Python Flask Blog

This is a simple blog based on Pythons Flask framework.

## Features/To-Dos

- [x] Infinite-scroll blog page
- [x] Archive page
  - [ ] Headers and dates
- [x] RSS feed
- [ ] Navigation: Header, Footer
- [ ] CSS dark-theme
- [ ] CSS light-theme

## Usage

### Create entries

Blog entries are managed by plain html files in the `templates/entry/` directory.
The first line of each document is reserved as the title of the document.
You have to specify the filetype by extension.

Currently supported filetypes are:
- HTML (.html)
- Markdown (.md)



## Deployment

### PIP/Python

- `git clone https://github.com/tiyn/flaskblog`
- `cd flaskblog/src`
- `pip3install -r requirements.txt` - install depenencies
- run `python app.py`
- blog is available on port 5000

### Docker

#### Volumes

Set the following volumes with the -v tag.

| Volume-Name | Container mount      | Description                                                           |
|-------------|----------------------|-----------------------------------------------------------------------|
| css         | /blog/src/static/css | Directory for css files                                               |
| html        | /blog/src/templates  | Directory for templates and html documents (contains entry directory) |

#### Ports

Set the following ports with the -p tag.

| Container-Port | Recommended outside port | Protocol | Description |
|----------------|--------------------------|----------|-------------|
| 5000           | 80                       | TCP      | HTTP port   |

#### Example run-command

`docker run --name blog --restart unless-stopped -v css:/blog/src/static/css -v html:/blog/src/templates -p 80:5000 -d tiynger/flaskblog`
