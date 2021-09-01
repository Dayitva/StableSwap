import smartpy as sp
fa12 = sp.io.import_script_from_url("https://smartpy.io/templates/FA1.2.py")

class Token(fa12.FA12):
    """ Our FA1.2 token template for testing """
    pass


class StableSwap(sp.Contract):
    """
    A Demo FA1.2 Token: KT1RxHojfHb1ASUmTKQLw7cYhdv2pu3BTd9Q
    Balances: 
        - tz1UQygrV4MbdeLRHMXHFwCumS8TgLVUJuJb: 9950
        - tz1UYZ6SMKD5A4fpviTDd1EBixZe1f5arN76: 1050
    """
    def __init__(self, fee_rate, kusd_address):
        self.init(
            invariant = sp.nat(0),
            tezPool = sp.mutez(0),
            kusd_tokenPool = sp.nat(0),

            fee_rate = fee_rate,
            kusd_address = kusd_address,
        )
    
    def TransferTokens(self, from_, to, amount):
        """ Transfer `amount` tokens to `to` """
        sp.verify(amount > 0, 'INSUFFICIENT_AMOUNT')
        transfer_type = sp.TRecord(
            account_from=sp.TAddress,
            destination=sp.TAddress,
            value=sp.TNat
        ),
        transfer_data = sp.record(
            account = to,
            destination = from_,
            value = amount
        )
        token_contract = sp.contract(transfer_type, self.data.kusd_address, "Transfer")
        sp.transfer(transfer_data, sp.mutez(0), token_contract)

    def TransferTez(self, from_, to, tezos_amount):
        """ Transfer `tezos_amount` tez to `to` account. """
        pass

    @sp.entry_point
    def InitializeExchange(self, params):
        """ Initialize the exchange for swapping. """
        token_amount = params.token_amount
        tez_amount = sp.amount
        sp.verify(token_amount > sp.nat(10), message="token_amount > 0")
        sp.verify(
            (tez_amount > sp.mutez(1)) & (tez_amount < sp.mutez(500000000)), 
            message="tez_amount > 0"
        )

        self.data.tezPool = tez_amount
        self.data.kusd_tokenPool = token_amount
        invariant = sp.split_tokens(self.data.tezPool, self.data.kusd_tokenPool, sp.nat(1))

        # Transfer `token_amount` amount of tokens form the sp.sender 
        # to the account of this contract i.e `sp.self_address`
        self.TransferTokens(from_=sp.sender, to=sp.self_address, amount=token_amount)

    
    @sp.entry_point
    def AddLiquidity(self, params):
        """ Add liquidity. """
        pass
    
    @sp.entry_point
    def RemoveLiquidity(self, params):
        """ Remove Liqidity. """
        pass

    @sp.entry_point
    def TezToTokenSwap(self, params):
        """ Swap tez to a FA1.2 token. """
        fee = params.token_amount / self.data.fee_rate
        invariant = self.data.kusd_tokenPool * self.data.tezPool
        new_tez_pool = self.data.tezPool + sp.amount
        new_token_pool = invariant / (self.data.kusd_tokenPool - fee)
        tokens_out = self.data.kusd_tokenPool - new_token_pool
        self.data.tezPool = new_tez_pool
        self.data.kusd_tokenPool = new_token_pool
        self.TransferTokens(sp.sender, sp.sender, tokens_out)

    @sp.entry_point
    def TokenToTezSwap(self, params):
        """ Swaps the FA1.2 Token to Tez """
        sp.set_type(params, sp.record(token_in=sp.TNat))
        sp.verify(params.token_in > 0, "INSUFFICIENT_TOKEN")

        fee = params.token_in / self.data.fee_rate
        invariant = self.data.kusd_tokenPool * self.data.tezPool
        new_token_pool = self.data.kusd_tokenPool + token_in # New kusd_tokenPool Value.
        new_tez_pool = self.data.invariant / (new_token_pool - fee) # New TezosPool Value.
        tez_out = self.data.tezPool - new_tez_pool
        self.TransferTez(from_, to, tezos_amount) # Transfer tezos the the sender's account.



@sp.add_test(name="STableSwap")
def test():
    admin = sp.test_account("Admin")
    kusd_admin = sp.test_account("KUSD Token Admin")
    alice = sp.test_account("Alice")
    bob = sp.test_account("Bob")
    scenario = sp.test_scenario()

    token_metadata = {
            "decimals"    : "18",               # Mandatory by the spec
            "name"        : "My Great Token",   # Recommended
            "symbol"      : "MGT",              # Recommended
            # Extra fields
            "icon"        : 'https://smartpy.io/static/img/logo-only.svg'
        }
    contract_metadata = {
        "" : "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    }
    kusd = Token(
            kusd_admin.address,
            config              = fa12.FA12_config(support_upgradable_metadata = True),
            token_metadata      = token_metadata,
            contract_metadata   = contract_metadata
        )
    scenario += kusd
    # Mint some kusd to alice's account.
    kusd.mint(sp.record(value=sp.nat(1000), address=alice.address)).run(sender=kusd_admin)
    stable_swap = StableSwap(fee_rate=500, kusd_address=kusd.address)
    
    # Initializing the exchange.
    stable_swap.InitializeExchange(sp.record(token_amount=sp.nat(20))).run(sender=alice, amount=sp.mutez(1000))



# sp.add_compilation_target("StableSwap", StableSwap(500, "KT1"))
