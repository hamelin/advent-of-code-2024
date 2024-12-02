import pytest

from . import (
    count_reports_safe,
    count_reports_safe_with_pd,
    is_report_safe,
    is_report_safe_with_pd,
)


@pytest.fixture
def reports_example():
    return [
        [7, 6, 4, 2, 1],
        [1, 3, 6, 7, 9],
        [1, 2, 7, 8, 9],
        [9, 7, 6, 2, 1],
        [1, 3, 2, 4, 5],
        [8, 6, 4, 4, 1],
    ]


@pytest.fixture
def report_n(request, reports_example):
    return reports_example[request.param]


@pytest.mark.parametrize(
    "is_safe,report_n",
    [
        [True, 0],
        [True, 1],
        [False, 2],
        [False, 3],
        [False, 4],
        [False, 5],
    ],
    indirect=["report_n"]
)
def test_is_report_safe(is_safe, report_n):
    assert is_safe == is_report_safe(report_n)


def test_count_reports_safe(reports_example):
    assert 2 == count_reports_safe(reports_example)


@pytest.mark.parametrize(
    "is_safe,report_n",
    [
        [True, 0],
        [True, 1],
        [False, 2],
        [False, 3],
        [True, 4],
        [True, 5],
    ],
    indirect=["report_n"]
)
def test_is_report_safe_with_pd(is_safe, report_n):
    assert is_safe == is_report_safe_with_pd(report_n)

    
def test_count_reports_safe_with_pd(reports_example):
    assert 4 == count_reports_safe_with_pd(reports_example)
