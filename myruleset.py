from datetime import date
from rulez import Rule


# ----------------------------------------------------------------------------------------------------------------------
# This rule will return whatever value is specified in the constructor
# ----------------------------------------------------------------------------------------------------------------------

class YesManRuleV1(Rule):
    answer: str

    def version(self) -> (str, date):
        return "YesMan", date.min

    def __init__(self, answer: str):
        self.answer = answer

    def execute(self, arguments, dependencies):
        return self.answer


# ----------------------------------------------------------------------------------------------------------------------
# This rule is similar to the "YesMan" rule, but will prefix and suffix !! for extra specialness
# ----------------------------------------------------------------------------------------------------------------------

class YesManRuleV2(YesManRuleV1):

    def version(self) -> (str, date):
        return "YesMan", date(2022, 1, 1)

    def __init__(self, answer):
        super().__init__("!!" + answer + "!!")


# ----------------------------------------------------------------------------------------------------------------------
# This rule will return whatever 'NhsNumber' you passed as an argument
# ----------------------------------------------------------------------------------------------------------------------

class TellMeMyNhsNumber(Rule):
    def version(self) -> (str, date):
        return "WhatIsMyNhsNumber", date.min

    def execute(self, arguments, dependencies):
        return arguments["NhsNumber"]


# ----------------------------------------------------------------------------------------------------------------------
# This rule will lookup your NhsNumber in a dataset and return path
# ----------------------------------------------------------------------------------------------------------------------
class GetMyNhsRecord(Rule):
    def version(self) -> (str, date):
        return "GetMyNhsRecord", date.min

    def execute(self, arguments, dependencies):
        nhs_number = arguments["NhsNumber"]
        data = dependencies.fetch("records", arguments)
        return data[nhs_number]
