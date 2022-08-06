from Main.solution.solution import Solution
from Main.operational_status.down import Down

class Human(Solution):
    
    def next_status(self):
        return Down(10)

    def solve(self, api, rig_id, email_sender, problem, logger):
        logger.error('human strategy reached for problem: {}'.format(problem))
        email_sender.send_email(email_content=str(problem), subject='Issue OPEN Rig {}'.format(rig_id))