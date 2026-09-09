import os

from structsim.gluecode.my_simulator import MySimulator
from structsim.gluecode.simple_simulation_handler import SimpleSimulationHandler


class MySimulatorHandler(SimpleSimulationHandler):
    """A ``SimpleSimulationHandler`` that runs the bundled ``MySimulator``.

    The faithful ``SimpleSimulationHandler.start_simulation`` only creates an
    empty result file (matching the Java original, where the framework is
    simulator-agnostic). This variant additionally invokes ``MySimulator`` on
    the input file, so a default run actually produces ``result=val1*val2``
    output at the configured ``pathToSimulatorResultFile``.

    Note: the framework calls ``start_simulation`` with the *global*
    ``pathParameters`` file, so the computed result reflects the base
    parameters rather than each environment's modified parameters. This is a
    property of the framework's plug-in contract, not of this handler.
    """

    def start_simulation(self, path_to_input_file: str) -> None:
        result_file = self._options.get_path_to_simulator_result_file()
        os.makedirs(os.path.dirname(result_file), exist_ok=True)
        MySimulator.run(path_to_input_file, result_file)
