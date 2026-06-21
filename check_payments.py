"""Validate common data-quality issues in payments.csv."""

from __future__ import annotations

import csv
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path


PAYMENTS_FILE = Path(__file__).with_name("payments.csv")


def format_issue_rows(rows: list[int]) -> str:
    return ", ".join(str(row) for row in rows)


def main() -> None:
    missing_invoices: list[int] = []
    negative_amounts: list[tuple[int, str]] = []
    zero_amounts: list[int] = []
    payments_by_key: dict[tuple[str, str, Decimal, str], list[int]] = defaultdict(list)
    total_rows = 0

    with PAYMENTS_FILE.open(newline="", encoding="utf-8") as csv_file:
        for row_number, payment in enumerate(csv.DictReader(csv_file), start=2):
            total_rows += 1

            if not payment["invoice_number"].strip():
                missing_invoices.append(row_number)

            try:
                amount = Decimal(payment["amount"])
            except (InvalidOperation, KeyError):
                print(f"Invalid amount on row {row_number}: {payment.get('amount', '')!r}")
                continue

            if amount < 0:
                negative_amounts.append((row_number, payment["amount"]))
            elif amount == 0:
                zero_amounts.append(row_number)

            duplicate_key = (
                payment["date"].strip(),
                payment["supplier"].strip(),
                amount,
                payment["currency"].strip(),
            )
            payments_by_key[duplicate_key].append(row_number)

    possible_duplicates = [
        (key, rows) for key, rows in payments_by_key.items() if len(rows) > 1
    ]

    print(f"Payment data check: {PAYMENTS_FILE.name}")
    print(f"Records checked: {total_rows}\n")

    print(f"Missing invoice numbers: {len(missing_invoices)}")
    if missing_invoices:
        print(f"  Rows: {format_issue_rows(missing_invoices)}")

    print(f"Negative amounts: {len(negative_amounts)}")
    for row_number, amount in negative_amounts:
        print(f"  Row {row_number}: {amount}")

    print(f"Zero amounts: {len(zero_amounts)}")
    if zero_amounts:
        print(f"  Rows: {format_issue_rows(zero_amounts)}")

    print(f"Possible duplicate payments: {len(possible_duplicates)}")
    for (date, supplier, amount, currency), rows in possible_duplicates:
        print(
            f"  Rows {format_issue_rows(rows)}: {date}, {supplier}, "
            f"{amount} {currency}"
        )


if __name__ == "__main__":
    main()
