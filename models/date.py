import datetime
from dataclasses import dataclass

from jsoncompat import Date

from .base import BaseModel

__all__ = ['DateDimension']

_MONTH_NAMES = [None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_DAY_NAMES = [None, "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

_FULL_MONTH_NAMES = [None, "January", "February", "March", "April", "May", "June",
                     "July", "August", "September", "October", "November", "December"]
_FULL_DAY_NAMES = [None, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

_FISCAL_MISMATCH = datetime.timedelta(days=365 // 4)


@dataclass
class DateDimension(BaseModel):
    _instances = []
    fields = (
        ('Date Key', None, 'int'),
        ('Full date description', None, 'nvarchar(255)'),
        ('Date', None, 'date'),
        ('Day Of Half Year', None, 'int'),
        ('Day Of Month', None, 'int'),
        ('Day Of Quarter', None, 'int'),
        ('Day Of Week', None, 'int'),
        ('Day Of Year', None, 'int'),
        ('Half Year Of Year', None, 'int'),
        ('Month Of Half Year', None, 'int'),
        ('Month Of Quarter', None, 'int'),
        ('Month Of Year', None, 'int'),
        ('Quarter Of Half Year', None, 'int'),
        ('Quarter Of Year', None, 'int'),
        # ('Week Of Half Year', None, 'int'),
        # ('Week Of Month', None, 'int'),
        # ('Week Of Quarter', None, 'int'),
        ('Week Of Year', None, 'int'),
        ('Fiscal Date', None, 'date'),
        ('Fiscal Day Of Half Year', None, 'int'),
        ('Fiscal Day Of Month', None, 'int'),
        ('Fiscal Day Of Quarter', None, 'int'),
        ('Fiscal Day Of Week', None, 'int'),
        ('Fiscal Day Of Year', None, 'int'),
        ('Fiscal Half Year Of Year', None, 'int'),
        ('Fiscal Month Of Half Year', None, 'int'),
        ('Fiscal Month Of Quarter', None, 'int'),
        ('Fiscal Month Of Year', None, 'int'),
        ('Fiscal Quarter Of Half Year', None, 'int'),
        ('Fiscal Quarter Of Year', None, 'int'),
        # ('Fiscal Week Of Half Year', None, 'int'),
        # ('Fiscal Week Of Month', None, 'int'),
        # ('Fiscal Week Of Quarter', None, 'int'),
        ('Fiscal Week Of Year', None, 'int'),
        ('Calendar Week Ending Date', None, 'date'),
        ('Day Name', None, 'nvarchar(3)'),
        ('Month Name', None, 'nvarchar(3)'),
        ('Full Day Name', None, 'nvarchar(9)'),
        ('Full Month Name', None, 'nvarchar(9)'),
        ('Fiscal Day Name', None, 'nvarchar(3)'),
        ('Fiscal Month Name', None, 'nvarchar(3)'),
        ('Fiscal Full Day Name', None, 'nvarchar(9)'),
        ('Fiscal Full Month Name', None, 'nvarchar(9)'),
    )

    date: Date

    @property
    def date_key(self) -> int:
        return self.key

    @property
    def fiscal_date(self) -> Date:
        return self.date + _FISCAL_MISMATCH

    @property
    def full_date_description(self) -> str:
        return f"{self.calendar_month_name} {self.date.day}, {self.date.year}"

    @property
    def day_of_half_year(self) -> int:
        month = ((self.half_year_of_year - 1) * 6) + 1
        res = ((self.date - datetime.date(self.date.year, month, 1)) + datetime.timedelta(days=1)).days
        assert 1 <= res <= 184, f'{res=} {self.date=}'
        return res

    @property
    def day_of_month(self) -> int:
        return self.date.day

    @property
    def day_of_quarter(self) -> int:
        month = ((self.quarter_of_year - 1) * 3) + 1
        res = ((self.date - datetime.date(self.date.year, month, 1)) + datetime.timedelta(days=1)).days
        assert 1 <= res <= 92
        return res

    @property
    def day_of_week(self) -> int:
        res = self.date.isoweekday()
        assert 1 <= res <= 7
        return res

    @property
    def day_of_year(self) -> int:
        res = ((self.date - datetime.date(self.date.year, 1, 1)) + datetime.timedelta(days=1)).days
        assert 1 <= res <= 366
        return res

    @property
    def half_year_of_year(self) -> int:
        if self.date - datetime.date(self.date.year, 7, 1) >= datetime.timedelta(0):
            return 2
        return 1

    @property
    def month_of_half_year(self) -> int:
        res = ((self.date.month - 1) % 6) + 1
        assert 1 <= res <= 6
        return res

    @property
    def month_of_quarter(self) -> int:
        res = ((self.date.month - 1) % 3) + 1
        assert 1 <= res <= 3
        return res

    @property
    def month_of_year(self) -> int:
        res = self.date.month
        assert 1 <= res <= 12
        return res

    @property
    def quarter_of_half_year(self) -> int:
        res = ((self.quarter_of_year - 1) % 2) + 1
        assert 1 <= res <= 2
        return res

    @property
    def quarter_of_year(self) -> int:
        res = (self.date.month - 1) // 3 + 1
        assert 1 <= res <= 4
        return res

    # @property
    # def week_of_half_year(self) -> int:
    #     month = ((self.half_year_of_year - 1) * 6) + 1
    #     res = self.date.isocalendar()[1] - datetime.date(self.date.year, month, 1).isocalendar()[1] + 1
    #     assert 0 <= res <= 27
    #     return res
    #
    # @property
    # def week_of_month(self) -> int:
    #     res = self.date.isocalendar()[1] - datetime.date(self.date.year, self.date.month, 1).isocalendar()[1] + 1
    #     assert 0 <= res <= 5
    #     return res
    #
    # @property
    # def week_of_quarter(self) -> int:
    #     month = ((self.quarter_of_year - 1) * 3) + 1
    #     res = self.date.isocalendar()[1] - datetime.date(self.date.year, month, 1).isocalendar()[1] + 1
    #     assert 0 <= res <= 14  # 92/7
    #     return res

    @property
    def week_of_year(self) -> int:
        res = self.date.isocalendar()[1]
        if res == 53:
            if self.date.month == 1:
                res = 0
        assert 0 <= res <= 53
        return res

    @property
    def fiscal_day_of_half_year(self) -> int:
        month = ((self.fiscal_half_year_of_year - 1) * 6) + 1
        res = ((self.fiscal_date - datetime.date(self.fiscal_date.year, month, 1)) + datetime.timedelta(days=1)).days
        assert 1 <= res <= 184
        return res

    @property
    def fiscal_day_of_month(self) -> int:
        res = self.fiscal_date.day
        assert 1 <= res <= 31
        return res

    @property
    def fiscal_day_of_quarter(self) -> int:
        month = ((self.fiscal_quarter_of_year - 1) * 3) + 1
        res = ((self.fiscal_date - datetime.date(self.fiscal_date.year, month, 1)) + datetime.timedelta(days=1)).days
        assert 1 <= res <= 92
        return res

    @property
    def fiscal_day_of_week(self) -> int:
        res = self.fiscal_date.isoweekday()
        assert 1 <= res <= 7
        return res

    @property
    def fiscal_day_of_year(self) -> int:
        res = ((self.fiscal_date - datetime.date(self.fiscal_date.year, 1, 1)) + datetime.timedelta(days=1)).days
        assert 1 <= res <= 366
        return res

    @property
    def fiscal_half_year_of_year(self) -> int:
        if self.fiscal_date - datetime.date(self.fiscal_date.year, 7, 1) >= datetime.timedelta(0):
            return 2
        return 1

    @property
    def fiscal_month_of_half_year(self) -> int:
        res = ((self.fiscal_date.month - 1) % 6) + 1
        assert 1 <= res <= 6
        return res

    @property
    def fiscal_month_of_quarter(self) -> int:
        res = ((self.fiscal_date.month - 1) % 3) + 1
        assert 1 <= res <= 3
        return res

    @property
    def fiscal_month_of_year(self) -> int:
        res = self.fiscal_date.month
        assert 1 <= res <= 12
        return res

    @property
    def fiscal_quarter_of_half_year(self) -> int:
        res = ((self.fiscal_quarter_of_year - 1) % 2) + 1
        assert 1 <= res <= 2
        return res

    @property
    def fiscal_quarter_of_year(self) -> int:
        res = (self.fiscal_date.month - 1) // 3 + 1
        assert 1 <= res <= 4
        return res

    # @property
    # def fiscal_week_of_half_year(self) -> int:
    #     month = ((self.fiscal_half_year_of_year - 1) * 6) + 1
    #     assert month == 1 or month == 7, month
    #     res = self.fiscal_date.isocalendar()[1] - datetime.date(self.fiscal_date.year, month, 1).isocalendar()[1] + 1
    #     assert 1 <= res <= 27, f'{res=} {month=} {self.fiscal_date=} {self.fiscal_half_year_of_year=} {self.fiscal_date.isocalendar()[1]=} {datetime.date(self.fiscal_date.year, month, 1)=}'
    #     return res
    #
    # @property
    # def fiscal_week_of_month(self) -> int:
    #     res = self.fiscal_date.isocalendar()[1] - datetime.date(self.fiscal_date.year, self.fiscal_date.month, 1).isocalendar()[1] + 1
    #     assert 1 <= res <= 5
    #     return res
    #
    # @property
    # def fiscal_week_of_quarter(self) -> int:
    #     month = ((self.fiscal_quarter_of_year - 1) * 3) + 1
    #     res = self.fiscal_date.isocalendar()[1] - datetime.date(self.fiscal_date.year, month, 1).isocalendar()[1] + 1
    #     assert 1 <= res <= 14  # 92/7
    #     return res

    @property
    def fiscal_week_of_year(self) -> int:
        res = self.fiscal_date.isocalendar()[1]
        if res == 53:
            if self.fiscal_date.month == 1:
                res = 0
        assert 0 <= res <= 53
        return res

    @property
    def day_name(self) -> str:
        return _DAY_NAMES[self.date.isoweekday()]

    @property
    def month_name(self) -> str:
        return _MONTH_NAMES[self.month_of_year]

    @property
    def full_day_name(self) -> str:
        return _FULL_DAY_NAMES[self.date.isoweekday()]

    @property
    def full_month_name(self) -> str:
        return _FULL_MONTH_NAMES[self.month_of_year]

    @property
    def fiscal_day_name(self) -> str:
        return _DAY_NAMES[self.fiscal_date.isoweekday()]

    @property
    def fiscal_month_name(self) -> str:
        return _MONTH_NAMES[self.fiscal_month_of_year]

    @property
    def fiscal_full_day_name(self) -> str:
        return _FULL_DAY_NAMES[self.fiscal_date.isoweekday()]

    @property
    def fiscal_full_month_name(self) -> str:
        return _FULL_MONTH_NAMES[self.fiscal_month_of_year]

    @property
    def last_day_in_month_indicator(self) -> str:
        if (self.date + datetime.timedelta(days=1)).month != self.date.month:
            return 'Last day in month'
        return 'Not the last day in month'

    @property
    def calendar_week_ending_date(self) -> Date:
        # Sunday
        return self.date + (datetime.timedelta(days=7 - self.date.isoweekday()))

    @property
    def calendar_month_name(self) -> str:
        return _FULL_MONTH_NAMES[self.date.month]
