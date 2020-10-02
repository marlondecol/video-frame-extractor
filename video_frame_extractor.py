from argparse import ArgumentParser

from datetime import datetime

from imutils import is_cv2

from os import W_OK, access, mkdir, path

from threading import Thread

import cv2

from modules.formatter.formatter import Formatter as F

from modules.utils.utils import (_l, _lt, ellipsis, error, header,
                                 humanize_duration, info, press_enter_to,
                                 success, warning)


def can_extract_at(index: int) -> bool:
    """
    Check whether to extract the image from a frame at `index`.

    ---
    Arguments
    ---

        index (int)
    The current frame index.

    ---
    Returns
    ---

        bool
    True if the image from the frame can be extracted.
    """

    # Use the user inputs.
    global extraction_rate, offset

    return index >= offset and (index % extraction_rate) + offset == (
        offset % extraction_rate) + offset


def print_video_information() -> None:
    """
    Print some information about the video file.
    """

    # Use the global variables.
    global FRAMES, FPS, WIDTH, HEIGHT, VIDEO_STREAM

    # Use the user input variables.
    global video_file, extraction_rate, offset, output_dir

    print(_l('{} {}'.format(info('Input video:'), video_file)))

    # Try to determine some information about the video file.
    try:

        # Get the total number of frames.
        FRAMES = int(
            VIDEO_STREAM.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT if is_cv2(
            ) else cv2.CAP_PROP_FRAME_COUNT))

        # Get the frame rate.
        FPS = float(
            VIDEO_STREAM.get(
                cv2.cv.CV_CAP_PROP_FPS if is_cv2() else cv2.CAP_PROP_FPS))

        # Get the frames width.
        WIDTH = int(
            VIDEO_STREAM.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH if is_cv2(
            ) else cv2.CAP_PROP_FRAME_WIDTH))

        # Get the frames height.
        HEIGHT = int(
            VIDEO_STREAM.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT if is_cv2(
            ) else cv2.CAP_PROP_FRAME_HEIGHT))

        # Print these information.
        print(
            _lt('{} {}'.format(info('Duration:'),
                               humanize_duration(FRAMES / FPS))))

        print(_lt('{} {}'.format(info('Total of frames:'), FRAMES)))
        print(_l('{} {}'.format(info('Frame rate (FPS):'), FPS)))

        print(_lt('{} {}x{}'.format(info('Resolution:'), WIDTH, HEIGHT)))

    # An error occurred while trying to determine some information about the
    # video.
    except:
        print(
            _lt(warning(
                'Could not determine any information about the video!')))

    # Show the extraction rate, if already defined.
    if extraction_rate is not None:
        print(
            _lt('{} {}'.format(F().bold().magenta('Extraction frame rate:'),
                               extraction_rate)))

        # Show the offset, if already defined.
        if offset is not None:
            print(
                _l('{} {}'.format(F().bold().magenta('Frame offset:'),
                                  offset)))

            # Show the output path, if already defined.
            if output_dir is not None:
                print(
                    _lt('{} {}'.format(F().bold().magenta('Output folder:'),
                                       output_dir)))


# Construct the arguments parser and parse them.
parser = ArgumentParser(
    description='Extracts frames from an input video and exports them to images'
)

parser.add_argument('-i', '--input', help='path to the input video file')

parser.add_argument('-r',
                    '--extraction-rate',
                    type=int,
                    help='extraction frame rate')

parser.add_argument('-o', '--offset', type=int, help='frame offset')

parser.add_argument('-C',
                    '--output',
                    nargs='?',
                    const='',
                    help='output path for image files')

args = vars(parser.parse_args())

# Store the arguments values in temporary variables.
_video_file = args['input']
_extraction_rate = args['extraction_rate']
_offset = args['offset']
_output_dir = args['output']

# User input variables.
video_file = extraction_rate = offset = output_dir = None

# Global variables.
FRAMES = FPS = WIDTH = HEIGHT = 0

# Initialize the video stream variable.
VIDEO_STREAM = None

