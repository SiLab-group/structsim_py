import threading
from queue import PriorityQueue
from typing import IO

from structsim.experimenthandling.environment import Environment
from structsim.experimenthandling.experiment_plan_generator import ExperimentPlanGenerator
from structsim.experimenthandling.experiment_simulator_handler import ExperimentSimulatorHandler
from structsim.interfaces.a_simulation_system_handler import ASimulationSystemHandler
from structsim.util.file_management import FileManagement


class StartProgram:
    """Entry point that orchestrates the planning, simulation, and result threads."""

    @staticmethod
    def start_program(path_config_file, glue_code) -> None:
        """Start the simulation framework.

        Args:
            path_config_file: Path string or IO stream to the config properties file.
            glue_code: An ASimulationSystemHandler instance providing the glue code.
        """
        fm = FileManagement()
        glue_code_class: ASimulationSystemHandler = glue_code

        o = fm.load_data_from_properties_file(path_config_file)

        list_param = glue_code_class.read_parameters_file_from_stream(
            open(o.get_path_parameters(), "rb")
        )

        base_env = Environment(0, list_param, 1.0)

        queue: PriorityQueue = PriorityQueue()
        result_queue: PriorityQueue = PriorityQueue()

        glue_code_class.set_options(o)

        if o.get_type_of_cuttof_planning() != "CRITERIA" or o.get_stop_criteria() > 0:
            planning = ExperimentPlanGenerator(queue, base_env, o, glue_code_class, fm)
            planning_thread = threading.Thread(target=planning.run, name="Planning Thread")
            planning_thread.start()

            simulator = ExperimentSimulatorHandler(
                queue, result_queue, o, glue_code_class, fm, planning
            )
            simulation_thread = threading.Thread(target=simulator.run, name="Simulation Thread")
            simulation_thread.start()

            # Block until the full pipeline has finished so that, once this method
            # returns, all output files (SummaryFile.txt, measures) are on disk.
            # (Fixes the "start_program returns before threads finish" issue
            # documented in the thesis's slowness analysis.)
            planning_thread.join()
            simulation_thread.join()
