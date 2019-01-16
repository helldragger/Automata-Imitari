from hypothesis import given
from hypothesis.strategies import *


@given(integers())
def sorted_list(data):
    assert type(data) == list
    assert sorted(data) == data
