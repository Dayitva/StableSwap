import smartpy as sp

dex = sp.io.import_script_from_url("file:./contracts/dex.py")
Dex = dex.Dex

def main():
    ## Token 1
    # sp.add_compilation_target("Token", Token(
    #     admin=admin,
    #     config=fa12.FA12_config(support_upgradable_metadata=True),
    #     token_metadata= {
    #         "decimals": "18",
    #         "name": "Kolibri USD",
    #         "symbol": "KUSD",
    #         "icon": 'https://smartpy.io/static/img/logo-only.svg'
    #     },
    #     contract_metadata={
    #         "": "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    #     }
    # ))

    ## Token 2
    # sp.add_compilation_target("Token", Token(
    #     admin=admin,
    #     config=fa12.FA12_config(support_upgradable_metadata=True),
    #     token_metadata= {
    #         "decimals": "6",
    #         "name": "USD Tez",
    #         "symbol": "USDtz",
    #         "icon": 'https://smartpy.io/static/img/logo-only.svg'
    #     },
    #     contract_metadata={
    #         "": "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    #     }
    # ))

    ## LP Token
    # sp.add_compilation_target("Token", Token(
    #     admin=admin,
    #     config=fa12.FA12_config(support_upgradable_metadata=True),
    #     token_metadata= {
    #         "decimals": "18",
    #         "name": "KUSD <-> USDtz",
    #         "symbol": "LP Token",
    #         "icon": 'https://smartpy.io/static/img/logo-only.svg'
    #     },
    #     contract_metadata={
    #         "": "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    #     }
    # ))

    sp.add_compilation_target("Dex Compilation Target", Dex(
        x_address=sp.address('KT1WJUr74D5bkiQM2RE1PALV7R8MUzzmDzQ9'),
        y_address=sp.address('KT1CNQL6xRn5JaTUcMmxwSc5YQjwpyHkDR5r'),
        _lp_token=sp.address('KT1Nv2h1bHPLYZsGrCdfdvwKzXsZrFEfJnpJ'),
        x_decimals=sp.nat(1000000),
        y_decimals=sp.nat(1000000000000),
        _admin=sp.address("tz1WNKahMHz1bkuAfZrsvtmjBhh4GJzw8YcU")
    ))

if __name__ == "__main__":
    main()