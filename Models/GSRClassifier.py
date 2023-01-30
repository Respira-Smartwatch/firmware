import sys

sys.path.insert(0, "./Models/eda-classifier/src")

from Drivers.GSRDriver import GSRDriver
from cvx_solver import CVX

class GSRClassifier:
    def __init__(self):
        self.gsr = GSRDriver()
        self.sample_rate = self.gsr.sample_rate
        self.model = CVX(f_s=self.sample_rate)
    
    # TODO: Fix this once Model has been updated
    def predict(self):
        data = self.gsr.get_sample()
        phasic_av, tonic_av = self.model.predict(data)
        print(phasic_av, tonic_av)
        return tonic_av
