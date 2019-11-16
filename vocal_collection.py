"""
    the class for collecting the vocal
"""
import pyaudio
import wave
import time
import threading

class Recorder:
    """
        the class for recoder
    """

    def __init__(self, chunk=256, channels=1, rate=11025, save_path="sample.wav"):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []
        self.save_path = save_path

    def start(self):
        """

        :return:
        """
        threading._start_new_thread(self.__recording, ())

    def __recording(self):
        self._running = True
        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        while self._running:
            data = stream.read(self.CHUNK)
            self._frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop(self):
        """

        :return:
        """
        self._running = False
        self.save(self.save_path)

    def save(self, filename):
        """

        :param filename:
        :return:
        """
        p = pyaudio.PyAudio()
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()
        # print("Saved")


if __name__ == "__main__":
        rec = Recorder()
        begin = time.time()
        rec.start()
        rec.stop()
        fina = time.time()
        t = fina - begin
        print('录音时间为%ds' % t)
        rec.save("1_%y.wav")
