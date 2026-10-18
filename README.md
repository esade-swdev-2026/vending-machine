# Vending Machine

> A terminal vending machine: list the products, see what your coins can buy, buy one and get your change. The machine remembers every sale: stock goes down and the coins it holds are updated.

Group project for *Software Development for Business* (ESADE, 2026–27).

## Install

You need [uv](https://docs.astral.sh/uv/getting-started/installation/). It installs Python 3.13 for you.

```
git clone https://github.com/esade-swdev-2026/vending-machine.git
cd vending-machine
uv sync
```

`uv sync` creates a virtual environment (`.venv`) and installs the exact versions pinned
in `uv.lock`, so every teammate and CI get the same ones. When you change a dependency in
`pyproject.toml`, run `uv lock` and commit the updated `uv.lock`; CI fails if the two disagree.

## Run

Run every command from the repository root, so the default data files in `data/` are found.

```
uv run vending-machine --help
```

### See every product

```
$ uv run vending-machine products
  1  Choco bons      1.50 €
  2  KitKat          1.30 €
  3  Kinder Bueno    SOLD OUT
  4  Water           1.00 €
  5  Coca-Cola       2.00 €
```

### See what your coins can buy

```
$ uv run vending-machine affordable 100 50
Credit: 1.50 €
  1  Choco bons      1.50 €
  2  KitKat          1.30 €
  4  Water           1.00 €
```

### Buy a product

`buy SLOT COINS...`: buy the KitKat in slot 2 with a 2 € coin:

```
$ uv run vending-machine buy 2 200
Enjoy your KitKat!
Change: 1 x 0.50 € + 1 x 0.20 €
```

Coins are given **in cents**, separated by spaces (`100 50 50` is 1 € + 50c + 50c).
Accepted coins: `200, 100, 50, 20, 10, 5, 2, 1`.

How the change is made:
- The machine first adds the coins you inserted to the coins it already holds, so it can give some of your own coins back as change.
- It pays with the largest coins first. If that leaves an amount it can't pay, it uses one big coin fewer and tries again with smaller ones. With one 50c and three 20c, 60c of change is paid as 3 x 20c.

**`buy` saves the machine after each sale.** The product's quantity in `data/products.csv`
goes down by one, and `data/machine_coins_change.csv` gets the inserted coins and loses the change.
After 5 KitKat sales, `products` shows `SOLD OUT` for slot 2. A failed sale (any error below) saves nothing.
To reset the sample data, run `git checkout data/`.

### Options

Every command accepts:

| option               | default                         | meaning                         |
|----------------------|---------------------------------|---------------------------------|
| `--stock PATH`       | `data/products.csv`             | the products CSV file           |
| `--coins-file PATH`  | `data/machine_coins_change.csv` | the coins available for change  |

## Errors

Bad input never shows a traceback: it prints `Error: ...` and exits with code 1.

| problem                              | example                                               | message                                                     |
|--------------------------------------|-------------------------------------------------------|-------------------------------------------------------------|
| unknown slot                         | `uv run vending-machine buy 99 200`                   | `Error: No product in slot 99.`                             |
| sold-out product                     | `uv run vending-machine buy 3 200`                    | `Error: Kinder Bueno is sold out.`                          |
| coin that is not accepted            | `uv run vending-machine buy 1 3`                      | `Error: Coin 3 is not accepted.`                            |
| not enough money                     | `uv run vending-machine buy 1 100`                    | `Error: Choco bons costs 150 cents, you inserted 100.`      |
| the machine cannot make the change   | (when its coins run out)                              | `Error: Cannot give 70 cents of change.`                    |
| missing data file                    | `uv run vending-machine products --stock missing.csv` | `Error: [Errno 2] No such file or directory: 'missing.csv'` |
| bad row in a data file               | (e.g. a price that is not a number)                   | `Error: data/products.csv: bad product on line 3.`          |
| the same slot twice in the CSV       | (two rows with slot `1`)                              | `Error: data/products.csv: slot 1 is repeated on line 3.`   |

## Data files

`data/products.csv`, one product per row (each slot only once):

| column        | meaning                          |
|---------------|----------------------------------|
| `slot`        | slot number (integer)            |
| `name`        | product name                     |
| `price_cents` | price in cents (integer)         |
| `quantity`    | units left; `0` shows SOLD OUT   |

`data/machine_coins_change.csv`, the coins the machine holds to give change:

| column       | meaning                        |
|--------------|--------------------------------|
| `coin_cents` | coin value in cents            |
| `count`      | how many of that coin it holds |

## Checks

The script `scripts/check.sh` runs the same four checks as CI (GitHub Actions,
`.github/workflows/check.yml`), in the same order, and stops at the first one that fails.
Run it from the repository root before every commit and push. If it passes here, CI passes.

```
bash scripts/check.sh
```

It works in any bash terminal: Linux, macOS, WSL, or Git Bash on Windows. It runs:

```
uv run ruff check .            # lint
uv run ruff format --check .   # formatting (fails if a file is not formatted)
uv run mypy src tests          # types
uv run pytest                  # tests
```

Without bash, run those four commands one by one. If the formatting check fails, run
`uv run ruff format .` once to fix every file, then commit.

The tests never touch the real `data/` files: the command-line tests work on copies in a temporary folder.

## How it works

The machine is plain data, and a sale is a function from the machine before to the machine after:

- `MachineState` (a frozen dataclass) holds `products` (`{slot: Product}`) and `coin_float` (`{coin_cents: count}`).
- `sell(state, slot, coins)` checks the sale, makes the change and returns a `SaleResult`: the `Sale` (product and change) and the **new** `MachineState`. It never changes the state it was given.
- `cli.py` reads the state from the CSVs, calls `sell`, saves the new state and prints the result.

## Project layout

```
src/vending_machine/
  models.py       Product, Sale, MachineState, SaleResult, the Coins/Products types,
                  the accepted coins and the error classes (no I/O)
  inventory.py    find_product, affordable_products (pure)
  payment.py      credit_from_coins, add_coins, remove_coins, make_change (pure)
  machine.py      sell: one whole purchase, old state in, new state out (pure)
  formatting.py   format_cents, format_change, format_product_lines (pure)
  storage.py      reads and writes the CSV data files (the only module that touches files)
  cli.py          the typer commands: read, call the pure functions, save, print
  __main__.py     lets `python -m vending_machine` work
data/             sample products.csv and machine_coins_change.csv
scripts/check.sh  runs the four CI checks locally
tests/            pytest tests, one file per module in src/
pyproject.toml    dependencies and tool settings
```
## Use of AI

We used AI as a supporting tool throughout the project to guide our development, clarify concepts and help us work through problems.

We remained responsible for the final implementation and took the time to understand the suggestions we used. We understand how the different modules work together, how a purchase is processed, and how the machine handles stock, payments and change. We can explain the code and the decisions behind it.

## Team

Sara Alsius, Côme Ozanne, Hugo Ciaurriz, Jan Masdevall. MIT licence, see `LICENSE`.
