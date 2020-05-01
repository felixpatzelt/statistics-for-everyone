Notes on nbconvert and reveal.js:

- nbconvert only works with the older reveal.js 3.5 and doesn't support all features
- slide fragments seem pretty broken in Safari
- figure alignment is off but custom.css fixes it (the exported file looks for it automatically)
- widgets don't show up when converting a saved .ipynb ([issue](https://github.com/jupyter/nbconvert/issues/1097))
- if there is an output when the `--execute` flag is used, that does show up in the slides
- That is, `jupyter nbconvert --execute *.ipynb --to slides --no-input`


Notes on voila-reveal:
- has working slide fragments but otherwise an even more basic stylesheet 
- has to be modified to change styling
- obviously only works with a local installation (maybe with binder??)
    

Javascript output shows up in slides, so maybe there is an alternative to Jupyter widgets that works everywhere.