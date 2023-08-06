import datetime
import filecmp
import os
import re
import shutil
import subprocess
from pathlib import Path

from . import vcs
from .user_data import get_user_data
from .tools import (
    copy_file,
    get_jinja_renderer,
    get_name_filter,
    make_folder,
    printf,
    prompt_bool,
    STYLE_OK,
    STYLE_IGNORE,
    STYLE_DANGER,
    STYLE_WARNING,
)


__all__ = ("copy", "copy_local")

# Files of the template to exclude from the final project
DEFAULT_EXCLUDE = (
    "copier.toml",
    "copier.json",
    "voodoo.json",
    "~*",
    "*.py[co]",
    "__pycache__",
    "__pycache__/*",
    ".git",
    ".git/*",
    ".DS_Store",
    ".svn",
)

DEFAULT_INCLUDE = ()

DEFAULT_DATA = {"now": datetime.datetime.utcnow}


def copy(
    src_path,
    dst_path,
    data=None,
    *,
    extra_paths=None,
    exclude=None,
    include=None,
    tasks=None,
    envops=None,
    pretend=False,
    force=False,
    skip=False,
    quiet=False
):
    """
    Uses the template in src_path to generate a new project at dst_path.

    Arguments:

    - src_path (str):
        Absolute path to the project skeleton. May be a version control system URL

    - dst_path (str):
        Absolute path to where to render the skeleton

    - data (dict):
        Optional. Data to be passed to the templates in addtion to the user data from
        a `copier.json`.

    - extra_paths (list):
        Optional. Additional directories to find parent templates in.

    - exclude (list):
        A list of names or shell-style patterns matching files or folders
        that must not be copied.

    - include (list):
        A list of names or shell-style patterns matching files or folders that
        must be included, even if its name are in the `exclude` list.
        Eg: `['.gitignore']`. The default is an empty list.

    - tasks (list):
        Optional lists of commands to run in order after finishing the copy.
        Like in the templates files, you can use variables on the commands that will
        be replaced by the real values before running the command.
        If one of the commands fail, the rest of them will not run.

    - envops (dict):
        Extra options for the Jinja template environment.

    - pretend (bool):
        Run but do not make any changes

    - force (bool):
        Overwrite files that already exist, without asking

    - skip (bool):
        Skip files that already exist, without asking

    - quiet (bool):
        Suppress the status output

    """
    repo = vcs.get_repo(src_path)
    if repo:
        src_path = vcs.clone(repo)

    _data = DEFAULT_DATA.copy()
    _data.update(data or {})

    if extra_paths is None:
        extra_paths = []

    try:
        copy_local(
            src_path,
            dst_path,
            data=_data,
            extra_paths=extra_paths,
            exclude=exclude,
            include=include,
            tasks=tasks,
            envops=envops,
            pretend=pretend,
            force=force,
            skip=skip,
            quiet=quiet,
        )
    finally:
        if repo:
            shutil.rmtree(src_path)


RE_TMPL = re.compile(r"\.tmpl$", re.IGNORECASE)


def resolve_single_path(path):
    try:
        path = Path(path).resolve()
    except FileNotFoundError:
        raise ValueError("Project template not found")

    if not path.exists():
        raise ValueError("Project template not found")

    if not path.is_dir():
        raise ValueError("The project template must be a folder")

    return path


def resolve_paths(src_path, dst_path, extra_paths):
    src_path = resolve_single_path(src_path)
    dst_path = Path(dst_path).resolve()
    extra_paths = [str(resolve_single_path(p)) for p in extra_paths]
    return src_path, dst_path, extra_paths


