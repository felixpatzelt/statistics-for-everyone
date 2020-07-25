"""Find useful combinations of coins for mental calculations. Execute with python 3.

Basic shell usage:
    python3 find_nice_coin_examples.py
    
Alternatively, import and use find_coins
"""
import numpy as np

coin_types_default = np.array([1,2,5,10,20,50])
min_coins_default  = 5
max_coins_default  = 9

def int_to_base(number:int,base:int):
    digits = []
    while number:
        digits.append(number % base)
        number //= base
    return digits[::-1]

def find_coins(
        min_coins:int=min_coins_default, 
        max_coins:int=max_coins_default ,
        coin_types:list=coin_types_default
    ):
    """Brute-force search for combinations of min_coins to max_coins drawn out of coin_types.
    Returns dict with n_coins: set_of_nice_results
    """
    n_coin_types = len(coin_types)
    results = dict()

    for n_coins in range(min_coins,max_coins+1):
        n_combinations = n_coin_types**n_coins

        print(f"{n_coins} coins ({n_combinations} combinations)")

        coin_states = np.zeros(n_coins, dtype=int)

        solutions = set()

        for i in range(n_combinations):
            print(f"\r {int(100*i/n_combinations)}%", end="")
            coin_states_i = int_to_base(i, n_coin_types)
            if len(coin_states_i):
                coin_states[-len(coin_states_i):] = coin_states_i
            coins_in_pocket = coin_types[coin_states]

            n_unique_coins = len(np.unique(coins_in_pocket))
            if n_unique_coins > 2:
                coin_median  = np.median(coins_in_pocket)
                coin_mean    = np.mean(coins_in_pocket)
                coin_std     = np.std(coins_in_pocket)
                if coin_std == int(coin_std) and coin_mean != coin_median:
                    solution = tuple(sorted(coins_in_pocket))
                    if not solution in solutions:
                        print (f"\r{coins_in_pocket}: median = {coin_median}, mean = {coin_mean}, std = {coin_std}")
                        solutions.add(solution)
        
        results[n_coins] = solutions
        print("\r    ")
    return results

if __name__ == "__main__":
    find_coins()