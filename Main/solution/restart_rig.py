from Main.solution.solution import Solution
from Main.operational_status.wait import Wait

class RestartRig(Solution):
    
    def next_status(self):
        return Wait(10)

    def solve(self, api, rig_id, email_sender, problem, logger):
        logger.error('restart rig strategy reached for problem: {}'.format(problem))
        api.restart_rig(rig_id)
        logger.info('rig restarted')