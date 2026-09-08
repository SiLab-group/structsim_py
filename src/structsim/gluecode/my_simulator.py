class MySimulator:
    """Example simulator: reads val1 and val2 from input file and writes their product."""

    @staticmethod
    def run(path_to_input_file: str, path_to_result_file: str) -> None:
        params: dict = {}
        try:
            with open(path_to_input_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    pos = line.index("=")
                    key = line[:pos].strip()
                    value = float(line[pos + 1:].strip())
                    params[key] = value

            result = params["val1"] * params["val2"]

            with open(path_to_result_file, "w", encoding="utf-8") as f:
                f.write(f"result={result}\n")

        except Exception as e:
            import traceback
            traceback.print_exc()
