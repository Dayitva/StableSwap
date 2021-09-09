
# This can (and needs to) be changed at compile time
N_COINS = 3  # <- change

FEE_DENOMINATOR = 10 ** 10
LENDING_PRECISION = 10 ** 18
PRECISION = 10 ** 18  # The precision to convert to
PRECISION_MUL= [1, 1000000000000, 1000000000000]
RATES= [1000000000000000000, 1000000000000000000000000000000, 1000000000000000000000000000000]
FEE_INDEX = 2  # Which coin may potentially have fees (USDT)

MAX_ADMIN_FEE = 10 * 10 ** 9
MAX_FEE = 5 * 10 ** 9
MAX_A = 10 ** 6
MAX_A_CHANGE = 10

ADMIN_ACTIONS_DELAY = 3 * 86400
MIN_RAMP_TIME = 86400


def __init__(self,
    _owner,
    _coins,
    _pool_token,
    _A,
    _fee,
    _admin_fee
):
    """
    @notice Contract constructor
    @param _owner Contract owner address
    @param _coins Addresses of ERC20 conracts of coins
    @param _pool_token Address of the token representing LP share
    @param _A Amplification coefficient multiplied by n * (n - 1)
    @param _fee Fee to charge for exchanges
    @param _admin_fee Admin fee
    """
    for i in range(N_COINS):
        #assert _coins[i] != ZERO_ADDRESS
    self.coins = _coins
    self.initial_A = _A
    self.future_A = _A
    self.fee = _fee
    self.admin_fee = _admin_fee
    self.owner = _owner


def _A():
    """
    Handle ramping A up or down
    """
    return 85

def A(self):
    return self._A()


def _xp(self):
    result = RATES
    for i in range(N_COINS):
        result[i] = result[i] * self.balances[i] / LENDING_PRECISION
    return result


def _xp_mem(_balances):
    result = RATES
    for i in range(N_COINS):
        result[i] = result[i] * _balances[i] / PRECISION
    return result


def get_D(xp, amp):
    S = 0
    for _x in xp:
        S += _x
    if S == 0:
        return 0

    Dprev= 0
    D= S
    Ann= amp * N_COINS
    for _i in range(255):
        D_P= D
        for _x in xp:
            D_P = D_P * D / (_x * N_COINS)  # If division by 0, this will be borked: only withdrawal will work. And that is good
        Dprev = D
        D = (Ann * S + D_P * N_COINS) * D / ((Ann - 1) * D + (N_COINS + 1) * D_P)
        # Equality with the precision of 1
        if D > Dprev:
            if D - Dprev <= 1:
                break
        else:
            if Dprev - D <= 1:
                break
    return D


def get_D_mem(self, _balances, amp):
    return self.get_D(self._xp_mem(_balances), amp)


def calc_token_amount(self, amounts, deposit):
    """
    Simplified method to calculate addition or reduction in token supply at
    deposit or withdrawal without taking fees into account (but looking at
    slippage).
    Needed to prevent front-running, not for precise calculations!
    """
    _balances = self.balances
    amp = self._A()
    D0 = self.get_D_mem(_balances, amp)
    for i in range(N_COINS):
        if deposit:
            _balances[i] += amounts[i]
        else:
            _balances[i] -= amounts[i]
    D1 = self.get_D_mem(_balances, amp)
    token_amount = self.token.totalSupply()
    diff = 0
    if deposit:
        diff = D1 - D0
    else:
        diff = D0 - D1
    return diff * token_amount / D0



