#!/usr/bin/env python3

A = 85                          # Higher A, more towards x+y=k | Lower A, more towards xy=k
N_COINS = 2                     # Number of tokens in pool
FEE = 15                        # Fee for exchanges
ADMIN_FEE_POOL = [0, 0]         # Counter to track Admin fee 
TOKEN_POOL = [1000, 10]         # Liquidity Pools
LP_SUPPLY = sum(TOKEN_POOL)
    
def get_D():
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
    
    while abs(y - y_prev) > 1:
        y_prev = y
        y = (y*y + c) / (2 * y + b - D)
        
    return y

def xchg(i, dx):
    global ADMIN_LP_SUPPLY
    global LP_SUPPLY
    j = 1 - i
    xp = TOKEN_POOL
    x = TOKEN_POOL[i] + dx
    y = get_y(i, j, x, xp)
    dy = TOKEN_POOL[j] - y
    fee_collected = (dy * FEE) / 10000
    dy = dy - fee_collected
    # ADMIN_FEE_POOL[j] += (fee_collected / 2)

    # ADMIN_LP_SUPPLY += (fee_collected / 2)/(TOKEN_POOL[0] + TOKEN_POOL[1] + (fee_collected / 2))
    # LP_SUPPLY += (fee_collected / 2)/(TOKEN_POOL[0] + TOKEN_POOL[1] + (fee_collected / 2))

    TOKEN_POOL[i] += dx
    TOKEN_POOL[j] = TOKEN_POOL[j] - dy
    return dy

def add_liquidity(_amount0, _amount1):
    global LP_SUPPLY
    token_supply_initial = TOKEN_POOL[0] + TOKEN_POOL[1]
    D0 = get_D()
    
    TOKEN_POOL[0] = TOKEN_POOL[0] + _amount0
    TOKEN_POOL[1] = TOKEN_POOL[1] + _amount1
    
    D1 = get_D()

    # print("D0:", D0)
    # print("D1:", D1)
    
    lp_amount = token_supply_initial * (D1 - D0) / D0 
    LP_SUPPLY += lp_amount

    return lp_amount

def remove_liquidity(_amount):
    global LP_SUPPLY
    # global ADMIN_LP_SUPPLY
    # global ADMIN_FEE_POOL
    token_supply = TOKEN_POOL[0] + TOKEN_POOL[1]

    print(LP_SUPPLY)
    value0 = (TOKEN_POOL[0] - ADMIN_FEE_POOL[0]) * _amount / LP_SUPPLY
    TOKEN_POOL[0] = TOKEN_POOL[0] - value0

    value1 = (TOKEN_POOL[1] - ADMIN_FEE_POOL[1]) * _amount / LP_SUPPLY
    TOKEN_POOL[1] = TOKEN_POOL[1] - value1

    LP_SUPPLY = LP_SUPPLY - _amount
    # if admin:
    #     ADMIN_LP_SUPPLY = ADMIN_LP_SUPPLY - _amount
    #     ADMIN_FEE_POOL[0] = 0
    #     ADMIN_FEE_POOL[1] = 0
    return value0, value1

### TESTS BEGIN HERE ###

# swap_amounts = [5000, 4000, 3000, 2000]

# for i in swap_amounts:
#     amount_to_be_swapped = i
#     print("For", amount_to_be_swapped, "of token 0 you get", xchg(0, amount_to_be_swapped), "of token 1.")
#     print(TOKEN_POOL)
#     print(ADMIN_FEE_POOL)

# for i in swap_amounts:
#     amount_to_be_swapped = i
#     print("For", amount_to_be_swapped, "of token 1 you get", xchg(1, amount_to_be_swapped), "of token 0.") 
#     print(TOKEN_POOL)
#     print(ADMIN_FEE_POOL)

# print(TOKEN_POOL)
# print("For", 0, "of token 0 and", 1000, "of token 1, you get", add_liquidity(0, 1000), " LP tokens.")

# print(TOKEN_POOL)
# print("For", 1230, "of LP tokens you get", remove_liquidity(1230), "tokens.")

# print(TOKEN_POOL)
# print("For", 1000, "of token 0 you get", xchg(0, 1000), "of token 1.") 

# print(TOKEN_POOL)
# print("For", 1000, "of token 0 you get", xchg(0, 1000), "of token 1.") 

print(TOKEN_POOL)
print("For", 1000, "of token 1 you get", xchg(1, 1000), "of token 0.") 

print(TOKEN_POOL)
print("For", 100000, "of LP tokens you get", remove_liquidity(100000), "tokens.")

print(TOKEN_POOL)
print(ADMIN_FEE_POOL)

for i, j in zip(TOKEN_POOL, ADMIN_FEE_POOL):
    print(i - j)
    
# print("For", 5_000, "of token 1 you get", add_liquidity(1000, 0), " LP tokens.")
  
### Track & Compare Results against Log ###

    # FIRST SET OF TESTS
    # 10.480597358646_963242
    # 10.480597358646_963242
    # 10.480597358646_856
    # 10.480597358646_856

    # SECOND SET OF TESTS
    # 10.5193928_88786877
    # 10.5193928_98190833429
    # 10.480597358646_856
    # 10.480597358646_963242

    # THIRD SET OF TESTS
    # 10.5193928_98190833429
    # 10.5193928_88786877
    # 10.480597358646_963242
    # 10.480597358646_856