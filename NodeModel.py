class NodeModel:
    def __init__(self, power_model):
         self.power_model = power_model

    def get_power(self,usage: float) -> float:
        if usage < 0 or usage > 1:
            raise ValueError("In NodeModel::get_power. usage must be in [0,1]")
        return self.power_model(usage)
