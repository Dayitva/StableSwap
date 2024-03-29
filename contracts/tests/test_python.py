#!/usr/bin/env python3
import random

A = 85                          # Higher A, more towards x+y=k | Lower A, more towards xy=k
N_COINS = 2                     # Number of tokens in pool
FEE = 15                        # Fee for exchanges
ADMIN_FEE_POOL1 = [0, 0]         # Counter to track Admin fee
ADMIN_FEE_POOL2 = [0, 0]         # Counter to track Admin fee
TOKEN_POOL1 = [50000, 50000]         # Liquidity Pools
TOKEN_POOL2 = [1000, 1000]         # Liquidity Pools
LP_SUPPLY1 = sum(TOKEN_POOL1)
LP_SUPPLY2 = sum(TOKEN_POOL2)
FEE_COLLECTED = 0


def get_D(xp):
    S = 0

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
        D = (Ann * S + D_P * N_COINS) * D / \
            ((Ann - 1) * D + (N_COINS + 1) * D_P)

    return D


def get_y(i, j, x, _xp):
    D = get_D(_xp)
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


def xchg(i, dx, xp, afp, range=False):
    global FEE_COLLECTED

    j = 1 - i
    x = xp[i] + dx
    dy = 0

    if range:
        if x < 0.75 * sum(TOKEN_POOL2) and x > 0.25 * sum(TOKEN_POOL2):
            # print("Range Pool")
            dy = dx
        else:
            y = get_y(i, j, x, xp)
            dy = xp[j] - y

    else:
        y = get_y(i, j, x, xp)
        dy = xp[j] - y

    fee_collected = (dy * FEE) / 10000
    dy = dy - fee_collected
    afp[j] += (fee_collected / 2)
    FEE_COLLECTED += (fee_collected / 2)

    xp[i] += dx
    xp[j] = xp[j] - dy
    return dy, afp


def add_liquidity(_amount0, _amount1, xp, lps):
    global FEE_COLLECTED

    token_supply_initial = xp[0] + xp[1]
    D0 = get_D(xp)

    xp[0] += _amount0
    xp[1] += _amount1

    D1 = get_D(xp)

    # print("D0:", D0)
    # print("D1:", D1)

    lp_amount = (token_supply_initial - FEE_COLLECTED) * (D1 - D0) / D0
    lps += lp_amount

    return lp_amount, lps


def remove_liquidity(_amount, xp, afp, lps):
    global FEE_COLLECTED

    value0 = (xp[0] - afp[0]) * _amount / lps
    xp[0] = xp[0] - value0

    value1 = (xp[1] - afp[1]) * _amount / lps
    xp[1] = xp[1] - value1

    FEE_COLLECTED -= FEE_COLLECTED * (_amount / lps)
    lps -= _amount

    return value0, value1, lps

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

lp_tokens1, LP_SUPPLY1 = add_liquidity(50000, 50000, TOKEN_POOL1, LP_SUPPLY1)
print("For", 50000, "of token 0 and", 50000, "of token 1, you get", lp_tokens1, "LP tokens.")
print(LP_SUPPLY1)
print(TOKEN_POOL1)

_amount1 = xchg(0, 10000, TOKEN_POOL1, ADMIN_FEE_POOL1)
print("For", 10000, "of token", 0, "you get", _amount1, "of token", 0)
print(LP_SUPPLY1)
print(TOKEN_POOL1)

_amount1 = xchg(1, 20000, TOKEN_POOL1, ADMIN_FEE_POOL1)
print("For", 20000, "of token", 1, "you get", _amount1, "of token", 1)
print(LP_SUPPLY1)
print(TOKEN_POOL1)

_amount1 = xchg(0, 9999.935, TOKEN_POOL1, ADMIN_FEE_POOL1)
print("For", 9999.935, "of token", 0, "you get", _amount1, "of token", 0)
print(LP_SUPPLY1)
print(TOKEN_POOL1)

print("Fee:")
print(FEE_COLLECTED)

lp_tokens1, LP_SUPPLY1 = add_liquidity(100000, 100000, TOKEN_POOL1, LP_SUPPLY1)
print("For", 100000, "of token 0 and", 100000, "of token 1, you get", lp_tokens1, "LP tokens.")
print(LP_SUPPLY1)
print(TOKEN_POOL1)

