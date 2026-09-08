import logging
import time
from datetime import datetime, timedelta
from queue import Queue
from typing import List

from structsim.experimenthandling.environment import Environment
from structsim.experimenthandling.options import Options
from structsim.interfaces.a_modifier import AModifier

logger = logging.getLogger(__name__)


class ExperimentPlanGenerator:
    """First thread: generates the planning queue of environments."""

    def __init__(
        self,
        planning_queue: Queue,
        base_env: Environment,
        o: Options,
        glue_code,
        fm,
    ) -> None:
        self.base_environment = base_env
        self.planning_queue = planning_queue
        self.options = o
        self.glue_code = glue_code
        self.fm = fm
        self.is_finish: bool = False
        self._result: str = ""

        glue_code.initiate_modifier_list()

    def _create_modifier_file(self, e: Environment) -> None:
        self._result += e.to_string_modifier() + "\n"
        self.fm.create_modifier_file(self.options.folder_path_out, self._result)

    def _add_env_to_queue(self, e: Environment) -> None:
        self.planning_queue.put(e)
        logger.debug(f"Event : {e.id} is added !")

    def _create_next_environments(self, base_env: Environment) -> None:
        to_explore: List[Environment] = []
        self.fm.create_new_folder_simulation(base_env, self.glue_code)

        list_modifiers: List[AModifier] = self.glue_code.get_list_modifier_class()
        to_explore.append(base_env)
        self._add_env_to_queue(base_env)

        id_cpt = base_env.id
        cpt = 0

        while to_explore:
            if (
                self.options.get_type_of_cuttof_planning() == "INT"
                and cpt >= self.options.get_cuttof_planning()
            ):
                break

            parent_env = to_explore.pop(0)

            for modifier in list_modifiers:
                id_cpt += 1
                current_env = Environment.from_environment(id_cpt, parent_env)
                current_env = modifier.apply_modifier(current_env)
                current_env.get_trace().append(modifier.get_name())

                logger.debug(
                    f"--------------------------------------------{current_env.id} {current_env.trace}"
                )

                current_env.set_probability(
                    parent_env.get_probability() * modifier.get_probability()
                )

                if (
                    self.options.get_type_of_cuttof_planning() == "CRITERIA"
                    and current_env.get_probability() > self.options.get_stop_criteria()
                ):
                    to_explore.append(current_env)

                if self.options.get_type_of_cuttof_planning() == "INT":
                    to_explore.append(current_env)

                self.fm.create_new_folder_simulation(current_env, self.glue_code)
                self._add_env_to_queue(current_env)
                self._create_modifier_file(current_env)

            cpt += 1
            logger.debug(f"CPT : {cpt}")

            to_explore.sort(reverse=True)

    def run(self) -> None:
        type_of_cuttof = self.options.get_type_of_cuttof_planning()
        logger.debug(f"option = {type_of_cuttof}")

        cuttof_format = ""

        if type_of_cuttof in ("INT", "CRITERIA"):
            self._create_next_environments(self.base_environment)
        elif type_of_cuttof == "DAY":
            end_time = datetime.now() + self.options.get_cuttof_planning_h()
            cuttof_format = "TIME"
        elif type_of_cuttof == "HOURS":
            end_time = datetime.now() + self.options.get_cuttof_planning_h()
            cuttof_format = "TIME"
        elif type_of_cuttof == "MINUTES":
            end_time = datetime.now() + self.options.get_cuttof_planning_h()
            cuttof_format = "TIME"

        if cuttof_format == "TIME":
            while datetime.now() < end_time:
                self._create_next_environments(self.base_environment)

        self.is_finish = True

        self.fm.copy_file(
            self.options.folder_path_out + "/SummaryFile.txt",
            self.options.path_simulator + "/SummaryFile.txt",
        )
