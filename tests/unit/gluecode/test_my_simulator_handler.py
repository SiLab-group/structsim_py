from structsim.experimenthandling.options import Options
from structsim.gluecode.my_simulator_handler import MySimulatorHandler


class TestMySimulatorHandler:

    def test_start_simulation_writes_product_of_val1_and_val2(self, tmp_path):
        # Arrange: an input parameters file and a result-file location.
        input_file = tmp_path / "parameters.txt"
        input_file.write_text("val1=3.0\nval2=4.0\n", encoding="utf-8")

        result_file = tmp_path / "results" / "results.txt"

        options = Options()
        options.set_path_to_simulator_result_file(str(result_file))

        handler = MySimulatorHandler()
        handler.set_options(options)

        # Act
        handler.start_simulation(str(input_file))

        # Assert: MySimulator wrote result = val1 * val2 = 12.0
        assert result_file.exists()
        assert result_file.read_text(encoding="utf-8").strip() == "result=12.0"
