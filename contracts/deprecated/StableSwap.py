

import smartpy as sp
fa12 = sp.io.import_script_from_url("https://smartpy.io/templates/FA1.2.py")


class Token(fa12.FA12):
    """ Test USDTZ FA1.2 Token """
    pass


class StableSwap(sp.Contract):
    def __init__(self, _fee_rate, x_address, y_address, _admin, sp_address):
        self.init(
            invariant = sp.nat(0),
            x_pool = sp.nat(0),
            y_pool = sp.nat(0),
            x_address = x_address,
            y_address = y_address,
            fee_rate = _fee_rate,
            total_x_fee = sp.nat(0),
            total_y_fee = sp.nat(0),
            admin = _admin,
            lp_address = sp_address,
        )
    
    def check_admin(self):
        sp.verify(sp.sender == self.data.admin, 'NOT_ADMIN')
    
    def transfer_x(self, from_, to, amount):
        """ Utility Function to transfer x  FA1.2 Tokens."""
        sp.verify(amount > sp.nat(0), 'INSUFFICIENT_TOKENS[transfer_token]')
        
        transfer_type = sp.TRecord(
            from_ = sp.TAddress,
            to_ = sp.TAddress,
            value = sp.TNat
        ).layout(("from_ as from", ("to_ as to", "value")))
        transfer_data = sp.record(from_=from_, to_=to, value=amount)
        token_contract = sp.contract(  
            transfer_type, 
            self.data.x_address, 
            "transfer"
        ).open_some()
        sp.transfer(transfer_data, sp.mutez(0), token_contract)
    
    def transfer_y(self, from_, to, amount):
        """ Utility Function to transfer y FA1.2 Tokens."""
        sp.verify(amount > sp.nat(0), 'INSUFFICIENT_TOKENS[transfer_token]')
        
        transfer_type = sp.TRecord(
            from_ = sp.TAddress,
            to_ = sp.TAddress,
            value = sp.TNat
        ).layout(("from_ as from", ("to_ as to", "value")))
        transfer_data = sp.record(from_=from_, to_=to, value=amount)
        token_contract = sp.contract(  
            transfer_type, 
            self.data.y_address, 
            "transfer"
        ).open_some()
        sp.transfer(transfer_data, sp.mutez(0), token_contract)

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
            self.data.lp_address,
            'mint'
        )
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
            self.data.lp_address,
            'burn'
        )
        sp.transfer(transfer_value, sp.mutez(0), contract)

    
    @sp.entry_point
    def initialize_enchange(self, params):
        sp.set_type(params, sp.TRecord(x_amount=sp.TNat, y_amount=sp.TNat))
        # token_amount = sp.local('token_amount', params.token_amount)
        # tez_amount = sp.local('tez_amount', sp.amount)

        sp.verify(params.x_amount > sp.nat(10), message="NOT_ENOUGH_X_TOKEN")
        sp.verify(params.y_amount > sp.nat(10), message="NOT_ENOUGH_Y_TOKEN")

        self.data.x_pool = params.x_amount
        self.data.y_pool = params.y_amount
        self.data.invariant = params.x_amount * params.y_amount
        
        # Trannsfering the liquidity from the sender's account to the contract's acc.
        self.transfer_x(from_=sp.sender, to=sp.self_address, amount=params.x_amount)
        self.transfer_y(from_=sp.sender, to=sp.self_address, amount=params.y_amount)
    
    @sp.entry_point
    def invest_liquidity(self, params):
        sp.set_type(params, sp.TRecord(x_amount=sp.TNat, y_amount=sp.TNat))
        sp.verify(params.x_amount > sp.nat(0), message="NOT_ENOUGH_TOKEN")
        sp.verify(params.y_amount > sp.nat(0), message="NOT_ENOUGH_TOKEN")

        self.data.x_pool += params.x_amount
        self.data.y_pool += params.y_amount
        self.data.invariant = self.data.x_pool * self.data.y_pool

        self.transfer_x(from_=sp.sender, to=sp.self_address, amount=params.x_amount)
        self.transfer_y(from_=sp.sender, to=sp.self_address, amount=params.y_amount)
    
    @sp.entry_point
    def divest_liquidity(self):
        pass
    

    @sp.entry_point
    def x_to_y(self, x_amount):
        sp.verify(x_amount > sp.nat(0), "NOT_ENOUGH_X_TOKENS")
        fee = x_amount / self.data.fee_rate
        self.data.total_x_fee += fee

        new_x_pool = self.data.x_pool + x_amount
        new_y_pool = self.data.invariant / sp.as_nat(new_x_pool - fee)
        # Fee on y_token

        y_out = sp.as_nat(self.data.y_pool - new_y_pool)

        sp.if y_out > sp.nat(0):
            # Transfer the tokens.
            self.transfer_y(from_=sp.self_address, to=sp.sender, amount=y_out)

        self.data.x_pool = new_x_pool
        self.data.y_pool = new_y_pool
        self.data.invariant = new_x_pool * new_y_pool
        
    @sp.entry_point
    def y_to_x(self, y_amount):
        sp.verify(y_amount > sp.nat(0), "NOT_ENOUGH_Y_TOKENS")
        fee = y_amount / self.data.fee_rate
        self.data.total_y_fee += fee

        new_y_pool = self.data.y_pool + y_amount
        new_x_pool = self.data.invariant / sp.as_nat(new_y_pool - fee)
        # Fee on y_token

        x_out = sp.as_nat(self.data.x_pool - new_x_pool)

        sp.if x_out > sp.nat(0):
            # Transfer the tokens.
            self.transfer_y(from_=sp.self_address, to=sp.sender, amount=x_out)

        self.data.x_pool = new_x_pool
        self.data.y_pool = new_y_pool
        self.data.invariant = new_x_pool * new_y_pool
    
    @sp.entry_point
    def withdraw_fee(self):
        """
        This entry_point allows admin to withdraw fee collected so far.
        """
        self.check_admin()

        x = sp.local('x', self.data.total_x_fee)
        y = sp.local('y', self.data.total_y_fee)
        sp.if x.value > sp.nat(0):
            self.transfer_x(from_=sp.self._address, to=sp.sender, amount=x.value)
            self.data.total_x_fee = sp.nat(0)
        sp.if y.value > sp.nat(0):
            self.transfer_y(from_=sp.self._address, to=sp.sender, amount=y.value)
            self.data.total_y_fee = sp.nat(0)



