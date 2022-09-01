from Main.singleton import Singleton
import json

@Singleton
class GeneralStatus():
    def __init__(self):
        self.init()
    
    def init(self, environment='production'):
        self.status = {}
        self.environment = environment

    def update(self, rig):
        self.status[rig.name] = {
            "status": rig.status,
            "problem": rig.problem,
            "current_solution": rig.solution,
            "future_solutions": rig.solutions            
        }
        if (self.environment == 'production'):
            try:
                with open("Main/static/dashboard.html", "w") as text_file:
                    text_file.write(self.html_status())
                with open("db/dashboard.json", "w") as text_file:
                    text_file.write(json.dumps(self.status, default=str))
            except Exception as e:
                print(e)

    def html_status(self):
        html = ""
        for rig in self.status:
            html += "<div class='rig'><div class='rig-name'>{}</div><div class='status'>{}</div>".format(rig, self.status[rig]["status"])
            if (self.status[rig]["problem"] != None):
                html += "<div class='problem'>{}</div>".format(self.status[rig]["problem"])
                html += "<div class='appying solution'>{}</div>".format(self.status[rig]["current_solution"])
                html += "<div class='next solutions'>{}</div>".format(self.status[rig]["future_solutions"])
            html += "</BR></div>"
        return html