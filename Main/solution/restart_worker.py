from Main.solution.solution import Solution
from Main.operational_status.wait import Wait

class RestartWorker(Solution):
   
    def next_status(self):
        return Wait(4)

    def solve(self, api, rig_id, email_sender, problem, logger):
        logger.error('restart worker strategy reached for problem: {}'.format(problem))
        api.restart_worker(rig_id)
        logger.info('worker restarted')
        