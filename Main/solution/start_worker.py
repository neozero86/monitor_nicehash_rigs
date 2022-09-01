from Main.solution.solution import Solution
from Main.operational_status.wait import Wait

class StartWorker(Solution):

    def __init__(self, cicles_to_wait= 5):
        super(Solution, self).__init__()
        self.cicles_to_wait = cicles_to_wait
   
    def next_status(self):
        return Wait(self.cicles_to_wait)

    def solve(self, api, rig_id, rig_name, email_sender, problem, logger):
        logger.error('start worker strategy reached for problem: {}'.format(problem))
        api.start_worker(rig_id)
        logger.info('worker started')
        