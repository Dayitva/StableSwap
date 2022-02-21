import smartpy as sp
from contracts.utility import TokenUtility
from contracts.errors import Error
fa12 = sp.io.import_script_from_url("https://smartpy.io/templates/FA1.2.py")

admin = sp.address("tz1WNKahMHz1bkuAfZrsvtmjBhh4GJzw8YcU")
kusd = sp.address("KT1WJUr74D5bkiQM2RE1PALV7R8MUzzmDzQ9")
usdtz = sp.address("KT1CNQL6xRn5JaTUcMmxwSc5YQjwpyHkDR5r")
lp = sp.address("KT1StTa4Bv1hFMRFnYQq2jgx6tCHkLUd632s")
dex = sp.address("KT1DJGEjVSKWYoypUvUPV1RJ7Td9YJT5rJYt")
metadata = open("./contracts/metadata.json").read()

class Token(fa12.FA12):
    """ Test FA1.2 Token """
    pass

sp.add_compilation_target("LP Token", Token(
    admin,
    config=fa12.FA12_config(support_upgradable_metadata=True),
    token_metadata={
        "decimals": "18",
        "name": "LP Token",
        "symbol": "LP-TOKEN",
        "icon": 'https://smartpy.io/static/img/logo-only.svg'
    },
    contract_metadata={
        "": "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    }
))

class Dex(sp.Contract, TokenUtility):
    def __init__(self, x_address, y_address, _lp_token, x_decimals, y_decimals, _admin):
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
                0: sp.record(
                    address=x_address,
                    decimals=x_decimals,
                    pool=sp.nat(0),
                    admin_fee=sp.nat(0),
                    fa2=False,
                    token_id=0,
                ),
                1: sp.record(
                    address=y_address,
                    decimals=y_decimals,
                    pool=sp.nat(0),
                    admin_fee=sp.nat(0),
                    fa2=False,
                    token_id=1,
                ),
            }),
            admin=_admin,
            eighteen=1000000000000000000,
            fee=sp.nat(15),
            lp_token=_lp_token,
            metadata = sp.big_map(l = {
                "": sp.utils.bytes_of_string("tezos-storage:content"),
                "content": sp.utils.bytes_of_string(metadata),
            }),
        )

    @sp.private_lambda(with_storage="read-only", with_operations=True, wrap_call=True)
    def mint_lp(self, amount):
        """Mint `amount` LP tokens to `sp.sender` account."""
        transfer_type = sp.TRecord(
            address=sp.TAddress,
            value=sp.TNat,
        )
        transfer_value = sp.record(
            address=sp.sender,
            value=amount,
        )
        contract = sp.contract(
            transfer_type,
            self.data.lp_token,
            'mint'
        ).open_some()
        sp.transfer(transfer_value, sp.mutez(0), contract)

    @sp.private_lambda(with_storage="read-only", with_operations=True, wrap_call=True)
    def burn_lp(self, amount):
        """ Burn `amount` LP Tokens. """
        transfer_type = sp.TRecord(
            address=sp.TAddress,
            value=sp.TNat,
        )
        transfer_value = sp.record(
            address=sp.sender,
            value=amount,
        )
        contract = sp.contract(
            transfer_type,
            self.data.lp_token,
            'burn'
        ).open_some()
        sp.transfer(transfer_value, sp.mutez(0), contract)

    def transferToTokenId(self, params):
        _from = params._from 
        _to = params._to
        _amount = params._amount 
        _token_id = params._token_id

        token = self.data.token_pool.get(_token_id)

        sp.if token.fa2:
            self.fa2Transfer(_from, _to, _amount,
                             token.token_id, token.address)
        sp.else:
            self.fa12Transfer(_from, _to, _amount, token.address)

    @sp.private_lambda(with_storage="read-write", with_operations=False, wrap_call=False)
    def get_D(self, S):
        pool_record = self.data.token_pool.values()

        sp.if S == sp.nat(0):
            sp.result(S)

        sp.else:
            Dprev = sp.local('Dprev', sp.nat(0))
            D = sp.local('D', S)

            Ann = sp.local('Ann', self.data.A * self.data.N_COINS)
            D_P = sp.local('D_P', D.value)

            # sp.trace({"S": S})
            # sp.trace({"Ann": Ann.value})

            sp.while abs(D.value - Dprev.value) > 1:
                D_P.value = D.value
                D_P.value = D_P.value * D.value // (self.data.N_COINS * self.data.token_pool[0].pool)
                D_P.value = D_P.value * D.value // (self.data.N_COINS * self.data.token_pool[1].pool)
                Dprev.value = D.value
                D1 = (Ann.value * S + D_P.value * self.data.N_COINS) * D.value
                D2 = ((sp.as_nat(Ann.value - 1) * D.value) +
                    ((self.data.N_COINS + 1) * D_P.value))
                D.value = D1 // D2

                # sp.trace({"D_P": D_P.value})
                # sp.trace({"Dprev": Dprev.value})
                # sp.trace({"D1": D1})
                # sp.trace({"D2": D2})
                # sp.trace({"D": D.value})

            # sp.trace({"D": D.value})
            # return D.value
            sp.result(D.value)

    def get_y(self, x):
        token_supply = sp.local('ts', self.data.token_pool[0].pool + self.data.token_pool[1].pool)
        D = sp.local('D1', self.get_D(token_supply.value))
        c = sp.local('c', D.value)
        Ann = sp.local('Ann1', self.data.A * self.data.N_COINS)

        c.value = D.value * D.value / (x * self.data.N_COINS)
        c.value = c.value * D.value / (Ann.value * self.data.N_COINS)
        b = sp.local('b', x + D.value / Ann.value)

        y_prev = sp.local('y_prev', sp.nat(0))
        y = sp.local('y', D.value)

        sp.while abs(y.value - y_prev.value) > 1:
            y_prev.value = y.value
            y.value = (y.value*y.value + c.value) / sp.as_nat((2 * y.value + b.value) - D.value)
        
        # sp.trace({"y": y.value})
        return y.value

    @sp.entry_point
    def update_fee(self, new_fee):
        sp.verify(sp.sender == self.data.admin, Error.ADMIN_ERROR)
        sp.verify(sp.amount == sp.tez(0), Error.NO_TEZ)
        self.data.fee = new_fee

    @sp.entry_point
    def admin_claim(self):
        sp.verify(sp.sender == self.data.admin, Error.ADMIN_ERROR)
        sp.verify(sp.amount == sp.tez(0), Error.NO_TEZ)

        self.transferToTokenId(
            sp.record(
                _from=sp.self_address,
                _to=sp.sender,
                _amount=self.data.token_pool[0].admin_fee/(self.data.eighteen/self.data.token_pool[0].decimals),
                _token_id=0
            )
        )
    
        self.transferToTokenId(
            sp.record(
                _from=sp.self_address,
                _to=sp.sender,
                _amount=self.data.token_pool[1].admin_fee/(self.data.eighteen/self.data.token_pool[1].decimals),
                _token_id=1
            )
        )

        # Update Pools
        self.data.token_pool[0].pool = sp.as_nat(self.data.token_pool[0].pool - self.data.token_pool[0].admin_fee)
        self.data.token_pool[1].pool = sp.as_nat(self.data.token_pool[1].pool - self.data.token_pool[1].admin_fee)
        
        # Set admin fee 0
        self.data.token_pool[0].admin_fee = sp.nat(0)
        self.data.token_pool[1].admin_fee = sp.nat(0)

    @sp.entry_point
    def set_lp_address(self, address: sp.TAddress):
        sp.verify(sp.sender == self.data.admin, Error.ADMIN_ERROR)
        sp.verify(sp.amount == sp.tez(0), Error.NO_TEZ)
        self.data.lp_token = address

    @sp.entry_point
    def initialize_exchange(self, token1_amount, token2_amount):
        """ Initialize the exchange with the token2 and token2 amounts."""
        sp.verify(self.data.token_pool[0].pool <= 0, Error.INITIALIZED_ERROR)
        sp.verify(self.data.token_pool[1].pool <= 0, Error.INITIALIZED_ERROR)
        sp.verify(sp.sender == self.data.admin, Error.ADMIN_ERROR)
        sp.verify(sp.amount == sp.tez(0), Error.NO_TEZ)

        # Transfer tokens from the user's account to our contract's address.
        self.transferToTokenId(
            sp.record(
                _from=sp.sender,
                _to = sp.self_address,
                _amount=token1_amount,
                _token_id=0
            )
        )
        self.transferToTokenId(
            sp.record(
                _from=sp.sender,
                _to = sp.self_address,
                _amount=token2_amount,
                _token_id=1
            )
        )
        
        # Update the storage.
        self.data.token_pool[0].pool = token1_amount*(self.data.eighteen/self.data.token_pool[0].decimals)
        self.data.token_pool[1].pool = token2_amount*(self.data.eighteen/self.data.token_pool[1].decimals)
        # sp.trace({"Pool 1" : self.data.token_pool[0].pool})
        # sp.trace({"Pool 2" : self.data.token_pool[1].pool})
        self.mint_lp(self.data.token_pool[0].pool + self.data.token_pool[1].pool)

    @sp.entry_point
    def update_A(self, new_A):
        sp.verify(sp.sender == self.data.admin, Error.NOT_ADMIN)
        sp.verify(sp.amount == sp.tez(0), Error.NO_TEZ)
        self.data.A = new_A

    @sp.entry_point
    def exchange(self, i, dx, min_dy):
        """
        min_dy: minimum amount of tokens that the user should get.
        """
        sp.verify(dx > 0, Error.AMOUNT_ERROR)
        sp.verify(i >= 0, Error.TOKEN_ERROR)
        sp.verify(i < self.data.N_COINS, Error.TOKEN_ERROR)
        sp.verify(sp.amount == sp.tez(0), Error.NO_TEZ)

        j = sp.as_nat(1-i)
        
        self.transferToTokenId(
            sp.record(
                _from=sp.sender,
                _to=sp.self_address,
                _amount=dx,
                _token_id=i
            )
        )
        dx = dx * self.data.eighteen/self.data.token_pool[i].decimals
        x = self.data.token_pool[i].pool + dx
        y = self.get_y(x)
        dy = sp.local('dy', sp.as_nat(self.data.token_pool[j].pool - y))
        fee_collected = sp.local('fee', ((dy.value * self.data.fee) / 10000))
        dy.value = sp.as_nat(dy.value - fee_collected.value)
        self.data.token_pool[j].admin_fee += (fee_collected.value / 2)
        self.data.token_pool[i].pool += dx
        self.data.token_pool[j].pool = sp.as_nat(self.data.token_pool[j].pool - dy.value)

        dy.value /= (self.data.eighteen/self.data.token_pool[j].decimals)
        # sp.trace(dy.value)
        # return dy
        sp.verify(dy.value >= min_dy, Error.POOL_STATE)

        self.transferToTokenId(
            sp.record(
                _from=sp.self_address,
                _to=sp.sender,
                _amount=dy.value,
                _token_id=j
            )
        )

    @sp.entry_point
    def add_liquidity(self, _amount0, _amount1, min_token):
        sp.verify(sp.amount == sp.tez(0), Error.NO_TEZ)

        # Initial invariant
        token_supply_initial = sp.local('ts0', self.data.token_pool[0].pool + self.data.token_pool[1].pool)
        D0 = sp.local('D0', self.get_D(token_supply_initial.value))
        
        self.data.token_pool[0].pool = self.data.token_pool[0].pool + _amount0*(self.data.eighteen/self.data.token_pool[0].decimals)
        self.data.token_pool[1].pool = self.data.token_pool[1].pool + _amount1*(self.data.eighteen/self.data.token_pool[1].decimals)
        
        # Invariant after change
        token_supply_final = sp.local('ts1', self.data.token_pool[0].pool + self.data.token_pool[1].pool)
        D1 = sp.local('D1', self.get_D(token_supply_final.value))
        
        # sp.trace({'D1': D1.value})
        # sp.trace({'D0': D0.value})
        # sp.trace({"D1-D0": D1.value-D0.value})
        
        lp_amount = token_supply_initial.value * sp.as_nat(D1.value - D0.value) / D0.value 
        sp.verify(lp_amount >= min_token, Error.POOL_STATE)

        sp.if lp_amount > sp.nat(0):
            self.mint_lp(lp_amount)

        # Take coins from the sender
        self.transferToTokenId(
            sp.record(
                _from=sp.sender,
                _to=sp.self_address,
                _amount=_amount0,
                _token_id=0
            )
        )

        self.transferToTokenId(
            sp.record(
                _from=sp.sender,
                _to=sp.self_address,
                _amount=_amount1,
                _token_id=1
            )
        )

    @sp.entry_point
    def remove_liquidity(self, _amount, min_tokens):
        sp.verify(sp.amount == sp.tez(0), Error.NO_TEZ)
        sp.set_type(min_tokens, sp.TMap(sp.TNat, sp.TNat))

        token_supply = sp.local('ts1', self.data.token_pool[0].pool + self.data.token_pool[1].pool)

        value = sp.local('val1', self.data.token_pool[0].pool * _amount / token_supply.value)
        self.data.token_pool[0].pool = sp.as_nat(self.data.token_pool[0].pool - value.value)
        value.value /= (self.data.eighteen/self.data.token_pool[0].decimals)
        
        sp.verify(value.value >= min_tokens[0], Error.POOL_STATE)
        self.transferToTokenId(
            sp.record(
                _from=sp.self_address, 
                _to=sp.sender, 
                _amount=value.value, 
                _token_id=0
            )
        )

        value.value = self.data.token_pool[1].pool * _amount / token_supply.value
        self.data.token_pool[1].pool = sp.as_nat(self.data.token_pool[1].pool - value.value)
        value.value /= (self.data.eighteen/self.data.token_pool[1].decimals)
        
        sp.verify(value.value >= min_tokens[1], Error.POOL_STATE)
        self.transferToTokenId(
            sp.record(
                _from=sp.self_address, 
                _to=sp.sender, 
                _amount=value.value, 
                _token_id=1
            )
        )

        self.burn_lp(_amount)


sp.add_compilation_target("USDTZ-KUSD", Dex(
    x_address=kusd, 
    y_address=usdtz, 
    _lp_token=lp, 
    x_decimals = 10 ** 8,
    y_decimals = 10 ** 6,
    _admin=admin
))