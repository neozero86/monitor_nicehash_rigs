from Main.report.report_constants import *
from Main.report.collector import Collector
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from Main.singleton import Singleton
from datetime import datetime
import os

@Singleton
class Reporter():
    def __init__(self):
        pass
    
    def init(self, email_sender, config,logger):
        self.email_sender = email_sender
        self.config = config
        self.logger = logger
        self.persist = config["production"]
        self.reset_collector()
        if(config["production"]):
            self.load_collectors()
            scheduler = BackgroundScheduler()
            scheduler.add_job(func=self.send_report, trigger="interval", seconds=config["interval_seconds"])
            scheduler.start()
            atexit.register(lambda: scheduler.shutdown())
            scheduler_backup = BackgroundScheduler()
            scheduler_backup.add_job(func=self.save_to_disk, trigger="interval", seconds=60)
            scheduler_backup.start()
            atexit.register(lambda: scheduler_backup.shutdown())

    def reset_collector(self):
        self.collectors = {
            DAILY: Collector(),
            WEEKLY: Collector(),
            MONTHLY: Collector(),
            YEARLY: Collector(),
            FULL: Collector()
        }
    def load_collectors(self):
        self.collectors = {
            DAILY: self.load_collector(DAILY),
            WEEKLY: self.load_collector(WEEKLY),
            MONTHLY: self.load_collector(MONTHLY),
            YEARLY: self.load_collector(YEARLY),
            FULL: self.load_collector(FULL)
        }

    def load_collector(self, frequency):
        return Collector.from_json(DB_FILE.format(frequency.lower())) if os.path.isfile(DB_FILE.format(frequency.lower())) else Collector()

    def exec_collector(self, collector, method, args):
        return getattr(collector, method)(*args)

    def exec_collectors(self, collectors, method, args):
        for collector in collectors.values():
            self.exec_collector(collector, method, args)

    def pay(self, rig_name, amount):
        self.exec_collectors(self.collectors, "pay", [rig_name, amount])

    def add_errors(self, rig_name, errors):
        self.exec_collectors(self.collectors, "add_errors", [rig_name, errors])

    def add_problems(self, rig_name, problems):
        self.exec_collectors(self.collectors, "add_problems", [rig_name, problems])
    
    def add_solutions(self, rig_name, solutions):
        self.exec_collectors(self.collectors, "add_solutions", [rig_name, solutions])

    def add_error(self, rig_name, error):
        self.exec_collectors(self.collectors, "add_error", [rig_name, error])

    def add_problem(self, rig_name, problem):
        self.exec_collectors(self.collectors, "add_problem", [rig_name, problem])

    def add_solution(self, rig_name, solution):
        self.exec_collectors(self.collectors, "add_solution", [rig_name, solution])

    def add_interaction_with_error(self, rig_name):
        self.exec_collectors(self.collectors, "add_interaction_with_error", [rig_name])

    def send_report(self, dt = datetime.now()):
        self.logger.info("executing send_report at" + str(dt))
        self.logger.info("hour: " + str(dt.hour))
        self.logger.info("minute: " + str(dt.minute))
        if (dt.hour == 7):
            self.logger.info("hour 7 OK")
        if (dt.minute == 0):
            self.logger.info("minute 0 OK")
        if (dt.hour == 7 and dt.minute == 0):
            self.send_report_by(DAILY)
            self.daily_collector=Collector()
            if (dt.weekday() == 0):
                self.send_report_by(WEEKLY)
                self.weekly_collector=Collector()
            if (dt.day == 1):
                self.send_report_by(MONTHLY)
                self.monthly_collector=Collector()
                if (dt.month == 1):
                    self.send_report_by(YEARLY)
                    self.yearly_collector=Collector()
            self.save_to_disk()

    def send_report_by(self, frequency):
        self.logger.info("Sending {} Report".format(frequency))
        report = self.report_from_collector(self.collectors[frequency], frequency)
        self.email_sender.send_email(report, "{} Report".format(frequency))

    def save_to_disk(self):
        if (self.persist):
            self.logger.debug("Persisting reports to disk")
            for frequency in self.collectors:
                self.save_to_disk_by(frequency)

    def save_to_disk_by(self, frequency):
        with open("Main/static/{}.html".format(frequency.lower()), "w") as text_file:
            text_file.write(self.report_from_collector(self.collectors[frequency], frequency))
        with open(DB_FILE.format(frequency.lower()), "w") as text_file:
            text_file.write(self.collectors[frequency].to_json())
        
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

    def report_from_collector(self, collector, frequency):
        return self.build_report(collector.paid_amounts(), collector.problems(), collector.applied_solutions(), collector.interaction_errors(), collector.errors(), frequency)

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