import math


class LogisticModel:
    def __init__(
        self,
        weeks,
        premature_birth,
        smokes,
        adynamia,
        smoothness,
        wb_level,
        bmi,
        sti,
        spotting
    ):
        self.weeks = weeks
        self.premature_birth = premature_birth
        self.smokes = smokes
        self.adynamia = adynamia
        self.smoothness = smoothness
        self.wb_level = wb_level
        self.bmi = bmi
        self.sti = sti
        self.spotting = spotting

    def calculate(self):
        z = (
            -1.9567
            + 1.1345 * self.weeks
            + 1.1668 * self.premature_birth
            + 1.7293 * self.smokes
            + 1.1885 * self.adynamia
            + 1.0833 * self.smoothness
            + 0.8961 * self.wb_level
            + 0.9136 * self.bmi
            + 0.6464 * self.sti
            + 0.9618 * self.spotting
        )

        sigmoid = 1 / (1 + math.exp(-z))

        return sigmoid
    

class LogisticModel2:
    def __init__(
        self,
        wb_level,
        wb_avg_ep_avg_ratio,
        abortion,
        polycystic_ovary,
        wb_count,
    ):
        self.wb_level = wb_level
        self.wb_avg_ep_avg_ratio = wb_avg_ep_avg_ratio
        self.abortion = abortion
        self.polycystic_ovary = polycystic_ovary
        self.wb_count = wb_count
        
    def calculate(self):
        z = (
            -3.7268 +
            + 0.7541 * self.wb_level
            + 1.0288 * self.wb_avg_ep_avg_ratio
            + 1.3084 * self.abortion
            + 0.8088 * self.polycystic_ovary
            + 0.4110 * self.wb_count
        )

        sigmoid = 1 / (1 + math.exp(-z))

        return sigmoid
    

        