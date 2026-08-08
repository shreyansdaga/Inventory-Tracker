# Inventory Tracker

A desktop inventory management system built for **CATalyst Studios**, tracking stock across teams (Fabrication, Fiber Arts, Multimedia, Crafting) and their sub-categories. It calculates how much of each item needs to be reordered based on current stock and a set par level.

## Features

- **Browse by team and category** — select a team (e.g. Fabrication) to filter inventory by its sub-categories (e.g. Filament, Wood, Acrylic, Resin)
- **Search** for a specific item by name
- **Editable table** — toggle Edit mode to update "Qty on Floor" and "Qty in Back" directly in the GUI
- **Automatic reorder calculation**: `Qty to Order = max(0, Par − (Qty on Floor + Qty in Back))`
- Changes are saved back to the data source when you lock the table

## Versions in this repo

This repo contains a few iterations of the tracker as it evolved:

| File | Description | Storage backend |
|---|---|---|
| `inventory_tracker.py` | Original command-line prototype (add / update / set quantity / low-stock alerts) | Excel (`openpyxl`) |
| `inv_app.py` | GUI version with team/category filtering, search, and an editable table | Excel (`openpyxl`) |
| `inv_app_d.py` | GUI version identical in functionality to `inv_app.py`, migrated to a proper database | PostgreSQL (`SQLAlchemy`) |

`inv_app_d.py` is the most current version and the one intended for regular use.

## Tech Stack

- **Python 3**
- **CustomTkinter** — GUI framework
- **CTkTable** — editable table widget
- **Pillow (PIL)** — image handling for the edit-mode icon
- **SQLAlchemy** + **psycopg2** — ORM and PostgreSQL driver (`inv_app_d.py`)
- **openpyxl** — Excel read/write (`inventory_tracker.py`, `inv_app.py`)

## Getting Started

### Prerequisites

```bash
pip install customtkinter CTkTable pillow openpyxl sqlalchemy psycopg2
```

### Running the database-backed version (`inv_app_d.py`)

1. Set up a PostgreSQL database with a table named `inventory` containing columns for `item`, `team`, `category`, `qty_f` (qty on floor), `qty_b` (qty in back), `par`, and `qty_o` (qty to order).
2. Update the `DATABASE_URL` connection string in `inv_app_d.py` with your own credentials:
   ```python
   DATABASE_URL = "postgresql://<user>:<password>@<host>:<port>/<database>"
   ```
3. Run the app:
   ```bash
   python inv_app_d.py
   ```

### Running the Excel-backed version (`inv_app.py`)

1. Make sure an `inventory.xlsx` file is present in the project directory, with columns for item name, qty on floor, qty in back, par, qty to order, team, and category (columns A–G).
2. Run the app:
   ```bash
   python inv_app.py
   ```

### Running the CLI prototype (`inventory_tracker.py`)

```bash
python inventory_tracker.py
```
Follow the on-screen prompts to add, update, or check inventory levels against a low-stock threshold.
