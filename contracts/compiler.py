import smartpy as sp


dex = sp.io.import_script_from_url("file:./contracts/dex.py")
Dex = dex.Dex

def main():
    sp.add_compilation_target("Dex Compilation Target", Dex(
        x_address=sp.address('KT1WJUr74D5bkiQM2RE1PALV7R8MUzzmDzQ9'),
        y_address=sp.address('KT1CNQL6xRn5JaTUcMmxwSc5YQjwpyHkDR5r'),
        _lp_token=sp.address('KT1Nv2h1bHPLYZsGrCdfdvwKzXsZrFEfJnpJ'),
        _admin=sp.address("tz1WNKahMHz1bkuAfZrsvtmjBhh4GJzw8YcU")
    ))

if __name__ == "__main__":
    main()