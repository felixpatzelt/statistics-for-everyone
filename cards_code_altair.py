import altair as alt
import numpy as np
import pandas as pd
import os
from cards_code import draw_cards

def repeated_experiments_df(p_win_1, p_win_2, n_cards, n_repeats, seed=0):
    res = []
    
    for i in range(n_repeats):
        wins = draw_cards(p_win_1, p_win_2, n_cards, seed=seed+i*n_cards*2)
        res.append(
            pd.DataFrame({
                'experiment': i+1,
                'stack':      [1] * n_cards + [2] * n_cards,
                'card_pair':  np.tile(np.arange(1, n_cards+1), 2),
                'win':        np.concatenate(wins)
            })
        )
    return pd.concat(res)

def df_to_datasource(
        df,
        embed_in_notebook = True,
        embed_in_slides   = False
    ):
    """Transparently replace datasource depending on notebook use or export.
    Embedding will lead to big file sizes.
    """
    if not embed_in_slides and os.environ.get('CONVERT') == 'TRUE':
        # the exported slide should be hosted such that
        # the data is hosted on the same server
        datafile = 'card_experiments.csv'
        df.to_csv(datafile, index=False)
        data = alt.Data(
            url=datafile, 
            format={
                'type': 'csv', 
                # for some reason automatic type inferrence
                # gets confused arount experiment = 100
                # should investigate and report bug
                'parse': {
                    'experiment': 'number', 
                    'stack':      'number', 
                    'card_pair': 'number', 
                    'win':       'number'
                }
            }
        )
    elif not embed_in_notebook:
        # disable arning:
        # use data transformer
        # json creates bigger files but is more reliable (see manual parsing note above)
        alt.data_transformers.enable('json')
        # make it work in Jupyter Lab
        alt.renderers.enable('mimetype')
        # note: this will export a static png when saving the notebook!
        data = df
    else:
        alt.data_transformers.disable_max_rows()
        data = df
    return data