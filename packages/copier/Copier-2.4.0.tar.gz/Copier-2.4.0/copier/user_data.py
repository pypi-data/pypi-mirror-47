from pathlib import Path

from .tools import printf, prompt, STYLE_WARNING


__all__ = ("get_user_data", )

INDENT = "  "


def load_toml_data(src_path, quiet=False):
    toml_path = Path(src_path) / "copier.toml"
    if not toml_path.exists():
        return {}

    import toml

    toml_src = toml_path.read_text()
    try:
        return toml.loads(toml_src)
    except Exception as e:
        if not quiet:
            print("")
            printf("INVALID", msg=toml_path, style=STYLE_WARNING, indent=0)
            print("-" * 42)
            print(e)
            print("-" * 42)
        return {}


def load_yaml_data(src_path, quiet=False):
    yaml_path = Path(src_path) / "copier.yml"
    if not yaml_path.exists():
        yaml_path = Path(src_path) / "copier.yaml"
        if not yaml_path.exists():
            return {}

    from ruamel.yaml import YAML
    yaml = YAML(typ="safe")

    try:
        return yaml.load(yaml_path)
    except Exception as e:
        if not quiet:
            print("")
            printf("INVALID", msg=yaml_path, style=STYLE_WARNING, indent=0)
            print("-" * 42)
            print(e)
            print("-" * 42)
        return {}


def load_json_data(src_path, quiet=False, warning=True):
    json_path = Path(src_path) / "copier.json"
    if not json_path.exists():
        return load_old_json_data(src_path, quiet=quiet, warning=warning)

    import json

    json_src = json_path.read_text()
    try:
        return json.loads(json_src)
    except ValueError as e:
        if not quiet:
            print("")
            printf("INVALID", msg=json_path, style=STYLE_WARNING, indent=0)
            print("-" * 42)
            print(e)
            print("-" * 42)
        return {}


def load_old_json_data(src_path, quiet=False, warning=True):
    # TODO: Remove on version 3.0
    json_path = Path(src_path) / "voodoo.json"
    if not json_path.exists():
        return {}

    if warning and not quiet:
        print("")
        printf(
            "WARNING",
            msg="`voodoo.json` is deprecated. "
            + "Replace it with a `copier.toml`, `copier.yaml` or `copier.json`.",
            style=STYLE_WARNING,
            indent=10,
        )

    import json

    json_src = json_path.read_text()
    try:
        return json.loads(json_src)
    except ValueError as e:
        if not quiet:
            print("")
            printf("INVALID", msg=json_path, style=STYLE_WARNING, indent=0)
            print("-" * 42)
            print(e)
            print("-" * 42)
        return {}


def load_default_data(src_path, quiet=False, warning=True):
    """Try to load a `copier.yml`, or a `copier.toml`, or a `copier.json`, or
    the deprecated `voodoo.json`, in that order. Returns as soon as it founds one.
    """
    data = load_yaml_data(src_path, quiet=quiet)
    if not data:
        data = load_toml_data(src_path, quiet=quiet)
    if not data:
        data = load_json_data(src_path, quiet=quiet, warning=warning)
    return data


SPECIAL_KEYS = ("_exclude", "_include")


def get_user_data(src_path, **flags):  # pragma:no cover
    """Query to user for information needed as per the template's ``copier.toml``.
    """
    default_user_data = load_default_data(src_path, quiet=flags["quiet"])
    if flags["force"] or not default_user_data:
        return default_user_data

    print("")
    user_data = {}
    for key in default_user_data:
        if key in SPECIAL_KEYS:
            continue
        default = default_user_data[key]
        user_data[key] = prompt(INDENT + " {0}?".format(key), default)

    print("\n" + INDENT + "-" * 42)
    return user_data