def copy_local(
    src_path,
    dst_path,
    data,
    *,
    extra_paths=None,
    exclude=None,
    include=None,
    tasks=None,
    envops=None,
    **flags
):
    src_path, dst_path, extra_paths = resolve_paths(src_path, dst_path, extra_paths)

    user_data = get_user_data(src_path, **flags)

    user_exclude = user_data.pop("_exclude", None)
    if exclude is None:
        exclude = user_exclude or DEFAULT_EXCLUDE

    user_include = user_data.pop("_include", None)
    if include is None:
        include = user_include or DEFAULT_INCLUDE

    user_tasks = user_data.pop("_tasks", None)
    if tasks is None:
        tasks = user_tasks or []

    must_filter = get_name_filter(exclude, include)
    data.update(user_data)
    data.setdefault("folder_name", dst_path.name)
    render = get_jinja_renderer(src_path, data, extra_paths, envops)

    if not flags["quiet"]:
        print("")  # padding space

    for folder, _, files in os.walk(str(src_path)):
        rel_folder = folder.replace(str(src_path), "", 1).lstrip(os.path.sep)
        rel_folder = render.string(rel_folder)
        rel_folder = rel_folder.replace("." + os.path.sep, ".", 1)

        if must_filter(rel_folder):
            continue

        folder = Path(folder)
        rel_folder = Path(rel_folder)

        render_folder(dst_path, rel_folder, **flags)

        source_paths = get_source_paths(folder, rel_folder, files, render, must_filter)
        for source_path, rel_path in source_paths:
            render_file(dst_path, rel_path, source_path, render, **flags)

    if not flags["quiet"]:
        print("")  # padding space

    if tasks:
        run_tasks(dst_path, render, tasks)


def get_source_paths(folder, rel_folder, files, render, must_filter):
    source_paths = []
    for src_name in files:
        dst_name = re.sub(RE_TMPL, "", src_name)
        dst_name = render.string(dst_name)
        rel_path = rel_folder / dst_name

        if must_filter(rel_path):
            continue
        source_paths.append((folder / src_name, rel_path))
    return source_paths


def render_folder(dst_path, rel_folder, **flags):
    final_path = dst_path / rel_folder
    display_path = str(rel_folder) + os.path.sep

    if str(rel_folder) == ".":
        if not flags["pretend"]:
            make_folder(final_path)
        return

    if final_path.exists():
        if not flags["quiet"]:
            printf("identical", display_path, style=STYLE_IGNORE)
        return

    if not flags["pretend"]:
        make_folder(final_path)
    if not flags["quiet"]:
        printf("create", display_path, style=STYLE_OK)


def render_file(dst_path, rel_path, source_path, render, **flags):
    """Process or copy a file of the skeleton.
    """
    if source_path.suffix == ".tmpl":
        content = render(source_path)
    else:
        content = None

    display_path = str(rel_path)
    final_path = dst_path / rel_path

    if final_path.exists():
        if file_is_identical(source_path, final_path, content):
            if not flags["quiet"]:
                printf("identical", display_path, style=STYLE_IGNORE)
            return

        if not overwrite_file(display_path, source_path, final_path, content, **flags):
            return
    else:
        if not flags["quiet"]:
            printf("create", display_path, style=STYLE_OK)

    if flags["pretend"]:
        return

    if content is None:
        copy_file(source_path, final_path)
    else:
        final_path.write_text(content)


def file_is_identical(source_path, final_path, content):
    if content is None:
        return files_are_identical(source_path, final_path)

    return file_has_this_content(final_path, content)


def files_are_identical(path1, path2):
    return filecmp.cmp(str(path1), str(path2), shallow=False)


def file_has_this_content(path, content):
    return content == path.read_text()


def overwrite_file(display_path, source_path, final_path, content, **flags):
    if not flags["quiet"]:
        printf("conflict", display_path, style=STYLE_DANGER)
    if flags["force"]:
        overwrite = True
    elif flags["skip"]:
        overwrite = False
    else:  # pragma:no cover
        msg = " Overwrite {}?".format(final_path)
        overwrite = prompt_bool(msg, default=True)

    if not flags["quiet"]:
        printf("force" if overwrite else "skip", display_path, style=STYLE_WARNING)

    return overwrite


def run_tasks(dst_path, render, tasks):
    dst_path = str(dst_path)
    for task in tasks:
        task = render.string(task)
        subprocess.run(task, shell=True, check=True, cwd=dst_path)
