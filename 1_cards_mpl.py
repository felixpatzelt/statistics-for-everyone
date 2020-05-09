# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Introductory experiment: drawing cards from two stacks
#
# - Imagine a game with **two stacks of cards**
# - Each stack contains **winning cards** and **blanks**.
# - You have to decide **which stack has more wins**
# - How often do you have to draw pairs of cards (one from each stack)?

# %% slideshow={"slide_type": "skip"}
# setup notebook
# %matplotlib inline
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('svg')

# %%
# embed style sheet fixing slides
#from IPython.core.display import HTML
#HTML("""
#<style>
#div.output_subarea {
#    text-align: center;
#    max-width: 100%; 
#    padding-left: 11ex;
#    padding-right: 8ex;
#}
#</style>
#""")

# %% slideshow={"slide_type": "skip"}
# get the functions to generate the figures in this notebook
from cards_code_mpl import *

# %% [markdown] slideshow={"slide_type": "slide"}
# ### Draw cards from two different stacks, one from each stack at a time

# %% [markdown] slideshow={"slide_type": "skip"}
# The next three figures are interactive! Unfortunately they won't work on GitHub, in that case please keep on scrolling.

# %%
interactive_experiment(seed=0, initial_cards=1)

# %% [markdown]
# You can keep on drawing cards for as long as you like and the results keep on changing!

# %% [markdown] slideshow={"slide_type": "skip"}
# **Spoilers below!**
# .
#
# .
#
# .
#
# Scroll down when you are finished drawing cards
#
# .
#
# .
#
# .
#
# .
#
# .
#
# .
#
# .
#
# .
#
# .
#
# .
#
# .
#
# .
#
# .
#
# **Spoilers below!**

# %% [markdown] slideshow={"slide_type": "subslide"}
# ### What can we know after drawing a certain number of cards?

# %%
interactive_experiment(seed=0, initial_cards=25)

# %% [markdown] slideshow={"slide_type": "subslide"}
# ### When have we drawn enough cards to be certain?

# %%
interactive_experiment(seed=0, initial_cards=100)

# %% [markdown] slideshow={"slide_type": "slide"}
# ### It can take a while to see which stack is better

# %%
stack1, stack2 = draw_cards(
    p_win_1 = 0.5, # winning probability for stack 1
    p_win_2 = 0.4, # stack 2 is 20% worse than stack 1!
    n_cards = 150, # maximum number of cards to draw
    seed     = 0   # each seed yields a different experiment
)

plot_wins(stack1, stack2);

# %% [markdown] slideshow={"slide_type": "slide"}
# ### Repeat the experiment
# - Draw 25 cards from each stack
# - Calculate each stack's winning probability = number of wins / 25
# - Repeat 100 times

# %% [markdown] slideshow={"slide_type": "slide"}
# ### Each repetition yields a different winning probability for each stack. 

# %%
means = repeated_experiment_means(
    p_win_1  = 0.5,
    p_win_2  = 0.4,
    n_cards  = 25,
    n_repeats = 100,
    seed      = 1
)
fig, ax = plot_experiments(means)
fig.tight_layout(pad=2)

# %% [markdown]
# - A **histogram** can quantify how often we observed a certain outcome
# - The standard deviation (std.) over the repetitions quantifies our uncertainty
# - It corresponds to the **standard error** of the mean obtained in a single experiment.

# %% [markdown] slideshow={"slide_type": "slide"}
# ### A single small experiment (25 cards)
#
# - **Error bars** show the **standard error** of a single experiment
# - Here they **overlap** - the difference betwen the stacks is smaller than the uncertainty
# - **We can't decide** which stack is better

# %%
stack1, stack2 = draw_cards(
    p_win_1 = 0.5,
    p_win_2 = 0.4,
    n_cards = 25,
    seed     = 0
)
plot_p_win(stack1, stack2);

# %% [markdown] slideshow={"slide_type": "slide"}
# ### An bigger experiment (100 cards)
#
# - The **error bars don't overlap**
# - We can say the difference is **statistically significant**
# - We can be very certain that stack 1 has more wins

# %%
stack1, stack2 = draw_cards(
    p_win_1 = 0.5,
    p_win_2 = 0.4,
    n_cards = 1000,
    seed     = 0
)
plot_p_win(stack1, stack2);

# %% [markdown] slideshow={"slide_type": "slide"}
# # How to calculate these quantities? 
# See next section `practical basics`!

# %% slideshow={"slide_type": "skip"}
# export to slideshow AFTER saving the notebook
# #!jupyter nbconvert --execute 1_cards.ipynb --to slides --no-input
# --ExecutePreprocessor.store_widget_state=True

# %%

# %%
