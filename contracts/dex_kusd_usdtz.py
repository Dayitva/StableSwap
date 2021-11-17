import smartpy as sp
from contracts.utility import TokenUtility
fa12 = sp.io.import_script_from_url("https://smartpy.io/templates/FA1.2.py")

class Token(fa12.FA12):
    """ Test FA1.2 Token """
    pass


class Dex(sp.Contract, TokenUtility):
    def __init__(self, x_address, y_address, _lp_token, _admin):
        """
        x_address: The address of the x token
        y_address: The address of the y token
        _lp_token: The address of the LP token
        _admin: The address of the admin
        N_COINS: The number of coins in the pool
        A: Amplification factor
        fee: The fee for the transaction
        """
        self.init(
            N_COINS=sp.nat(2),
            A=sp.nat(85),
            token_pool=sp.map(l={
                0: sp.record(address=x_address, pool=sp.nat(0), fa2=False, token_id=0, decimals = 1000000000000000000),
                1: sp.record(address=y_address, pool=sp.nat(0), fa2=False, token_id=0, decimals = 1000000),
            }),
            admin=_admin,
            eighteen = 1000000000000000000,
            fee = sp.nat(15),
            admin_fee_pool=sp.map(l={
                0: sp.record(address=x_address, pool=sp.nat(0)),
                1: sp.record(address=y_address, pool=sp.nat(0)),
            }),
            lp_token=_lp_token,
        )

    def mint_lp(self, amount):
        """Mint `amount` LP tokens to `sp.sender` account."""
        transfet_type = sp.TRecord(
            address=sp.TAddress,
            value=sp.TNat,
        )
        transfer_value = sp.record(
            address=sp.sender,
            value=amount,
        )
        contract = sp.contract(
            transfet_type,
            self.data.lp_token,
            'mint'
        ).open_some()
        sp.transfer(transfer_value, sp.mutez(0), contract)

    def burn_lp(self, amount):
        """ Burn `amount` LP Tokens. """
        transfet_type = sp.TRecord(
            address=sp.TAddress,
            value=sp.TNat,
        )
        transfer_value = sp.record(
            address=sp.sender,
            value=amount,
        )
        contract = sp.contract(
            transfet_type,
            self.data.lp_token,
            'burn'
        ).open_some()
        sp.transfer(transfer_value, sp.mutez(0), contract)
    
    def transferToTokenId(self, _from, _to, _amount, _token_id=0):
        token = self.data.token_pool.get(_token_id)
        sp.if token.fa2:
            self.fa2Transfer(_from, _to, _amount, token.token_id, token.address)
        sp.else:
            self.fa12Transfer(_from, _to, _amount, token.address)

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

        # sp.trace({"S": S.value})
        # sp.trace({"Ann": Ann.value})

        sp.while abs(D.value - Dprev.value) > 1:
            D_P.value = D.value
            x = sp.local('x', sp.nat(0))
            sp.while x.value < sp.len(pool_record):
                D_P.value = D_P.value * \
                    D.value // (self.data.N_COINS *
                                self.data.token_pool[x.value].pool)
                x.value += 1
            Dprev.value = D.value
            D1 = (Ann.value * S.value + D_P.value * self.data.N_COINS) * D.value
            D2 = ((sp.as_nat(Ann.value - 1) * D.value) +
                  ((self.data.N_COINS + 1) * D_P.value))
            D.value = D1 // D2

            # sp.trace({"D_P": D_P.value})
            # sp.trace({"Dprev": Dprev.value})
            # sp.trace({"D1": D1})
            # sp.trace({"D2": D2})
            # sp.trace({"D": D.value})

        # sp.trace({"D": D.value})

        return D.value

    def get_y(self, i, j, x):
        D = sp.local('D1', self.get_D())
        # sp.trace({"D": D.value})
        c = sp.local('c', D.value)
        Ann = sp.local('Ann1', self.data.A * self.data.N_COINS)
        
        # S_ = sp.local('S_', sp.nat(0))
        # _x1 = sp.local('_x1', sp.nat(0))
        # sp.for _i in sp.range(0, self.data.N_COINS, step=1):
        #     sp.if _i == i:
        #         _x1.value = x
        #     sp.else:
        #         sp.if _i != j:
        #             _x1.value = self.data.token_pool[_i].pool
        #     # sp.else:
        #     #     continue
        #     S_.value += _x1.value
        #     c.value = c.value * D.value / (_x1.value * self.data.N_COINS)

        # c.value = c.value * D.value / (Ann.value * self.data.N_COINS)

        c.value = D.value * D.value / (x * self.data.N_COINS)
        c.value = c.value * D.value / (Ann.value * self.data.N_COINS)
        b = sp.local('b', x + D.value / Ann.value)  # - D

        y_prev = sp.local('y_prev', sp.nat(0))
        y = sp.local('y', D.value)

        sp.while abs(y.value - y_prev.value) > 1:
            y_prev.value = y.value
            y.value = (y.value*y.value + c.value) / \
                sp.as_nat((2 * y.value + b.value) - D.value)
        # sp.trace({"y": y.value})
        return y.value

    @sp.entry_point
    def update_fee(self, new_fee):
        sp.verify(sp.sender == self.data.admin, "NOT_ADMIN")
        self.data.fee = new_fee

    @sp.entry_point
    def admin_claim(self):
         sp.verify(sp.sender == self.data.admin, "NOT_ADMIN")
        # CHECK
        # sp.trace({"0 admin fee" : self.data.admin_fee_pool[0].pool})
        # sp.trace({"1 admin fee" : self.data.admin_fee_pool[1].pool})
        sp.if self.data.admin_fee_pool[0].pool > 0:
            self.transfer(
            from_=sp.self_address,
            to=sp.sender,
            amount=self.data.admin_fee_pool[0].pool/(self.data.eighteen/self.data.token_pool[0].decimals),
            token_id=0
            )
        sp.if self.data.admin_fee_pool[1].pool > 0:
            self.transfer(
            from_=sp.self_address,
            to=sp.sender,
            amount=self.data.admin_fee_pool[1].pool/(self.data.eighteen/self.data.token_pool[1].decimals),
            token_id=1
            )
        # /(self.data.eighteen/self.data.token_pool[0].decimals)
        # Update Pools
        self.data.token_pool[0].pool = sp.as_nat(self.data.token_pool[0].pool - self.data.admin_fee_pool[0].pool)
        self.data.token_pool[1].pool = sp.as_nat(self.data.token_pool[0].pool - self.data.admin_fee_pool[1].pool)
        # Set admin fee 0
        self.data.admin_fee_pool[0].pool = sp.nat(0)
        self.data.admin_fee_pool[0].pool = sp.nat(0)

    @sp.entry_point
    def set_lp_address(self, address: sp.TAddress):
        sp.verify(sp.sender == self.data.admin, "NOT_ADMIN")
        self.data.lp_token = address

    @sp.entry_point
    def initialize_exchange(self, token1_amount, token2_amount):
        """ Initialize the exchange with the token2 and token2 amounts."""
        sp.verify(token1_amount > sp.nat(0), "INVALID_AMOUNT")
        sp.verify(token2_amount > sp.nat(0), "INVALID_AMOUNT")
        
        # Transfer tokens from the user's account to our contract's address.
        self.transferToTokenId(
            _from=sp.sender,
            _to = sp.self_address,
            _amount=token1_amount,
            _token_id=0
        )
        self.transferToTokenId(
            _from=sp.sender,
            _to = sp.self_address,
            _amount=token2_amount,
            _token_id=1
        )
        
        # Update the storage.
        self.data.token_pool[0].pool = token1_amount*(self.data.eighteen/self.data.token_pool[0].decimals)
        self.data.token_pool[1].pool = token2_amount*(self.data.eighteen/self.data.token_pool[1].decimals)
        self.mint_lp(token1_amount*(self.data.eighteen/self.data.token_pool[0].decimals) + token2_amount*(self.data.eighteen/self.data.token_pool[1].decimals))

    @sp.entry_point
    def update_A(self, new_A):
        sp.verify(sp.sender == self.data.admin, "Permission denied")
        self.data.A = new_A

    @sp.entry_point
    def exchange(self, i, j, dx):
        sp.verify(i != j, "Same token")
        sp.verify(dx > 0, "Invalid Amount")
        sp.verify(i >= 0, "Invalid Token")
        sp.verify(j >= 0, "Invalid Token")
        sp.verify(i < self.data.N_COINS, "Invalid Token")
        sp.verify(j < self.data.N_COINS, "Invalid Token")
        
        self.transferToTokenId(
            _from=sp.sender,
            _to=sp.self_address,
            _amount=dx,
            _token_id=i
        )
        
        x = self.data.token_pool[i].pool + dx
        y = self.get_y(i, j, x)
        dy = sp.local('dy', sp.as_nat(self.data.token_pool[j].pool - y))
        fee_collected = sp.local('fee', ((dy.value * self.data.fee) / 10000))
        dy.value = sp.as_nat(dy.value - fee_collected.value)
        self.data.admin_fee_pool[j].pool += (fee_collected.value / 2)
        self.data.token_pool[i].pool += dx
        self.data.token_pool[j].pool = sp.as_nat(
            self.data.token_pool[j].pool - dy.value)

        dy.value /= (self.data.eighteen/self.data.token_pool[j].decimals)
        # sp.trace(dy.value)
        # return dy
        sp.if dy.value > 0:
            self.transferToTokenId(
                _from=sp.self_address,
                _to=sp.sender,
                _amount=dy.value,
                _token_id=j
            )

    @sp.entry_point
    def add_liquidity(self, i, dx):
        """
        """
        pool_record = self.data.token_pool.values()
        token_supply = sp.local('ts', sp.nat(0))
        _x2 = sp.local('_x2', sp.nat(0))
        sp.while _x2.value < sp.len(pool_record):
            token_supply.value += self.data.token_pool[_x2.value].pool
            _x2.value += 1
        # Initial invariant
        D0 = sp.local('D0', sp.nat(0))
        sp.if token_supply.value > 0:
            D0.value = self.get_D()

        self.data.token_pool[i].pool = self.data.token_pool[i].pool + dx
        # Invariant after change
        D1 = sp.local('D1', self.get_D())
        # sp.trace({'D1': D1.value})
        # sp.trace({'D0': D0.value})
        sp.trace({"D1-D0": D1.value-D0.value})
        lp_amount = token_supply.value * sp.as_nat(D1.value - D0.value) / D0.value 
        sp.trace({"lp_amount": lp_amount})
        sp.if lp_amount > sp.nat(0):
            self.mint_lp(lp_amount)

        dx /= (self.data.eighteen/self.data.token_pool[i].decimals)
        
        # Take coins from the sender
        self.transferToTokenId(
            _from=sp.sender,
            _to=sp.self_address,
            _amount=dx,
            _token_id=i
        )

    @sp.entry_point
    def remove_liquidity(self, _amount: sp.TNat):
        pool_record = self.data.token_pool.values()
        token_supply = sp.local('ts1', sp.nat(0))
        _x3 = sp.local('_x3', sp.nat(0))
        sp.while _x3.value < sp.len(pool_record):
            token_supply.value += self.data.token_pool[_x3.value].pool
            _x3.value += 1

        _x4 = sp.local('_x4', sp.nat(0))
        sp.while _x4.value < sp.len(pool_record):
            value = sp.local('val', self.data.token_pool[_x4.value].pool * _amount / token_supply.value)
            self.data.token_pool[_x4.value].pool = sp.as_nat(self.data.token_pool[_x4.value].pool - value.value)
            value.value /= (self.data.eighteen/self.data.token_pool[_x4.value].decimals)
            self.transfer(
                from_=sp.self_address, 
                to=sp.sender, 
                amount=value.value, 
                token_id=_x4.value
            )
            _x4.value += 1


        self.burn_lp(_amount)

    @sp.offchain_view(pure=True)
    def get_totalSupply(self):
        """Returns the total supply"""
        pool_record = self.data.token_pool.values()
        token_supply = sp.local('_ts1', sp.nat(0))

        _x6 = sp.local('_x6', sp.nat(0))
        sp.while _x6.value < sp.len(pool_record):
            token_supply.value += self.data.token_pool[_x6.value].pool
            _x6.value += 1

        sp.result(token_supply.value)

    @sp.offchain_view(pure=True)
    def get_dy(self, params):
        """Returns the number of tokens user will get after the swap"""
        x = self.data.token_pool[params.i].pool + params.dx
        y = self.get_y(params.i, params.j, x)
        dy = sp.as_nat(self.data.token_pool[params.j].pool - y)
        sp.result(dy)
