import sys

sys.path.insert(0, "/home/pi/firmware/Models/eda-classifier/src/")
sys.path.insert(0, "/home/pi/firmware/Drivers/")

from GSRDriver import GSRDriver
from cvx_solver import CVX


class GSRClassifier:
    def __init__(self):
        self.gsr = GSRDriver()
        self.sample_rate = self.gsr.sample_rate
        self.model = CVX(f_s=self.sample_rate)

    def predict(self):
        data = self.gsr.get_sample()
        phasic_av, tonic_av, stat = self.model.predict(data)
        return phasic_av, tonic_av, stat[0]


if __name__ == "__main__":
    gc = GSRClassifier()

    print(gc.predict())
