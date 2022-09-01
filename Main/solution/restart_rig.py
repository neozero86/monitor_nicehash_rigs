from Main.solution.solution import Solution
from Main.operational_status.wait import Wait

class RestartRig(Solution):

    def __init__(self, cicles_to_wait= 10):
        super(Solution, self).__init__()
        self.cicles_to_wait = cicles_to_wait
    
    def next_status(self):
        return Wait(self.cicles_to_wait)

    def solve(self, api, rig_id, rig_name, email_sender, problem, logger):
        logger.error('restart rig strategy reached for problem: {}'.format(problem))
        api.restart_rig(rig_id)
        logger.info('rig restarted')