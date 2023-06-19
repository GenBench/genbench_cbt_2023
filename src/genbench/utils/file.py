import json
from pathlib import Path
from typing import Union, Mapping, Any, List


def get_repo_dir() -> Path:
    """Get the path to the repository."""
    return Path(__file__).parent.parent.parent.parent


def load_jsonnet(
    path: Union[Path, str],
) -> Union[Mapping[str, Any], List[Any], str, int, float, bool, None]:
    """Load a jsonnet file.

    Args:
        path: The path to the jsonnet file.

    Returns:
        The contents of the jsonnet
    """
    import _jsonnet

    if isinstance(path, str):
        path = Path(path)

    jsonnet_str = path.read_text()

    json_str = _jsonnet.evaluate_snippet("snippet", jsonnet_str)
    json_dict = json.loads(json_str)

    return json_dict
