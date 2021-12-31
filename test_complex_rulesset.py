from datetime import date
from rulez import Rule, RulesEngine
from warnings import warn, filterwarnings

filterwarnings('always')


# ----------------------------------------------------------------------------------------------------------------------
# This rule will return whatever value is specified in the constructor
# ----------------------------------------------------------------------------------------------------------------------

class YesManRuleV1(Rule):

    def version(self) -> (str, date):
        return "YesMan", date.min

    def __init__(self, answer: str):
        self.answer = answer

    def execute(self, arguments=None, **dependencies):
        return self.answer


# ----------------------------------------------------------------------------------------------------------------------
# This rule is similar to the "YesMan" rule, but will prefix and suffix !! for extra specialness
# ----------------------------------------------------------------------------------------------------------------------

class YesManRuleV2(YesManRuleV1):

    def version(self) -> (str, date):
        return super().version()[0], date(2022, 1, 1)

    def __init__(self, answer):
        super().__init__("!! " + answer + " !!")


# ----------------------------------------------------------------------------------------------------------------------
# This rule is similar to the "YesMan" rule, but will prefix and suffix ?? for extra specialness
# ----------------------------------------------------------------------------------------------------------------------

class YesManRuleV3(YesManRuleV2):

    def version(self) -> (str, date):
        return super().version()[0], date(2032, 1, 1)

    def __init__(self, answer):
        super().__init__("?? " + answer + " ??")


# ----------------------------------------------------------------------------------------------------------------------
# This rule will return whatever 'NhsNumber' you passed as an argument
# ----------------------------------------------------------------------------------------------------------------------

class TellMeMyNhsNumber(Rule):
    def version(self) -> (str, date):
        return "WhatIsMyNhsNumber", date.min

    def execute(self, arguments=None, **dependencies):
        return arguments["NhsNumber"]


# ----------------------------------------------------------------------------------------------------------------------
# This rule will lookup your NhsNumber in a dataset and return path
# ----------------------------------------------------------------------------------------------------------------------
class GetMyNhsRecord(Rule):
    def version(self) -> (str, date):
        return "GetMyNhsRecord", date.min

    def execute(self, arguments=None, **dependencies):
        nhs_number = arguments["NhsNumber"]
        data = dependencies["records"]
        return data[nhs_number]


def test_a_more_complex_setup():
    engine = RulesEngine()
    engine.add_many(
        YesManRuleV1("Yes"),
        YesManRuleV2("Yes"),
        YesManRuleV3("Yes"),
        TellMeMyNhsNumber(),
        GetMyNhsRecord()
    )

    records = {
        "1234567890": {"message": "OK"}
    }

    args = {
        "NhsNumber": "1234567890"
    }

    questions = [
        "YesMan",
        "WhatIsMyNhsNumber",
        "GetMyNhsRecord"
    ]

    result1 = engine.execute_many(questions, date(2020, 1, 1), args, records=records)
    result2 = engine.execute_many(questions, date(2030, 1, 1), args, records=records)
    result3 = engine.execute_many(questions, date(2040, 1, 1), args, records=records)

    assert result1 == ['Yes', '1234567890', {"message": 'OK'}]
    assert result2 == ['!! Yes !!', '1234567890', {"message": "OK"}]
    assert result3 == ['!! ?? Yes ?? !!', '1234567890', {"message": "OK"}]

