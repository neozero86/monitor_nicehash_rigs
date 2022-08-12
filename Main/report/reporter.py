from asyncio.log import logger
from Main.report.collector import Collector
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from Main.singleton import Singleton
from datetime import datetime

@Singleton
class Reporter():
    def __init__(self):
        pass
    
    def init(self, email_sender, config,logger):
        self.email_sender = email_sender
        self.config = config
        self.logger = logger
        self.daily_collector = Collector()
        self.weekly_collector = Collector()
        self.monthly_collector = Collector()
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
        self.daily_collector.pay(rig_name, amount)
        self.weekly_collector.pay(rig_name, amount)
        self.monthly_collector.pay(rig_name, amount)

    def add_errors(self, rig_name, errors):
        self.daily_collector.add_errors(rig_name, errors)
        self.weekly_collector.add_errors(rig_name, errors)
        self.monthly_collector.add_errors(rig_name, errors)

    def add_problems(self, rig_name, problems):
        self.daily_collector.add_problems(rig_name, problems)
        self.weekly_collector.add_problems(rig_name, problems)
        self.monthly_collector.add_problems(rig_name, problems)
    
    def add_solutions(self, rig_name, solutions):
        self.daily_collector.add_solutions(rig_name, solutions)
        self.weekly_collector.add_solutions(rig_name, solutions)
        self.monthly_collector.add_solutions(rig_name, solutions)

    def add_error(self, rig_name, error):
        self.daily_collector.add_error(rig_name, error)
        self.weekly_collector.add_error(rig_name, error)
        self.monthly_collector.add_error(rig_name, error)

    def add_problem(self, rig_name, problem):
        self.daily_collector.add_problem(rig_name, problem)
        self.weekly_collector.add_problem(rig_name, problem)
        self.monthly_collector.add_problem(rig_name, problem)

    def add_solution(self, rig_name, solution):
        self.daily_collector.add_solution(rig_name, solution)
        self.weekly_collector.add_solution(rig_name, solution)
        self.monthly_collector.add_solution(rig_name, solution)

    def add_interaction_with_error(self, rig_name):
        self.daily_collector.add_interaction_with_error(rig_name)
        self.weekly_collector.add_interaction_with_error(rig_name)
        self.monthly_collector.add_interaction_with_error(rig_name)

    def send_report(self):
        self.logger.info("Sending Daily Report")
        report = self.daily_report()
        self.email_sender.send_email(report, "Daily Report")
        self.daily_collector=Collector()
        dt = datetime.now()
        if (dt.weekday() == 1):
            self.logger.info("Sending Weekly Report")
            report = self.weekly_report()
            self.email_sender.send_email(report, "Weekly Report")
            self.weekly_collector=Collector()
        if (dt.day == 1):
            self.logger.info("Sending Monthly Report")
            report = self.monthly_report()
            self.email_sender.send_email(report, "Monthly Report")
            self.monthly_collector=Collector()
        

    def save_to_disk(self):
        self.logger.debug("Persisting reports to disk")
        with open("Main/static/daily.html", "w") as text_file:
            text_file.write(self.daily_report())
        with open("Main/static/weekly.html", "w") as text_file:
            text_file.write(self.weekly_report())
        with open("Main/static/monthly.html", "w") as text_file:
            text_file.write(self.monthly_report())
        
    def dict_to_html(self, dictionary):
        result = ""
        for k in dictionary:
            result += "<span style=\"color:#2980b9\"><strong><span style=\"font-size:16px\">" + k + "</strong></span></span>"
            table = "<table border=0 style=\"border-spacing: 10px 0rem;\">"
            for k2,v in self.sorted_by_key(dictionary[k]).items():
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

    def daily_report(self):
        return self.report_from_collector(self.daily_collector, "Daily")
    
    def weekly_report(self):
        return self.report_from_collector(self.weekly_collector, "Weekly")

    def monthly_report(self):
        return self.report_from_collector(self.monthly_collector, "Monthly")

    def report_from_collector(self, collector, frequency):
        return self.build_report(collector.paid_amounts, collector.problems, collector.applied_solutions, collector.interaction_errors, collector.errors, frequency)


    def build_report(self, paid_amounts, problems, applied_solutions, interaction_errors, errors, frequency):
        report = ""
        report += "<p><center><span style=\"font-size:48px\"><u><strong>{} Report</strong></u></span></center></p>".format(frequency)
        report += "<p><br />&nbsp;</p>"
        report += "<p><span style=\"color:#cc3300\"><span style=\"font-size:28px\"><strong>Profitability</strong></span></span></p>"
        report += self.to_html(self.sorted_by_key(paid_amounts))
        report += "<p><br />&nbsp;</p>"
        report += "<p><span style=\"color:#ff0000\"><span style=\"font-size:28px\"><strong>Problems</strong></span></span></p>"
        report += self.dict_to_html(problems)
        report += "<p><br />&nbsp;</p>"
        report += "<p><span style=\"color:#70ad47\"><span style=\"font-size:28px\"><strong>Solutions</strong></span></span></p>"
        report += self.dict_to_html(applied_solutions)
        report += "<p><br />&nbsp;</p>"
        report += "<p><span style=\"color:#cc3300\"><span style=\"font-size:28px\"><strong>Accumulated Errors</strong></span></span></p>"
        report += self.to_html(self.sorted_by_key(interaction_errors))
        report += "<p><br />&nbsp;</p>"
        report += "<p><span style=\"color:#f4b083\"><span style=\"font-size:28px\"><strong>Errors Detail</strong></span></span></p>"
        report += self.dict_to_html(errors)
        return report

    def sorted_by_key(self, dictionary):
        return dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))