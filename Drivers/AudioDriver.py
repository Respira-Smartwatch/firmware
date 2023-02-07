import pyaudio
import wave
import numpy as np
import sys
import struct


class AudioDriver:
    def __init__(self, sample_rate_hz: int = 16_000):
        self.p = pyaudio.PyAudio()
        self.device_ID = self._get_device_id()

        self.sample_rate = sample_rate_hz
        self.format = pyaudio.paInt16

    def _get_device_id(self):
        info = self.p.get_host_api_info_by_index(0)

        n_devices = info.get('deviceCount')

        for i in range(0, n_devices):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", self.p.get_device_info_by_host_api_device_index(0, i).get('name'))

                if "seeed" in self.p.get_device_info_by_host_api_device_index(0, i).get('name'):
                    return i

            else:
                print("Output Device id ", i, " - ", self.p.get_device_info_by_host_api_device_index(0, i).get('name'))

        return -1
    
    def __capture(self, length: float = 5.0):
        stream = self.p.open(
                rate=self.sample_rate,
                format=self.format,
                channels=2,
                input=True,
                input_device_index=self.device_ID
                )

        print(f"* Recording {length}s")
        frames = []

        for i in range(int(self.sample_rate / 1024 * length)):
            data = stream.read(1024, exception_on_overflow=False)
            a = np.fromstring(data,dtype=np.int16)[0::2]
            frames.append(a.tostring())

        print("* Done")
        stream.stop_stream()
        stream.close()

        return frames

    def record(self, outfile: str = "output.wav", length: float = 5.0):
        frames = self.__capture(length)

        wf = wave.open(outfile, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    # simplified method to call record for mono mode
    def get_sample(self, length: float = 5.0):
        frames = self.__capture(length)
        frames = b''.join(frames)

        n_ints = int(len(frames) / 2)
        int_data = struct.unpack(f"{n_ints * 'h'}", frames)

        float_data = np.zeros(n_ints)
        for i, num in enumerate(int_data):
            float_val = num / 32768.0
            float_data[i] = float_val

        return float_data

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
