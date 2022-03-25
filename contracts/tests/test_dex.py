import smartpy as sp

dex = sp.io.import_script_from_url("file:./contracts/dex.py")
fa12 = dex.fa12
Dex = dex.Dex
Token = dex.Token


@sp.add_test(name="Test_DEX")
def test():
    admin = sp.address("tz1-Admin")
    alice = sp.address("tz1-Alice")
    bob = sp.address("tz1-Robert")
    oscar = sp.address("tz1-Oscar")
    token_admin = sp.address("tz1-TokenAdmin")

    DECIMALS_USDTZ = 10 ** 6
    DECIMALS_KUSD = 10 ** 8
    DECIMALS_EIGHTEEN = 10 ** 18

    scenario = sp.test_scenario()

    scenario.table_of_contents()
    scenario.h1("Test DEX")

    scenario.h2("Test Accounts")

    scenario.table_of_contents()

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
        "decimals": "8",
        "name": "Kolibri USD",
        "symbol": "KUSD",
        "icon": 'https://smartpy.io/static/img/logo-only.svg'
    }
    contract2_metadata = {
        "": "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    }

    usdtz = Token(
        token_admin,
        config=fa12.FA12_config(support_upgradable_metadata=True),
        token_metadata=token1_metadata,
        contract_metadata=contract1_metadata
    )

    kusd = Token(
        token_admin,
        config=fa12.FA12_config(support_upgradable_metadata=True),
        token_metadata=token2_metadata,
        contract_metadata=contract2_metadata
    )

    scenario += usdtz
    scenario += kusd

    scenario.h2("Minting tokens to users")

    kusd.mint(
        address=alice,
        value=sp.nat(100000 * DECIMALS_KUSD)
    ).run(sender=token_admin)
    kusd.mint(
        address=admin,
        value=sp.nat(100000 * DECIMALS_KUSD)
    ).run(sender=token_admin)
    kusd.mint(
        address=bob,
        value=sp.nat(100000 * DECIMALS_KUSD)
    ).run(sender=token_admin)
    usdtz.mint(
        address=alice,
        value=sp.nat(100000 * DECIMALS_USDTZ)
    ).run(sender=token_admin)
    usdtz.mint(
        address=admin,
        value=sp.nat(100000 * DECIMALS_USDTZ)
    ).run(sender=token_admin)
    usdtz.mint(
        address=bob,
        value=sp.nat(100000 * DECIMALS_USDTZ)
    ).run(sender=token_admin)
    
    lp_metadata = {
        "decimals": "9",
        "name": "LP Token",
        "symbol": "LP-TOKEN",
        "icon": 'https://smartpy.io/static/img/logo-only.svg'
    }
    lp_contract_metadata = {
        "": "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    }
    lp = Token(
        token_admin,
        config=fa12.FA12_config(support_upgradable_metadata=True),
        token_metadata=lp_metadata,
        contract_metadata=lp_contract_metadata
    )

    dex = Dex(
        x_address=kusd.address,
        # x_address=sp.address('KT1WJUr74D5bkiQM2RE1PALV7R8MUzzmDzQ9'),
        y_address=usdtz.address,
        # y_address=sp.address('KT1CNQL6xRn5JaTUcMmxwSc5YQjwpyHkDR5r'),
        _lp_token=lp.address,
        _admin=admin,
        x_decimals=sp.nat(DECIMALS_KUSD),
        y_decimals=sp.nat(DECIMALS_USDTZ),
        x_is_fa2=False,
        y_is_fa2=False,
        x_token_id=0,
        y_token_id=0
    )

    scenario += lp
    scenario += dex

    scenario.h2("Making dex, the admin of LP token")
    lp.setAdministrator(dex.address).run(sender=token_admin)

    # dex.set_lp_address(lp.address).run(sender=admin)

    scenario.h2("Approving tokens")

    kusd.approve(sp.record(
        spender=dex.address,
        value=sp.nat(50_000 * DECIMALS_KUSD
                     ))).run(sender=admin)
    usdtz.approve(sp.record(
        spender=dex.address,
        value=sp.nat(50_000 * DECIMALS_USDTZ
                     ))).run(sender=admin)

    scenario.h2("[INVALID] Initialize exchange.")
    dex.initialize_exchange(
        token1_amount=sp.nat(50_000 * DECIMALS_KUSD),
        token2_amount=sp.nat(50_000 * DECIMALS_USDTZ)
    ).run(sender=alice, valid=False)

    scenario.h2("Initialize exchange.")
    dex.initialize_exchange(
        token1_amount=sp.nat(50_000 * DECIMALS_KUSD),
        token2_amount=sp.nat(50_000 * DECIMALS_USDTZ)
    ).run(sender=admin)

    # scenario.h2("[INVALID] Remove liquidity.")
    # dex.remove_liquidity(_amount=25000 * (10**18), min_tokens={
    #                      0: sp.as_nat(1), 1: sp.as_nat(1)}).run(sender=alice, valid=False)
    # scenario.h2("[INVALID] Remove liquidity.")
    # dex.remove_liquidity(_amount=25000 * (10**18), min_tokens={
    #                      0: sp.as_nat(1), 1: sp.as_nat(1)}).run(sender=oscar, valid=False)

    kusd.approve(sp.record(
        spender=dex.address,
        value=sp.nat(50_000 * DECIMALS_KUSD)
    )).run(sender=bob)
    usdtz.approve(sp.record(
        spender=dex.address,
        value=sp.nat(50_000 * DECIMALS_USDTZ)
    )).run(sender=bob)
    
    scenario.h2("Exchange tokens")
    dex.exchange(i=1, dx=5000 * DECIMALS_USDTZ, min_dy=1 * DECIMALS_KUSD,
                 time_valid_upto=sp.timestamp(100000)).run(sender=bob)

    kusd.approve(sp.record(
        spender=dex.address,
        value=sp.nat(50_000 * DECIMALS_KUSD
                     ))).run(sender=alice)

    usdtz.approve(sp.record(
        spender=dex.address,
        value=sp.nat(50_000 * DECIMALS_USDTZ
                     ))).run(sender=alice)

    ### TESTS BEGIN HERE ###

    scenario.h2("Test 1: Initialising by Oscar. Should fail as he is not admin.")
    dex.initialize_exchange(
        token1_amount=sp.nat(50_000 * DECIMALS_KUSD),
        token2_amount=sp.nat(50_000 * DECIMALS_USDTZ)
    ).run(sender=oscar, valid=False)

    scenario.h2("Alice :: Adding liquidity. 200")
    dex.add_liquidity(_amount0=200 * DECIMALS_USDTZ, _amount1=0 *
                      DECIMALS_KUSD, min_token=1).run(sender=alice)
    scenario.h2("Alice :: Adding liquidity. 10")
    dex.add_liquidity(_amount0=10 * DECIMALS_USDTZ, _amount1=0 *
                      DECIMALS_KUSD, min_token=1).run(sender=alice)
    scenario.h2("Alice :: Adding liquidity. 5000")
    dex.add_liquidity(_amount0=5000 * DECIMALS_USDTZ, _amount1=0 *
                      DECIMALS_KUSD, min_token=1).run(sender=alice)
    scenario.h2("Alice :: Adding liquidity. 200")
    dex.add_liquidity(_amount0=200 * DECIMALS_USDTZ, _amount1=200 *
                      DECIMALS_KUSD, min_token=1).run(sender=alice)
    scenario.h2("Alice :: Adding liquidity. 100")
    dex.add_liquidity(_amount0=100 * DECIMALS_USDTZ, _amount1=10 *
                      DECIMALS_KUSD, min_token=1).run(sender=alice)
    scenario.h2("Alice :: Adding liquidity. 5000")
    dex.add_liquidity(_amount0=5000 * DECIMALS_USDTZ, _amount1=100 *
                      DECIMALS_KUSD, min_token=1).run(sender=alice)

    dex.remove_liquidity(_amount=200 * DECIMALS_USDTZ,
                         min_tokens={0: 1, 1: 1}).run(sender=alice)
    dex.remove_liquidity(_amount=10 * DECIMALS_USDTZ,
                         min_tokens={0: 1, 1: 1}).run(sender=alice)
    dex.remove_liquidity(_amount=5000 * DECIMALS_USDTZ,
                         min_tokens={0: 1, 1: 1}).run(sender=alice)
    dex.remove_liquidity(_amount=400 * DECIMALS_USDTZ,
                         min_tokens={0: 1, 1: 1}).run(sender=alice)
    dex.remove_liquidity(_amount=110 * DECIMALS_USDTZ,
                         min_tokens={0: 1, 1: 1}).run(sender=alice)
    dex.remove_liquidity(_amount=4500 * DECIMALS_USDTZ,
                         min_tokens={0: 1, 1: 1}).run(sender=alice)

    dex.remove_liquidity(_amount=50_000 * DECIMALS_USDTZ,
                         min_tokens={0: 1, 1: 1}).run(sender=admin)
    dex.remove_liquidity(_amount=50_000 * DECIMALS_USDTZ,
                         min_tokens={0: 1, 1: 1}).run(sender=admin)

    scenario.h2(
        "Test 5: Adding liquidity by Alice. Should fail as she is asking for more min tokens than possible.")
    dex.add_liquidity(_amount0=200 * DECIMALS_KUSD, _amount1=0 *
                      DECIMALS_USDTZ, min_token=200).run(sender=alice, valid=False)

    scenario.h2(
        "Test 6: Adding liquidity by Alice. Should fail as she is adding more liquidity than what she is approved for.")
    dex.add_liquidity(_amount0=100001 * DECIMALS_KUSD, _amount1=200 *
                      DECIMALS_USDTZ, min_token=400).run(sender=alice, valid=False)

    scenario.h2(
        "Test 7: Adding liquidity by Alice. Should fail as she is sending tez along with the transaction.")
    dex.add_liquidity(_amount0=200 * DECIMALS_KUSD, _amount1=0 * DECIMALS_USDTZ,
                      min_token=200).run(sender=alice, amount=sp.mutez(1), valid=False)

    scenario.h2(
        "Test 8: Adding liquidity by Alice. Should succeed with correct return values.")
    dex.add_liquidity(_amount0=200 * DECIMALS_KUSD, _amount1=200 *
                      DECIMALS_USDTZ, min_token=400).run(sender=alice)
    scenario.verify(dex.data.token_pool[0].pool == 50200 * DECIMALS_EIGHTEEN)
    scenario.verify(dex.data.token_pool[1].pool == 50200 * DECIMALS_EIGHTEEN)
    # scenario.verify(dex.data.lp_balance[alice.address] == 400 * DECIMALS_EIGHTEEN)

    scenario.h2(
        "Test 9: Removing liquidity by Alice. Should fail as she is asking for more min tokens than possible.")
    dex.remove_liquidity(_amount=400 * DECIMALS_EIGHTEEN, min_tokens={
                         0: 1000*DECIMALS_KUSD, 1: 1000*DECIMALS_USDTZ}).run(sender=alice, valid=False)

    scenario.h2(
        "Test 10: Removing liquidity by Alice. Should fail as she does not have sufficient LP tokens.")
    dex.remove_liquidity(_amount=401 * DECIMALS_EIGHTEEN, min_tokens={
                         0: 200*DECIMALS_KUSD, 1: 200*DECIMALS_USDTZ}).run(sender=alice, valid=False)

    scenario.h2(
        "Test 11: Removing liquidity by Alice. Should fail as she is sending tez along with the transaction.")
    dex.remove_liquidity(_amount=100 * DECIMALS_EIGHTEEN, min_tokens={
                         0: 2*DECIMALS_KUSD, 1: 2*DECIMALS_USDTZ}).run(sender=alice, amount=sp.mutez(1), valid=False)

    scenario.h2(
        "Test 12: Removing liquidity by Alice. Should succeed with correct return values.")
    dex.remove_liquidity(_amount=400 * DECIMALS_EIGHTEEN,
                         min_tokens={0: 200*DECIMALS_KUSD, 1: 200*DECIMALS_USDTZ}).run(sender=alice)
    scenario.verify(dex.data.token_pool[0].pool == 50000 * DECIMALS_EIGHTEEN)
    scenario.verify(dex.data.token_pool[1].pool == 50000 * DECIMALS_EIGHTEEN)
    # scenario.verify(dex.data.lp_balance[alice.address] == 0 * DECIMALS_EIGHTEEN)

    scenario.h2(
        "Test 13: Exchange operation by Bob. Should fail as he is asking for more min tokens than allowed.")
    dex.exchange(i=0, dx=5000 * DECIMALS_KUSD, min_dy=5001 * DECIMALS_USDTZ, time_valid_upto=sp.timestamp_from_utc(2022,
                 2, 21, 23, 59, 59)).run(sender=bob, valid=False, now=sp.timestamp_from_utc(2022, 2, 20, 23, 59, 59))

    scenario.h2(
        "Test 14: Exchange operation by Bob. Should fail as he is exchanging more tokens than he is approved for.")
    dex.exchange(i=0, dx=100001 * DECIMALS_KUSD, min_dy=5001 * DECIMALS_USDTZ, time_valid_upto=sp.timestamp_from_utc(
        2022, 2, 21, 23, 59, 59)).run(sender=bob, valid=False, now=sp.timestamp_from_utc(2022, 2, 20, 23, 59, 59))

    scenario.h2(
        "Test 15: Exchange operation by Bob. Should fail as the transaction takes more than he wanted it valid for.")
    dex.exchange(i=0, dx=100001 * DECIMALS_KUSD, min_dy=5001 * DECIMALS_USDTZ, time_valid_upto=sp.timestamp_from_utc(
        2022, 2, 21, 23, 59, 59)).run(sender=bob, valid=False, now=sp.timestamp_from_utc(2022, 2, 22, 23, 59, 59))

    scenario.h2(
        "Test 16: Exchange operation by Bob. Should fail as he is sending tez along with the transaction.")
    dex.exchange(i=0, dx=100 * DECIMALS_KUSD, min_dy=50 * DECIMALS_USDTZ, time_valid_upto=sp.timestamp_from_utc(2022, 2, 21,
                 23, 59, 59)).run(sender=bob, amount=sp.mutez(1), valid=False, now=sp.timestamp_from_utc(2022, 2, 22, 23, 59, 59))

    scenario.h2(
        "Test 17: Exchange operation by Bob. Should succeed with correct return values.")
    dex.exchange(i=0, dx=5000 * DECIMALS_KUSD, min_dy=4986 * DECIMALS_USDTZ, time_valid_upto=sp.timestamp_from_utc(
        2022, 2, 21, 23, 59, 59)).run(sender=bob, now=sp.timestamp_from_utc(2022, 2, 20, 23, 59, 59))
    scenario.verify(dex.data.token_pool[0].pool == 55000 * DECIMALS_EIGHTEEN)
    scenario.verify(dex.data.token_pool[1].pool >= 45213 * DECIMALS_KUSD)

    scenario.h2(
        "Test 18: Exchange operation by Bob from token 0 to token 1. Should succeed with correct return values.")
    dex.exchange(i=0, dx=1000 * DECIMALS_KUSD, min_dy=995 * DECIMALS_USDTZ, time_valid_upto=sp.timestamp_from_utc(
        2022, 2, 21, 23, 59, 59)).run(sender=bob, now=sp.timestamp_from_utc(2022, 2, 20, 23, 59, 59))
    scenario.verify(dex.data.token_pool[0].pool == 56000 * DECIMALS_EIGHTEEN)
    scenario.verify(dex.data.token_pool[1].pool >= 44017 * DECIMALS_KUSD)

    scenario.h2(
        "Test 19: Exchange operation by Bob from token 1 to token 0. Should succeed with correct return values.")
    dex.exchange(i=1, dx=1000 * DECIMALS_USDTZ, min_dy=1001 * DECIMALS_KUSD, time_valid_upto=sp.timestamp_from_utc(
        2022, 2, 21, 23, 59, 59)).run(sender=bob, now=sp.timestamp_from_utc(2022, 2, 20, 23, 59, 59))
    scenario.verify(dex.data.token_pool[0].pool >= 54998 * DECIMALS_EIGHTEEN)
    scenario.verify(dex.data.token_pool[1].pool >= 45017 * DECIMALS_KUSD)

    scenario.h2(
        "Test 20: Claiming admin fees by Oscar. Should fail as he is not admin.")
    dex.admin_claim().run(sender=oscar, valid=False)

    scenario.h2("Test 21: Claiming admin fees by Admin. Should succeed.")
    dex.admin_claim().run(sender=admin)
    scenario.verify(dex.data.token_pool[0].pool >= 54998 * DECIMALS_EIGHTEEN)
    scenario.verify(dex.data.token_pool[1].pool >= 45012 * DECIMALS_EIGHTEEN)

    scenario.h2(
        "Test 22: Removing all liquidity by Admin. Should fail as admin is removing more liquidity than allowed for.")
    dex.remove_liquidity(_amount=100001 * DECIMALS_EIGHTEEN, min_tokens={
                         0: 50000*DECIMALS_KUSD, 1: 50000*DECIMALS_USDTZ}).run(sender=admin, valid=False)

    scenario.h2("Test 23: Removing all liquidity by Admin. Should succeed.")
    dex.remove_liquidity(_amount=100000 * DECIMALS_EIGHTEEN,
                         min_tokens={0: 40000*DECIMALS_KUSD, 1: 40000*DECIMALS_USDTZ}).run(sender=admin)
    scenario.verify(dex.data.token_pool[0].pool <= 10 * DECIMALS_EIGHTEEN)
    scenario.verify(dex.data.token_pool[1].pool <= 10 * DECIMALS_EIGHTEEN)
    # scenario.verify(dex.data.lp_balance[admin.address] == 0 * DECIMALS_EIGHTEEN)

    scenario.h2("Test 24: Updating A by Oscar. Should fail as he is not admin.")
    dex.update_A(sp.nat(100)).run(sender=oscar, valid=False)

    scenario.h2("Test 25: Updating A by Admin. Should succeed.")
    dex.update_A(sp.nat(100)).run(sender=admin)
    scenario.verify(dex.data.A == 100)

    scenario.h2(
        "Test 26: Updating fee by Oscar. Should fail as he is not admin.")
    dex.update_fee(sp.nat(200)).run(sender=oscar, valid=False)

    scenario.h2("Test 27: Updating fee by Admin. Should succeed.")
    dex.update_fee(sp.nat(20)).run(sender=admin)
    scenario.verify(dex.data.fee == 20)

    scenario.h2(
        "Test 28: Update the lp token address by Oscar. Should fail as he is not admin.")
    dex.set_lp_address(lp.address).run(sender=oscar, valid=False)

    scenario.h2("Test 29: Update the lp token address. Should succeed.")
    dex.set_lp_address(lp.address).run(sender=admin)

    # scenario.h2(
    #     "Test 30: Adding liquidity by Alice. Should fail as the the contract is paused by the admin.")
    # dex.togglePause().run(sender=admin)
    # dex.add_liquidity(_amount0=10 * DECIMALS_KUSD, _amount1=20 *
    #                   DECIMALS_USDTZ, min_token=1).run(sender=alice, valid=False)
