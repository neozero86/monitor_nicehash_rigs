from Main.solution.solution import Solution
from Main.operational_status.down import Down

class Human(Solution):
    
    def next_status(self):
        return Down()

    def solve(self, api, rig_id, rig_name, email_sender, problem, logger):
        logger.error('human strategy reached for problem: {}'.format(problem))
        email_sender.send_email(email_content=str(problem), email_subject='Issue OPEN Rig {}'.format(rig_name))