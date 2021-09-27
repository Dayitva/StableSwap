import smartpy as sp

def get_token_list():
    return [
        sp.record(name="USDTz", pool=1210),
        sp.record(name="kUSD", pool=1200),
    ]

class Dex(sp.Contract):
    def __init__(self):
        self.init(
            token_pool = get_token_list(),

        )
    
    def get_D(self):
        S = 0
        xp = self.data.token_pool
        for _x in xp:
            S += _x.pool
        sp.if S == 0:
        

    @sp.entry_point
    def exchange(self, params):
        """ 
        params.i: Index of the first coin.
        params.j: Index of second coin.
        params.dx: Min. tokens out.
        """
        self.set_type(params, sp.TRecord(
            i = sp.TNat,
            j = sp.TNat,
            dx = sp.TNat,
        ))
