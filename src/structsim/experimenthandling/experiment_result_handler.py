import logging
import threading
from queue import Queue

from structsim.experimenthandling.options import Options

logger = logging.getLogger(__name__)


class ExperimentResultHandler:
    """Third thread: extracts measures from result files and saves them."""

    def __init__(self, results_queue: Queue, glue_code, fm, o: Options) -> None:
        self.results_queue = results_queue
        self.glue_code = glue_code
        self.fm = fm
        self.options = o

    def run(self) -> None:
        if not self.results_queue.empty():
            items = []
            while not self.results_queue.empty():
                items.append(self.results_queue.get())

            for str_path in items:
                logger.debug(f"Result queue string : {str_path}")
                measures = self.glue_code.extract_measures(str_path)
                position_of_last_slash = str_path.rfind("/")
                folder_to_save = str_path[:position_of_last_slash]
                logger.debug(f"Folder where it's saved : {folder_to_save}")
                position_last_slash = folder_to_save.rfind("/")
                name_simulation = folder_to_save[position_last_slash + 1:]
                logger.debug(f"Name Simulation : {name_simulation}")
                self.fm.create_measures_file(measures, folder_to_save + "/measures.txt")
                self.fm.copy_file(
                    folder_to_save + "/measures.txt",
                    self.options.path_simulator + "/" + name_simulation + "/measures.txt",
                )
        else:
            threading.current_thread()  # mirror of Java's Thread.currentThread().interrupt()
