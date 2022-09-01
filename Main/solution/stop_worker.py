from Main.solution.solution import Solution
from Main.operational_status.wait import Wait

class StopWorker(Solution):
   
    def next_status(self):
        return Wait(0)

    def solve(self, api, rig_id, rig_name, email_sender, problem, logger):
        logger.error('stop worker strategy reached for problem: {}'.format(problem))
        api.stop_worker(rig_id)
        logger.info('worker stopped')
        