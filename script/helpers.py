import subprocess
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_command(command: str) -> None:
    """Run a command using a subprocess
    """
    try:
        # Execute the command
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        logging.info("Command output: %s", result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error("Command failed with return code %d", e.returncode)
        logging.error("Command output: %s", e.output)
        logging.error("Command error output: %s", e.stderr)
        raise
    return result
