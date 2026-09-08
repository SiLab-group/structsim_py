"""Command-line entry point: ``python -m structsim`` / ``structsim``.

Runs the bundled example simulation described by a ``config.properties`` file.
"""
import argparse
import logging
import sys

from structsim import __version__
from structsim.gluecode.simulation import Simulation


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="structsim",
        description="Run a structured simulation from a config.properties file.",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.properties",
        help="Path to the config.properties file (default: ./config.properties).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    Simulation.main(args.config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