try:
    input_message = _l(F().bold().cyan('Input video: '))

    while True:
        print(F().blue(header()))

        if _video_file is None:

            # Let the user set the input video file.
            _video_file = input(input_message)
        else:

            # Print in case of passing by argument.
            print('{}{}'.format(input_message, _video_file))

        # Invalid input.
        if not _video_file:
            print(_lt(error('Invalid input!')))
            press_enter_to('try again', F().red(), F().white())

            _video_file = None

            continue

        # Input is not a file.
        if not path.isfile(_video_file):
            print(_lt(error('The input path is not a valid file!')))
            press_enter_to('try again', F().red(), F().white())

            _video_file = None

            continue

        print(F().blue(header()))

        # Get the file absolute path.
        _video_file = path.abspath(_video_file)

        print(_l('{} {}'.format(info('Input video:'), _video_file)))

        # Set the video stream and pointer to the input video file.
        VIDEO_STREAM = cv2.VideoCapture(_video_file)

        # Check whether the video file is valid.
        if not VIDEO_STREAM.isOpened():
            print(_lt(error('The input file is not a valid video file!')))
            press_enter_to('try again', F().red(), F().white())

            _video_file = None

            continue

        video_file = _video_file

        break

    input_message = _lt(F().bold().cyan('Extraction frame rate: '))

    while True:
        print(F().blue(header()))
        print_video_information()

        try:
            if _extraction_rate is None:

                # Let the user set the extraction rate.
                _extraction_rate = int(input(input_message))
            else:

                # Print in case of passing by argument.
                print('{}{}'.format(input_message, _extraction_rate))

            # Check whether the value is valid.
            if _extraction_rate < 1:
                print(_lt(error('This value must be greater than zero!')))
                press_enter_to('try again', F().red(), F().white())

                _extraction_rate = None

                continue

        # Invalid value.
        except ValueError:
            print(_lt(error('Invalid value!')))
            press_enter_to('try again', F().red(), F().white())

            _extraction_rate = None

            continue

        extraction_rate = _extraction_rate

        break

    input_message = _l(F().bold().cyan('Frame offset: '))

    while True:
        print(F().blue(header()))
        print_video_information()

        try:
            if _offset is None:

                # Let the user set the offset.
                _offset = int(input(input_message))
            else:

                # Print in case of passing by argument.
                print('{}{}'.format(input_message, _offset))

            # Check whether the value is positive.
            if _offset < 0:
                print(_lt(error('This value must be positive!')))
                press_enter_to('try again', F().red(), F().white())

                _offset = None

                continue

            # Check whether the value is lower than the total of frames.
            if _offset >= FRAMES:
                print(
                    _lt(
                        error('This value must be lower than {}!'.format(
                            FRAMES))))
                press_enter_to('try again', F().red(), F().white())

                _offset = None

                continue

        # Invalid value.
        except ValueError:
            print(_lt(error('Invalid value!')))
            press_enter_to('try again', F().red(), F().white())

            _offset = None

            continue

        offset = _offset

        break

    input_message = _lt(F().bold().cyan('Output folder (optional): '))

    while True:
        print(F().blue(header()))
        print_video_information()

        try:
            if _output_dir is None:

                # Let the user set the output folder.
                _output_dir = input(input_message)
            else:

                # Print in case of passing by argument.
                print('{}{}'.format(input_message, _output_dir))

            # If the user didn't pass any path,...
            if not _output_dir:

                # ... use the input video filename without its extension.
                _output_dir = path.splitext(video_file)[0] + '_images'

            # Check whether the folder exists and the user has write permission.
            if path.isdir(_output_dir) and not access(_output_dir, W_OK):
                raise PermissionError()

            # Try to make the folder.
            mkdir(_output_dir)

        # Ignore if the folder already exists.
        except FileExistsError:
            pass

        # The user doesn't have write permission.
        except PermissionError:
            print(_lt(error('Write permission denied!')))
            press_enter_to('try again', F().red(), F().white())

            _output_dir = None

            continue

        # Get the output folder absolute path.
        output_dir = path.abspath(_output_dir)

        break

    print(F().blue(header()))
    print_video_information()
    print()

    # Start a counter for all frames read.
    frame_index = -1

    # Total of extracted frames.
    extracted_frames = 0

    # Initialize the feedback animation thread variable.
    thread = None

    # Initial time to count elapsed time.
    start_time = datetime.now()

    # Loop over frames from the video file stream.
    while True:

        # Read the next frame from the video file.
        grabbed, frame = VIDEO_STREAM.read()

        # If it isn't successful, it has reached the end of the stream.
        if not grabbed:
            break

        frame_index += 1

        # Check whether to extract the image from the frame.
        if not can_extract_at(frame_index):
            continue

        # Get the current frame time.
        current_time = (1 / FPS) * frame_index

        # If there's a thread running,...
        if thread is not None:

            # ... stop it to run it again.
            thread.alive = False

        # Show the current extracting frame...
        thread = Thread(target=ellipsis,
                        args=(_l('Extracting frame {} at {} (# {})'.format(
                            extracted_frames + 1,
                            humanize_duration(current_time),
                            frame_index)), F().bold().blue()),
                        daemon=True)

        # ... and start the feedback animation.
        thread.start()

        # Get hours.
        hours = int(current_time // 3600)
        current_time %= 3600

        # Get minutes.
        minutes = int(current_time // 60)
        current_time %= 60

        # Get seconds.
        seconds = int(current_time)

        # Get milliseconds.
        milliseconds = int((current_time - seconds) * 1000)

        # Save the current frame as a JPEG image.
        cv2.imwrite(
            '{}/{}_{}_{}_{:02d}_{:02d}_{:02d}_{:03d}.jpg'.format(
                output_dir,
                path.splitext(path.split(video_file)[1])[0], extracted_frames,
                frame_index, hours, minutes, seconds, milliseconds), frame)

        extracted_frames += 1

    # Final time.
    end_time = datetime.now()

    # If there was a thread running,...
    if thread is not None:

        # ... stop it.
        thread.alive = False

    # Calculates the total process time.
    total_time = end_time - start_time

    print(F().blue(header()))
    print_video_information()

    print(_lt(success('Success!')))

    print(_lt('{} {}'.format(info('Extracted frames:'), extracted_frames)))
    print(
        _l('{} {}\n'.format(info('Elapsed time:'),
                            humanize_duration(total_time.total_seconds()))))

# Ctrl+C pressed.
except (EOFError, KeyboardInterrupt):

    # If there was a thread running,...
    if 'thread' in locals() and thread is not None:

        # ... stop it.
        thread.alive = False

    print(_lt(_lt(error('Operation canceled by the user!'))))
    press_enter_to('quit', F().red(), F().white())

    print()

    pass
