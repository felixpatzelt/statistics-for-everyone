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

### To edit or create new lessons

- Each lesson is a [jupyter](https://jupyter.org) notebook. Start

    `jupyter lab`
    
    and open any of the `.ipynb`files or create a new one.


### Converting notebooks to slides is automated

- Export all slides, serve at localhost:8000 & update upon changes with

    `make serve`

- or convert to slides only once with

    `make slides`.

### Editing the reveal.js theme 

- If you are editing the theme for the first time, you need to run
    
    `make build-reveal`.
    
    You may need to install [node.js](https://nodejs.org) first.

- Edit `reveal.js/css/theme/source/statistics-for-everyone-slides.scss` and run
    
    `make theme`

    to compile the stylesheets and copy them to the `slides` directory.
    
- Reveal.js is included as a [git subtree](https://www.atlassian.com/git/tutorials/git-subtree). To update, run

```sh
git subtree --prefix reveal.js pull https://github.com/hakimel/reveal.js.git 0582f57517c97a4c7bfeb58762138c78883f94c5 --squash
```
Change the commit ID as desired.