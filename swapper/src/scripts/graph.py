import matplotlib.pyplot as plt
import numpy as np


KUSD_POOL = 1_255_718.35 
USDTZ_POOL = 1_145_401.29
token_pool = [
  {'pool': KUSD_POOL, 'name': 'KUSD'},
  {'pool': USDTZ_POOL, 'name': 'USDtz'}
]
invariant = KUSD_POOL * USDTZ_POOL

def exchange(i, j, dx):
  """ Exchanging `i` into `j`, `dx` amount of tokens. """
  from_token = token_pool[i]
  to_token = token_pool[j]

  new_from_token = from_token['pool'] + dx
  new_to_token = invariant / (new_from_token)
  token_out = to_token['pool'] - new_to_token
  return token_out

A = 50
N_COINS = 2
    
def get_D():
  S = 0
  xp = [KUSD_POOL, USDTZ_POOL]
  
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
  # print("D =", D)
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

def get_dy(i, j, dx):
  xp = [KUSD_POOL, USDTZ_POOL]

  x = xp[i] + dx
  # print("x: ",x)
  y = get_y(i, j, x, xp)
  # print("y: ",y)
  dy = (xp[j] - y)
  return dy


x = range(1000, 1_000_000, 2000)
cpmm = []
curve = []
for i in x:
  cpmm.append(i - exchange(0, 1, i))
  curve.append(i - get_dy(0, 1, i))

plt.xlabel("Amount To Exchange")
plt.ylabel("Slippage")
plt.title("CPMM vs Liquibrium")

plt.plot(x, cpmm, label="CPMM")
plt.plot(x, curve, label="Liquibrium")
plt.ticklabel_format(useOffset=False, style='plain')
plt.legend()
plt.show()