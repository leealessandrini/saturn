import wave
import numpy as np


def read_wave(filename):
    """
        Reads a wave file.

        Args:
            filename: string

        Returns:
            wave object
    """
    # Open wav file
    fp = wave.open(filename, "rb")
    # Get wav file parameters
    nchannels = fp.getnchannels()
    nframes = fp.getnframes()
    sampwidth = fp.getsampwidth()
    framerate = fp.getframerate()
    # Read frames and close file
    z_str = fp.readframes(nframes)
    fp.close()
    # Convert binary string to integer array
    dtype_map = {1: np.int8, 2: np.int16, 3: "special", 4: np.int32}
    if sampwidth not in dtype_map:
        raise ValueError("sampwidth %d unknown" % sampwidth)
    if sampwidth == 3:
        xs = np.fromstring(z_str, dtype=np.int8).astype(np.int32)
        ys = (xs[2::3] * 256 + xs[1::3]) * 256 + xs[0::3]
    else:
        ys = np.fromstring(z_str, dtype=dtype_map[sampwidth])
    # If it's in stereo pull out the first channel
    if nchannels == 2:
        ys = ys[::2]
    # Create Waveform instance, normalize to amplitude of 1 and return
    waveform = Waveform(ys, framerate=framerate)
    waveform.normalize()

    return waveform


def normalize(ys, amp=1.0):
    """
        Normalizes a wave array so the maximum amplitude is +amp or -amp.

        Args:
            ys: wave array
            amp: max amplitude (pos or neg) in result

        Returns:
            wave array
    """
    high, low = abs(max(ys)), abs(min(ys))

    return amp * ys / max(high, low)


def find_index(x, xs):
    """
        Find the index corresponding to a given value in an array.
    """
    n = len(xs)
    start = xs[0]
    end = xs[-1]
    i = round((n - 1) * (x - start) / (end - start))

    return int(i)


class Waveform:
    """
        Represents a discrete-time waveform.
    """

    def __init__(self, ys, ts=None, framerate=None):
        """
            Initializes the wave.

            Args:
                ys: wave array
                ts: array of times
                framerate: samples per second
        """
        # Setup waveform array and framerate
        self.ys = np.asanyarray(ys)
        self.framerate = framerate if framerate is not None else 11025
        # Setup time array and time duration
        if ts is None:
            self.ts = np.arange(len(ys)) / self.framerate
        else:
            self.ts = np.asanyarray(ts)
        self.duration = max(self.ts)

    def __len__(self):
        return len(self.ys)

    @property
    def start(self):
        return self.ts[0]

    @property
    def end(self):
        return self.ts[-1]

    def segment(self, start=None, duration=None):
        """
            Extracts a segment.

            Args:
                start: float start time in seconds
                duration: float duration in seconds

            Returns:
                Wave
        """
        if start is None:
            start = self.ts[0]
            i = 0
        else:
            i = self.find_index(start)

        j = None if duration is None else self.find_index(start + duration)

        return self.slice(i, j)

    def normalize(self, amp=1.0):
        """
            Normalizes the signal to the given amplitude.

            Args:
                amp: float amplitude
        """
        self.ys = normalize(self.ys, amp=amp)

    def slice(self, i, j):
        """
            Makes a slice from a Wave.

            Args:
                i: first slice index
                j: second slice index

            Returns:
                waveform instance of slice
        """
        ys = self.ys[i:j].copy()
        ts = self.ts[i:j].copy()

        return Waveform(ys, ts, self.framerate)

    def make_spectrum(self, full=False):
        """
            Computes the spectrum using FFT.

            Args:
                full: boolean, whethere to compute a full FFT
                      (as opposed to a real FFT)

            Returns: Spectrum
        """
        n = len(self.ys)
        d = 1 / self.framerate

        if full:
            hs = np.fft.fft(self.ys)
            fs = np.fft.fftfreq(n, d)
        else:
            hs = np.fft.rfft(self.ys)
            fs = np.fft.rfftfreq(n, d)

        return Spectrum(hs, fs, self.framerate, full)

    def find_index(self, t):
        """Find the index corresponding to a given time."""
        n = len(self)
        start = self.start
        end = self.end
        i = round((n - 1) * (t - start) / (end - start))
        return int(i)


class Spectrum:
    """
        Waveform signal spectrum.
    """

    def __init__(self, hs, fs, framerate, full=False):
        """
            Initializes a spectrum.

            Args:
                hs: array of amplitudes (real or complex)
                fs: array of frequencies
                framerate: frames per second
                full: boolean to indicate full or real FFT
        """
        self.hs = np.asanyarray(hs)
        self.fs = np.asanyarray(fs)
        self.framerate = framerate
        self.full = full

    def render_full(self, high=None):
        """
            Extracts amps and fs from a full spectrum.

            Args:
                high: cutoff frequency

            Returns: fs, amps
        """
        hs = np.fft.fftshift(self.hs)
        amps = np.abs(hs)
        fs = np.fft.fftshift(self.fs)
        i = 0 if high is None else find_index(-high, fs)
        j = None if high is None else find_index(high, fs) + 1

        return fs[i:j], amps[i:j]
