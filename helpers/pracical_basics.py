import altair as alt
import pandas as pd
import numpy as np

def plot_population_vs_sample_mean():
    """Create interactive plot with random samples from normal distribution.
    Show population & sample mean ± uncertainty, histogram, and sampled values.
    """
    # inputs
    plot_width  = 500
    max_samples = 200
    input_mean = alt.binding(
        input='range',
        min=-5,
        max=5,
        step=.1,
        name='Pop. mean'
    )
    input_std = alt.binding(
        input='range',
        min=0.1,
        max=5,
        step=.1,
        name='Pop. Std.'
    )
    input_samples = alt.binding(
        input='range',
        min=10,
        max=max_samples,
        step=1,
        name='Sample size'
    )
    input_uncertainty = alt.binding(
        input='range',
        min=1,
        max=3,
        step=1,
        name='Show std. errors'
    )
    mean_selection = alt.selection_single(
        bind=input_mean,
        init={'mean': 0}
    )
    std_selection = alt.selection_single(
        bind=input_std,
        init={'std': 1.5}
    )
    samples_selection = alt.selection_single(
        bind=input_samples,
        init={'samples': 50}
    )
    uncertainty_selection = alt.selection_single(
        bind=input_uncertainty,
        init={'ses': 2}
    )


    scale = alt.Scale(domain=[-10,10])

    # simple plot with population mean + population error
    pop_mean_chart = alt.Chart(
        data=pd.DataFrame({'x': [1]})
    )
    title_only_ax_kwargs = dict(
        ticks=False,
        labels=False,
        #grid=False,
        domain=False,
        orient='top'
    )
    pop_mean = (
        pop_mean_chart.mark_errorbar(color='red', rule=alt.MarkConfig(size=1.5), ticks=True).encode(
            x=alt.X(
                "xmin:Q", 
                axis=alt.Axis(
                    title="Population mean ± expected sample uncertainty", **title_only_ax_kwargs
                )
            ),
            x2="xmax:Q",
        ) + pop_mean_chart.mark_point(color='red', size=20, filled=True, stroke=None).encode(
            x=alt.X("mean:Q", scale=scale, axis=alt.Axis(title=""))
        )
    ).add_selection(
        samples_selection, std_selection, mean_selection, 
    ).transform_calculate(
      mean = mean_selection['mean'],
      std  = std_selection['std'],
      samples = samples_selection['samples'],
      ses = uncertainty_selection['ses']
    ).transform_calculate(
        xmin='+datum.mean - datum.ses * datum.std / sqrt(+datum.samples)',
        xmax='+datum.mean + datum.ses * datum.std / sqrt(+datum.samples)',
    ).properties(
        view=alt.ViewConfig(strokeWidth=0), width=plot_width
    )

    # combined chart with different ways to represent sample 
    data = alt.sequence(0, max_samples, as_='t')
    sample_chart = alt.Chart(data)

    samp_mean = (
        sample_chart.mark_errorbar(rule=alt.MarkConfig(size=1.5), ticks=True).encode(
            x=alt.X(
                "bar_min:Q", 
                scale=scale, 
                axis=alt.Axis(
                    title="Sample mean ± sample uncertainty", **title_only_ax_kwargs
                )
            ),
            x2='bar_max:Q'
        ) + sample_chart.mark_point(size=20, filled=True, stroke=None).encode(
            x='sample_mean:Q'
        )
    ).transform_aggregate(
            sample_mean = 'mean(x)',
            sample_err = 'stderr(x)',
    ).transform_calculate(
        ses = uncertainty_selection['ses'],
        bar_min = '+datum.sample_mean - datum.ses * datum.sample_err',
        bar_max = '+datum.sample_mean + datum.ses * datum.sample_err'
    ).properties(
        view=alt.ViewConfig(strokeWidth=0), width=plot_width
    )

    hist = sample_chart.mark_bar(clip=True).encode(
        alt.X("x:Q", bin=alt.Bin(), scale=scale, axis=alt.Axis(title='Sample Histogram', **title_only_ax_kwargs)),
        y=alt.Y('count()', title='Count'),
    ).properties(
        width=plot_width,
        height=100
    )

    ticks = sample_chart.mark_tick(clip=True).encode(
        x=alt.X('x:Q', scale=scale, axis=alt.Axis(title='Sample Values'))
    ).properties(
        view=alt.ViewConfig(strokeWidth=0), width=plot_width
    )

    combined_sample = (
        samp_mean & hist & ticks
    ).add_selection(
        uncertainty_selection, samples_selection, std_selection, mean_selection
    ).transform_filter(
        alt.datum.t <= alt.expr.toNumber(samples_selection.samples),
    ).transform_calculate(
        mean = mean_selection['mean'],
        std  = std_selection['std'],
        x='sampleNormal(+datum.mean,+datum.std)', # the plus casts to number
    )

    (pop_mean & combined_sample).display(renderer='svg')
    
    
    
def print_example_statistics(examples, print_only_sample=False):
    for sample in examples:
        print("Values in sample:          ", sample)
        if not print_only_sample:
            print("Sum of values:             ", np.sum(sample))
            print("Mean:                      ", np.mean(sample))
            print("Median:                    ", np.median(sample))
            print("Sum of deviations:         ", 
                np.sum(
                    (np.array(sample) - np.mean(sample))**2
                )
            )
            print("Sample Variance:           ", np.var(sample, ddof=0).round(3))
            print("Sample Standard deviation: ", np.std(sample, ddof=0).round(3))
            print("Population Variance:       ", np.var(sample, ddof=1).round(3))
            print("Pop. Standard deviation:   ", np.std(sample, ddof=1).round(3))
            print("Standard error:            ", (np.std(sample, ddof=1) / np.sqrt(len(sample))).round(3))
            print()

