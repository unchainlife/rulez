from abc import ABC, abstractmethod
from datetime import date


# ----------------------------------------------------------------------------------------------------------------------
# Abstract Base Class for a Rule
# ----------------------------------------------------------------------------------------------------------------------

class Rule(ABC):
    # Returns a name/date tuple for versioning
    @abstractmethod
    def version(self) -> (str, date):
        pass

    # Returns true if the name matches and the version is greater than or equal
    def matches(self, name: str, version: date):
        (n, v) = self.version()
        return name == n and version >= v

    #
    @abstractmethod
    def execute(self, arguments=None, **dependencies):
        pass


# ----------------------------------------------------------------------------------------------------------------------
# The rules engine, which allows for rules to be registered and then executed
# ----------------------------------------------------------------------------------------------------------------------

class RulesEngine:

    def __init__(self):
        self.rules: [Rule] = []

    # add a rule to the list
    def add(self, rule: Rule):
        matches = [r for r in self.rules if r.version() == rule.version()]
        if len(matches) > 0:
            raise KeyError(f"Item exists {rule.version()}")
        self.rules.append(rule)

    # add multiple rules to the list
    def add_many(self, *rules: [Rule]):
        for rule in rules:
            self.add(rule)

    # returns a single rule for the given name/version
    def match(self, name: str, version: date) -> Rule:
        filtered = [r for r in self.rules if r.matches(name, version)]
        filtered.sort(key=lambda r: r.version()[1], reverse=True)
        if len(filtered) < 1:
            raise KeyError(f'Unable to find rule for {name}:{version}')
        return filtered[0]

    # execute a single rule at a given date
    def execute_single(self, name: str, version: date, arguments=None, **dependencies):
        rule = self.match(name, version)
        return rule.execute(arguments, **dependencies)

    # execute multiple rules at a given date
    def execute_many(self, names: [str], version: date, arguments=None, **dependencies):
        return [self.execute_single(name, version, arguments, **dependencies) for name in names]
