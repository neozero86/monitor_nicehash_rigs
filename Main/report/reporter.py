from asyncio.log import logger
from Main.report.collector import Collector
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from Main.singleton import Singleton
import pprint

@Singleton
class Reporter():
    def __init__(self):
        pass
    
    def init(self, email_sender, config,logger):
        self.email_sender = email_sender
        self.config = config
        self.logger = logger
        self.collector = Collector()
        if(config["production"]):
            scheduler = BackgroundScheduler()
            scheduler.add_job(func=self.send_report, trigger="interval", seconds=config["interval_seconds"])
            scheduler.start()
            atexit.register(lambda: scheduler.shutdown())
            scheduler_backup = BackgroundScheduler()
            scheduler_backup.add_job(func=self.save_to_disk, trigger="interval", seconds=300)
            scheduler_backup.start()
            atexit.register(lambda: scheduler_backup.shutdown())

    def add_errors(self, rig_name, errors):
        self.collector.add_errors(rig_name, errors)

    def add_problems(self, rig_name, problems):
        self.collector.add_problems(rig_name, problems)
    
    def add_solutions(self, rig_name, solutions):
        self.collector.add_solutions(rig_name, solutions)

    def add_error(self, rig_name, error):
        self.collector.add_error(rig_name, error)

    def add_problem(self, rig_name, problem):
        self.collector.add_problem(rig_name, problem)

    def add_solution(self, rig_name, solution):
        self.collector.add_solution(rig_name, solution)

    def add_interaction_with_error(self, rig_name):
        self.collector.add_interaction_with_error(rig_name)

    def send_report(self):
        self.logger.info("Sending Daily Report")
        report = self.build_report()
        self.email_sender.send_email(report, "Daily Report")
        self.collector=Collector()

    def save_to_disk(self):
        self.logger.debug("Persisting report to disk")
        report = self.build_report()
        with open("logs/Report_bkp.txt", "w") as text_file:
            text_file.write(report)
        

    def build_report(self):
        report = ""
        report += "Daily Report\n"
        report += "================\n"
        report += "\n"
        report += "Errors:\n"
        report += pprint.pformat(self.collector.errors, indent=4) + "\n"
        report += "\n"
        report += "Problems:\n"
        report += pprint.pformat(self.collector.problems, indent=4) + "\n"
        report += "\n"
        report += "Solutions:\n"
        report += pprint.pformat(self.collector.applied_solutions, indent=4) + "\n"
        report += "\n"
        report += "Amount of errors:\n"
        report += pprint.pformat(self.collector.interaction_errors, indent=4) + "\n"
        return report