@sp.add_test(name="StableSwap Tests")
def test():
    DECIMALS = 10 ** 9
    token_admin = sp.test_account("Token Admin")
    alice = sp.test_account("Alice")
    bob = sp.test_account("Bob")
    scenario = sp.test_scenario()

    kusd_token_metadata = {
        "decimals": "9",            
        "name": "KUSD Token",
        "symbol": "KUSD",           
        "icon": 'https://smartpy.io/static/img/logo-only.svg'
    }
    kusd_contract_metadata = {
        "" : "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    }
    usdtz_token_metadata = {
        "decimals": "9",            
        "name": "USDTZ Token",
        "symbol": "USDTZ",           
        "icon": 'https://smartpy.io/static/img/logo-only.svg'
    }
    usdtz_contract_metadata = {
        "" : "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    }
    kusd = Token(
        token_admin.address,
        config              = fa12.FA12_config(support_upgradable_metadata = True),
        token_metadata      = kusd_token_metadata,
        contract_metadata   = kusd_contract_metadata
    )
    usdtz = Token(
        token_admin.address,
        config              = fa12.FA12_config(support_upgradable_metadata = True),
        token_metadata      = usdtz_token_metadata,
        contract_metadata   = usdtz_contract_metadata
    )
    scenario += kusd
    scenario += usdtz

    # x: KUSD, y: USDTz

    stable_swap = StableSwap(_fee_rate = sp.nat(500), x_address=kusd.address, y_address=usdtz.address)
    scenario += stable_swap
    kusd.mint(address=alice.address, value=sp.nat(100_000 * DECIMALS)).run(sender=token_admin)
    kusd.mint(address=bob.address, value=sp.nat(100_000 * DECIMALS)).run(sender=token_admin)

    usdtz.mint(address=alice.address, value=sp.nat(100_000 * DECIMALS)).run(sender=token_admin)
    usdtz.mint(address=bob.address, value=sp.nat(100_000 * DECIMALS)).run(sender=token_admin)

    # Initialize the exchange.
    # Approve to spend by stable_swap address
    kusd.approve(sp.record(
        spender=stable_swap.address, 
        value=sp.nat(50_000 * DECIMALS
    ))).run(sender=alice)
    usdtz.approve(sp.record(
        spender=stable_swap.address, 
        value=sp.nat(50_000 * DECIMALS
    ))).run(sender=alice)
    stable_swap.initialize_enchange(sp.record(
        x_amount=sp.nat(50_000 * DECIMALS),
        y_amount=sp.nat(50_000 * DECIMALS)
    )).run(sender=alice)

    # Approving again to provide liquidity.
    # token.approve(sp.record(spender=stable_swap.address, value=sp.nat(100))).run(sender=bob)
    # stable_swap.invest_liquidity(sp.record(token_amount=sp.nat(100))).run(sender=bob, amount=sp.mutez(10000000))

    # # Swap 10 tokens in xtz
    # token.approve(sp.record(spender=stable_swap.address, value=sp.nat(1))).run(sender=alice)
    # stable_swap.token_to_tez(sp.record(token_amount=sp.nat(1))).run(sender=alice)

    kusd.approve(sp.record(
        spender=stable_swap.address, 
        value=sp.nat(20 * DECIMALS)
    )).run(sender=bob)
    stable_swap.x_to_y(sp.nat(20 * DECIMALS)).run(sender=bob)

# Scenario
# sp.add_compilation_target("StableSwap", StableSwap(_fee_rate=sp.nat(500), _token_address=sp.address("KT1")))
