from Main.singleton import Singleton

@Singleton
class GeneralStatus():
    def __init__(self):
        self.status = {}

    def update(self, rig):
        self.status[rig.name] = {
            "status": rig.status,
            "problem": rig.problem,
            "solutions": rig.solutions
        }
        try:
            with open("Main/static/dashboard.html", "w") as text_file:
                text_file.write(self.html_status())
        except Exception as e:
            print(e)

    def html_status(self):
        html = ""
        for rig in self.status:
            html += "<div class='rig'><div class='rig-name'>{}</div><div class='rig-status'>{}</div><div class='rig-problem'>{}</div><div class='rig-solutions'>{}</div></div>".format(rig, self.status[rig]["status"], self.status[rig]["problem"], self.status[rig]["solutions"])
        return html