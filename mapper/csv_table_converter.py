from sqlalchemy import Table

from extended_csv import read_xsv_file

Table()
read_xsv_file(fieldnames=[])
fieldnames: list[str] = []
read_xsv_file("tests/data/csv/branded_food-10000.csv", "csv", load_at_most=1)
