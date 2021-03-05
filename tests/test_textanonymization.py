#!/usr/bin/env python

"""Tests for `textanonymization` package."""

import pytest

from click.testing import CliRunner

from textanonymization import textanonymization
from textanonymization import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_cpr_mask(response):
    """Tests CPR mask on pre-defined text"""

    test_string = "Hej med dig, mit CPR nr er 010203-2010"
    test_output = "Hej med dig, mit CPR nr er [CPR]"
    output = textanonymization.TextAnonymizer.mask_cpr(test_string)

    assert output == test_output


def test_tlf_mask(response):
    """Tests telephone mask on pre-defined text"""

    test_string = "Hej med dig, mit telefon nr er +4545454545"
    test_output = "Hej med dig, mit telefon nr er [TELEFON]"
    output = textanonymization.TextAnonymizer.mask_telefon_nr(test_string)

    assert output == test_output


def test_email_mask(response):
    """Tests email mask on pre-defined text"""

    test_string = "Hej med dig, min email er jakob.jakobsen@gmail.com"
    test_output = "Hej med dig, min email er [EMAIL]"
    output = textanonymization.TextAnonymizer.mask_email(test_string)

    assert output == test_output


def test_corpus_mask(response):
    """Tests all masks on pre-defined text"""

    test_corpus = [
        "Hej, jeg hedder Martin Jespersen, er 20 år, mit cpr er 010203-2010,"
        "telefon: +4545454545 og email: martin.martin@gmail.com"
    ]
    test_output = [
        "Hej, jeg hedder Martin Jespersen, er 20 år, mit cpr er [CPR],"
        "telefon: [TELEFON] og email: [EMAIL]"
    ]
    CorpusObj = textanonymization.TextAnonymizer(test_corpus)
    masked_corpus = CorpusObj.mask_corpus()

    assert masked_corpus == test_output, "{}\nvs.\n{}".format(
        masked_corpus[0], test_output[0]
    )


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "textanonymization.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
