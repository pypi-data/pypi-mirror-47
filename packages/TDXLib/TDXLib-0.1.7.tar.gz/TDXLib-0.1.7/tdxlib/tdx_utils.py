import dateutil.parser
import datetime
import json
import xlrd


# Prints out dict as JSON with indents
def print_nice(myjson):
    print(json.dumps(myjson, indent=4))
    print("")


# Print summary of ticket, or dict of tickets
def print_simple(my_json, attributes=None):
    if isinstance(my_json, list):
        this_json = my_json
    else:
        this_json = list([my_json])
    default_attributes = ['FullName', 'Name', 'Title',  'ID', 'UID', 'Requestor', 'TypeName']
    if not attributes:
        attributes = default_attributes
    for j in this_json:
        for i in attributes:
            if i in j:
                print(i,':\t', j[i])

# Print only ['Name'] attribute of list of objects
def print_names(myjson):
    if isinstance(myjson,list):
        this_json = myjson
    else:
        this_json = list([myjson])
    for i in this_json:
        if 'Name' in i:
            print(i['Name'])


# Imports a string from an excel date string, returns a python datetime object
def import_excel_date(date_string: str) -> datetime:
    return xlrd.xldate_as_datetime(date_string, 0)


# Imports a string from a TDX Datetime attribute, returns a python datetime object
def import_tdx_date(date_string: str) -> datetime:
    return dateutil.parser.parse(date_string)


# Takes a python datetime object, returns a string compatible with a TDX Datetime attribute
def export_tdx_date(date: datetime) -> str:
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')