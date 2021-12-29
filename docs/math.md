# Math

Consider x and y to be the token amounts available in the liquidity pool.

A Constant Product Market Maker (CPMM) Curve is a curve that is defined by the following equation:

```
x * y = k
```

where k is called the pool invariant.

It tries to keep the product constant. If you need to exchange `a` number of tokens , you will receive ```y - k/(x+a)``` tokens.

However, this curve is not suited for stablecoins because the amount you get of exchanging goes down as you try to exchange more tokens.

Hence, a new curve needs to be defined that is more suited for stablecoins.

`

## Goto Home

[Goto Home](./README.md)
