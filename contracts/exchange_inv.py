#!/usr/bin/env python3

A = 85      #Higher A, more towards x+y=k
            #Lower A, more towards xy=k
N_COINS = 2 #diff tokens in pool


token0_pool = 800
token1_pool = 1200
amount_to_be_swapped = 5
    
def get_D():
    S = 0
    xp = [token0_pool, token1_pool]
    
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
    print("D =", D)
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

def get_dy(i, j, dx):
    xp = [token0_pool, token1_pool]

    x = xp[i] + dx
    print("x: ",x)
    y = get_y(i, j, x, xp)
    print("y: ",y)
    dy = (xp[j] - y)
    return dy

print("For", amount_to_be_swapped, "of token 1 you get", get_dy(1, 0, amount_to_be_swapped), "of token 0.")