print(FEE_COLLECTED)
_val0, _val1, LP_SUPPLY1 = remove_liquidity(199970.00909642936, TOKEN_POOL1, ADMIN_FEE_POOL1, LP_SUPPLY1)
_amount1 = _val0 + _val1
print("For", 199970.00909642936, "of LP tokens you get", _amount1, "tokens.")
print(LP_SUPPLY1)
print(TOKEN_POOL1)
print(FEE_COLLECTED)

print(FEE_COLLECTED)
_val0, _val1, LP_SUPPLY1 = remove_liquidity(199999.99999999997, TOKEN_POOL1, ADMIN_FEE_POOL1, LP_SUPPLY1)
_amount1 = _val0 + _val1
print("For", 199999.99999999997, "of LP tokens you get", _amount1, "tokens.")
print(LP_SUPPLY1)
print(TOKEN_POOL1)
print(FEE_COLLECTED)

# LP_AMOUNTS1 = []
# LP_AMOUNTS2 = []

# NO_OF_TRANSACTIONS = 1000
# ADD_LIQUIDITY_SIZE = 1000
# EXCHANGE_SIZE = 100000

# print("\n\n Adding Liquidity \n\n")
# for i in range(NO_OF_TRANSACTIONS):
#     # print(TOKEN_POOL)
#     _amount0 = random.randint(0, ADD_LIQUIDITY_SIZE)
#     _amount1 = random.randint(0, ADD_LIQUIDITY_SIZE)
#     lp_tokens1, LP_SUPPLY1 = add_liquidity(
#         _amount0, _amount1, TOKEN_POOL1, LP_SUPPLY1)
#     lp_tokens2, LP_SUPPLY2 = add_liquidity(
#         _amount0, _amount1, TOKEN_POOL2, LP_SUPPLY2)
#     LP_AMOUNTS1.append(lp_tokens1)
#     LP_AMOUNTS2.append(lp_tokens2)
#     # print("For", _amount0, "of token 0 and", _amount1, "of token 1, you get", lp_tokens, " LP tokens.")

# print(TOKEN_POOL1)
# print(TOKEN_POOL2)

# print("\n\n Exchanging \n\n")
# for i in range(NO_OF_TRANSACTIONS):
#     # print(TOKEN_POOL)
#     _amount0 = random.randint(0, EXCHANGE_SIZE)
#     index = random.randint(0, 1)
#     _amount1 = xchg(index, _amount0, TOKEN_POOL1, ADMIN_FEE_POOL1)
#     _amount2 = xchg(index, _amount0, TOKEN_POOL2, ADMIN_FEE_POOL2, range=True)
#     # print("For", _amount0, "of token", index, "you get", _amount1, "of token", 1 - index)

# print("Curve     ", TOKEN_POOL1, sum(TOKEN_POOL1))
# print("Range Pool", TOKEN_POOL2, sum(TOKEN_POOL2))

# print("\n\n Removing Liquidity \n\n")
# for i in range(NO_OF_TRANSACTIONS):
#     # print(TOKEN_POOL)
#     _amount0 = LP_AMOUNTS1[i]
#     _amount1 = LP_AMOUNTS2[i]
#     _val0, _val1, LP_SUPPLY1 = remove_liquidity(
#         _amount0, TOKEN_POOL1, ADMIN_FEE_POOL1, LP_SUPPLY1)
#     _val0, _val1, LP_SUPPLY2 = remove_liquidity(
#         _amount1, TOKEN_POOL2, ADMIN_FEE_POOL2, LP_SUPPLY2)
#     # print("For", _amount0, "of LP tokens you get", _amount1, "tokens.")

# print(TOKEN_POOL1)
# print(TOKEN_POOL2)

# print("\n\n Admin Claim and Removal \n\n")

# print("For", 2000, "of LP tokens you get", remove_liquidity(
#     2000, TOKEN_POOL1, ADMIN_FEE_POOL1, LP_SUPPLY1), "tokens.")
# print("For", 2000, "of LP tokens you get", remove_liquidity(
#     2000, TOKEN_POOL2, ADMIN_FEE_POOL2, LP_SUPPLY2), "tokens.")

# print("TOKEN_POOL1    ", TOKEN_POOL1)
# print("ADMIN_FEE_POOL1", ADMIN_FEE_POOL1)
# print("TOKEN_POOL2    ", TOKEN_POOL2)
# print("ADMIN_FEE_POOL2", ADMIN_FEE_POOL2)

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