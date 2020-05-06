# Package imports
import os
import subprocess
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import matplotlib.cbook as cbook
from matplotlib import gridspec
import ffmpeg
# Local imports
from saturn.common import audio


def create_animation(wave_file, image_file, title=None, fps=30, dpi=200):
    """
        Create animation provided wave file and image

        Args:
            wave_file (werkzeug.datastructures.FileStorage): audio file
            image_file (werkzeug.datastructures.FileStorage): image file
            title (str): title for video animation
            fps (int): frames per second
            dpi (int): dots per inch, controls movie size

        Returns:
            None
    """
    # Write audio file to wav
    wave_file.save('audio.wav')
    # Initialize waveform instance
    waveform = audio.read_wave('audio.wav')
    # Setup frame duration based on frames per second
    frame_duration = 1 / fps
    starting_points = np.arange(0, waveform.duration, frame_duration)
    image = plt.imread(image_file)
    # --- Create animation ---
    # Setup plot
    fig = plt.figure(figsize=(6, 4))
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
    ax1 = plt.subplot(gs[0])
    ax = plt.subplot(gs[1])
    # Plot image on first axis
    im = ax1.imshow(image)
    # Remove border and tickets 
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.get_xaxis().set_ticks([])
    ax1.get_yaxis().set_ticks([])
    # Set title
    print("Title: ", title)
    if title is not None:
        ax1.set_xlabel(title, fontname='sans-serif', fontsize=14)
    # Setup limits
    ax.set_ylim(-1, 10)
    ax.set_xlim(20, 10000)
    # Setup initial frame
    segment = waveform.segment(0, frame_duration)
    spectrum = segment.make_spectrum()
    fs = spectrum.fs
    amps = np.abs(spectrum.hs)
    line, = ax.semilogx(fs, amps, '-', color='black', lw=2)
    # Remove borders and ticks
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_ticks([], [])
    ax.get_yaxis().set_ticks([], [])
    ax.xaxis.set_ticks_position('none') 

    def animation_frame(i):
        start = starting_points[i]
        segment = waveform.segment(start, frame_duration)
        spectrum = segment.make_spectrum()
        fs = spectrum.fs
        amps = np.abs(spectrum.hs)
        # Smooth amplitudes
        #amps = gaussian_filter1d(amps, sigma=3, order=2)
        amps = gaussian_filter1d(np.cbrt(amps), sigma=3, order=0)
        line.set_ydata(amps)
        
        return line,

    # Create line animation
    line_animation = FuncAnimation(
        fig, func=animation_frame, interval=1000 / fps,
        frames=np.arange(0, len(starting_points) - 1), blit=True)
    # Set up formatting for the movie files
    Writer = animation.writers['ffmpeg'](fps=fps)
    line_animation.save('animation.mp4', writer=Writer, dpi=dpi)
    # Join the audio file to the mp4 file using ffmpeg
    input_audio = ffmpeg.input('audio.wav')
    input_video = ffmpeg.input('animation.mp4')
    ffmpeg.output(
        input_audio.audio,
        input_video.video,
        "output.mp4",
        vcodec="copy",
        acodec="aac"
    ).overwrite_output().run()

    return

