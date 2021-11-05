def remove_liquidity_imbalance(dx):
    token_supply: uint256 = self.token.totalSupply()
    assert token_supply != 0  # dev: zero total supply
    _fee: uint256 = self.fee * N_COINS / (4 * (N_COINS - 1))
    _admin_fee: uint256 = self.admin_fee
    amp: uint256 = self._A()

    old_balances: uint256[N_COINS] = self.balances
    new_balances: uint256[N_COINS] = old_balances
    D0: uint256 = self.get_D_mem(old_balances, amp)
    for i in range(N_COINS):
        new_balances[i] -= amounts[i]
    D1: uint256 = self.get_D_mem(new_balances, amp)
    fees: uint256[N_COINS] = empty(uint256[N_COINS])
    for i in range(N_COINS):
        ideal_balance: uint256 = D1 * old_balances[i] / D0
        difference: uint256 = 0
        if ideal_balance > new_balances[i]:
            difference = ideal_balance - new_balances[i]
        else:
            difference = new_balances[i] - ideal_balance
        fees[i] = _fee * difference / FEE_DENOMINATOR
        self.balances[i] = new_balances[i] - (fees[i] * _admin_fee / FEE_DENOMINATOR)
        new_balances[i] -= fees[i]
    D2: uint256 = self.get_D_mem(new_balances, amp)

    token_amount: uint256 = (D0 - D2) * token_supply / D0
    assert token_amount != 0  # dev: zero tokens burned
    token_amount += 1  # In case of rounding errors - make it unfavorable for the "attacker"
    assert token_amount <= max_burn_amount, "Slippage screwed you"

    self.token.burnFrom(msg.sender, token_amount)  # dev: insufficient funds
    ### TODO Actual transfer to sender
    

def remove_liquidity_old(self, dx):
    pool_record = self.data.token_pool.values()
    token_supply = sp.local('ts1_old', sp.nat(0))
    _x5 = sp.local('_x5', sp.nat(0))
    sp.while _x5.value < sp.len(pool_record):
        token_supply.value += self.data.token_pool[_x5.value].pool
        _x5.value += 1
    val1 = sp.local('val1', sp.nat(0))
    # val1.value = sp.as_nat(token_supply.value - dx)/2
    val1.value = token_supply.value/2
    tok0_ret = sp.local('tk1_ret', sp.nat(0))
    tok1_ret = sp.local('tk2_ret', sp.nat(0))
    sp.if val1.value > self.data.token_pool[0].pool:
        sp.trace('val1')
        sp.trace(val1.value)
        sp.trace(self.data.token_pool[0].pool)
        tok0_ret.value = sp.as_nat(
            val1.value - self.data.token_pool[0].pool)
    sp.if val1.value > self.data.token_pool[1].pool:
        tok1_ret.value = sp.as_nat(
            val1.value - self.data.token_pool[1].pool)
    # # Initial invariant
    # D0 = sp.local('D0', sp.nat(0))
    # sp.if token_supply.value > 0:
    #     D0.value = self.get_D()
    # Trasfer tok0 to the sender
    sp.if tok0_ret.value > 0:
        self.transfer(
            from_=sp.self_address,
            to=sp.sender,
            amount=dx,
            token_id=0
        )
        self.data.token_pool[0].pool = sp.as_nat(
            self.data.token_pool[0].pool - tok0_ret.value)
    # Trasfer tok1 to the sender
    sp.if tok1_ret.value > 0:
        self.transfer(
            from_=sp.self_address,
            to=sp.sender,
            amount=dx,
            token_id=1
        )
        self.data.token_pool[1].pool = sp.as_nat(
            self.data.token_pool[1].pool - tok1_ret.value)
    # Invariant after change
    # D1 = sp.local('D1', self.get_D())
    # sp.trace({'D1': D1.value})
    # sp.trace({'D0': D0.value})
    # sp.trace({"D1-D0": D1.value-D0.value})
    # return D1 - D0

