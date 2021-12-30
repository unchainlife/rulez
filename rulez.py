from abc import ABC, abstractmethod
from datetime import date


# ----------------------------------------------------------------------------------------------------------------------
# Abstract Base Class for a Rule
# ----------------------------------------------------------------------------------------------------------------------

class Rule(ABC):
    @abstractmethod
    def version(self) -> (str, date):
        pass

    def matches(self, name, version):
        (n, v) = self.version()
        return name == n and version >= v


# ----------------------------------------------------------------------------------------------------------------------
# The rules engine, which allows for rules to be registered and then executed
# ----------------------------------------------------------------------------------------------------------------------

class RulesEngine:
    rules: [Rule] = []

    def add(self, rule):
        self.rules.append(rule)
        return self

    def add_many(self, rules: [Rule]):
        for rule in rules:
            self.add(rule)

    def execute_single(self, name: str, version: date, arguments, dependencies):
        filtered = [r for r in self.rules if r.matches(name, version)]
        filtered.sort(key=lambda r: r.version()[1], reverse=True)
        if len(filtered) < 1:
            raise KeyError(f'Unable to file rule for {name}:{version}')
        return filtered[0].execute(arguments, dependencies)

    def execute_many(self, names: [str], version: date, arguments, dependencies):
        return [self.execute_single(name, version, arguments, dependencies) for name in names]


# ----------------------------------------------------------------------------------------------------------------------
# Abstract Base Class, that can lookup dependencies (e.g. Load data from db, fetch URL, etc.)
# ----------------------------------------------------------------------------------------------------------------------

class DependencyFetcher(ABC):
    @abstractmethod
    def fetch(self, name: str, args: {str, any}):
        pass


# ----------------------------------------------------------------------------------------------------------------------
# Simple version that just reads dependency data from a dictionary
# ----------------------------------------------------------------------------------------------------------------------

class StaticDependencyFetcher(DependencyFetcher):
    dataset: {str, any} = {}

    def __init__(self, dataset: {str: any}):
        self.dataset = dataset

    def fetch(self, name: str, args: {str, any}):
        return self.dataset[name]

