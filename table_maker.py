"""
This code creates tables in either HTML or Markdown format.
We plan to add other formats later, like reStructuredText.
But the code needs refactoring first.

Refactor:
1. Replace conditional logic (switch) with polymorphism.
   Use a class hierarchy, not Enum.

2. Add a factory method to create tables.
   table = Table.create_table("HTML")

When you are done there should not be a tabletype attribute,
but may be tabletype param in the factory method.
"""
from abc import ABC, abstractmethod


class Table(ABC):
    """Create an HTML or Markdown table with formatting.

    The tabletype should be 'HTML' or 'Markdown'.
    """

    def __init__(self):
        self.result = ""

    @classmethod
    def create_table(cls, tabletype: str) -> 'Table':
        dct = {
            cls_._get_tabletype(): cls_ for cls_ in cls.__subclasses__()
        }
        try:
            table = dct[tabletype]()
            table.start_table()
            return table
        except KeyError:
            # tabletype isn't valid
            raise ValueError(f"tabletype must be [{', '.join(dct.keys())}], not '{tabletype}'")

    @classmethod
    @abstractmethod
    def _get_tabletype(cls) -> str:
        """Return the tabletype format implemented"""
        raise NotImplementedError

    @abstractmethod
    def start_table(self):
        """Start a table using the tabletype format."""
        raise NotImplementedError

    @abstractmethod
    def add_header(self, *column_headers):
        """Add a header row to the table.

        column_headers - string values of the table column headers
        """
        raise NotImplementedError

    @abstractmethod
    def add_row(self, *column_data):
        """Add a row of data to the table.

        column_data are string values to put in the columns, one per column.
        """
        raise NotImplementedError

    @abstractmethod
    def end_table(self):
        """Finish and end the table."""
        raise NotImplementedError

    def __str__(self):
        """Return the formatted table data."""
        return self.result


class HTMLTable(Table):
    """Create an HTML table with formatting."""

    @classmethod
    def _get_tabletype(cls) -> str:
        """Return the tabletype format implemented"""
        return 'HTML'

    def start_table(self):
        """Start a table using HTML format."""
        self.result = "<table>\n"

    def add_header(self, *column_headers):
        """Add a header row to the table.

        column_headers - string values of the table column headers
        """
        header = "<tr>"
        header += " ".join(f"<th>{header}</th> " for header in column_headers)
        header += "</tr>\n"
        self.result += header

    def add_row(self, *column_data):
        """Add a row of data to the table.

        column_data are string values to put in the columns, one per column.
        """
        row = "<tr>"
        row += " ".join(f"<td>{header}</td>" for header in column_data)
        row += "</tr>\n"
        self.result += row

    def end_table(self):
        """Finish and end the table."""
        self.result += "</table>\n"


class MarkdownTable(Table):
    """Create a Markdown table with formatting."""

    @classmethod
    def _get_tabletype(cls) -> str:
        """Return the tabletype format implemented"""
        return 'Markdown'

    def start_table(self):
        """Start a table using Markdown format."""
        self.col_widths = []
        self.result = ""

    def add_header(self, *column_headers):
        """Add a header row to the table.

        column_headers - string values of the table column headers
        """
        header = "| "
        header += " | ".join(column_headers)
        header += " |\n"
        header += '|'
        header += "|".join("-" * (len(header) + 2) for header in column_headers)
        header += "|\n"
        self.col_widths = [len(header) for header in column_headers]
        self.result += header

    def add_row(self, *column_data):
        """Add a row of data to the table.

        column_data are string values to put in the columns, one per column.
        """
        if not self.col_widths:
            self.col_widths = [len(data) for data in column_data]
        row = "| "
        row += " | ".join(f"{data:{w}}"
                          for (data, w) in zip(column_data, self.col_widths))
        row += " |\n"
        self.result += row

    def end_table(self):
        """Finish and end the table."""
        pass


if __name__ == '__main__':
    table = Table.create_table("Markdown")
    table.add_header("First Name", "Last Name", "E-mail")
    table.add_row("Bill", "Gates", "bill@msft.com")
    table.add_row("Taksin", "Shinawat", "shin@ais.co.th")
    table.end_table()
    print(table)
