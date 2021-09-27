import smartpy as sp
fa12 = sp.io.import_script_from_url("https://smartpy.io/templates/FA1.2.py")

class Token(fa12.FA12):
  pass

@sp.add_test(name="Token")
def test():
  admin = sp.address("tz1UYZ6SMKD5A4fpviTDd1EBixZe1f5arN76")
  scenario = sp.test_scenario()
  token_metadata = {
      "decimals": "9",
      "name": "KUSD Token",
      "symbol": "KUSD",
      "icon": 'https://smartpy.io/static/img/logo-only.svg'
  }
  contract_metadata = {
      "" : "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
  }

  token = Token(
    admin,
    config = fa12.FA12_config(support_upgradable_metadata=True),
    token_metadata = token_metadata,
    contract_metadata = contract_metadata
  )
  scenario += token