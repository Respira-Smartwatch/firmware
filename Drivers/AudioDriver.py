import pyaudio
import wave
import numpy as np
import sys
import struct


class AudioDriver:
    def __init__(self, sample_rate_hz: int = 16_000, n_mics: int = 1):
        # One stereo mic is considered a single channel
        self.byte_order = sys.byteorder
        self.channels = n_mics
        self.sample_rate = sample_rate_hz
        self.p = pyaudio.PyAudio()
        self.device_ID = self._get_device_id()

    def _get_device_id(self):
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        for i in range(0, numdevices):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                if 'seeed' in self.p.get_device_info_by_host_api_device_index(0, i).get('name'):
                    return i
            else:
                print(f"Output Device id {i} - {self.p.get_device_info_by_host_api_device_index(0, i).get('name')}")

    #   @brief: internal function that handles the recording function
    #   @params:    outfile: string to store the output filename
    #               fs: Sampling rate of the file - default 16000Hz
    #               length: length (in seconds) of the sample recording
    #               stereo: True if recording with both channels, false if mono
    #               mono_channel: channel to select if recording mono
    #               chunk:  size of the recording chunks
    #               w:      width of the respeaker?
    #   @retval:    None
    def __capture(self, length: float = 5.0, stereo: bool = False):
        mono_channel = 0
        chunk_size = 1024
        window = 2
        # stream_format = self.p.get_format_from_width(1)
        stream_format = pyaudio.paFloat32

        stream = self.p.open(rate=self.sample_rate, format=stream_format, channels=self.channels, input=True,
                             input_device_index=self.device_ID)

        print(f"* Recording {length}s of audio...")
        frames = []
        for i in range(0, int(self.sample_rate / chunk_size * length)):
            data = stream.read(chunk_size)

            if stereo:
                data = np.frombuffer(data, dtype=np.int16)[mono_channel::2].tobytes()

            frames.append(data)

        print("* Done recording")
        stream.stop_stream()
        stream.close()
        return frames

    def record(self, outfile: str = "output.wav", length: float = 5.0, stereo: bool = False):
        frames = self.__capture(length, stereo)

        wf = wave.open(outfile, 'wb')
        wf.setnchannels(2 if stereo else 1)
        wf.setsampwidth(self.p.get_sample_size(self.p.get_format_from_width(2)))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    # simplified method to call record for mono mode
    def get_sample(self, length: float = 5.0):
        frames = self.__capture(length)
        frames = b''.join(frames)

        n_floats = int(len(frames) / 4)
        data = struct.unpack(f"{n_floats}f", frames)
        return np.array(data)

    def play(self, infile: str, chunk: int = 1024):
        wf = wave.open(infile, 'rb')

        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                             channels=wf.getnchannels(),
                             rate=wf.getframerate(),
                             output=True,
                             output_device_index=self.device_ID)

        data = wf.readframes(chunk)

        while data:
            stream.write(data)
            data = wf.readframes(chunk)

        stream.close()

    # cleanup the pyaudio instance
    def __del__(self):
        self.p.terminate()
