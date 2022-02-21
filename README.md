# Liquibrium

A decentralised stablecoin exchange on Tezos allowing users to trade similar assets at low slippage.

## Docs

[Read the docs](./docs/README.md)

## What's the need?

The simple answer is that a constant product market maker formula does not work well for stablecoins. Now that is a mouthful but the idea behind is not only simple but ingenious.

The use of automated market makers or AMMs for short completely removes the need for orderbooks like in traditional markets and users can exchange tokens based on a bonding curve which is only dependent of the supply of tokens available in the pool.

Quipuswap uses CPMM (Constant Product Market Maker). It just means that the product of the supply of both tokens must always remain constant. That's why constant product. There are other curves as well like constant sum where the sum must remain constant.

Now, while a CPMM works well for most assets, it puts stable assets at a disadvantage. Because if the pool is imbalanced or you want to exchange a large amount of tokens, you would have to pay a premium for that. Because as the supply of that asset goes down, it becomes pricier and pricier to get it. Hence, users have to incur high slippage for exchange tokens that should ideally trade 1:1

## The solution

Now that we have established the need, how do we actually do it?

And the answer is to use another curve. A curve that better models the dynamics of the stablecoin pools.

An added benefit of this is that liquidity providers also can now provide liquidity without the risk of impermanent loss.

Impermanent loss happens when you provide liquidity to a liquidity pool, and the price of your deposited assets changes compared to when you deposited them. The bigger this change is, the more you are exposed to impermanent loss. But since the assets are pegged to a certain value or move together in the case of wrapped tokens, users don't have to worry about it.

### Some tokens with decimals and standards

- kUSD = 10\*\*18 [FA1.2]
- wBUSD = 10\*\*18 [FA 2]
- wDAI = 10\*\*18[FA 2]
- uUSD = 10\*\*12[FA 2]
- USDtz = 10\*\*6[FA1.2]
- wUSDC = 10\*\*6[FA 2]
- wUSDT = 10\*\*6[FA 2]

## Reference

1. Curve Whitepaper
2. Uniswap Whitepaper

Changes

1. dx has been adjusted in 304
2. Early check for lp_amount implemented
3. rejected sent tez
4. improved get_y, exchange.
5. Loops removed to make it efficient for 2 coins
6. token_supply calculated once and passed in get_D
7. TZIP-016 standard
8. admin_fee now in token_pool record
9. mint_lp, burn_lp, get_D are private lambdas
10. double checking for amount before transferring removed

To test and prove:
1. Check when D is 0 and One side of pool is empty.
2. Fee and LP calc and handling
3. newton method for get_D and get_y

To do:
1. improve documentation
2. improved tests checked with exact values
3. convert transferToTokenId to a lambda
4. implement transaction deadline

To ask:
1. sp.local changes at multiple places
2. euclidean division in get_D and / over //