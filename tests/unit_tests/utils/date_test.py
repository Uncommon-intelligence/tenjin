from tenjin.utils.date import today
from unittest import mock
import datetime

def test_today_function():
    today_date = datetime.datetime(2019, 11, 5, 13, 30, 30)
    expected_result = "Tuesday, Nov 05 2019"

    # mock the now() function in the datetime module with the specified date and time
    with mock.patch('datetime.datetime') as mock_now:
        mock_now.now.return_value = today_date
        result = today()
        assert result == expected_result