from pathlib import Path
from typing import IO, Union


def open_and_write_file(file: Union[IO, str, Path], s: str) -> None:
    """Convenience function to write to file.

    Ensures `s` is written to `file` using either its name or its path.

    Args:
        file: A filename or an opened file (IO object).
        s: The string to write to the file.
        options: Options to open the file with if unopened.

    Returns:
        None

    Raises:
        OSError: When `file` is an IO that doesn't support writing.
    """
    try:
        file.write(s)
        return
    except OSError:
        raise
    except AttributeError:
        if isinstance(file, (str, Path)):
            with open(file, 'w', 'utf-8') as f:
                f.write(s)
                return
    raise AssertionError
