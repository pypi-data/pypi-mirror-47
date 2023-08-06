# salesforce-reporting-chunked

## Get > 2000 rows from Your Date-Sortable Salesforce Reports

`salesforce-reporting-chunks` is a wrapper around [cghall](https://pypi.org/user/cghall/)'s `salesforce-reporting` module. The Salesforce API limits output to 2000 rows for a given report. `salesforce-reporting-chunked` works around this limitation by returning a generator that simply pulls a date range from your report a given number of days at a time.

## Install
```pip install salesforce-reporting-chunked```

## Documentation
Documentation at [readthedocs](https://salesforce-reporting-chunks.readthedocs.io/).

## Usage

1. Obtain a Salesforce security token.
1. Choose your API version
1. Get your report id from the Salesforce report URL

```python
from salesforce_reporting_chunked import chunk_report_by_date

CONFIG = {
    "security_token": "REPLACE WITH YOUR TOKEN",
    "username": "REPLACE WITH YOUR USERNAME",
    "password": "REPLACE WITH YOUR PASSWORD",
    "api_version": "v38.0"
}

FIELDNAMES = [
    "First Name",
    "Last Name",
    "Date Column", # this is the magic column use for chunking.
    "Corhuscorrated Plethanth",
    "Other Column",
]

REPORT_ID = "YOURREPORTID"

>>> data = chunk_report_by_date(
    CONFIG,
    REPORT_ID,
    FIELDNAMES,
    date_fieldname="Date Column",
    start_date="2018-01-01",
    start_date="2019-01-31",
)
>>> next(data)
OrderedDict([('First Name', 'Fred'),('Last Name', 'Garvin'),('DATE_COLUMN_NAME', '2018-01-01'),('Corhuscorrated Plethanth', True),('Other Column': 'Yep. Another')])
```
