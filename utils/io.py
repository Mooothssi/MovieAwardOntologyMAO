from pathlib import Path
from typing import IO, Union

from utils.dict import select_not_null


def open_and_write_file(file: Union[IO, str, Path],
                        s: str,
                        *,
                        mode: str = 'w',
                        buffering: int = None,
                        encoding: str = None,
                        errors: str = None,
                        newline: str = None,
                        closefd: bool = None) -> None:
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
        options = {
            'mode': mode,
            'buffering': buffering,
            'encoding': encoding if encoding is not None else 'utf-8',
            'errors': errors,
            'newline': newline,
            'closefd': closefd,
        }
        if isinstance(file, (str, Path)):
            with open(file, **select_not_null(options)) as f:
                f.write(s)
                return
    raise AssertionError
