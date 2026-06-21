# Finance Excel Checker

Finance Excel Checker is a small Python utility for finding common data-quality problems in a payments export. It reads the included `payments.csv` file and prints a clear validation report in the terminal.

## Files

- `payments.csv`: sample payment data used as the validation input.
- `check_payments.py`: the validation script.

The script checks for:

- missing invoice numbers;
- negative payment amounts;
- zero payment amounts; and
- possible duplicate payments, identified by matching date, supplier, amount, and currency.

## Run the checker

Python 3 is required. From the project directory, run:

```powershell
python check_payments.py
```

The script reads `payments.csv` from the same directory and reports the number of records checked along with any issues it finds.
