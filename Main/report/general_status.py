from Main.singleton import Singleton

@Singleton
class GeneralStatus():
    def __init__(self):
        self.status = {}

    def update(self, rig):
        self.status[rig.name] = {
            "status": rig.status,
            "problem": rig.problem,
            "current_solution": rig.solution,
            "future_solutions": rig.solutions            
        }
        try:
            with open("Main/static/dashboard.html", "w") as text_file:
                text_file.write(self.html_status())
        except Exception as e:
            print(e)

    def html_status(self):
        html = ""
        for rig in self.status:
            html += "<div class='rig'><div class='rig-name'>{}</div><div class='status'>{}</div>".format(rig, self.status[rig]["status"])
            html += "<div class='problem'>{}</div>".format(self.status[rig]["problem"])
            html += "<div class='appying solution'>{}</div>".format(self.status[rig]["current_solution"])
            html += "<div class='next solutions'>{}</div>".format(self.status[rig]["future_solutions"])
            html += "</div>"
        return html