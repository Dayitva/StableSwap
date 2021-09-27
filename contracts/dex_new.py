#!/usr/bin/env python3
import smartpy as sp
fa12 = sp.io.import_script_from_url("https://smartpy.io/templates/FA1.2.py")


class USDTZ(fa12.FA12):
    """ Test USDTZ FA1.2 Token """
    pass

class KUSD(fa12.FA12):
    """ Test KUSD FA1.2 Token """
    pass


class Dex(sp.Contract):
    def __init__(self, x_address, y_address, _admin):
        self.init(
            invariant = sp.nat(0),
            N_COINS = sp.nat(2),
            A = sp.nat(4500),
            token_pool = sp.map(l={
                0: sp.record(address=x_address, pool=sp.nat(10000000)),
                1: sp.record(address=y_address, pool=sp.nat(8000000)),
            }),
            admin = _admin
        )

    def get_D(self):
        S = sp.local('S', sp.nat(0))
        pool_record = self.data.token_pool.values()

        _x = sp.local('_x', sp.nat(0))
        sp.while _x.value < sp.len(pool_record):
            S.value += self.data.token_pool[_x.value].pool
            _x.value += 1
            
        # sp.if S.value == 0:
        #     return 0

        Dprev = sp.local('Dprev', sp.nat(0))
        D = sp.local('D', S.value)
        
        Ann = sp.local('Ann', self.data.A * self.data.N_COINS)
        D_P = sp.local('D_P', D.value)
        
        # sp.trace("S")
        # sp.trace(S.value)
        # sp.trace("Ann")
        # sp.trace(Ann.value)

        sp.while abs(D.value - Dprev.value) > 1:
            D_P.value = D.value

            x = sp.local('x', sp.nat(0))
            sp.while x.value < sp.len(pool_record):
                D_P.value = D_P.value * D.value // (self.data.N_COINS * self.data.token_pool[x.value].pool)
                x.value += 1

            Dprev.value = D.value
            D1 = (Ann.value * S.value + D_P.value * self.data.N_COINS) * D.value
            D2 = ((sp.as_nat(Ann.value - 1) * D.value) + ((self.data.N_COINS + 1) * D_P.value))
            D.value = D1 // D2
            
            # sp.trace("D_P")
            # sp.trace(D_P.value)
            # sp.trace("Dprev")
            # sp.trace(Dprev.value)
            # sp.trace("D1")
            # sp.trace(D1)
            # sp.trace("D2")
            # sp.trace(D2)
            # sp.trace("D")
            # sp.trace(D.value)
        
        # sp.trace("D")
        # sp.trace(D.value)
            
        return D.value

    def get_y(self, i, j, x):
        D = sp.local('D1', self.get_D())
        # sp.trace(D.value)
        c = sp.local('c', D.value)
        # S_ = sp.local('S_', sp.nat(0))
        Ann = sp.local('Ann1', self.data.A * self.data.N_COINS)

        # _x = sp.local('_x1', sp.nat(0))
        # sp.for _i in sp.range(0, self.data.N_COINS, step=1):
        #     sp.if _i == i:
        #         _x.value = x
        #     sp.else:
        #         sp.if _i != j:
        #             _x.value = self.data.token_pool[_i].pool
        #     # sp.else:
        #     #     continue
        #     S_.value += _x.value
        #     c.value = c.value * D.value / (_x.value * self.data.N_COINS)
            
        # c.value = c.value * D.value / (Ann.value * self.data.N_COINS)
        
        c.value = D.value * D.value / (x * self.data.N_COINS)  
        c.value = c.value * D.value / (Ann.value * self.data.N_COINS)
        b = sp.local('b', x + D.value / Ann.value)  # - D
        
        y_prev = sp.local('y_prev', sp.nat(0))
        y = sp.local('y', D.value)
        
        sp.while abs(y.value - y_prev.value) > 1:
            y_prev.value = y.value
            y.value = (y.value*y.value + c.value) / sp.as_nat(2 * y.value + b.value - D.value)

        sp.trace(y.value)   
        return y.value

    @sp.entry_point
    def exchange(self, i, j, dx):
        sp.verify(i != j, "Same token")
        sp.verify(dx > 0, "Invalid Amount")
        sp.verify(i >= 0, "Invalid Token")
        sp.verify(j >= 0, "Invalid Token")
        sp.verify(i < self.data.N_COINS, "Invalid Token")
        sp.verify(j < self.data.N_COINS, "Invalid Token")

        x = self.data.token_pool[i].pool + dx
        y = self.get_y(i, j, x)
        sp.trace(y)        
        dy = sp.local('dy', sp.as_nat(self.data.token_pool[j].pool - y))

        self.data.token_pool[i].pool += dx
        self.data.token_pool[j].pool = sp.as_nat(self.data.token_pool[j].pool - dy.value)
        
        sp.trace(dy.value)
        # return dy


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
    usdtz = USDTZ(
        token_admin.address,
        config=fa12.FA12_config(support_upgradable_metadata=True),
        token_metadata=token1_metadata,
        contract_metadata=contract1_metadata
    )
    kusd = KUSD(
        token_admin.address,
        config=fa12.FA12_config(support_upgradable_metadata=True),
        token_metadata=token2_metadata,
        contract_metadata=contract2_metadata
    )

    scenario += usdtz
    scenario += kusd

    dex = Dex(
        x_address = kusd.address,
        y_address = usdtz.address,
        _admin = admin
    )
    
    scenario += dex
    # scenario += dex.get_D()
    scenario += dex.exchange(i=0, j=1, dx=5000)