def add_liquidity(self, amounts, min_mint_amount):
    fees= []
    _fee = self.fee * N_COINS / (4 * (N_COINS - 1))
    _admin_fee = self.admin_fee
    amp = self._A()

    token_supply = self.token.totalSupply()
    # Initial invariant
    D0 = 0
    old_balances= self.balances
    if token_supply > 0:
        D0 = self.get_D_mem(old_balances, amp)
    new_balances= old_balances

    for i in range(N_COINS):
        in_amount = amounts[i]
        if token_supply == 0:
            assert in_amount > 0  # dev: initial deposit requires all coins
        in_coin = self.coins[i]

        # Take coins from the sender
        if in_amount > 0:
            if i == FEE_INDEX:
                in_amount = ERC20(in_coin).balanceOf(self)

            # "safeTransferFrom" which works for ERC20s which return bool or not
            _response: Bytes[32] = raw_call(
                in_coin,
                concat(
                    method_id("transferFrom(address,address,uint256)"),
                    convert(msg.sender, bytes32),
                    convert(self, bytes32),
                    convert(amounts[i], bytes32),
                ),
                max_outsize=32,
            )  # dev: failed transfer
            if len(_response) > 0:
                assert convert(_response, bool)  # dev: failed transfer

            if i == FEE_INDEX:
                in_amount = ERC20(in_coin).balanceOf(self) - in_amount

        new_balances[i] = old_balances[i] + in_amount

    # Invariant after change
    D1 = self.get_D_mem(new_balances, amp)
    assert D1 > D0

    # We need to recalculate the invariant accounting for fees
    # to calculate fair user's share
    D2 = D1
    if token_supply > 0:
        # Only account for fees if we are not the first to deposit
        for i in range(N_COINS):
            ideal_balance = D1 * old_balances[i] / D0
            difference = 0
            if ideal_balance > new_balances[i]:
                difference = ideal_balance - new_balances[i]
            else:
                difference = new_balances[i] - ideal_balance
            fees[i] = _fee * difference / FEE_DENOMINATOR
            self.balances[i] = new_balances[i] - (fees[i] * _admin_fee / FEE_DENOMINATOR)
            new_balances[i] -= fees[i]
        D2 = self.get_D_mem(new_balances, amp)
    else:
        self.balances = new_balances


def get_y(self, i, j, x, xp_):
    # x in the input is converted to the same price/precision

    assert i != j       # dev: same coin
    assert j >= 0       # dev: j below zero
    assert j < N_COINS  # dev: j above N_COINS

    # should be unreachable, but good for safety
    assert i >= 0
    assert i < N_COINS

    amp = self._A()
    D = self.get_D(xp_, amp)
    c = D
    S_ = 0
    Ann = amp * N_COINS

    _x = 0
    for _i in range(N_COINS):
        if _i == i:
            _x = x
        elif _i != j:
            _x = xp_[_i]
        else:
            continue
        S_ += _x
        c = c * D / (_x * N_COINS)
    c = c * D / (Ann * N_COINS)
    b = S_ + D / Ann  # - D
    y_prev = 0
    y = D
    for _i in range(255):
        y_prev = y
        y = (y*y + c) / (2 * y + b - D)
        # Equality with the precision of 1
        if y > y_prev:
            if y - y_prev <= 1:
                break
        else:
            if y_prev - y <= 1:
                break
    return y


def get_dy(self, i, j, dx):
    # dx and dy in c-units
    rates = RATES
    xp = self._xp()

    x = xp[i] + (dx * rates[i] / PRECISION)
    y = self.get_y(i, j, x, xp)
    dy = (xp[j] - y - 1) * PRECISION / rates[j]
    _fee = self.fee * dy / FEE_DENOMINATOR
    return dy - _fee



def exchange(self, i, j, dx, min_dy):
    rates = RATES

    old_balances = self.balances
    xp = self._xp_mem(old_balances)

    # Handling an unexpected charge of a fee on transfer (USDT, PAXG)
    dx_w_fee = dx
    input_coin = self.coins[i]

    if i == FEE_INDEX:
        dx_w_fee = ERC20(input_coin).balanceOf(self)

    # "safeTransferFrom" which works for ERC20s which return bool or not
    _response: Bytes[32] = raw_call(
        input_coin,
        concat(
            method_id("transferFrom(address,address,uint256)"),
            convert(msg.sender, bytes32),
            convert(self, bytes32),
            convert(dx, bytes32),
        ),
        max_outsize=32,
    )  # dev: failed transfer
    if len(_response) > 0:
        assert convert(_response, bool)  # dev: failed transfer

    if i == FEE_INDEX:
        dx_w_fee = ERC20(input_coin).balanceOf(self) - dx_w_fee

    x = xp[i] + dx_w_fee * rates[i] / PRECISION
    y = self.get_y(i, j, x, xp)

    dy = xp[j] - y - 1  # -1 just in case there were some rounding errors
    dy_fee = dy * self.fee / FEE_DENOMINATOR

    # Convert all to real units
    dy = (dy - dy_fee) * PRECISION / rates[j]
    assert dy >= min_dy, "Exchange resulted in fewer coins than expected"

    dy_admin_fee = dy_fee * self.admin_fee / FEE_DENOMINATOR
    dy_admin_fee = dy_admin_fee * PRECISION / rates[j]

    # Change balances exactly in same way as we change actual ERC20 coin amounts
    self.balances[i] = old_balances[i] + dx_w_fee
    # When rounding errors happen, we undercharge admin fee in favor of LP
    self.balances[j] = old_balances[j] - dy - dy_admin_fee

    # "safeTransfer" which works for ERC20s which return bool or not
    _response = raw_call(
        self.coins[j],
        concat(
            method_id("transfer(address,uint256)"),
            convert(msg.sender, bytes32),
            convert(dy, bytes32),
        ),
        max_outsize=32,
    )  # dev: failed transfer
    if len(_response) > 0:
        assert convert(_response, bool)  # dev: failed transfer



