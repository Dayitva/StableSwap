import smartpy as sp


class Dex(sp.Contract):
    def __init__(self, feeRate: sp.TNat):
        self.init(
            feeRate=sp.nat(feeRate),
            invariant=sp.mutez(0)
        )

    @sp.entry_point
    def InitializeExchange(self, params):
        token_amount = sp.as_nat(params.token_amount)

        sp.verify(self.data.invariant == sp.mutez(0), message="Wrong invariant")
        sp.verify(((sp.amount > sp.mutez(1)) & (
            sp.amount < sp.tez(500000000))), message="Wrong amount")
        sp.verify(token_amount > sp.nat(10), message="Wrong tokenAmount")

        # TODO WE NEED TO DEFINE OUR Curve Invariant
        # self.data.invariant = sp.split_tokens(self.data.tezPool, self.data.tokenPool, sp.nat(1))

        # TODO set up links to our USDtz, kUSD addresses, so that we can add Liq to that address
        # pass 

        # TODO WE NEED TO Init a data structure to act as a Pool with USDtz + kUSD, roughly implemented below
        # IDEA We can also just maintain a single map with the $ balances, divest in a way that maintains pool balance
        USDtz_LP_balances = sp.big_map(tkey = sp.TAddress, tvalue = sp.TInt)
        total_USDtz = sp.nat(0)
        kUSD_LP_balances = sp.big_map(tkey = sp.TAddress, tvalue = sp.TInt)
        total_kUSD = sp.nat(0)
        total_supply = sp.nat(0)

    @sp.entry_point
    def AddLiquidity(self, params):
        sp.verify(sp.amount > sp.nat(0), message="Invalid amount")

        # TODO update the Invariant
        # self.data.invariant = sp.split_tokens(self.data.tezPool, self.data.tokenPool, sp.nat(1))

        # TODO update the local data structures
        sp.if self.data.balances.contains(params.address):
            self.data.USDtz_LP_balances[params.address] += sp.amount
            self.data.kUSD_LP_balances[params.address] += sp.amount
        sp.else:
            self.data.USDtz_LP_balances[params.address] = sp.amount
            self.data.kUSD_LP_balances[params.address] = sp.amount

        self.total_USDtz += sp.amount
        self.total_kUSD += sp.amount
        self.total_supply += 2*sp.amount

        # FIXME make the actual tansfer of tokens, unsure of Implementation
        # sp.transfer(sp.record(account_from=sp.sender,
        #                       destination=self.data.address,
        #                       value=tokensRequired),
        #             sp.mutez(0),
        #             token_contract)

    @sp.entry_point
    def RemoveLiquidity(self, params):
        sp.verify(sp.amount > 0, "Invalid Amount")
        sp.verify(self.data.USDtz_LP_balances.contains(sp.sender) | self.data.kUSD_LP_balances.contains(sp.sender), "Source account not found")
        sp.verify((self.data.USDtz_LP_balances.contains(sp.sender) + self.data.kUSD_LP_balances.contains(sp.sender)) - sp.amount >= 0, "Insufficient Balance")

        # TODO Divest in a way that maintains/restores Pool Balance
        # FIXME Calculate the best payout, store in USDtz_divest and kUSD_divest
        USDtz_divest = 0
        kUSD_divest = 0 
        # self.data.USDtz_LP_balances[sp.sender] -= USDtz_divest
        # self.data.kUSD_LP_balances[sp.sender] -= kUSD_divest
        sp.if self.data.USDtz_LP_balances[sp.sender] == 0:
            del self.data.USDtz_LP_balances[sp.sender]
        sp.if self.data.kUSD_LP_balances[sp.sender] == 0:
            del self.data.kUSD_LP_balances[sp.sender]

        # TODO update the local data structures
        self.total_USDtz -= USDtz_divest
        self.total_kUSD -= kUSD_divest
        self.total_supply -= sp.amount

        # TODO update the Invariant 
        # sp.if self.data.totalShares == 0:
        #     self.data.invariant = sp.mutez(0)
        # sp.else:
        #     self.data.invariant = sp.split_tokens(self.data.tezPool, self.data.tokenPool, sp.nat(1))


        # FIXME make the actual tansfer of tokens, unsure of Implementation
        # sp.transfer(sp.record(account_from=self.data.address,
        #                       destination=sp.sender,
        #                       value=tokensDivested),
        #             sp.mutez(0),
        #             token_contract)

        # TODO send the tokens to the LP address, maybe separate for kUSD and USDtz
        sp.send(sp.sender, sp.amount)
