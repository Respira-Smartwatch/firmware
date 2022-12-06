import pyaudio
import wave
import numpy as np

class Mics:

    def __init__(self):

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
                print(f"Output Device id {i} - {self.p.get_device_info_by_host_api_device_index(0,i).get('name')}")


    #   @breif: internal function that handles the recording function
    #   @params:    outfile: string to store the output filename
    #               fs: Sampling rate of the file - default 16000Hz
    #               length: length (in seconds) of the sample recording
    #               stereo: True if recording with both channels, false if mono
    #               mono_channel: channel to select if recording mono
    #               chunk:  size of the recording chunks
    #               w:      width of the respeaker?
    #   @retval:    None
    def _record(self, outfile: str = "output.wav", 
                     fs: int = 16000, 
                     length: float = 5.0,
                     stereo: bool = True, 
                     mono_channel: int=0,
                     chunk: int = 1024, 
                     w: int = 2):

        stream = self.p.open(rate = fs,
                             format=self.p.get_format_from_width(w),
                             channels=2,
                             input=True,
                             input_device_index=self.device_ID)

        print("* recording")

        frames = []

        if stereo:
            for i in range(0, int(fs / chunk*length)):
                data = stream.read(chunk)
                frames.append(data)

        else:
            for i in range(0, int(fs / chunk*length)):
                data = stream.read(chunk)
                a = np.frombuffer(data, dtype=np.int16)[mono_channel::2]
                frames.append(a.tobytes())


        print("* done recording")

        stream.stop_stream()
        stream.close()

        wf = wave.open(outfile, 'wb')
        wf.setnchannels(2 if stereo else 1)
        wf.setsampwidth(self.p.get_sample_size(self.p.get_format_from_width(w)))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

    # Will return instantaneous samples
    def record_single(self):
        pass

    # simplified method to call record for stereo mode
    def record_stereo(self, outfile: str="output.wav", length: float=5.0, fs: int=16000):
        self._record(outfile=outfile, length=length, fs=fs, stereo=True)

    # simplified method to call record for mono mode
    def record_mono(self, outfile: str="output.wav", length: float=5.0, fs: int=16000):
        self._record(outfile=outfile, length=length, fs=fs, stereo=False)

    def play(self, infile: str, chunk: int=1024):
        wf = wave.open(infile, 'rb')

        stream = self.p.open(format = self.p.get_format_from_width(wf.getsampwidth()),
                             channels = wf.getnchannels(),
                             rate = wf.getframerate(),
                             output = True,
                             output_device_index = self.device_ID)

        data = wf.readframes(chunk)

        while data:
            stream.write(data)
            data = wf.readframes(chunk)

        stream.close()

    # cleanup the pyaudio instance
    def cleanup(self):
        self.p.terminate()






if __name__ == "__main__":
    m = Mics()
    m.record_stereo(outfile="test.wav")
    m.play(infile="test.wav")
    m.cleanup()
