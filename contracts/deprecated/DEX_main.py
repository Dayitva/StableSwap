import smartpy as sp
fa12 = sp.io.import_script_from_url("https://smartpy.io/templates/FA1.2.py")

class Token(fa12.FA12):
    """ Test FA1.2 Token """
    pass

# kUSD = 10**18 (6.42 M) [FA1.2]
# wBUSD = 10**18 (1.85 M) [FA 2]
# wDAI = 10**18 (1 M) [FA 2]

# uUSD = 10**12 (8.35 M) [FA 2]

# USDtz = 10**6 (1.87 M) [FA1.2]
# wUSDC = 10**6 (2.5 M) [FA 2]
# wUSDT = 10**6 (0.75 M) [FA 2]

PRECISION = 10 ** 18
PRECISION_MUL = [1, 10**12]

class Dex(sp.Contract):
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
                0: sp.record(address=x_address, pool=sp.nat(0), decimals=sp.nat(10000)),
                1: sp.record(address=y_address, pool=sp.nat(0), decimals=sp.nat(100)),
            }),
            eighteen = 1000000,
            admin=_admin,
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

    def transfer(self, from_, to, amount, token_id):
        """ Utility Function to transfer x FA1.2 Tokens. """
        sp.verify(amount > sp.nat(0), 'INSUFFICIENT_TOKENS[transfer_token]')

        transfer_type = sp.TRecord(
            from_=sp.TAddress,
            to_=sp.TAddress,
            value=sp.TNat
        ).layout(("from_ as from", ("to_ as to", "value")))
        transfer_data = sp.record(from_=from_, to_=to, value=amount)
        token_contract = sp.contract(
            transfer_type,
            self.data.token_pool[token_id].address,
            "transfer"
        ).open_some()
        sp.transfer(transfer_data, sp.mutez(0), token_contract)

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
        self.transfer(
            sp.sender,
            sp.self_address,
            token1_amount,
            0
        )
        self.transfer(
            sp.sender,
            sp.self_address,
            token2_amount,
            1
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
        
        self.transfer(
            from_=sp.sender,
            to=sp.self_address,
            amount=dx,
            token_id=i
        )
        
        x = self.data.token_pool[i].pool + dx
        y = self.get_y(i, j, x)
        dy = sp.local('dy', sp.as_nat(self.data.token_pool[j].pool - y))
        fee_collected = sp.local('fee', ((dy.value * self.data.fee) / 10000))
        dy.value = sp.as_nat(dy.value - fee_collected.value)
        # CHECK
        sp.trace({"Fee" : (fee_collected.value / 2)})
        self.data.admin_fee_pool[j].pool += (fee_collected.value / 2)
        self.data.token_pool[i].pool += dx
        self.data.token_pool[j].pool = sp.as_nat(
            self.data.token_pool[j].pool - dy.value)

        dy.value /= (self.data.eighteen/self.data.token_pool[j].decimals)

        # sp.trace(dy.value)
        # return dy
        sp.if dy.value > 0:
            self.transfer(
                from_=sp.self_address,
                to=sp.sender,
                amount=dy.value,
                token_id=j
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
        self.transfer(
            from_=sp.sender,
            to=sp.self_address,
            amount=dx,
            token_id=i
        )

    @sp.entry_point
    def add_liquidity_old(self, i, dx, min_tok):
        pool_record = self.data.token_pool.values()
        token_supply = sp.local('ts', sp.nat(0))
        
        _x2 = sp.local('_x2', sp.nat(0))
        sp.while _x2.value < sp.len(pool_record):
            # sp.trace({"_x2": _x2.value})
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
        # sp.trace({"D1-D0": D1.value-D0.value})
        
        lp_amount = token_supply.value * sp.as_nat(D1.value - D0.value) / D0.value 
        # sp.trace({"lp_amount": lp_amount})
        sp.if lp_amount > sp.nat(0):
            self.mint_lp(lp_amount)

        dx /= (self.data.eighteen/self.data.token_pool[i].decimals)
        
        sp.verify(lp_amount >= min_tok, Error.POOL_STATE)

        # Take coins from the sender
        self.transferToTokenId(
            sp.record(
                _from=sp.sender,
                _to=sp.self_address,
                _amount=dx,
                _token_id=i
            )
        )

    @sp.entry_point
    def remove_liquidity(self, _amount: sp.TNat):
        """
        27508699211: first
        22466325791: second
        """
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
        # ​sp.result(self.data.token_pool[0].pool + self.data.token_pool[1].pool)

    @sp.offchain_view(pure=True)
    def get_dy(self, params):
        """Returns the number of tokens user will get after the swap"""
        x = self.data.token_pool[params.i].pool + params.dx
        y = self.get_y(params.i, params.j, x)
        dy = sp.as_nat(self.data.token_pool[params.j].pool - y)
        sp.result(dy)


@sp.add_test(name="Liquibrium")
def test():
    admin = sp.address("tz1d6ZpPZj4Xb9tPbLcnSnRN2VCxRdSz1i4o")
    alice = sp.test_account("Alice")
    bob = sp.test_account("Robert")
    token_admin = sp.test_account("Token Admin")
    
    DECIMALS_0 = 10 ** 2
    DECIMALS_1 = 10 ** 4
    scenario = sp.test_scenario()
    
    token1_metadata = {
        "decimals": "2",
        "name": "USD Tez",
        "symbol": "USDTz",
        "icon": 'https://smartpy.io/static/img/logo-only.svg'
    }
    contract1_metadata = {
        "": "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    }
    token2_metadata = {
        "decimals": "4",
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
    kusd.mint(
        address=alice.address,
        value=sp.nat(100000 * DECIMALS_1)
    ).run(sender=token_admin)
    kusd.mint(
        address=bob.address,
        value=sp.nat(100000 * DECIMALS_1)
    ).run(sender=token_admin)
    usdtz.mint(
        address=alice.address,
        value=sp.nat(100000 * DECIMALS_0)
    ).run(sender=token_admin)
    usdtz.mint(
        address=bob.address,
        value=sp.nat(100000 * DECIMALS_0)
    ).run(sender=token_admin)
    # Initialize the exchange.
    # Approve to spend by stable_swap address
    dex = Dex(
        x_address=kusd.address,
        # x_address=sp.address('KT1WJUr74D5bkiQM2RE1PALV7R8MUzzmDzQ9'),
        y_address=usdtz.address,
        # y_address=sp.address('KT1CNQL6xRn5JaTUcMmxwSc5YQjwpyHkDR5r'),
        _lp_token=sp.address('KT1-LP-TOKEN'),
        _admin=admin
    )
    # lp_metadata = {
    #     "decimals": "9",
    #     "name": "LP Token",
    #     "symbol": "LP-TOKEN",
    #     "icon": 'https://smartpy.io/static/img/logo-only.svg'
    # }
    # lp_contract_metadata = {
    #     "": "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    # }
    scenario += dex
    # lp = Token(
    #     dex.address,
    #     config=fa12.FA12_config(support_upgradable_metadata=True),
    #     token_metadata=lp_metadata,
    #     contract_metadata=lp_contract_metadata
    # )
    # dex.set_lp_address(lp.address).run(sender=admin)
    kusd.approve(sp.record(
        spender=dex.address,
        value=sp.nat(50_000 * DECIMALS_1
                     ))).run(sender=alice)
    usdtz.approve(sp.record(
        spender=dex.address,
        value=sp.nat(50_000 * DECIMALS_0
                     ))).run(sender=alice)
    dex.initialize_exchange(
        token1_amount=sp.nat(50_000 * DECIMALS_1),
        token2_amount=sp.nat(50_000 * DECIMALS_0)
    ).run(sender=alice)
    dex.remove_liquidity(25000 * (10**6)).run(sender=alice)
    kusd.approve(sp.record(
        spender=dex.address,
        value=sp.nat(5000 * DECIMALS_1)
    )).run(sender=bob)
    dex.exchange(i=0, j=1, dx=5000 * DECIMALS_1).run(sender=bob)
    kusd.approve(sp.record(
        spender=dex.address,
        value=sp.nat(100 * DECIMALS_1
    ))).run(sender=alice)
    dex.add_liquidity(i=0, dx=100 * DECIMALS_1).run(sender=alice)
    dex.remove_liquidity(50 * (10**6)).run(sender=alice)
    dex.admin_claim().run(sender=admin)
sp.add_compilation_target("Dex Compilation Target", Dex(
    x_address=sp.address('KT1WJUr74D5bkiQM2RE1PALV7R8MUzzmDzQ9'),
    y_address=sp.address('KT1CNQL6xRn5JaTUcMmxwSc5YQjwpyHkDR5r'),
    _lp_token=sp.address('KT1Nv2h1bHPLYZsGrCdfdvwKzXsZrFEfJnpJ'),
    _admin=sp.address("tz1WNKahMHz1bkuAfZrsvtmjBhh4GJzw8YcU")
))
