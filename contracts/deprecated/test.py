A = 4500
N_COINS = 2
PRECISION = 10 ** 18
A_MULTIPLIER = 10000
MIN_A = (N_COINS**N_COINS) * A_MULTIPLIER / 100
MAX_A = (N_COINS**N_COINS) * A_MULTIPLIER * 10000

token1_pool = 80000
token2_pool = 100000
amount_to_be_swapped = 1
    
def get_D():
    S = 0
    xp = [token1_pool, token2_pool]
    
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
            D_P = D_P * D // (N_COINS * x + 1) # +1 is to prevent /0
        Dprev = D
        D = (Ann * S + D_P * N_COINS) * D // ((Ann - 1) * D + (N_COINS + 1) * D_P)

    return D

def get_y(i, j, x):
    _xp = [token1_pool, token2_pool]
    D = get_D()
    print("D =", D)
    c = D
    S_ = 0
    Ann = A * (N_COINS ** N_COINS)

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

#print("For", amount_to_be_swapped, "kUSD, you get", get_y(1, 1, amount_to_be_swapped), "USDtz")
# print("For", amount_to_be_swapped, "you get", get_y(0, 1, 100))
print(get_D())