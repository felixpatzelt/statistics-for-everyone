import altair as alt
import numpy as np
import pandas as pd
import os

# numerical experiment
# ====================
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
    
# plotting setup
# ==============

def slide_theme():
    """Set a theme with a bigger font size for better readability during presenstations.
    
    See https://towardsdatascience.com/consistently-beautiful-visualizations-with-altair-themes-c7f9f889602
    for a good overview.
    """
    # global font settings
    base_font_size = 16
    font = ["Lato",  "Helvetica Neue", "Helvetica", "Arial", "Sans Serif"]
    labelFont  = font
    sourceFont = font
    return {
        "config": {
            "title": {
                "fontSize": base_font_size * 1.5,
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
    
    
def import_lato_font_in_notebook():
    """Have "Lato", the font used by the "simple" reveal.js theme, available in notebook.
    Returns a hidden HTML element.
    """
    from IPython.core.display import HTML
    return HTML("""<style>@import url(https://fonts.googleapis.com/css?family=Lato:400,700,400italic,700italic);</style>""")


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


# plotting
# ========

def plot_first_experiment_bars(data, n_card_pairs):
    """Plot the first experiment as a simple bar chart with interaction"""
    # define input selection
    input_n_cards = alt.binding(
        input='range',
        min=1,
        max=n_card_pairs, 
        step=1, 
        name='Draw Card Pairs: '
    )
    selection = alt.selection_single(
        bind=input_n_cards,
        init={'card_pair': 1}
    )

    # filter data & plot bar chart
    alt.Chart(data).mark_bar().encode(
        alt.X('stack:N', title='Card Stack'),
        alt.Y('sum(win):Q', axis=alt.Axis(title='Number of Wins', tickMinStep=1)),
        color=alt.Color('stack:N', legend=None)
    ).transform_filter(
        "datum.experiment == 1"
    ).add_selection(
        selection
    ).transform_filter(
        # there are sometimes problems with automatic types in comparisons, 
        # when comparing datum with a selection.
        # hence we just put the explicit types everywhere
        alt.datum.card_pair <= alt.expr.toNumber(selection.card_pair)
    ).properties(
        width=250,
        height = 250
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    ).display(renderer='svg')
    
def plot_first_experiment_lines(data):
    """Plot course of first experiment as line chart"""
    # plot ticks for each win per stack
    plot_width = 500
    ticks = alt.Chart(data).mark_tick(thickness=1.5).transform_filter(
        "(datum.experiment == 1) & (datum.win > 0)" 
    ).encode(
        alt.X(
            'card_pair:Q', 
            title='Cards drawn per stack', 
            axis=alt.Axis(ticks=False, grid=False, labels=False, title='Wins', orient='top')
        ),
        alt.Y(
            'stack:Q', 
            title='Stack', 
            scale=alt.Scale(domain=[2,0]),
            axis=None
        ),
        color=alt.Color('stack:N', title='Stack'),
    ).properties(
        width  = plot_width,
        height = 35,
        view=alt.ViewConfig(strokeWidth=0)
    )

    # plot cumulative wins per stack
    lines = alt.Chart(data).mark_line().transform_window(
        cumulative_wins='sum(win)',
        frame=[None, 0],
        groupby=['experiment','stack']
    ).transform_filter(
        "datum.experiment == 1" 
    ).encode(
        alt.X('card_pair:Q', title='Cards drawn per stack'),
        alt.Y('cumulative_wins:Q', title='Number of wins'),
        color=alt.Color('stack:N', title='Stack')
    ).properties(
        width  = plot_width,
        height = 265
    )

    # combine & show plots
    alt.vconcat(ticks, lines).display(renderer='svg')
    

def plot_repeated_experiments(data, n_card_pairs, show='Experiments, Histogram, Std', plot_height=225):

    plots = []

    # define input selection
    input_n_cards = alt.binding(
        input='range',
        min=1,
        max=n_card_pairs, 
        step=1, 
        name='Card pairs per Experiment: '
    )
    selection = alt.selection_single(
        bind=input_n_cards,
        init={'card_pair': 25}
    )

    # filter data
    base = alt.Chart(data).add_selection(
        selection
    ).transform_filter(
        alt.datum.card_pair <= alt.expr.toNumber(selection.card_pair)
    ).transform_aggregate(
        p_win='mean(win):Q',
        groupby=["stack","experiment"]
    )
    scale = alt.Scale(domain=[-.1,1.1])


    if 'experiments' in show.lower():
        # plot individual experiments
        dots = base.mark_point().encode(
            x=alt.X('experiment:Q', title='Experiment'),
            y=alt.Y(
                'p_win:Q', 
                scale=scale, 
                axis=alt.Axis(
                    values=np.arange(0,1.1,.2),
                    grid=True
                ), 
                title='Winning probability'
            ),
            color='stack:N'
        ).properties(
            width=400,
            height=plot_height
        )
        plots.append(dots)

    if 'histogram' in show.lower():
        # plot histogram over experiment results
        hist = base.mark_bar(
            fillOpacity=.33,
            strokeOpacity=.66,
            strokeWidth=2,
            cornerRadius=2,
            binSpacing=1
        ).encode(
            y=alt.Y(
                'p_win:Q', 
                bin=alt.Bin(extent=[0,1], step=.1),
                scale=scale, 
                axis=alt.Axis(
                    values=np.arange(0,1.1,.2), 
                    title=None, 
                    labels=False,
                    grid=True
                ), 
            ),
            x=alt.X(
                'count(experiment):Q', 
                stack=None, # no stacked bar chart
                title='Number of experiments'
            ),
            color=alt.Color('stack:N', legend=alt.Legend(title='Stack')),
            stroke=alt.Color('stack:N', legend=None),
            order='stack:Q',
        ).properties(
            width=150,
            height=plot_height
        )
        plots.append(hist)

    if 'std' in show.lower():
        # define custom label for standard deviation bars
        std_text = alt.Chart(
            pd.DataFrame({'x':[4], 'y':[.5], 'text':['Mean ± Standard Deviation']})
        ).mark_text(
            angle=90, baseline='middle'
        ).encode(
            x='x', y='y', text='text'
        )

        # plot standard deviation bars
        errorbars = alt.layer(
            base.mark_errorbar(extent='stdev', rule=alt.MarkConfig(size=2)).encode(
                y=alt.Y('p_win:Q',
                    axis=None,#alt.Axis(orient='right', ticks=False, labels=False, grid=False, style=None), 
                    scale=scale,
                ),
                x=alt.X('stack:Q', axis=None),
                color='stack:N',
            ),
            base.mark_point(size=0).encode(
                y=alt.Y('p_win:Q', aggregate='mean', scale=scale),
                x=alt.X('stack:Q', scale=alt.Scale(domain=[1,4])),
            ),
            std_text,
            view=alt.ViewConfig(strokeWidth=0),
        ).properties(
            width=25,
            height=plot_height
        )
        plots.append(errorbars)

    # combine & show
    alt.concat(*plots).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    ).display(renderer='svg')
    

def plot_experiment_bars_with_errors(data, n_card_pairs, n_card_pairs_init, n_repeats):

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
        name='Select one experiment: '
    )
    selection_experiment = alt.selection_single(
        bind=input_experiment,
        init={'experiment': 1}
    )
    
    # filter data
    base = alt.Chart(data).add_selection(
        selection_n_cards, selection_experiment
    ).transform_filter(
        # there are sometimes problems with automatic types in comparisons, 
        # when comparing datum with a selection.
        # hence we just put the explicit types everywhere
          (alt.expr.toNumber(alt.datum.card_pair)  <= alt.expr.toNumber(selection_n_cards.card_pair))
        & (alt.expr.toNumber(alt.datum.experiment) == alt.expr.toNumber(selection_experiment.experiment))
    
    )

    # plot bar chart
    bars = base.mark_bar().encode(
        x='stack:N',
        y='mean(win):Q',
        color=alt.Color('stack:N', legend=None)
    )

    # plot errorbars
    errors=base.mark_errorbar(extent='stderr', rule=alt.MarkConfig(size=2)).encode(
        alt.Y('win:Q', title='Winning probability'),
        x=alt.X('stack:N', title='Card Stack')
    )

    # combine plot
    alt.layer(bars, errors).properties(
        width  = 250,
        height = 250
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    ).display(renderer='svg')