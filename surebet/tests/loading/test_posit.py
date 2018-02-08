import time
import json

from unittest.mock import patch
from requests import Session

from surebet.json_funcs import json_dumps, obj_dumps
from surebet.loading.posit import *
from surebet.loading.selenium import SeleniumService
from surebet.tests.loading import check_result, package_dir
from surebet.bookmakers import Posit

import logging
from os import path

resource_dir = path.join(package_dir, 'posit')


def test_loading():
    session = Session()

    print("loaded")

    try_load(load, name, session=session)
    for i in range(4):
        print("load events: ({})".format(i))

        result = try_load(load_events, name, session=session)
        check_result(result)

        time.sleep(1)

    SeleniumService.quit()

    logging.info("PASS: loading")


def mock_load_events(sample):
    iter_sample = iter(sample)

    def get_next_html(load_func, site_name, **kwargs):  # it's called instead of try_load
        try:
            sample_next = next(iter_sample)
        except StopIteration:
            raise AssertionError("Sample requests overflow") from StopIteration

        return sample_next

    with patch("surebet.bookmakers.sleep") as mock_sleep:
        with patch("surebet.bookmakers.try_load") as mock_try_load:
            mock_try_load.side_effect = get_next_html
            posit = Posit()
            surebets_posit = posit.load_events()

    return surebets_posit


def test_sample():
    for sample_num in range(3):
        filename = path.join(resource_dir, "sample{}.json".format(sample_num))
        with open(filename) as file_sample:
            sample = json.load(file_sample)

        mock_load_events(sample)

    logging.info("PASS: samples")


def test_known_result():
    with open(path.join(resource_dir, "known.json"), "r") as file_known:
        sample_known = json.load(file_known)
    surebets_posit = mock_load_events(sample_known)

    with open(path.join(resource_dir, "knownResult.json")) as file_known_result:
        surebets_known = json.load(file_known_result)

    assert obj_dumps(surebets_posit) == json_dumps(surebets_known)

    logging.info("PASS: known result")
