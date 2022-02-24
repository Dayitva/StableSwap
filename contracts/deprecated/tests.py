#!/usr/bin/env python3

# Tweak the variables here
A = 85         
N_COINS = 2

token0_pool = 1000
token1_pool = 10

amount_to_be_swapped = 100000
amount0 = 0
amount1 = 1000
lp_token_amount = 100
TOKEN_POOL = [token0_pool, token1_pool]

# Functions
# def get_D(S):
#     if S == 0:
#         return 0

#     Dprev = 0
#     D = S
    
#     Ann = A * N_COINS
    
#     while abs(D - Dprev) > 0.001:
#         D_P = D
#         D_P = D_P * D / (N_COINS * TOKEN_POOL[0])
#         D_P = D_P * D / (N_COINS * TOKEN_POOL[1])
#         # print("D_P: ", D_P)
#         Dprev = D
#         D = (Ann * S + D_P * N_COINS) * D / ((Ann - 1) * D + (N_COINS + 1) * D_P)
#         # print("D:", D)
#         # print("Dprev:", Dprev)

#     return D

def get_D(S):
    S = 0
    xp = TOKEN_POOL
    
    for _x in xp:
        S += _x
        
    if S == 0:
        return 0

    Dprev = 0
    D = S
    
    Ann = A * N_COINS
    
    while abs(D - Dprev) > 1:
        D_P = D
        for x in xp:
            D_P = D_P * D / (N_COINS * x)

        Dprev = D
        D = (Ann * S + D_P * N_COINS) * D / ((Ann - 1) * D + (N_COINS + 1) * D_P)

    return D

def get_y(i, x, _xp):
    D = get_D(token0_pool + token1_pool)
   
    c = D
    S_ = 0
    Ann = A * N_COINS
    j = 1 - i
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
    
    while abs(y - y_prev) > 1:
        y_prev = y
        y = (y*y + c) / (2 * y + b - D)
        
    return y

def get_dy(i, dx):
    xp = [token0_pool, token1_pool]
    j = 1 - i
    x = xp[i] + dx
    # print("x: ",x)
    y = get_y(i, x, xp)
    # print("y: ",y)
    dy = (xp[j] - y)
    return dy

def add_liquidity_old(amount0, amount1):
    global TOKEN_POOL
    # Initial invariant
    token_supply_initial = token0_pool + token1_pool
    D0 = get_D(token_supply_initial)
    
    # Invariant after change
    TOKEN_POOL = [token0_pool + amount0, token1_pool + amount1]
    token_supply_final = token0_pool + token1_pool + amount0 + amount1
    D1 = get_D(token_supply_final)
    
    print(token0_pool, token1_pool)
    print("D0: ", D0)
    print("D1: ", D1)
    print("D1-D0: ", D1-D0)
    
    lp_amount = token_supply_initial * (D1 - D0)/D0
    
    return lp_amount

def add_liquidity(_amount0, _amount1):
    token_supply_initial = TOKEN_POOL[0] + TOKEN_POOL[1]
    D0 = get_D(0)
    
    TOKEN_POOL[0] = TOKEN_POOL[0] + _amount0
    TOKEN_POOL[1] = TOKEN_POOL[1] + _amount1
    
    D1 = get_D(0)
    
    lp_amount = token_supply_initial * (D1 - D0) / D0 

    return lp_amount

def remove_liquidity(_amount):
    token_supply = token0_pool + token1_pool

    value0 = token0_pool * _amount/token_supply    
    value1 = token1_pool * _amount/token_supply

    return value0, value1

# Print statements
# print("Liquibrium")
print("For", amount_to_be_swapped, "of token 1, you get", get_dy(1, amount_to_be_swapped), "of token 0.")
print("For", amount_to_be_swapped, "of token 0, you get", get_dy(0, amount_to_be_swapped), "of token 1.")
print("For adding", amount0, "of token 0 and", amount1, "of token 1, you get", add_liquidity(amount0, amount1), "lp tokens.")
TOKEN_POOL = [1000, 10]
print("For adding", amount1, "of token 0 and", amount0, "of token 1, you get", add_liquidity(amount0, amount1), "lp tokens.")
val0, val1 = remove_liquidity(lp_token_amount)
print("For removing", lp_token_amount, "lp tokens, you get", val0, "of token 0 and", val1, "of token 1.")
print()

# print("Quipuswap")
# print("For", amount_to_be_swapped, "of token 1 you get", token0_pool-(token0_pool*token1_pool)/(token1_pool+amount_to_be_swapped), "of token 0.")
# print("For", amount_to_be_swapped, "of token 0 you get", token1_pool-(token0_pool*token1_pool)/(token0_pool+amount_to_be_swapped), "of token 1.")
# print()