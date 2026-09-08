import logging
import os
import shutil
import datetime
from datetime import timedelta
from typing import IO, List, Optional

from structsim.experimenthandling.environment import Environment
from structsim.experimenthandling.measure import Measure
from structsim.experimenthandling.options import Options

logger = logging.getLogger(__name__)


class FileManagement:
    """Utility class for file operations: reading, writing, copying, and folder management."""

    def __init__(self) -> None:
        self.filename: str = ""
        self.options: Options = Options()
        self._path_result: str = ""
        self._path_simulator: str = ""

    def content_of_a_file(self) -> str:
        """Return the content of the file at self.filename as a string."""
        if not os.path.isfile(self.filename):
            return "this is not a file"
        content = ""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                for line in f:
                    content += line.rstrip("\n")
        except FileNotFoundError as e:
            logger.info("Just a stack trace", exc_info=e)
        return content

    def move_file(self, origin_file: str, destination_file: str) -> None:
        """Move a file from origin_file to destination_file."""
        if not os.path.exists(origin_file):
            return
        try:
            shutil.move(origin_file, destination_file)
        except OSError:
            logger.error("Impossible to move this file")

    def copy_file(self, file: str, destination: str) -> None:
        """Copy file to destination, replacing if it already exists."""
        try:
            shutil.copy2(file, destination)
        except Exception:
            logger.error("This file in this folder already exist")

    def create_folder(self, folder_path: str) -> None:
        """Create an empty folder at folder_path (no-op if it already exists)."""
        try:
            os.mkdir(folder_path)
        except (FileNotFoundError, FileExistsError):
            pass

    def save_simulation_result(self, result: str, env: Environment) -> str:
        """Save a simulation result string to a file and return the file path."""
        file_path = (
            self.options.get_folder_path_out()
            + "/_sim"
            + str(env.get_id())
            + "/results.txt"
        )
        try:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(f"Result={result}\n")
        except FileNotFoundError:
            logger.error("File not Found")
        return file_path

    def save_simultation_result(self, result: str, env: Environment) -> str:
        return self.save_simulation_result(result, env)

    def load_data_from_properties_file(self, file_path) -> Options:
        """Load options from a properties file (path string or IO stream)."""
        import configparser

        props: dict = {}

        if isinstance(file_path, str):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and "=" in line and not line.startswith("#"):
                            k, _, v = line.partition("=")
                            props[k.strip()] = v.strip()
            except OSError:
                logger.error("Error to load Data from Properties file")
        else:
            # file_path is an IO stream
            try:
                content = file_path.read()
                if isinstance(content, bytes):
                    content = content.decode("utf-8")
                for line in content.splitlines():
                    line = line.strip()
                    if line and "=" in line and not line.startswith("#"):
                        k, _, v = line.partition("=")
                        props[k.strip()] = v.strip()
                file_path.close()
            except OSError:
                logger.error("Error to load Data from Properties file")

        self.options.set_path_parameters(props.get("pathParameters"))
        self.options.set_folder_path_out(props.get("pathOUT"))
        self.options.set_path_simulator(props.get("pathSimulator"))
        self.options.set_path_to_simulator_result_file(props.get("pathToSimulatorResultFile"))

        cuttof_value = props.get("cuttOfPlanning", "")
        type_cuttof = props.get("typeCuttOfPlanning", "")
        self.options.set_type_of_cuttof_planning(type_cuttof)

        if type_cuttof == "INT":
            self.options.set_cuttof_planning(int(cuttof_value))
        elif type_cuttof == "DAY":
            self.options.set_cuttof_planning_h(datetime.datetime(1, 1, int(cuttof_value)))
        elif type_cuttof == "HOURS":
            self.options.set_cuttof_planning_h(datetime.datetime(1, 1, 1, int(cuttof_value)))
        elif type_cuttof == "MINUTES":
            self.options.set_cuttof_planning_h(datetime.datetime(1, 1, 1, 0, int(cuttof_value)))
        elif type_cuttof == "CRITERIA":
            self.options.set_stop_criteria(float(cuttof_value))

        return self.options

    def write_data_in_properties_file(
        self, data_to_write: dict, file_path: str, keep_previous_results: bool
    ) -> None:
        """Write key=value pairs to a properties file."""
        parent = os.path.dirname(file_path)
        if parent and not os.path.isdir(parent):
            return
        mode = "a" if keep_previous_results else "w"
        try:
            with open(file_path, mode, encoding="utf-8") as f:
                for k, v in data_to_write.items():
                    f.write(f"{k}={v}\n")
        except OSError as e:
            logger.error(str(e))

    def create_new_folder(self, e: Environment) -> str:
        """Create simulation folders for a given environment and return the result path."""
        self._path_result = self.options.get_folder_path_out() + "/_sim" + str(e.get_id())
        self.create_folder(self._path_result)

        self._path_simulator = self.options.get_path_simulator() + "/_sim" + str(e.get_id()) + "/"
        self.create_folder(self._path_simulator)
        return self._path_result

    def create_new_folder_simulation(self, env: Environment, glue_code) -> None:
        """Create folder for environment and write its parameters file, then mirror to simulator."""
        path_new_folder = self.create_new_folder(env)
        env.set_path_save_result(path_new_folder)
        glue_code.write_parameters_file(env.get_set_of_parameters(), path_new_folder)

        if os.path.isdir(self._path_result):
            for fname in os.listdir(self._path_result):
                src = os.path.join(self._path_result, fname)
                dst = os.path.join(self._path_simulator, fname)
                try:
                    shutil.copy2(src, dst)
                except OSError:
                    logger.error(
                        "Error when we create the new Folder of the simulation. "
                        "Is the path in the config properties right?"
                    )

    def create_measures_file(self, measures: List[Measure], measures_file_path: str) -> None:
        """Write measures to a file."""
        try:
            with open(measures_file_path, "w", encoding="utf-8") as f:
                for m in measures:
                    f.write(f"{m.get_key()}={m.get_value()}\n")
        except Exception:
            logger.error("Error when we create the measures file")

    def create_modifier_file(self, path: str, modifier: str) -> None:
        """Write modifier summary to SummaryFile.txt inside path."""
        try:
            with open(os.path.join(path, "SummaryFile.txt"), "w", encoding="utf-8") as f:
                f.write(modifier)
                f.write("\n")
        except OSError:
            logger.error("Error to save the summary File")

    def get_filename(self) -> str:
        return self.filename

    def set_filename(self, filename: str) -> None:
        self.filename = filename

    def get_options(self) -> Options:
        return self.options

    def set_options(self, options: Options) -> None:
        self.options = options
