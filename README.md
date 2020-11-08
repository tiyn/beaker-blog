# Beaker Blog

This is a simple blog based on Pythons Flask framework.
The basic design is based on LukeSmithXYZs blog.
However I dislike using a script for adding entries and just want to add entries via plain text files.

## Features/To-Dos

- [x] Plain text support for blog entries
    - [x] HTML files (.html)
    - [x] Markdown Files (.md)
- [x] Infinite-scroll blog page
- [x] Archive page
    - [x] Months as headings
    - [x] Links to scrolling blog page
    - [x] Links to standalone article
- [x] Standalone article page
    - [x] Links to scrolling blog page
- [x] RSS feed
- [x] Navigation
    - [x] Header
    - [x] Footer
- [x] Switchable CSS
    - [x] CSS dark-theme
    - [x] CSS light-theme
- [x] Config file
- [x] Docker installation
    - [ ] Enable variables/environment variables
- [ ] Logo

## Usage

### Create entries

Blog entries are managed by plain html files in the `templates/entry/` directory.
The first line of each document is reserved as the title of the document.
You have to specify the filetype by extension.

## Deployment

### PIP/Python

- `git clone https://github.com/tiyn/tiyny-blog`
- `cd tiyny-blog/src`
- edit the `config.py` file according to your needs
- `pip3install -r requirements.txt` - install depenencies
- run `python app.py`
- blog is available on port 5000

### Docker

Make sure you copy an example `config.py` and edit it before running the container.
The `config.py` can be found in the `src` folder.

#### Volumes

Set the following volumes with the -v tag.

| Volume-Name | Container mount           | Description                                                  |
|-------------|---------------------------|--------------------------------------------------------------|
| config-file | /blog/src/config.py       | Config file                                                  |
| entries     | /blog/src/templates/entry | Directory for blog entries                                   |
| css         | /blog/src/static/css      | (optional) Directory for css files                           |
| html        | /blog/src/templates       | (optional) Directory for templates (entry-volume not needed) |

#### Ports

Set the following ports with the -p tag.

| Container-Port | Recommended outside port | Protocol | Description |
|----------------|--------------------------|----------|-------------|
| 5000           | 80                       | TCP      | HTTP port   |

#### Example run-command

`docker run --name blog --restart unless-stopped -v ./config.py:/blog/src/config.py -v entries:/blog/src/templates/entry -p 80:5000 -d tiynger/tiyny-blog`
