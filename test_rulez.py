from datetime import date

import pytest

from rulez import Rule, RulesEngine, DependencyFetcher

TEST_NAME = "Test"
DATE_1 = date.min
DATE_2 = date(2020, 1, 1)
DATE_3 = date(2030, 1, 1)
DATE_4 = date(2040, 1, 1)


# Simple rule that returns 1
class TestRuleV1(Rule):
    def version(self) -> (str, date):
        return TEST_NAME, DATE_1

    def execute(self, arguments=None, dependencies: DependencyFetcher = None):
        return 1


# Revision of the rule that returns 2
class TestRuleV2(TestRuleV1):

    def version(self) -> (str, date):
        (n, _) = super().version()
        return n, DATE_3

    def execute(self, arguments=None, dependencies: DependencyFetcher = None):
        return 2


def test_engine_with_no_rules_throws_error():
    subject = RulesEngine()
    with pytest.raises(KeyError):
        subject.match(TEST_NAME, DATE_2)


def test_engine_with_future_rule_throws_error():
    subject = RulesEngine()
    subject.add(TestRuleV2())
    with pytest.raises(KeyError):
        subject.match(TEST_NAME, DATE_1)


def test_engine_with_duplicate_rules_throws_error():
    subject = RulesEngine()
    subject.add(TestRuleV1())
    with pytest.raises(KeyError):
        subject.add(TestRuleV1())


def test_engine_with_single_rule():
    subject = RulesEngine()
    subject.add(TestRuleV1())
    result = subject.execute_single(TEST_NAME, DATE_2)
    assert result == 1, "Expected 1"


def test_engine_with_multiple_versions():
    subject = RulesEngine()
    subject.add_many(
        TestRuleV1(),
        TestRuleV2()
    )
    result1 = subject.execute_single(TEST_NAME, DATE_1)
    result2 = subject.execute_single(TEST_NAME, DATE_2)
    result3 = subject.execute_single(TEST_NAME, DATE_3)
    result4 = subject.execute_single(TEST_NAME, DATE_4)
    assert result1 == 1, "Expected V1"
    assert result2 == 1, "Expected V1"
    assert result3 == 2, "Expected V2"
    assert result4 == 2, "Expected V2"
