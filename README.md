# Statistics for everyone

This course for a wide audience shows you why and how a better understanding of uncertainty can improve your decision making and your understanding of the world.

**Work in Progress**

## Installation

Install [anaconda](https://docs.anaconda.com/anaconda/install/) or miniconda.

Install conda environment

```bash
conda env create -f stats.yml
# conda env update --file stats.yml --prune
```

and activate conda enviroment

```bash
conda activate stats
# ...
conda deactivate
````

## Development

The interactive slides are generated from Jupyter Notebooks written in Python.

[list of possible topics](topics.md)

### everything needed to edit slides is automated

- export all slides, serve at localhost:8000 & update upon changes:

    ``python make_slides.py --serve True --watch True``

### manual alternative

- export:

    ``export CONVERT=TRUE; jupyter nbconvert --execute 1_cards.ipynb --output-dir='./slides' --to slides --no-inpuexport CONVERT=TRUE; jupyter nbconvert --execute 1_cards.ipynb --output-dir='./slides' --to slides --no-input``

- viewing:

    ``python -m http.server --directory slides``
