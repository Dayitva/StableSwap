# Liquibrium

A decentralised stablecoin exchange on Tezos

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

## Exchange Pairs Avaliable

### kUSD <-> USDtz

You can get these tokens from the faucet provided. Make sure you are on the Granada testnet and add these addresses in your wallet for the best experience.
Test kUSD address: `KT1WJUr74D5bkiQM2RE1PALV7R8MUzzmDzQ9`
Test USDtz address: `KT1CNQL6xRn5JaTUcMmxwSc5YQjwpyHkDR5r`
Test LP token address: `KT1Nv2h1bHPLYZsGrCdfdvwKzXsZrFEfJnpJ`

Decimals is 9 for all the tokens.