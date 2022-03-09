import smartpy as sp

dex = sp.io.import_script_from_url("file:./contracts/dex.py")
Dex = dex.Dex
Token = dex.Token
fa12 = dex.fa12
fa2 = dex.fa2
TokenFA2 = dex.TokenFA2

kusd_contract_metadata = """
{ "name": "Kolibri Token Contract", "description": "FA1.2 Implementation of kUSD", "authors": ["Hover Labs <hello@hover.engineering>"], "homepage":  "https://kolibri.finance", "interfaces": [ "TZIP-007-2021-01-29"] }
"""

llp_contract_metadata = """
{ "name": "Liquibrium LP contract", "description": "FA1.2 Implementation of LLP", "authors": ["@liquibrium"], "homepage":  "https://liquibrium.finance", "interfaces": [ "TZIP-007-2021-01-29"] }
"""
admin = sp.address("tz1WNKahMHz1bkuAfZrsvtmjBhh4GJzw8YcU")

def main():
    # Token 1
    sp.add_compilation_target("kUSD", Token(
        admin=admin,
        config=fa12.FA12_config(support_upgradable_metadata=True),
        token_metadata= {
            "decimals": "18",
            "name": "Kolibri USD",
            "symbol": "kUSD",
            "icon": 'https://kolibri-data.s3.amazonaws.com/logo.png'
        },
        contract_metadata={
            "": kusd_contract_metadata
        }
    ))

    sp.add_compilation_target("LLP", Token(
        admin=admin,
        config=fa12.FA12_config(support_upgradable_metadata=True),
        token_metadata= {
            "decimals": "18",
            "name": "Liquibrium LP",
            "symbol": "LLP",
            "icon": 'https://placekitten.com/100/100'
        },
        contract_metadata={
            "": llp_contract_metadata
        }
    ))

    # Token 2
    sp.add_compilation_target("TokenFA2", TokenFA2(
        admin = admin,
        config = fa2.FA2_config(),
        metadata = sp.big_map({
            "": sp.utils.bytes_of_string("tezos-storage:content"),
            "content": sp.utils.bytes_of_string("""{"name": "Liquibrium Finance"}"""),
        })
    ))

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

    # sp.add_compilation_target("Dex Compilation Target", Dex(
    #     x_address=sp.address('KT1WJUr74D5bkiQM2RE1PALV7R8MUzzmDzQ9'),
    #     y_address=sp.address('KT1CNQL6xRn5JaTUcMmxwSc5YQjwpyHkDR5r'),
    #     _lp_token=sp.address('KT1Nv2h1bHPLYZsGrCdfdvwKzXsZrFEfJnpJ'),
    #     x_decimals=sp.nat(1000000),
    #     y_decimals=sp.nat(1000000000000),
    #     _admin=sp.address("tz1WNKahMHz1bkuAfZrsvtmjBhh4GJzw8YcU")
    # ))

if __name__ == "__main__":
    main()