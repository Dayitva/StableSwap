
KUSD_POOL = 1000000 
USDTZ_POOL = 1000000 
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


for i in range(1000, 100000, 5000):
	print(i, exchange(0, 1, i))
