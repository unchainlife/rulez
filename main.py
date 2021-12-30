from datetime import date
from rulez import Rule, RulesEngine, StaticDependencyFetcher
from myruleset import YesManRuleV1, YesManRuleV2, TellMeMyNhsNumber, GetMyNhsRecord


if __name__ == '__main__':
    engine = RulesEngine()
    engine.add_many([
        YesManRuleV1("Yes"),
        YesManRuleV2("Yes"),
        TellMeMyNhsNumber(),
        GetMyNhsRecord()
    ])

    data = {
        "records": {
            "1234567890": "OK!"
        }
    }
    fetcher = StaticDependencyFetcher(data)

    args = {
        "NhsNumber": "1234567890"
    }
    d = date.today()

    result = engine.execute_many(["YesMan", "WhatIsMyNhsNumber", "GetMyNhsRecord"], date.today(), args, fetcher)
    print ("Result for today is ", result)

    result = engine.execute_many(["YesMan", "WhatIsMyNhsNumber", "GetMyNhsRecord"], date(2050, 1, 1), args, fetcher)
    print ("Result for 1-Jan-2050 is ", result)
