import altair as alt
import numpy as np
import pandas as pd
import os

# experiment
# ==========
def draw_cards(p_win_1, p_win_2, n_cards, seed=None):
    np.random.seed(seed)
    # alternate between drawing from stack 1 and 2 so we get the same initial results for different n
    # transpose output so we can just unpack the results for each stack
    return np.random.binomial(1, (p_win_1, p_win_2), size=(n_cards, 2)).T


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
    
# plotting
# ========
def df_to_datasource(
        df,
        embed_in_notebook = True,
        embed_in_slides   = False
    ):
    """Transparently replace datasource depending on notebook use or export.
    Embedding will lead to big file sizes.
    """
    if not embed_in_slides and os.environ.get('CONVERT') == 'TRUE':
        'slides'
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



def bar_chart_with_errorbars(data, n_card_pairs, n_card_pairs_init, n_repeats):

    # define input selection
    input_n_cards = alt.binding(
        input='range',
        min=1,
        max=n_card_pairs, 
        step=1, 
        name='Card pairs per experiment: '
    )
    selection_n_cards = alt.selection_single(
        bind=input_n_cards,
        init={'card_pair': n_card_pairs_init}
    )
    input_experiment = alt.binding(
        input='range',
        min=1,
        max=n_repeats, 
        step=1, 
        name='Select experiment: '
    )
    selection_experiment = alt.selection_single(
        bind=input_experiment,
        init={'experiment': 1}
    )

    # filter data
    base = alt.Chart(data).add_selection(
        selection_n_cards, selection_experiment
    ).transform_filter(
          (alt.datum.card_pair  <= selection_n_cards.card_pair)
        & (alt.datum.experiment - selection_experiment.experiment == 0)
    )

    # plot bar chart
    bars = base.mark_bar().encode(
        alt.X('stack:N', title='Card Stack'),
        alt.Y('mean(win):Q'),#, axis=alt.Axis(title='Number of Wins', tickMinStep=1)),
        color=alt.Color('stack:N', legend=None)
    )

    # plot errorbars
    errors=base.mark_errorbar(extent='stderr', rule=alt.MarkConfig(size=2)).encode(
        y=alt.Y(
            'win:Q',
        ),
        x=alt.X('stack:N'),
    )

    # combine plot
    alt.layer(bars, errors).properties(
        width=200,
        height = 250
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    ).display(renderer='svg')