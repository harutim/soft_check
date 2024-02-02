import inspect
import os


def get_full_context(level):
    """
    Get the full context information at a specified call stack level.

    Args:
    - level (int): The call stack level.

    Returns:
    - Tuple[str, int, str, str]: A tuple containing filename, line number, function name, and context.
    """
    (_, filename, line, funcname, contextlist) = inspect.stack()[level][0:5]
    try:
        filename = os.path.relpath(filename)
    except ValueError:
        filename = os.path.abspath(filename)
    context = contextlist[0].strip() if contextlist else ""
    return (filename, line, funcname, context)
