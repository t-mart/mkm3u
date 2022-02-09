# mkm3u

Create an `.m3u` playlist file from files in a local directory.

I use m3u's to randomly browse my media collections when I don't know what to watch or listen to.

**Once created, all you need to do is just load it into any supporting player (which is most of
them).**

```shell
% mkm3u .\mystuff\ --output playlist.m3u8
% cat playlist.m3u8
#EXTM3U
C:\Users\tim\mystuff\video1.mkv
C:\Users\tim\mystuff\video2.mpg
```

```shell
% mkm3u --help
Usage: mkm3u [OPTIONS] [PATH]

  Create an m3u file of files in PATH.

Options:
  --recurse / --no-recurse        Recurse into subdirectories of PATH.
                                  [default: recurse]
  --suffixes COMMA-SEPARATED-LIST
                                  Only include files with suffixes from the
                                  specified comma-separated list, such as
                                  ".foo,.bar,.baz".
  --video                         Only include files with common video
                                  suffixes. This is the same as "--suffixes .d
                                  ivx,.mpeg,.webm,.mpg,.mp4,.mkv,.mov,.wmv,.fl
                                  v,.asf,.m4v,.avi,.vob". This is the default
                                  set.
  --audio                         Only include files with common audio
                                  suffixes. This is the same as "--suffixes
                                  .mp3,.ogg,.opus,.wav,.ac3,.aif,.mka".
  --image                         Only include files with common image
                                  suffixes. This is the same as "--suffixes
                                  .jpg,.jp2,.gif,.png,.svg,.jpeg".
  -o, --output PATH               Write output to a file at path instead of
                                  stdout.
  --debug / --no-debug            Show debugging information.  [default: no-
                                  debug]
  --help                          Show this message and exit.
```

## Installation

Ensure you have Python >= 3.10.

```shell
git clone https://github.com/t-mart/mkm3u.git
pip install --user mkm3u/  # or pipx, or virtualenv, or whatever
```

Then, run it with:

```shell
mkm3u
```
