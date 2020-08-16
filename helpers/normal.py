import altair as alt
import pandas as pd
import numpy as np

def normal_dist_df(means, std, n_observations, n_repeats, seed=0):
    res = []
    for j in range(len(means)):
        for i in range(n_repeats):
            obs =  np.random.normal(means[j], std, n_observations)
            res.append(
                pd.DataFrame({
                    'population': j+1,
                    'sample': i+1,
                    'variable': obs
                })
            )
    return pd.concat(res)

def plot_normal(data):
    base_chart = alt.Chart(
        data
    ).transform_joinaggregate(
        pop_m='mean(variable)',
        pop_sd='stdev(variable)',
    ).transform_calculate(
        pop_mean='datum.pop_m',
        pop_mean_m_sd='(+datum.pop_m - datum.pop_sd)',
        pop_mean_p_sd='(+datum.pop_m + datum.pop_sd)'
    )
    
    alt.layer(
        base_chart.mark_bar().encode(
            x=alt.X('variable:Q', bin=alt.Bin(maxbins=50), title='Variable'),
            y=alt.Y('count()', title='Count')
        ),
        base_chart.mark_rule(
            color='red'
        ).encode(
            x='pop_mean:Q'
        ),
        base_chart.mark_rule(
            color='orange'
        ).encode(
            x='pop_mean_m_sd:Q'
        ),
        base_chart.mark_rule(
            color='orange'
        ).encode(
            x='pop_mean_p_sd:Q'
        )
    ).properties(
        width=250,
        height=250
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    ).display(
        renderer='svg'
    )

def plot_normal_n_populations(data, n_populations):
    """Plot population as historam"""
    selection1 = alt.selection_single(
        bind=alt.binding(
            input='range',
            min=1,
            max=n_populations, 
            step=1, 
            name='Population: '
        ),
        init={'population': 1}
    )

    base_chart = alt.Chart(
        data
    ).transform_joinaggregate(
        pop_m='mean(variable)',
        pop_sd='stdev(variable)',
    ).transform_calculate(
        pop_mean='datum.pop_m',
        pop_mean_m_sd='(+datum.pop_m - datum.pop_sd)',
        pop_mean_p_sd='(+datum.pop_m + datum.pop_sd)'
    )

    alt.layer(
        base_chart.mark_bar().encode(
            x=alt.X('variable:Q', bin=alt.Bin(maxbins=50), title='Variable'),
            y=alt.Y('count()', title='Count')
        ),
        base_chart.mark_rule(
            color='red'
        ).encode(
            x='pop_mean:Q'
        ),
        base_chart.mark_rule(
            color='orange'
        ).encode(
            x='pop_mean_m_sd:Q'
        ),
        base_chart.mark_rule(
            color='orange'
        ).encode(
            x='pop_mean_p_sd:Q'
        )
    ).add_selection(
        selection1
    ).transform_filter(
        0 == (alt.datum.population - selection1.population)
    ).properties(
        width=250,
        height=250
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    ).display(
        renderer='svg'
    )


def plot_normal_sample(data, n_populations, n_samples):
    """Plot sample as histogram"""
    selection1 = alt.selection_single(
        bind=alt.binding(
            input='range',
            min=1,
            max=n_populations, 
            step=1, 
            name='Population: '
        ),
        init={'population': 1}
    )

    selection2 = alt.selection_single(
        bind=alt.binding(
            input='range',
            min=1,
            max=n_samples, 
            step=1, 
            name='Sample: '
        ),
        init={'sample': 1}
    )

    base_chart = alt.Chart(
        data
    ).transform_joinaggregate(
        pop_m='mean(variable)',
        pop_sd='stdev(variable)',
    ).transform_calculate(
        pop_mean='datum.pop_m',
        pop_mean_m_sd='(+datum.pop_m - datum.pop_sd)',
        pop_mean_p_sd='(+datum.pop_m + datum.pop_sd)'
    )

    alt.layer(
        base_chart.mark_bar().encode(
            x=alt.X('variable:Q', bin=alt.Bin(maxbins=50), title='Variable'),
            y=alt.Y('count()', title='Count')
        ),
        base_chart.mark_rule(
            color='red'
        ).encode(
            x='pop_mean:Q'
        ),
        base_chart.mark_rule(
            color='orange'
        ).encode(
            x='pop_mean_m_sd:Q'
        ),
        base_chart.mark_rule(
            color='orange'
        ).encode(
            x='pop_mean_p_sd:Q'
        )
    ).add_selection(
        selection1
    ).transform_filter(
        0 == (alt.datum.population - selection1.population)
    ).add_selection(
        selection2
    ).transform_filter(
        0 == (alt.datum.sample - selection2.sample)
    ).properties(
        width=250,
        height=250
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    ).display(
        renderer='svg'
    )
