import json
import logging

import pytest
from os import path

from surebet.json_funcs import obj_dumps, json_dumps
from surebet.parsing import try_parse, ParseException
from surebet.parsing.bets import Bookmaker
from surebet.parsing.marat import parse
from surebet.tests.parsing import package_dir

name = "marat"
resource_dir = path.join(package_dir, name)


def abs_path(filename):
    return path.join(resource_dir, filename)


def test_samples():
    for num in range(3):
        filename = abs_path('sample{}.json'.format(num))
        with open(filename) as file:
            sample = json.load(file)
        try_parse(parse, sample, name, bookmaker=Bookmaker(name))
        logging.info('PASS: sample{}'.format(num))


def test_known_result():
    known_result_out_file = abs_path("knownResultOut.json")
    with open(known_result_out_file) as file:
        known_result = json.load(file)

    known_result_in_file = abs_path("knownResultIn.json")
    with open(known_result_in_file) as file:
        known_result_in = json.load(file)

    marat = Bookmaker(name)
    try_parse(parse, known_result_in, name, bookmaker=marat)
    marat.format()

    assert obj_dumps(marat) == json_dumps(known_result)

    logging.info('PASS: known result')


def test_broken_structure():
    filename = abs_path('brokenStructure.json')
    with open(filename) as file:
        broken_sample = json.load(file)

    with pytest.raises(ParseException, message='Expecting ParseException'):
        parse(broken_sample, Bookmaker(name))

    logging.info('PASS: broken structure')
