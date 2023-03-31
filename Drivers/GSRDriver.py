import smbus
import time

_DEBUG = True


class GSRDriver:
    def __init__(self, f_s=256):
        self.channel = 1
        self.address = 0x8
        self.bus = smbus.SMBus(self.channel)
        self.sample_rate = f_s

        if not self._connect():
            print("NO Device Found / Connection Error")
            exit(1)

    def _connect(self):
        try:
            return self.bus.read_byte_data(self.address, 1)
        except:
            return 0

    def read_once(self):
        try:
            return self.bus.read_byte_data(self.address, 1)
        except OSError:
            return None
    
    def tick(self):
        t = time.time()
        while True:
            t += 1/self.sample_rate
            yield max(t-time.time(), 0)

    def get_sample(self, seconds=1):
        g = self.tick()
        sample = []
        i = 0
        while i < (self.sample_rate * seconds):
            time.sleep(next(g))
            s = self.read_once()
            if type(s) == None:
                if _DEBUG:
                    print(f"SAMPLE ERROR {s}") 
                s = sample[i-1]
            sample += s,
            i += 1
        if _DEBUG:
            print("******* GSR DRIVER DEBUG: *******")
            print(f" Sample raw data: {sample}")
            print(f" Sample Len: {len(sample)}")
            print("*********************************")

        return sample

if __name__ == "__main__":
    gsr = GSRDriver()
    errors = 0
    number_tests=1000
    s_time = time.perf_counter()
    for i in range(number_tests):
        n = gsr.read_once()
        if n == -25:
            errors += 1
    e_time = time.perf_counter()
    t = (e_time - s_time)/number_tests

    s_time2 = time.perf_counter()
    x = gsr.get_sample()
    e_time2 = time.perf_counter()
    t2 = (e_time2 - s_time2)/gsr.sample_rate

    #s_time3 = time.perf_counter()
    #x1 = gsr.get_sample2()
    #e_time3 = time.perf_counter()
    #t3 = (e_time3 - s_time3)/gsr.sample_rate

    #print(f"Total errors = {errors}/{number_tests}")

    print("FOR SAMPLE ONCE IN LOOP: ----------------------")
    print(f"Total time = {e_time - s_time}")
    print(f"Average time per sample = {t}")
    print(f"Average frequency = {1/t}Hz")
    print("\n\n")
    print("FOR GET SAMPLE: ------------------------------")
    print(f"Total time = {e_time2 - s_time2}")
    print(f"Average time per sample = {t2}")
    print(f"Average frequency = {1/t2}Hz")
    print("\n\n")
    #print("FOR GET SAMPLE2: ------------------------------")
    #print(f"Total time = {e_time3 - s_time3}")
    #print(f"Average time per sample = {t3}")
    #print(f"Average frequency = {1/t3}Hz")
