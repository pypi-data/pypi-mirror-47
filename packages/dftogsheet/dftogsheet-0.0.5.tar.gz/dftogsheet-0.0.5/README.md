# dfgsheet
A Python module for writing pandas DataFrame objects directly to Google Spreadsheets

## Install dfgsheet
```shell
$ pip install dfgsheet
```

## Setup
1. Enable the
[Google Sheets API](https://developers.google.com/sheets/api/quickstart/python)
for the Google account you'd like to use.
2. Download `credentials.json` into `project/root/folder/secret`.

## Simple Usage
```python
import pandas as pd
import dfgsheet

data_frame = pd.DataFrame()
dfgsheet.write_to_sheet(data_frame, spreadsheet_id, sheet_name)
```

### Parameters
There are three mandatory parameters for the above function:
- `data_frame` is any pandas DataFrame object.
- `spreadsheet_id` is the part of the Google Spreadsheet URL
that is between `/d/` and `/edit`.
- `sheet_name` is the name of the sheet within the Google spreadsheet.
E.g. `Sheet1`.

## What's new in version 0.0.5
- Move location of credential files