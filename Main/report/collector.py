import json
from Main.report.report_constants import *

class Collector():
    def __init__(self):
        self.collections = {
            ERRORS: {},
            PROBLEMS: {},
            APPLIED_SOLUTIONS: {},
            INTERACTION_ERRORS: {},
            PAID_AMOUNTS: {},
            REVENUES: {},
            REVENUES_AVG: {}
        }
    
    def errors(self):
        return self.collections[ERRORS]
    
    def problems(self):
        return self.collections[PROBLEMS]

    def applied_solutions(self):
        return self.collections[APPLIED_SOLUTIONS]
    
    def interaction_errors(self):
        return self.collections[INTERACTION_ERRORS]

    def paid_amounts(self):
        return self.collections[PAID_AMOUNTS]
    
    def revenues(self):
        return self.collections[REVENUES]

    def revenues_avg(self):
        return self.collections[REVENUES_AVG]

    def pay(self, rig_name, amount):
        self.increment_collection(rig_name, self.collections[PAID_AMOUNTS], amount)

    def set_daily_revenue(self, rig_name, revenue):
        collection = self.collections[REVENUES]
        if rig_name not in collection:
            collection[rig_name] = {
                REVENUES_COUNT: 0,
                REVENUES_SUM: 0
            }
        collection[rig_name][REVENUES_SUM] += revenue
        collection[rig_name][REVENUES_COUNT] += 1
        self.collections[REVENUES_AVG][rig_name] = collection[rig_name][REVENUES_SUM] / collection[rig_name][REVENUES_COUNT]

    def add_error(self, rig_name, error):
        self.add_to_collection(rig_name, error.pretty_print(), self.collections[ERRORS])

    def add_problem(self, rig_name, problem):
        self.add_to_collection(rig_name, problem.pretty_print(), self.collections[PROBLEMS])

    def add_solution(self, rig_name, solution):
        self.add_to_collection(rig_name, solution.pretty_print(), self.collections[APPLIED_SOLUTIONS])

    def add_interaction_with_error(self, name):
        self.increment_collection(name, self.collections[INTERACTION_ERRORS])

    def add_errors(self, rig_name, errors):
        for error in errors:
            self.add_error(rig_name, error)
    
    def add_problems(self, rig_name, problems):
        for problem in problems:
            self.add_problem(rig_name, problem)

    def add_solutions(self, rig_name, solutions):
        for solution in solutions:
            self.add_solution(rig_name, solution)

    def add_to_collection(self, rig_name, object, collection):
        if rig_name not in collection:
            collection[rig_name] = {}
        self.increment_collection(object, collection[rig_name]) 

    def increment_collection(self, name, collection, amount=1):
        if name not in collection:
            collection[name] = 0
        collection[name] += amount

    def to_json(self):
        return json.dumps(self.collections)
    
    def from_json(file_name):
        with open(file_name, 'r') as f:
            collector = Collector()
            collector.collections = json.load(f)
            if (REVENUES not in collector.collections):
                collector.collections[REVENUES] = {}
            if (REVENUES_AVG not in collector.collections):
                collector.collections[REVENUES_AVG] = {}
            if (PAID_AMOUNTS not in collector.collections):
                collector.collections[PAID_AMOUNTS] = {}
            return collector
