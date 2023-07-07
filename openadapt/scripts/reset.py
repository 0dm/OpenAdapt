import os
from subprocess import PIPE, run

from loguru import logger

from openadapt import config


def reset():
    """
    The function clears the database by removing the database file and running a
    database migration using Alembic.

    It also clears the performance plots directory.
    """

    if os.path.exists(config.DB_FPATH):
        os.remove(config.DB_FPATH)

    # Prevents duplicate logging of config values by piping stderr and filtering the output.
    result = run(["alembic", "upgrade", "head"], stderr=PIPE, text=True)
    print(result.stderr[result.stderr.find("INFO  [alembic") :])
    if result.returncode != 0:
        raise RuntimeError("Database migration failed.")
    else:
        print("Database cleared successfully.")

    # clear performance
    if os.path.exists(config.DIRNAME_PERFORMANCE_PLOTS):
        for f in os.listdir(config.DIRNAME_PERFORMANCE_PLOTS):
            logger.info(f"removing {f}")
            os.remove(os.path.join(config.DIRNAME_PERFORMANCE_PLOTS, f))


if __name__ == "__main__":
    reset()
