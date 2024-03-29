"""Helpers to style altair plots and to improve working with datasets.
"""

import altair as alt
import numpy as np
import pandas as pd
import os
from IPython.core.display import HTML

def slide_theme():
    """Set a theme with a bigger font size for better readability during presenstations.
    
    See https://towardsdatascience.com/consistently-beautiful-visualizations-with-altair-themes-c7f9f889602
    for a good overview.
    """
    # global font settings
    base_font_size = 16
    font = ["Source Sans Pro", "Helvetica Neue", "Helvetica", "Arial", "sans-serif"]
    labelFont  = font
    sourceFont = font
    return {
        "config": {
            "title": {
                "fontSize": base_font_size * 1.25,
                "font": font,
                "fontWeight": 'normal',
            },
            "axisX": {
                "labelFont": labelFont,
                "labelFontSize": base_font_size,
                "titleFont": font,
                "titleFontSize": base_font_size,
                "titleFontWeight": 'normal',
                "titlePadding": 10,
            },
            "axisY": {
                "labelFont": labelFont,
                "labelFontSize": base_font_size,
                "titleFont": font,
                "titleFontSize": base_font_size,
                "titleFontWeight": 'normal',
                "titlePadding": 10,
            },
            "legend": {
                "labelFont": labelFont,
                "labelFontSize": base_font_size,
                "titleFont": font,
                "titleFontSize": base_font_size,
                "titleFontWeight": 'normal',
            },
            "text": {
               "font": sourceFont,
               "fontSize": base_font_size * .9,
            }, 
        }
    }

def enable_slide_theme():
    # activate theme
    alt.themes.register("statistics_slide_theme", slide_theme)
    alt.themes.enable("statistics_slide_theme");
    # the three dots menu is useful but a bit distracting in slides
    alt.renderers.set_embed_options(actions=False);
    
    
def import_slide_theme_font_in_notebook():
    """Have the font used by the slide theme, available in notebook.
    Returns a hidden HTML element.
    """
    return HTML(
        '<link rel="stylesheet" type="text/css" '
        'href="./reveal.js/dist/theme/fonts/source-sans-pro/source-sans-pro.css">'
    )


def df_to_datasource(
        df,
        embed_in_notebook = False,
        embed_in_slides   = False,
        export_dir  = 'slides',
        export_file = '1_cards_data.csv'
    ):
    """Transparently replace datasource depending on notebook use or export. 
    
    - Embedding will lead to big files. 
    - Altair will complain when embeding more than 5000 rows, so we disable that warning when embedding.
    
    Some explanations:
    A better alternative to embedding is to load data from a url. The only issue is, that then you have
    to pass a url that you can be accessed via the server. In Jupyter, you can find that url by right clicking 
    on the file in the Jupyter file browser and opening it in a new browser tab. However, if you intend 
    to export the notebook as slides, then this url ends up in your slides. In that case you have specify 
    a url where you will host the file and where it will be accessible for viewers of the slides.html. 
    Referencing local files doesn't work even when opening it locally (without a web server) because that is a 
    security features of modern browsers.
    
    Luckily there is an automated solution for the notebook in the form of an altair data_transformer doing the
    dirty work for us. However, we only can use it in the Notebook, not when exporting slides. So in that case
    we will export the data as a csv and point to the location where it will be found when the slides and
    the csv are hosted by a server with the same prefix.
    
    To view the exported slides locally when the data is not embedded, use python -m http.server --directory slides.
    If you really want to mail the file to someone or view them offline, you have to embed and live with the
    bigger file.
    """
    if not embed_in_slides and os.environ.get('CONVERT') == 'TRUE':
        # the exported slide should be hosted such that
        # the data is hosted on the same server
        df.to_csv(
            os.path.join(export_dir, export_file), 
            index=False
        )
        data = alt.Data(
            url=export_file, 
            format=dict(type='csv')
        )
    elif not embed_in_notebook and not os.environ.get('CONVERT') == 'TRUE':
        # use data transformer
        # json creates bigger files but is more reliable (see manual parsing note above)
        alt.data_transformers.enable('csv')
        # make it work in Jupyter Lab
        alt.renderers.enable('mimetype')
        # note: this will export a static png when saving the notebook!
        data = df
    else:
        # disable warning & embed data into notebook
        alt.data_transformers.disable_max_rows()
        data = df
    return data


def parameter_selection(
        min:float, max:float, step:float, init_value:float, name:str, type:float='range'
    ) -> alt.selection:
    """Return selection bound to parameter input element."""
    b = alt.binding(
        input=type, min=min, max=max, step=step, name=name
    )
    return alt.selection_single(
        bind = b,
        init = dict(value=init_value)
    )