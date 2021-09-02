
import smartpy as sp
fa12 = sp.io.import_script_from_url("https://smartpy.io/templates/FA1.2.py")


class Token(fa12.FA12):
    """ Test FA1.2 Token """
    pass


class StableSwap(sp.Contract):
    def __init__(self, _fee_rate, _token_address):
        self.init(
            invariant = sp.nat(0),
            tez_pool = sp.mutez(0),
            token_pool = sp.nat(0),
            fee_rate = _fee_rate,
            token_address = _token_address
        )
    
    def transfer_tokens(self, from_, to, amount):
        """ Utility Function to transfer FA1.2 Tokens."""
        sp.verify(amount > sp.nat(0), 'INSUFFICIENT_TOKENS[transfer_token]')
        
        # approve_type = sp.TRecord(spender = sp.TAddress, value = sp.TNat).layout(("spender", "value"))
        # approve_data = sp.record(spender=sp.self_address, value=amount)
        # approve_contract = sp.contract(approve_type, self.data.token_address, "approve").open_some()
        # sp.transfer(approve_data, sp.mutez(0), approve_contract)

        transfer_type = sp.TRecord(
            from_ = sp.TAddress,
            to_ = sp.TAddress,
            value = sp.TNat
        ).layout(("from_ as from", ("to_ as to", "value")))
        transfer_data = sp.record(from_=from_, to_=to, value=amount)
        token_contract = sp.contract(  
            transfer_type, 
            self.data.token_address, 
            "transfer"
        ).open_some()
        sp.transfer(transfer_data, sp.mutez(0), token_contract)
    
    def transfer_tez(self, to_, amount: sp.TMutez):
        """ Utility function to transfer tezos. """
        sp.send(to_, amount, message="SENDING_TEZ")
    
    @sp.entry_point
    def initialize_enchange(self, params):
        sp.set_type(params, sp.TRecord(token_amount=sp.TNat))
        token_amount = sp.local('token_amount', params.token_amount)
        tez_amount = sp.local('tez_amount', sp.amount)

        sp.verify(token_amount.value > sp.nat(10), message="NOT_ENOUGH_TOKEN")
        sp.verify((tez_amount.value > sp.mutez(1)) & (tez_amount.value < sp.mutez(50000000)), message="NOT_EMOUGH_TEZ")

        self.data.tez_pool = tez_amount.value
        self.data.token_pool = token_amount.value
        self.data.invariant = token_amount.value * sp.utils.mutez_to_nat(tez_amount.value)

        self.transfer_tokens(from_=sp.sender, to=sp.self_address, amount=token_amount.value)
    
    @sp.entry_point
    def invest_liquidity(self, params):
        sp.set_type(params, sp.TRecord(token_amount=sp.TNat))
        sp.verify(params.token_amount > sp.nat(0), message="NOT_ENOUGH_TOKEN")
        sp.verify(sp.amount > sp.mutez(0), message="NOT_ENOUGH_TOKEN")

        self.data.tez_pool += sp.amount
        self.data.token_pool += params.token_amount
        self.data.invariant = sp.utils.mutez_to_nat(self.data.tez_pool) * self.data.token_pool
        
        self.transfer_tokens(from_=sp.sender, to=sp.self_address, amount=params.token_amount)
    
    @sp.entry_point
    def divest_liquidity(self):
        pass
    
    @sp.entry_point
    def tez_to_token(self):
        sp.verify(sp.amount > sp.mutez(0), message="NOT_ENOUGH_TEZ") 
        # fee: 0.2% => 0.2/100 => 1/500
        tez_in_nat = sp.utils.mutez_to_nat(sp.amount) # 1000
        fee = tez_in_nat / self.data.fee_rate # 2
        new_token_pool = self.data.invariant / sp.as_nat(sp.utils.mutez_to_nat(self.data.tez_pool) - fee) # 10002
        # `token_out` is the amount of token the user will get.
        token_out =  new_token_pool - self.data.token_pool # 2
        self.data.tez_pool += sp.amount
        self.data.token_pool = new_token_pool
        self.data.invariant = new_token_pool * sp.utils.mutez_to_nat(self.data.tez_pool)
        
        
        self.transfer_tokens(from_=sp.self_address, to=sp.sender, amount=sp.as_nat(token_out))
    
    @sp.entry_point
    def token_to_tez(self, params):
        sp.set_type(params, sp.TRecord(token_amount=sp.TNat))
        sp.verify(params.token_amount > sp.nat(0), message="NOT_ENOUGH_TOKEN")
        fee = params.token_amount / self.data.fee_rate
        new_token_pool = self.data.token_pool + params.token_amount
        new_tez_pool = self.data.invariant / sp.as_nat(new_token_pool - fee)
        self.data.tez_pool = sp.utils.nat_to_mutez(new_tez_pool)
        self.data.token_pool = new_token_pool
        self.data.invariant = new_token_pool * new_tez_pool

        # Transfer `token_amount` to this contract's address
        self.transfer_tokens(from_=sp.sender, to=sp.self_address, amount=params.token_amount)

        tez_out = self.data.tez_pool - sp.utils.nat_to_mutez(new_tez_pool)
        # Transfer the swapped tezos.
        self.transfer_tez(to_=sp.sender, amount=tez_out)


@sp.add_test(name="StableSwap Tests")
def test():
    token_admin = sp.test_account("Token Admin")
    alice = sp.test_account("Alice")
    bob = sp.test_account("Bob")
    scenario = sp.test_scenario()

    token_metadata = {
        "decimals": "18",            
        "name": "My Great Token",
        "symbol": "MGT",           
        "icon": 'https://smartpy.io/static/img/logo-only.svg'
    }
    contract_metadata = {
        "" : "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    }
    token = Token(
        token_admin.address,
        config              = fa12.FA12_config(support_upgradable_metadata = True),
        token_metadata      = token_metadata,
        contract_metadata   = contract_metadata
    )
    scenario += token

    stable_swap = StableSwap(_fee_rate = sp.nat(500), _token_address=token.address)
    scenario += stable_swap
    token.mint(address=alice.address, value=sp.nat(20000)).run(sender=token_admin)
    token.mint(address=bob.address, value=sp.nat(1000)).run(sender=token_admin)

    # Initialize the exchange.
    # Approve to spend by stable_swap address
    token.approve(sp.record(spender=stable_swap.address, value=sp.nat(10000))).run(sender=alice)
    stable_swap.initialize_enchange(sp.record(token_amount=sp.nat(10000))).run(sender=alice, amount=sp.mutez(10000))

    # Approving again to provide liquidity.
    # token.approve(sp.record(spender=stable_swap.address, value=sp.nat(100))).run(sender=bob)
    # stable_swap.invest_liquidity(sp.record(token_amount=sp.nat(100))).run(sender=bob, amount=sp.mutez(10000000))

    # # Swap 10 tokens in xtz
    # token.approve(sp.record(spender=stable_swap.address, value=sp.nat(1))).run(sender=alice)
    # stable_swap.token_to_tez(sp.record(token_amount=sp.nat(1))).run(sender=alice)

    stable_swap.tez_to_token().run(sender=bob, amount=sp.mutez(1000))

        

