class Measurement_Validator:
    def __init__(self, soft_cut_off, hard_cut_off):
        self.measurement = None
        self.soft_cut_off = soft_cut_off
        self.hard_cut_off = hard_cut_off
        self.soft_cut_off_measurement = 0
        self.previous_soft_cut_off = False

    def give_validatet_measurement(self, measurement):
        if self.measurement is None:
            self.measurement = measurement
            return measurement
        diffrence = abs(measurement - self.measurement)
        if self.previous_soft_cut_off:
            self.previous_soft_cut_off = False
            if abs(measurement - self.soft_cut_off_measurement) <= self.soft_cut_off:
                self.measurement = measurement
                return measurement
        elif diffrence > self.hard_cut_off:
            return self.measurement
        elif diffrence > self.soft_cut_off:
            self.previous_soft_cut_off = True
            self.soft_cut_off_measurement = measurement
            return self.measurement
        else:
            self.measurement = measurement
            return measurement
        
