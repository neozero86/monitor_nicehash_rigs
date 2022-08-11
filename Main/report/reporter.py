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

    def pay(self, rig_name, amount):
        self.collector.pay(rig_name, amount)

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
        with open("logs/Report_bkp.html", "w") as text_file:
            text_file.write(report)
        
    def dict_to_html(self, dictionary):
        result = ""
        for k in dictionary:
            result += "<span style=\"color:#2980b9\"><strong><span style=\"font-size:16px\">" + k + "</strong></span></span>"
            table = "<table border=0 style=\"border-spacing: 10px 0rem;\">"
            for k2,v in dictionary[k].items():
                table += "<tr>"
                table += "<td>" + str(k2) + "</td>"
                table += "<td>" + str(v) + "</td>"
                table += "</tr>"
            table += "</table><br/>"
            result += table
        return result

    def to_html(self, plain_dict):
        data = ""
        for k in plain_dict:
            data += "<td style=\"text-align:left; padding: 10px;\"><span style=\"color:#2980b9\"><strong>" + k + "</strong></span></td>"
            data += "<td style=\"text-align:center; padding: 10px;\">" + str(plain_dict[k]) + "</td>"
            data += "<tr>"
 
        data = "<table border=1>" + data + "</table>"
        return data

    def build_report(self):
        report = ""
        report += "<p><center><span style=\"font-size:48px\"><u><strong>Daily Report</strong></u></span></center></p>"
        report += "<p><br />&nbsp;</p>"
        report += "<p><span style=\"color:#ff0000\"><span style=\"font-size:28px\"><strong>Problems</strong></span></span></p>"
        report += self.dict_to_html(self.collector.problems)
        report += "<p><br />&nbsp;</p>"
        report += "<p><span style=\"color:#70ad47\"><span style=\"font-size:28px\"><strong>Solutions</strong></span></span></p>"
        report += self.dict_to_html(self.collector.applied_solutions)
        report += "<p><br />&nbsp;</p>"
        report += "<p><span style=\"color:#cc3300\"><span style=\"font-size:28px\"><strong>Accumulated Errors</strong></span></span></p>"
        report += self.to_html(self.collector.interaction_errors)
        report += "<p><br />&nbsp;</p>"
        report += "<p><span style=\"color:#cc3300\"><span style=\"font-size:28px\"><strong>Profitability</strong></span></span></p>"
        report += self.to_html(dict(sorted(self.collector.paid_amounts.items(), key=lambda item: item[1], reverse=True)))
        report += "<p><br />&nbsp;</p>"
        report += "<p><span style=\"color:#f4b083\"><span style=\"font-size:28px\"><strong>Errors Detail</strong></span></span></p>"
        report += self.dict_to_html(self.collector.errors)
        return report