import logging
import threading
from queue import Empty, Queue

from structsim.experimenthandling.experiment_result_handler import ExperimentResultHandler
from structsim.experimenthandling.options import Options

logger = logging.getLogger(__name__)


class ExperimentSimulatorHandler:
    """Second thread: consumes environments from the planning queue and runs simulations."""

    def __init__(
        self,
        environment_queue: Queue,
        results_queue: Queue,
        o: Options,
        glue_code,
        fm,
        plan,
    ) -> None:
        self.environment_queue = environment_queue
        self.results_queue = results_queue
        self.options = o
        self.glue_code = glue_code
        self.fm = fm
        self.plan = plan

    def run(self) -> None:
        result_handler = ExperimentResultHandler(self.results_queue, self.glue_code, self.fm, self.options)
        result_thread = threading.Thread(target=result_handler.run, name="Result Thread")

        while True:
            try:
                logger.debug(f"Size of the Simulation Queue : {self.environment_queue.qsize()}")
                # Use a timeout so the thread cannot block forever once the
                # planning thread has finished and drained the queue.
                # (Fixes the "queue.get() without timeout" hang documented in
                # the thesis's slowness analysis.)
                env = self.environment_queue.get(timeout=0.5)
            except Empty:
                if self.plan.is_finish and self.environment_queue.empty():
                    break
                continue

            try:
                self.glue_code.start_simulation(self.options.get_path_parameters())
                result_path_for_this_simulation = (
                    env.path_save_result + "/results_sim" + str(env.id) + ".txt"
                )
                logger.debug(result_path_for_this_simulation)
                self.fm.copy_file(self.options.path_to_simulator_result_file, result_path_for_this_simulation)
                self.fm.copy_file(
                    self.options.path_to_simulator_result_file,
                    self.options.path_simulator
                    + "/"
                    + env.path_save_result[env.path_save_result.rfind("/") + 1:]
                    + "/results_sim"
                    + str(env.id)
                    + ".txt",
                )

                self.results_queue.put(result_path_for_this_simulation)

            except Exception as e:
                logger.error("Error in the run of the Thread Simulator", exc_info=e)

            if self.plan.is_finish and self.environment_queue.empty():
                logger.debug(
                    "It's empty ! and it's not the first time that we try to read the queue !"
                )
                break

        # Extract and persist the measures, then wait for that work to finish
        # before returning so callers can rely on the result files existing.
        result_thread.start()
        result_thread.join()
