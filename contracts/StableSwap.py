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
        sp.verify(amount > sp.nat(0), 'INSUFFICIENT_TOKENS')
        
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
    
    # @sp.entry_point
    # def invest_liquidity()

@sp.add_test(name="StableSwap Tests")
def test():
    token_admin = sp.test_account("Token Admin")
    alice = sp.test_account("Alice")
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
    token.mint(address=alice.address, value=sp.nat(10000)).run(sender=token_admin)

    # Initialize the exchange.
    # Approve to spend by stable_swap address
    token.approve(sp.record(spender=stable_swap.address, value=sp.nat(20))).run(sender=alice)
    stable_swap.initialize_enchange(sp.record(token_amount=sp.nat(20))).run(sender=alice, amount=sp.mutez(10000))


        
