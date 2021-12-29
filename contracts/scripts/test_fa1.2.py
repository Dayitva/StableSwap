import smartpy as sp
fa12 = sp.io.import_script_from_url("https://smartpy.io/templates/FA1.2.py")

class Token(fa12.FA12):
    """ Test FA1.2 Token """
    pass

@sp.add_test(name="deploy fa1.2")
    admin = sp.address("tz1WNKahMHz1bkuAfZrsvtmjBhh4GJzw8YcU")
    token_metadata = {
        "decimals": "9",
        "name": "USD Tez",
        "symbol": "USDTz",
        "icon": 'https://img.templewallet.com/insecure/fit/64/64/ce/0/plain/https://quipuswap.com/tokens/usdtz.png'
    }
    contract_metadata = {
        "": "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    }

