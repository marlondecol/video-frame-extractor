<p align="center">
    <img alt="VFEx logo" src="https://raw.githubusercontent.com/mlc2307/video-frame-extractor/assets/logo.svg" width="520">
</p>

<br>

<p align="center">
    <a href="#overview">Overview</a>
    &nbsp;&bull;&nbsp;
    <a href="#getting-started">Getting started</a>
    &nbsp;&bull;&nbsp;
    <a href="#how-to-use">How to use</a>
    &nbsp;&bull;&nbsp;
    <a href="#license">License</a>
</p>

<p align="center">
    <a href="requirements.txt"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/opencv-python"></a>
    <a href="LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/mlc2307/video-frame-extractor"></a>
</p>

<br>

# Video Frame Extractor

This Python software allows you to extract certain frames from a video file and then save them as image files.

This tool is useful when you want to create a training dataset for image localization and object detection, for example, which must be identified manually, frame by frame.

## Overview

The application's workflow consists of entering a video file, defining some extraction parameters and, if necessary, defining the output directory.

The software then starts to scan through the video frames, extract the ones that fit the established conditions and then save them. For this process, some features of the [`opencv-python`][opencv] package are used.

<br>

<p align="center">
    <img alt="Application's workflow" src="https://raw.githubusercontent.com/mlc2307/video-frame-extractor/assets/workflow.svg" width="480">
</p>

<br>

After the process is finished, the images must be available in the output directory previously defined.

## Getting started

This step consists of [cloning this repository](#cloning-the-repository) on your computer and, soon after, [installing the required Python packages](#installing-python-packages).

### Prerequisites

Before proceeding, make sure this is installed:

- A version of `python` 3, the newer the better, including PyPI. During development, version [3.7.9][python-v3.7.9] was used.
- And `git`, the newer version the better.

For the following steps, it is *strongly* recommended to use a Python virtual environment, such as [venv][venv] or [virtualenv][virtualenv].

### Cloning the repository

Since this project has a sub-module included, the [Python Formatter][formatter], you must clone it recursively by running the following command in a terminal:

```bash
git clone --recurse-submodules https://github.com/mlc2307/video-frame-extractor.git
```

If you want to know more about `git submodules`, it is worth checking out the [book][submodules-book] or [reference][submodules-reference] in the official [Git documentation][git-docs].

### Installing Python packages

In the newly cloned repository directory, run the command below to install the Python packages defined in the file [`requirements.txt`](requirements.txt) in your environment:

```bash
pip install --upgrade -r requirements.txt
```

After installing the packages, the setup is ready and you can proceed to the next step.

## How to use

To use the tool, just run the [`video_frame_extractor.py`](video_frame_extractor.py) file with Python, as in the following example:

```bash
python video_frame_extractor.py
```

The application will first ask for the location of the input video file. As soon as you define it, some attributes of the video will be listed, such as resolution, frame rate, etc.

Then you must define the extraction parameters, which can be defined more clearly due to the listed attributes and are as follows:

- *Extraction rate* `extraction_rate`, where `0 < extraction_rate` &ndash; The frame interval between one extracted frame and another. For example: assuming there is no offset, if the extraction rate is equal to 5, frames 0, 5, 10, 15, ... will be extracted; if it is equal to 1, all frames will be extracted.
- *Offset* `offset`, where `0 <= offset < frames_number`, for `frames_number` being the total number of frames &ndash; Shifts the start of the extraction, that is, it defines the index of the first frame to be extracted.

<br>

<p align="center">
    <img alt="Extraction parameters examples" src="https://raw.githubusercontent.com/mlc2307/video-frame-extractor/assets/examples.svg" width="640">
</p>

<br>

Optionally, you can also define the location of the image output directory. If you do not define it, the software will create a folder in the same directory as the video file, with the same name, without the extension, and with the suffix `_images`. For example: if the video name is `path/to/video-file.mp4`, the output directory will be `path/to/video-file_images`.

After all this, the extraction process will begin. When finished, if there were no errors, the images in `.jpg` format must be available in the defined output directory, which must have the same resolution as the input video.

It is worth remembering that you can stop the execution at any time by pressing <kbd>Ctrl</kbd>+<kbd>C</kbd>.

### Command line arguments

This application also provides some command line arguments during its execution, allowing you to directly assign the variables and parameters already mentioned, according to your needs.

The command syntax is as follows:

```bash
python video_frame_extractor.py [-h] [-i INPUT] [-r EXTRACTION_RATE]
                                [-o OFFSET] [-C [OUTPUT]]
```

And the arguments are as follows:

| Argument                 |      Optional      |        Type        |     Allow empty    | Description                  |
|--------------------------|:------------------:|:------------------:|:------------------:|------------------------------|
| `-h` `--help`            | :heavy_check_mark: | :heavy_minus_sign: |                    | Show a help message and exit |
| `-i` `--input`           | :heavy_check_mark: |       String       |                    | Path to the input video file |
| `-r` `--extraction-rate` | :heavy_check_mark: |      Integer       |                    | Extraction frame rate        |
| `-o` `--offset`          | :heavy_check_mark: |      Integer       |                    | Frame offset                 |
| `-C` `--output`          | :heavy_check_mark: |       String       | :heavy_check_mark: | Output path for image files  |

It is also possible to define only a few parameters using these arguments and the others during execution.

## License

This software is available under the [MIT license](LICENSE).

<!-- Links -->

[formatter]:https://github.com/mlc2307/python-formatter
[git-docs]:https://git-scm.com/doc
[opencv]:https://pypi.org/project/opencv-python
[python-v3.7.9]:https://www.python.org/downloads/release/python-379
[submodules-book]:https://www.git-scm.com/book/en/v2/Git-Tools-Submodules
[submodules-reference]:https://git-scm.com/docs/git-submodule
[venv]:https://docs.python.org/pt-br/dev/library/venv.html
[virtualenv]:https://virtualenv.pypa.io