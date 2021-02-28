# Statistics for Everyone

This course for a wide audience shows you why and how a better understanding of uncertainty can improve your decision making and your understanding of the world.

**Work in Progress**

To view the lessons that are available so far, check out the hosted [finished slides](https://felixpatzelt.com/statistics-for-everyone).

# Development

The interactive slides are generated from Jupyter Notebooks written in Python.

[list of possible topics](topics.md)


### Installation

```sh
# assuming python 3.7 is installed as python3
python3 -m venv testenv
source testenv/bin/activate
pip install -r requirements.txt
```

### Everything needed to edit slides is automated

- export all slides, serve at localhost:8000 & update upon changes:

    ``make serve``

- convert to slides only once:

    ``make slides``

### Editing the slide theme

If you are editing the theme for the first time, you need to run

    ``make build-reveal``

You may need to install [node.js](https://nodejs.org/en/) first.

Now you can edit `reveal.js/css/theme/source/statistics-for-everyone-slides.scss` 
and run

    ``make theme``

to compile the stylesheets and copy them to the `slides` directory.