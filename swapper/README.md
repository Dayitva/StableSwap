# Swapper

A client for StableSwap.

## How to setup the frontend

By doing `yarn install` and then `yarn start` to run.

## Contracts.

Below are some of the deployed FA1.2 token contract.

1. KUSD: `KT1WJUr74D5bkiQM2RE1PALV7R8MUzzmDzQ9`
2. USDTz: `KT1CNQL6xRn5JaTUcMmxwSc5YQjwpyHkDR5r`
3. LP Token: `KT1StTa4Bv1hFMRFnYQq2jgx6tCHkLUd632s`

> Admin: `tz1UYZ6SMKD5A4fpviTDd1EBixZe1f5arN76`

Below are some of the deployed StableSwap Contracts.

1. kUSD-USDtz

- Address: `KT1DJGEjVSKWYoypUvUPV1RJ7Td9YJT5rJYt`

## Todo

- [ ] To show the stats of the pool.

## TODO

- Show future plans.
  - What difference will it bring to ecosystem.
  - How will it make difference.
- How it is different.

- For scaling this we're raising funds.

## What is left ?

1. Introduction of fee.
2. Factory contract, to add multiple

<!-- {
  (address1, address2): pool_address,
  (address1, address2): pool_address,
  (address1, address2): pool_address,
} -->

## Transaction

```json
[
  {
    "destination": "KT1LJesKshgXJRQawFXYhTyjpjPnsymaqxL4",
    "kind": "transaction",
    "amount": 0,
    "parameters": {
      "entrypoint": "remove_liquidity",
      "value": {
        "prim": "Pair",
        "args": [
          { "int": "200119992519101583032808" },
          [
            {
              "prim": "Elt",
              "args": [{ "int": "0" }, { "int": "98829794820940785782501" }]
              "98829794820940777403208"
            },
            {
              "prim": "Elt",
              "args": [{ "int": "1" }, { "int": "101290900650" }]
            }
          ]
        ]
      }
    }
  }
]
```
