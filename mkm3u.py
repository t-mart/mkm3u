"""Creates m3u files """
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Optional

import click

VIDEO_SUFFIXES = {
    ".mkv",
    ".mp4",
    ".avi",
    ".webm",
    ".wmv",
    ".mpg",
    ".flv",
    ".vob",
    ".divx",
    ".asf",
    ".mov",
    ".mpeg",
    ".m4v",
}

IMAGE_SUFFIXES = {
    ".jpg",
    ".png",
    ".jpeg",
    ".svg",
    ".jp2",
    ".gif",
}

AUDIO_SUFFIXES = {
    ".opus",
    ".mp3",
    ".wav",
    ".mka",
    ".ogg",
    ".ac3",
    ".aif",
}


class CommaSeparatedSetParamType(click.ParamType):
    """Click type that converts a comma-separated string into a set"""

    name = "comma-separated-list"

    def convert(
        self, value: Any, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> set[str]:
        if isinstance(value, set) and all(isinstance(item, str) for item in value):
            return value

        if isinstance(value, str):
            return set(value.split(","))

        self.fail(f"{value!r} cannot be made into a set of str types", param, ctx)


COMMA_SEPARATED_SET_PARAM_TYPE = CommaSeparatedSetParamType()


class PathParamType(click.ParamType):
    """Click type that converts a string into a path"""

    name = "path"

    def convert(
        self, value: Any, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> Path:
        if isinstance(value, Path):
            return value

        try:
            return Path(value)
        except Exception as exc:  # pylint: disable=broad-except
            self.fail(f"{value!r} cannot be made into a path: {exc}", param, ctx)


PATH_PARAM_TYPE = PathParamType()


class DirPathParamType(PathParamType):
    """
    Click type that converts a string into an existing directory path.
    """

    name = "dir-path"

    def convert(
        self, value: Any, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> Path:
        path = super().convert(value, param, ctx)

        if not path.is_dir():
            self.fail(f"{value!r} is not a directory", param, ctx)

        return path


DIR_PATH_PARAM_TYPE = DirPathParamType()


def yield_files(path: Path, suffixes: set[str], recurse: bool) -> Iterable[Path]:
    """
    Yields file paths from path (recursively if recurse) if their suffix is in suffixes.
    """
    for subpath in path.iterdir():
        if subpath.is_file() and subpath.suffix in suffixes:
            yield subpath
        elif subpath.is_dir() and recurse:
            yield from yield_files(subpath, suffixes, True)


@click.command()
@click.option(
    "--recurse/--no-recurse",
    default=True,
    help="Recurse into subdirectories of PATH.",
    show_default=True,
)
@click.option(
    "--suffixes",
    type=COMMA_SEPARATED_SET_PARAM_TYPE,
    help=(
        "Only include files with suffixes from the specified comma-separated list, "
        'such as ".foo,.bar,.baz".'
    ),
)
@click.option(
    "--video",
    "suffixes",
    flag_value=VIDEO_SUFFIXES,
    type=COMMA_SEPARATED_SET_PARAM_TYPE,
    default=True,
    help=(
        "Only include files with common video suffixes. This is the same as "
        f"\"--suffixes {','.join(VIDEO_SUFFIXES)}\". This is the default set."
    ),
)
@click.option(
    "--audio",
    "suffixes",
    flag_value=AUDIO_SUFFIXES,
    type=COMMA_SEPARATED_SET_PARAM_TYPE,
    help=(
        "Only include files with common audio suffixes. This is the same as "
        f"\"--suffixes {','.join(AUDIO_SUFFIXES)}\"."
    ),
)
@click.option(
    "--image",
    "suffixes",
    flag_value=IMAGE_SUFFIXES,
    type=COMMA_SEPARATED_SET_PARAM_TYPE,
    help=(
        "Only include files with common image suffixes. This is the same as "
        f"\"--suffixes {','.join(IMAGE_SUFFIXES)}\"."
    ),
)
@click.option(
    "-o",
    "--output",
    "output_path",
    type=PATH_PARAM_TYPE,
    help="Write output to a file at path instead of stdout.",
    show_default=True,
    default=None,
)
@click.option(
    "--debug/--no-debug",
    default=False,
    help="Show debugging information.",
    show_default=True,
)
@click.argument("PATH", type=DIR_PATH_PARAM_TYPE, default=Path("."))
def main(
    path: Path,
    recurse: bool,
    suffixes: set[str],
    output_path: Optional[Path],
    debug: bool,
) -> None:
    """Create an m3u file of files in PATH."""
    if output_path is None:
        output_file = sys.stdout
        output_desc = "on stdout"
    else:
        output_file = output_path.open("w")
        output_desc = f"at {output_path.absolute()}"

    if debug:
        print(
            f"Creating an m3u {output_desc} of files from {path.absolute()} "
            f"{'(recursively) ' if recurse else ''}with suffixes "
            f"{suffixes}.",
            file=sys.stderr,
        )

    output_file.write("#EXTM3U\n")
    for media_file_path in yield_files(path, suffixes, recurse):
        output_file.write(str(media_file_path.absolute()) + "\n")

    output_file.close()


if __name__ == "__main__":
    main.main()
