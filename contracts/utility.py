import smartpy as sp 
from contracts.errors import Error


class TokenUtility:
    """ Contains Utility Method. """
    def fa12Transfer(self, _from, _to, _amount, _address):
        """ Transfer for FA1.2 Token """
        sp.verify(_amount > 0, Error.INSUFFICIENT_AMOUNT)

        transfer_type = sp.TRecord(
            from_=sp.TAddress,
            to_=sp.TAddress,
            value=sp.TNat
        ).layout(("from_ as from", ("to_ as to", "value")))
        transfer_data = sp.record(from_=_from, to_=_to, value=_amount)

        token_contract = sp.contract(
            transfer_type,
            _address,
            "transfer"
        ).open_some()
        sp.transfer(transfer_data, sp.mutez(0), token_contract)
    
    def fa2Transfer(self, _from, _to, _amount, _token_id, _address):
        """ Transfer for FA2 tokens. """
        sp.verify(_amount > 0, Error.INSUFFICIENT_AMOUNT)
        
        TTransferParams = sp.TList(
            sp.TRecord(
                from_ = sp.TAddress,
                txs = sp.TList(
                    sp.TRecord(
                        amount = sp.TNat,
                        to_ = sp.TAddress,
                        token_id = sp.TNat
                    ).layout(("to_", ("token_id", "amount")))
                )
            )
        )

        transfer_data = [
            sp.record(
                from_ = _from,
                txs = [
                    sp.record(
                        to_ = _to,
                        token_id = _token_id,
                        amount = _amount
                    )
                ]
            )
        ]
        # Transfer the tokens.
        contract = sp.contract(
            TTransferParams,
            _address,
            "transfer"
        ).open_some("INVALID_CONTRACT")

        sp.transfer(transfer_data, sp.mutez(0), contract)
