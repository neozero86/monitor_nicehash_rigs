from Main.solution.solution import Solution
from Main.operational_status.wait import Wait

class StartWorker(Solution):
   
    def next_status(self):
        return Wait(4)

    def solve(self, api, rig_id, rig_name, email_sender, problem, logger):
        logger.error('start worker strategy reached for problem: {}'.format(problem))
        api.start_worker(rig_id)
        logger.info('worker started')
        