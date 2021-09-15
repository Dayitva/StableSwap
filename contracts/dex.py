#!/usr/bin/env python3

A = 85       #Higher A, more towards x+y=k
             #Lower A, more towards xy=k
N_COINS = 2  #diff tokens in pool


token_pool = [1210, 1200]
amount_to_be_swapped = 5
coins = ['USDtz', 'kUSD']
amount_to_be_added = 5

def get_D():
    S = 0
    xp = token_pool
    
    for _x in xp:
        S += _x
        
    if S == 0:
        return 0

    Dprev = 0
    D = S
    
    Ann = A * N_COINS
    
    while abs(D - Dprev) > 0.001:
        D_P = D
        for x in xp:
            D_P = D_P * D / (N_COINS * x)
        Dprev = D
        D = (Ann * S + D_P * N_COINS) * D / ((Ann - 1) * D + (N_COINS + 1) * D_P)

    return D

def get_y(i, j, x, _xp):
    D = get_D()
    c = D
    S_ = 0
    Ann = A * N_COINS

    _x = 0
    for _i in range(N_COINS):
        if _i == i:
            _x = x
        elif _i != j:
            _x = _xp[_i]
        else:
            continue
        S_ += _x
        c = c * D / (_x * N_COINS)
        
    c = c * D / (Ann * N_COINS)
    b = S_ + D / Ann  # - D
    y_prev = 0
    y = D
    
    while abs(y - y_prev) > 0.001:
        y_prev = y
        y = (y*y + c) / (2 * y + b - D)
        
    return y

def exchange(i, j, dx):
    xp = token_pool

    x = xp[i] + dx
    y = get_y(i, j, x, xp)
    dy = (xp[j] - y)

    token_pool[i] += dx
    token_pool[j] -= dy
    return dy

def add_liquidity(i, dx):
    token_supply = 0
    for k in token_pool:
        token_supply += k

    # Initial invariant
    D0 = 0
    if token_supply > 0:
        D0 = get_D()

    # Take coins from the sender
    if dx > 0:
        ### TODO Transfer tokens to our token addresses
        pass
        
    token_pool[i] = token_pool[i] + dx

    # Invariant after change
    D1 = get_D()
    return D1 - D0

def remove_liquidity(dx):
    token_supply = 0
    for k in token_pool:
        token_supply += k

   ### TODO Make on contract changes & transfer to LP address(es)


print("For", amount_to_be_swapped, "of token 1 you get", exchange(1, 0, amount_to_be_swapped), "of token 0.")
print("For", amount_to_be_swapped, "of token 1 you get", exchange(1, 0, amount_to_be_swapped), "of token 0.")

print("For providing", amount_to_be_added, "of token 0, you make a profit of", amount_to_be_added - add_liquidity(1, amount_to_be_added), ".")
