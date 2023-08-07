"""
    custom filters
"""

import re
import datetime

def last_day_of_month(year: int, month: int) -> int:
    """ returns last day of a year/months """

    last_day = 28 # the minimum possible last day
    last_date = datetime.datetime(year, month, last_day)
    next_month = last_date + datetime.timedelta(days = 4)
    last_date = next_month - date.time.timedelta(days = next_month.day)
    last_day = last_date.date().day
    return last_day

def has_expired(date: str, base, max_days: int, date_pattern=None) -> bool:
    """ True if base - date > max_days
        
        Args: 
            date(str) - date to check (YYYY/MM/DD)
            base(str) - current date (YYYY/MM/DD)
            max_days(int) - expiry period in days
        Example:
            >>> has_expired('2023/03/01', '2023/03/10', 4)
            True
            >>> has_expired('2023/03/09', '2023/03/10', 4)
            False
    """

    if date_pattern == None:
        date_pattern = "%y/%m/%d"

    date_date = datetime.datetime.strptime(date, date_pattern)
    base_date = datetime.datetime.strptime(base, date_pattern)
    delta = base_date - date_date
    if delta.days > max_days:
        result = True 
    else:
        result = False 
    return result 

def get_expired_folders(folders: list, base_date: str, days: int) -> list:
    """ returns a list of folders older than given number of days 

        Args: 
            folders(lists of str) - list of folders (full path)
            base_date(str) - date to compare against (YYYY/MM/DD)
            days(int) - expired period in days
        Notes:
            a folder must have one of the following elements:
            - YYYY
            - YYYY/MM
            - YYYY/MM/DD
        Example: 
            >>> folders = ['dir/2022', 'dir/2023', 'dir/2023/01', 'dir/2023/03', 'dir/2023/03/01/subfolder', 'dir/2023/03/12']
            >>> get_expired_folders(folders, '2023/03/15', 5)
            ['dir/2022', 'dir/2023/01', 'dir/2023/03/01/subfolder']
    """

    YEAR_PATTERN = '^.*(?P<year>20\d\d)$'
    MONTH_PATTERN = '^.*(?P<year>20\d\d)/(?P<month>[0-1]\d)$'
    DAY_PATTERN = '^.*(?P<year>20\d\d)/(?P<month>[0-1\d)/(?P<day>[0-3]\d).*$'

    expired_folders = []
    for folder in folders:
        found_pattern = False 
        m = re.search(YEAR_PATTERN, folder)
        if m:
            yyyy = m.groupdict().get('year')
            mm = '12'
            dd = '31'
            found_pattern = True 
        
        m= re.search(MONTH_PATTERN, folder)
        if m:
            yyyy = m.groupdict().get('year')
            mm = m.groupdict().get('month')
            dd = str(last_day_of_month(int(yyyy), int(mm))).zfill(2)
            found_pattern = True 

        m = re.search(DAY_PATTERN, folder)
        if m:
            yyyy = m.groupdict().get('year')
            mm = m.groupdict().get('month')
            dd = m.groupdict().get('day')
            found_pattern = True

        if found_pattern:
            date_stamp = '{}/{}/{}'.format(yyyy,mm,dd)
            if has_expired(date_stamp, base_date, days):
                expired_folders.append(folder)

    expired_folders = sorted(list(set(expired_folders)))  # remove duplicates and sort
    return expired_folders

# 
# Ansible Filter Wrapper
#

class FilterModule(object):
    def filters(self):
        return {
            "get_expired_folders": self.filter_get_expired_folders
        }
    
    def filter_get_expired_folders(self, folders: list, base_date: str, days: int) -> list:
        """ return expired folders
            Ansible Example:
            - set_fact:
                expired_folders: "{{ folders | get_expired_folders(base_date, days) }}"
              delegate_to: localhost
        """

        return get_expired_folders(folders, base_date, days)