def remove_liquidity(self, _amount, min_amounts):
    total_supply = self.token.totalSupply()
    amounts = []
    fees = []  # Fees are unused but we've got them historically in event

    for i in range(N_COINS):
        value = self.balances[i] * _amount / total_supply
        assert value >= min_amounts[i], "Withdrawal resulted in fewer coins than expected"
        self.balances[i] -= value
        amounts[i] = value

        # "safeTransfer" which works for ERC20s which return bool or not
        _response: Bytes[32] = raw_call(
            self.coins[i],
            concat(
                method_id("transfer(address,uint256)"),
                convert(msg.sender, bytes32),
                convert(value, bytes32),
            ),
            max_outsize=32,
        )  # dev: failed transfer
        if len(_response) > 0:
            assert convert(_response, bool)  # dev: failed transfer

    self.token.burnFrom(msg.sender, _amount)  # dev: insufficient funds


def remove_liquidity_imbalance(self, amounts, max_burn_amount):
    token_supply = self.token.totalSupply()
    assert token_supply != 0  # dev: zero total supply
    _fee = self.fee * N_COINS / (4 * (N_COINS - 1))
    _admin_fee = self.admin_fee
    amp = self._A()

    old_balances = self.balances
    new_balances = old_balances
    D0 = self.get_D_mem(old_balances, amp)
    for i in range(N_COINS):
        new_balances[i] -= amounts[i]
    D1 = self.get_D_mem(new_balances, amp)
    fees = []
    for i in range(N_COINS):
        ideal_balance = D1 * old_balances[i] / D0
        difference = 0
        if ideal_balance > new_balances[i]:
            difference = ideal_balance - new_balances[i]
        else:
            difference = new_balances[i] - ideal_balance
        fees[i] = _fee * difference / FEE_DENOMINATOR
        self.balances[i] = new_balances[i] - (fees[i] * _admin_fee / FEE_DENOMINATOR)
        new_balances[i] -= fees[i]
    D2 = self.get_D_mem(new_balances, amp)

    token_amount = (D0 - D2) * token_supply / D0
    assert token_amount != 0  # dev: zero tokens burned
    token_amount += 1  # In case of rounding errors - make it unfavorable for the "attacker"
    assert token_amount <= max_burn_amount, "Slippage screwed you"

    self.token.burnFrom(msg.sender, token_amount)  # dev: insufficient funds
    for i in range(N_COINS):
        if amounts[i] != 0:

            # "safeTransfer" which works for ERC20s which return bool or not
            _response: Bytes[32] = raw_call(
                self.coins[i],
                concat(
                    method_id("transfer(address,uint256)"),
                    convert(msg.sender, bytes32),
                    convert(amounts[i], bytes32),
                ),
                max_outsize=32,
            )  # dev: failed transfer
            if len(_response) > 0:
                assert convert(_response, bool)  # dev: failed transfer


def get_y_D(A_, i, xp, D):
    """
    Calculate x[i] if one reduces D from being calculated for xp to D

    Done by solving quadratic equation iteratively.
    x_1**2 + x1 * (sum' - (A*n**n - 1) * D / (A * n**n)) = D ** (n + 1) / (n ** (2 * n) * prod' * A)
    x_1**2 + b*x_1 = c

    x_1 = (x_1**2 + c) / (2*x_1 + b)
    """
    # x in the input is converted to the same price/precision

    assert i >= 0  # dev: i below zero
    assert i < N_COINS  # dev: i above N_COINS

    c = D
    S_ = 0
    Ann = A_ * N_COINS

    _x = 0
    for _i in range(N_COINS):
        if _i != i:
            _x = xp[_i]
        else:
            continue
        S_ += _x
        c = c * D / (_x * N_COINS)
    c = c * D / (Ann * N_COINS)
    b = S_ + D / Ann
    y_prev = 0
    y = D
    for _i in range(255):
        y_prev = y
        y = (y*y + c) / (2 * y + b - D)
        # Equality with the precision of 1
        if y > y_prev:
            if y - y_prev <= 1:
                break
        else:
            if y_prev - y <= 1:
                break
    return y







