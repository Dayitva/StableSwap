#!/bin/bash

smartpy=~/smartpy-cli/SmartPy.sh

# Compile the contract.
$smartpy compile ./dex_new.py ./output 

# Deploy the contract.
$smartpy originate-contract \
    --code ./output/Dex_Compilation_Target/step_000_cont_0_contract.tz \
    --storage ./output/Dex_Compilation_Target/step_000_cont_0_storage.tz \
    --rpc https://granadanet.smartpy.io