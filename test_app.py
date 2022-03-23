import pytest
from app import *
load_from_file()

def test_find_epochs():
    assert isinstance(find_epochs(),str)==True
def test_find_epoch_data():
    assert isinstance(find_epoch_data('w'),dict)==True
def test_get_countries():
    assert isinstance(get_countries(),dict)==True
def test_country_data():
    assert isinstance(country_data('w'),str)==True
def test_get_regions():
    assert isinstance(get_regions('w'),dict)==True
def test_region_data():
    assert isinstance(region_data('w','w'),str)==True
def test_get_cities():
    assert isinstance(get_cities('w','w'),dict)==True
def test_get_city_data():
    assert isinstance(get_city_data('w','w','w'),str)==True
def test_help():
    assert isinstance(help(),str)==True
