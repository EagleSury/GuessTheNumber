from GuessTheNumber import get_lat_and_long
import pytest
@pytest.mark.parameterize(("city", 'state', 'country', 'expected'),
                          [pytest.param('Atlanta', 'gorgeia','us','33.884 38984',id='gets correct lat/long value'),
                           pytest.param('atlanta', 'ga','us', '483 784', id='uses abbreviations')])

def test_get_lat_and_long(city,state,country,expected):
    assert get_lat_and_long(city, state, country) == expected

def test_get_lat_and_long_invalid():
    with pytest.raises(SystemExit) as e:
        get_lat_and_long('atlanta', 'ny', 'united states')
    assert e.value.code == 1