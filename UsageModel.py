class UsageModel:

    def __init__(self,prob_distro):
        self.prob_distro = prob_distro

    def cast(self) -> float:
        retval=self.prob_distro()
        if retval<0 or retval >1:
            raise ValueError("In UsageModel. Passed probability distribution generated value outside [0,1]: "+retval)
        return retval
