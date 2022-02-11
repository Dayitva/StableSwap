import smartpy as sp

dex = sp.io.import_script_from_url("file:./contracts/dex.py")
fa12 = dex.fa12
Dex = dex.Dex
Token = dex.Token

@sp.add_test(name="Test DEX")
def test():
    admin = sp.test_account("Admin")
    alice = sp.test_account("Alice")
    bob = sp.test_account("Robert")
    oscar = sp.test_account("Oscar")
    token_admin = sp.test_account("Token Admin")
    
    DECIMALS_0 = 10 ** 6
    DECIMALS_1 = 10 ** 18
    scenario = sp.test_scenario()
    
    token1_metadata = {
        "decimals": "6",
        "name": "USD Tez",
        "symbol": "USDTz",
        "icon": 'https://smartpy.io/static/img/logo-only.svg'
    }
    contract1_metadata = {
        "": "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    }
    token2_metadata = {
        "decimals": "18",
        "name": "Kolibri USD",
        "symbol": "KUSD",
        "icon": 'https://smartpy.io/static/img/logo-only.svg'
    }
    contract2_metadata = {
        "": "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    }
    
    usdtz = Token(
        token_admin.address,
        config=fa12.FA12_config(support_upgradable_metadata=True),
        token_metadata=token1_metadata,
        contract_metadata=contract1_metadata
    )
    kusd = Token(
        token_admin.address,
        config=fa12.FA12_config(support_upgradable_metadata=True),
        token_metadata=token2_metadata,
        contract_metadata=contract2_metadata
    )
    
    scenario += usdtz
    scenario += kusd
    kusd.mint(
        address=alice.address,
        value=sp.nat(100000 * DECIMALS_1)
    ).run(sender=token_admin)
    kusd.mint(
        address=admin.address,
        value=sp.nat(100000 * DECIMALS_1)
    ).run(sender=token_admin)
    kusd.mint(
        address=bob.address,
        value=sp.nat(100000 * DECIMALS_1)
    ).run(sender=token_admin)
    usdtz.mint(
        address=alice.address,
        value=sp.nat(100000 * DECIMALS_0)
    ).run(sender=token_admin)
    usdtz.mint(
        address=admin.address,
        value=sp.nat(100000 * DECIMALS_0)
    ).run(sender=token_admin)
    usdtz.mint(
        address=bob.address,
        value=sp.nat(100000 * DECIMALS_0)
    ).run(sender=token_admin)
    # Initialize the exchange.
    # Approve to spend by stable_swap address
    dex = Dex(
        x_address=kusd.address,
        # x_address=sp.address('KT1WJUr74D5bkiQM2RE1PALV7R8MUzzmDzQ9'),
        y_address=usdtz.address,
        # y_address=sp.address('KT1CNQL6xRn5JaTUcMmxwSc5YQjwpyHkDR5r'),
        _lp_token=sp.address('KT1-LP-TOKEN'),
        _admin=admin.address,
        x_decimals = sp.nat(DECIMALS_0),
        y_decimals = sp.nat(DECIMALS_1),
    )
    # lp_metadata = {
    #     "decimals": "9",
    #     "name": "LP Token",
    #     "symbol": "LP-TOKEN",
    #     "icon": 'https://smartpy.io/static/img/logo-only.svg'
    # }
    # lp_contract_metadata = {
    #     "": "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    # }
    scenario += dex
    # lp = Token(
    #     dex.address,
    #     config=fa12.FA12_config(support_upgradable_metadata=True),
    #     token_metadata=lp_metadata,
    #     contract_metadata=lp_contract_metadata
    # )
    # dex.set_lp_address(lp.address).run(sender=admin)
    kusd.approve(sp.record(
        spender=dex.address,
        value=sp.nat(50_000 * DECIMALS_1
                     ))).run(sender=admin)
    usdtz.approve(sp.record(
        spender=dex.address,
        value=sp.nat(50_000 * DECIMALS_0
                     ))).run(sender=admin)


    dex.initialize_exchange(
        token1_amount=sp.nat(50_000 * DECIMALS_1),
        token2_amount=sp.nat(50_000 * DECIMALS_0)
    ).run(sender=alice, valid=False)
    
    dex.initialize_exchange(
        token1_amount=sp.nat(50_000 * DECIMALS_1),
        token2_amount=sp.nat(50_000 * DECIMALS_0)
    ).run(sender=admin)
    
    dex.remove_liquidity(_amount = 25000 * (10**18), min_tok = {0: 1, 1: 1}).run(sender=alice, valid=False)
    dex.remove_liquidity(_amount = 25000 * (10**18), min_tok = {0: 1, 1: 1}).run(sender=oscar, valid=False)
    
    kusd.approve(sp.record(
        spender=dex.address,
        value=sp.nat(5000 * DECIMALS_1)
    )).run(sender=bob)
    
    dex.exchange(i=0, j=1, dx=5000 * DECIMALS_1, min_dy = 1).run(sender=bob)
    
    kusd.approve(sp.record(
        spender=dex.address,
        value=sp.nat(100 * DECIMALS_1
    ))).run(sender=alice)
    
    dex.add_liquidity(i=0, dx=100 * DECIMALS_1, min_tok=1).run(sender=alice)
    # dex.add_liquidity(i=0, dx=100 * DECIMALS_1, min_tok=1).run(sender=alice)
    # dex.add_liquidity(i=0, dx=100 * DECIMALS_1 ,min_tok=1).run(sender=alice)

    dex.remove_liquidity(_amount=100 * DECIMALS_1,  min_tok={0: 1, 1: 1}).run(sender=alice)
    dex.remove_liquidity(_amount=100 * DECIMALS_1,  min_tok={0: 1, 1: 1}).run(sender=alice)
    dex.remove_liquidity(_amount=100 * DECIMALS_1,  min_tok={0: 1, 1: 1}).run(sender=alice)
    
    dex.admin_claim().run(sender=admin)
    dex.admin_claim().run(sender=alice, valid=False)

    dex.update_A(sp.nat(1000)).run(sender=alice, valid=False)
    dex.update_A(sp.nat(100)).run(sender=admin)

    dex.update_fee(sp.nat(200)).run(sender=alice, valid=False)
    dex.update_fee(sp.nat(20)).run(sender=admin)