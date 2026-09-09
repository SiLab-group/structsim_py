from structsim.gluecode.concrete_modifier import ConcreteModifier
from structsim.gluecode.my_simulator_handler import MySimulatorHandler
from structsim.interfaces.start_program import StartProgram


class Simulation(StartProgram):
    """Entry point for the example simulation."""

    @staticmethod
    def main(config_path: str = "config.properties") -> None:
        """Run the bundled example simulation.

        Uses ``MySimulatorHandler`` so the run produces real
        ``result=val1*val2`` output (via the bundled ``MySimulator``) rather
        than empty result files.

        Args:
            config_path: Path to the ``config.properties`` file describing the
                run (input/output paths and the cut-off planning strategy).
        """
        modifiers = [
            ConcreteModifier("val2", "+", 1.0, 0.5),
            ConcreteModifier("val2", "+", 10.0, 0.5),
        ]

        ssh = MySimulatorHandler(modifiers)

        with open(config_path, "rb") as config_file:
            StartProgram.start_program(config_file, ssh)


if __name__ == "__main__":
    Simulation.main()
