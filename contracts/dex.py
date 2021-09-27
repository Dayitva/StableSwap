#!/usr/bin/env python3
import smartpy as sp
fa12 = sp.io.import_script_from_url("https://smartpy.io/templates/FA1.2.py")

class Token(fa12.FA12):
    """ Test FA1.2 Token """
    pass

# A = 85       #Higher A, more towards x+y=k
#              #Lower A, more towards xy=k
# N_COINS = 2  #diff tokens in pool

# def get_token_list():
#     return [
#         1210,
#         1200
#     ]

# token_pool = [1210, 1200]
# amount_to_be_swapped = 5
# coins = ['USDtz', 'kUSD']
# amount_to_be_added = 5

class Dex(sp.Contract):
    def __init__(self, admin, token1_address, token2_address):
        self.init(
            # token_pool = get_token_list(),
            admin = admin,
            N_COINS = sp.nat(2),
            A = sp.nat(85),
            token_pool = sp.map(l={
                0: sp.record(address=token1_address, pool=sp.nat(10000000)),
                1: sp.record(address=token2_address, pool=sp.nat(8000000)),
            })
            # USDtz_balances = sp.big_map(tkey = sp.TAddress, 
            #                             tvalue = sp.TInt),
            # kUSD_balances = sp.big_map(tkey = sp.TAddress, 
            #                             tvalue = sp.TInt)
        )

    def get_D(self):
        S = 0
        xp = self.data.token_pool
        
        sp.for _x in xp:
            S += _x
            
        sp.if S == 0:
            return 0

        Dprev = 0
        D = S
        
        Ann = self.data.A * self.data.N_COINS
        
        sp.while abs(D - Dprev) > 1:
            D_P = sp.local('D_P', D)
            sp.for x in xp:
                D_P.value = D_P.value * D / (self.data.N_COINS * x.pool)
            Dprev = D
            D = (Ann * S + D_P.value * self.data.N_COINS) * D / ((sp.as_nat(Ann - 1) * D) + (self.data.N_COINS + 1 * D_P.value))

        return D

    
    def get_y(self, i, j, x, _xp):
        D = self.get_D()
        c = D
        S_ = 0
        Ann = A * N_COINS

        _x = 0
        sp.for _i in range(N_COINS):
            sp.if _i == i:
                _x = x
            sp.else:
                sp.if _i != j:
                    _x = _xp[_i]
            sp.else:
                continue
            S_ += _x
            c = c * D / (_x * N_COINS)
            
        c = c * D / (Ann * N_COINS)
        b = S_ + D / Ann  # - D
        y_prev = 0
        y = D
        
        sp.while abs(y - y_prev) > 1:
            y_prev = y
            y = (y*y + c) / (2 * y + b - D)
            
        return y

    @sp.entry_point
    def exchange(self, i, j, dx):
        sp.verify(i != j, "Same token")
        sp.verify(dx > 0, "Invalid Amount")
        sp.verify(i >= 0, "Invalid Token")
        sp.verify(j >= 0, "Invalid Token")
        sp.verify(i < self.data.N_COINS, "Invalid Token")
        sp.verify(j < self.data.N_COINS, "Invalid Token")

        xp = self.data.token_pool

        x = xp[i] + dx
        y = self.get_y(i, j, x, xp)
        dy = (xp[j] - y)

        self.data.token_pool[i].pool += dx
        self.data.token_pool[j].pool -= dy
        return dy

    # def add_liquidity(i, dx):
    #     token_supply = 0
    #     sp.for k in self.data.token_pool:
    #         token_supply += k

    #     # Initial invariant
    #     D0 = 0
    #     sp.if token_supply > 0:
    #         D0 = get_D()

    #     # Take coins from the sender
    #     sp.if dx > 0:
    #         ### TODO Transfer tokens to our token addresses
    #         pass
            
    #     self.data.token_pool[i] = self.data.token_pool[i] + dx

    #     # Invariant after change
    #     D1 = get_D()
    #     return D1 - D0

    # def remove_liquidity(dx):
    #     token_supply = 0
    #     sp.for k in self.data.token_pool:
    #         token_supply += k

    ### TODO Make on contract changes & transfer to LP address(es)
    @sp.add_test(name = "StableSwap")
    def test():
        admin = sp.address("tz1d6ZpPZj4Xb9tPbLcnSnRN2VCxRdSz1i4o")
        alice = sp.test_account("Alice")
        bob   = sp.test_account("Robert")
        token_admin = sp.test_account("Token Admin")

        scenario = sp.test_scenario()

        token1_metadata = {
            "decimals": "18",
            "name": "USD Tez",
            "symbol": "USDTz",
            "icon": 'https://smartpy.io/static/img/logo-only.svg'
        }
        contract1_metadata = {
            "": "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
        }
        token2_metadata = {
            "decimals": "18",
            "name": "Kolibri USD",
            "symbol": "KUSD",
            "icon": 'https://smartpy.io/static/img/logo-only.svg'
        }
        contract2_metadata = {
            "": "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
        }
        usdtz = Token(
            token_admin.address,
            config=fa12.FA12_config(support_upgradable_metadata=True),
            token_metadata=token1_metadata,
            contract_metadata=contract1_metadata
        )
        kusd = Token(
            token_admin.address,
            config=fa12.FA12_config(support_upgradable_metadata=True),
            token_metadata=token2_metadata,
            contract_metadata=contract2_metadata
        )

        scenario += usdtz
        scenario += kusd

        dex = Dex(
            admin = admin,
            token1_address = usdtz.address,
            token2_address = kusd.address,
        )
        
        scenario += dex
        scenario += dex.get_D()
        # scenario += dex.exchange(address = alice.address, i = 0, j = 1, dx = 10).run(sender = alice, valid=True)


# print("For", amount_to_be_swapped, "of token 1 you get", exchange(1, 0, amount_to_be_swapped), "of token 0.")
# print("For", amount_to_be_swapped, "of token 1 you get", exchange(1, 0, amount_to_be_swapped), "of token 0.")

# print("For providing", amount_to_be_added, "of token 0, you make a profit of", amount_to_be_added - add_liquidity(1, amount_to_be_added), ".")
