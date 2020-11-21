import altair as alt
import pandas as pd
import numpy as np
import itertools

from .plotting import parameter_selection

def plot_uniform_probability_mass_function(maximum_outcome=20):
    max_outcome = parameter_selection(
        min=2,
        max=maximum_outcome,
        step=1,
        init_value=2,
        name='Max. Outcome'
    )
    x_max = maximum_outcome + 1

    return alt.Chart(
        alt.sequence(0, x_max, 1, as_='x')
    ).mark_bar().encode(
        x=alt.X('x:Q', scale=alt.Scale(domain=(0,x_max)), title='Outcome x'),
        y=alt.Y('px:Q', scale=alt.Scale(domain=(0,0.51)), title='Probability of x'),
    ).transform_calculate(
        px = 1/max_outcome.value * (1 <= alt.datum.x) * (alt.datum.x <= max_outcome.value)
    ).add_selection(
        max_outcome
    ).display(renderer='svg')
    
    
def plot_continuous_uniform_density(xmax=3):
    dx = xmax / 1000 # step size for plotting

    # value ranges to show on the axes
    xscale = alt.Scale(domain=(-0.1, 3.1), nice=False)
    yscale = alt.Scale(domain=(0,2))
    pscale = alt.Scale(domain=(0,1.1))

    # interactive parameters (just selections bound to inputs)
    sel_min = parameter_selection(
        min=0,
        max=xmax,
        step=0.1,
        init_value=0,
        name='Selection min'
    )
    sel_max = parameter_selection(
        min=0,
        max=xmax,
        step=0.1,
        init_value=xmax+0,
        name='Selection max'
    )
    dist_max = parameter_selection(
        min=0.5,
        max=xmax,
        step=0.1,
        init_value=2,
        name='Distribution max'
    )

    # all parts of the chart
    base = alt.Chart(
        alt.sequence(start=-0.1, stop=xmax+0.1, step=dx, as_='x')
    )
    density = base.mark_line().encode(
        x=alt.X('x:Q', scale=xscale, title='x'),
        y=alt.Y('px:Q', scale=yscale, title='Probability Density'),
    ).properties(
        width=400
    )
    selected = base.mark_area(color='LightBlue', opacity=0.5).encode(
        x=alt.X('x:Q'),
        y=alt.Y('ps:Q', title='Probability Density'),
    )
    selection_min = base.mark_rule(color='SlateGrey').encode(
        x=alt.X('mean(sel_min):Q', title=''),
        opacity=alt.condition(sel_min.value > 0, alt.value(1), alt.value(0))
    )
    selection_max = base.mark_rule(color='SlateGrey').encode(
        x=alt.X('mean(sel_max):Q', title=''),
        opacity=alt.condition(sel_max.value < xmax, alt.value(1), alt.value(0))
    )
    selected_area = base.encode(
        y=alt.Y('sum(probability):Q', scale=pscale, title='Probability in Selection'),
    ).mark_bar(clip=True, color='LightBlue').properties(
            width=50
    )
    # combine
    alt.hconcat(
        selection_min + selection_max + selected + density  | selected_area
    ).add_selection(
        sel_max,
        sel_min,
        dist_max,
    ).transform_calculate(
        sel_max=sel_max.value,
        sel_min=sel_min.value,
        dist_max=dist_max.value,
        px = f'1 / datum.dist_max * ((datum.x > 0 ) & (datum.x < datum.dist_max))',
        ps = f'datum.px * ((datum.x > datum.sel_min ) & (datum.x < datum.sel_max))',
        probability = f'datum.ps*{dx}'
    ).display(renderer='svg')
    
    
    
def plot_normal_distribution(xmin = -5, xmax = 5, stdmin=.5, stdmax=5, step=.1,):
    mean = parameter_selection(
        min=xmin,
        max=xmax,
        step=.1,
        init_value=0,
        name='Mean'
    )
    std = parameter_selection(
        min=stdmin,
        max=stdmax,
        step=.1,
        init_value=1,
        name='Standard Deviation'
    )
    
    return alt.Chart(
        alt.sequence(xmin, xmax, step, as_='x')
    ).mark_line().encode(
        x=alt.X('x:Q'),
        y=alt.Y('pdf:Q', title='Probability Density of x')
    ).transform_calculate(
        mean = mean.value,
        std = std.value,
        pdf='densityNormal(datum.x, datum.mean, datum.std)'
    ).add_selection(
        std, mean
    ).properties(
            width=500
    )
    
def plot_sum_of_n_dice(n_max=7):
   
    # a naive brute-force calculation of the probability mass function for the sum of n dice
    # ======================================================================================

    res = pd.DataFrame(index=pd.Index(range(1,6*n_max+1), name='Sum of Points'))
    # for n = 1 ... n_max dice
    for n in range(1, n_max+1):
        # calculate number of possibilities to get each possible outcome value
        outcome, possibilities = np.unique(
            # sum of points for each outcome
            np.array(
                # create list of all possible outcomes
                # each outcome is a list of the number of points for each die
                list(itertools.product(*[list(range(1,7))]*n))
            ).sum(1), 
            return_counts=True
        )
        res.loc[outcome, n] = possibilities
    
    # normalise counts to probabilities
    res /= res.sum()

    # add mean points per die
    dice_sum_df = pd.melt(res.reset_index(), id_vars=['Sum of Points'], var_name='Dice', value_name='Probability')
    dice_sum_df['Points per Die'] = dice_sum_df['Sum of Points'] / dice_sum_df['Dice']
    
    # plot
    # ====
    n_dice = parameter_selection(
        min=1,
        max=n_max,
        step=1,
        init_value=1,
        name='Dice'
    )
    measure_dropdown = alt.binding_select(
        options=['Sum of Points', 'Points per Die'], 
        name='Measure:'
    )
    selection = alt.selection_single(
        bind=measure_dropdown, 
        fields=['Measure'], 
        init=dict(Measure = 'Sum of Points')
    )
    
    # chart base
    chart = alt.Chart(
        dice_sum_df
    ).mark_bar().encode(
        x=alt.X('Value:Q', title='Points'),
        y='Probability:Q'
    )
    
    # add parameters & filters
    return chart.transform_filter(
        +alt.datum.Dice == +n_dice.value,
    ).transform_fold(
        # transform the two measure columns to long format
        # i.e. measure denotes from which column the value came
        ['Sum of Points', 'Points per Die'],
        as_=['Measure', 'Value']
    ).add_selection(
        n_dice, selection
    ).transform_filter(
        selection
    ).properties(
        width=250
    ).display(renderer='svg')