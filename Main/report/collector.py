class Collector():
    def __init__(self):
        self.errors = {}
        self.problems = {}
        self.applied_solutions = {}
        self.interaction_errors = {}
    
    def add_errors(self, rig_name, errors):
        for error in errors:
            self.add_error(rig_name, error)
    
    def add_problems(self, rig_name, problems):
        for problem in problems:
            self.add_problem(rig_name, problem)

    def add_solutions(self, rig_name, solutions):
        for solution in solutions:
            self.add_solution(rig_name, solution)

    def add_error(self, rig_name, error):
        self.add_to_collection(rig_name, type(error).__name__, self.errors)

    def add_problem(self, rig_name, problem):
        self.add_to_collection(rig_name, type(problem).__name__, self.problems)

    def add_solution(self, rig_name, solution):
        self.add_to_collection(rig_name, solution, self.applied_solutions)

    def add_to_collection(self, rig_name, object, collection):
        if rig_name not in collection:
            collection[rig_name] = {}
        self.increment_collection(object, collection[rig_name]) 

    def add_interaction_with_error(self, name):
        self.increment_collection(name, self.interaction_errors)

    def increment_collection(self, name, collection):
        if name not in collection:
            collection[name] = 0
        collection[name] += 1
