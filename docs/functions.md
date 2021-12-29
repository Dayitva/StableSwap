# Functions

## Mint Helper

Definition: `mint_lp(amount: sp.TNat)`

Type: `Helper`

This method is used to mint FA1.2 tokens by doing an inter contract
call to the `mint` entry point in the FA1.2 token contract.

## Burn Helper

Definition: `burn_lp(amount: sp.TNat)`

Type: `Helper`

This method is used to burn FA1.2 tokens by doing an inter contract
call to the `burn` entry point in the FA1.2 token contract.

## Transfer Helper

Definition: `transferToTokenId(_from: sp.TAddress, _to: sp.TAddress, _amount: sp.TNat, _token_id: sp.TNat=0)`

Type: `Helper`

This method provides a abstraction to transfer `_amount` amount of FA1.2/FA2 token from `_from` to `_to`. `_token_id` here represents the key of the tokens in the `token_pool` contract. We use this id to get the corresponding value from the storage and call `fa2Transfer` or `fa12Transfer` depending upon a `fa2` which is a boolean variable that represents whether that token in FA1.2 or FA2.

## get_D

Definition: `get_D()`

Type: `Helper`

This a helper method that calculates `D`, which is a constant for any given pool. It represents the total amount of tokens when they have an equal price`

## get_y

Definition: `get_y(i: sp.TNat, j: sp.TNat, x: sp.TNat)`

Type: `Helper`

This method returns the new amount of `j` tokens that will be left in the pool when the user wants to exchange `i` token into `j` tokens where `x` is the new amount of `i` tokens into the pool i.e the sum of old amount of `i` tokens in the pool and the amount of `i` tokens that the user wants to exchange.

## Fee Update

Definition: `update_fee(new_fee: sp.TNat)`

Type: `Entry Point`

This entry point allows the admin to change the fee (in parts per 10 thousand) that we'll deduct when someone make trades in the pool.

## Claim for Admin

Definition: `admin_claim()`

Type: `Entry Point`

This is the function that allows an admin to withdraw the accumulated fees from the protocol.

## Update LP Token Address

Definition: `set_lp_address(address: sp.TAddress)`

Type: `Entry Point`

This entry point allows admin to set the LP token address (an FA1.2 token contract address) for the pool.

## Initialize Exchange

Definition: `initialize_exchange(token1_amount: sp.TNat, token2_amount: sp.TNat)`

Type: `Entry Point`

This function allows the dex to be initialized, positive non-zero amounts of both the tokens in the pool need to be provided to initialize the pool.

## Update A

Definition: `update_A(new_A: sp.TNat)`

Type: `Entry Point`

This entry point allows user to change the value of `A`, the amplication coefficient for a specific pool. `A` represents the skewness of the pool, with `A = 0` meaning that the pool exibhits a constant-product market maker character, and `A > 0` decides the pools constant-sum market maker character.

## Exchange

Definition: `exchange(i: sp.TNat, j: sp.TNat, dx: sp.TNat)`

Type: `Entry Point`

This entry point exchange `dx` amount of `i` tokens into the `j` tokens the resulting amount of `j` tokens that the user will get is calculated by the difference between existing amount of `j` tokens in the pool and `y` which we get from `get_y()`.

## Add Liquidity

Definition: `add_liquidity(i: sp.TNat, dx: sp.TNat)`

Type: `Entry Point`

This function is used to add `dx` amount of `i` tokens to the pool. It uses the intial invariant (before addition of the token) and final invariant value (after addition of these `dx` tokens) to decide the amount of LP tokens to be disbursed.

## Remove Liquidity

Definition: `remove_liquidity(_amount: sp.TNat)`

Type: `Entry Point`

This entry point removes the user's liquidity from the pool based on the amount of LP tokens the user wants to burn which is represented by the `_amount`.

## Total Supply

Definition: `get_totalSupply()`

Type: `OffChain View`

This function is used to obtain the total supply for a given pool.

## get_dy

Definition: `get_dy(params: sp.TRecord(i: sp.TNat, j: sp.TNat, dx: sp.TNat))`

Type: `OffChain View`

It's a offchain view that calculates the amount of `params.j` tokens you will get when you want to exchange `params.dx` amount of `params.i` tokens into `params.j` tokens.

## Goto Home

[Goto Home](./README.md)
