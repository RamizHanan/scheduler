class Scheduler(object):

    def __init__(self, task_count: int, exec_time: int, ap1188: int, ap918: int,
                 ap648: int, ap384: int, apidle: int, sch_type: str, ee: bool):
        self.task_count = task_count
        self.exec_time = exec_time
        self.ap1188 = ap1188
        self.ap918 = ap918
        self.ap648 = ap648
        self.ap384 = ap384
        self.apidle = apidle
        self.sch_type = sch_type
        self.ee = ee

    def schedule(self):
        if self.sch_type.lower() is 'edf' and self.ee is False:
            self.EDF()
        elif self.sch_type.lower() is 'rm' and self.ee is False:
            self.RM()
        elif self.sch_type.lower() is 'edf' and self.ee is True:
            self.EDF_EE()
        elif self.sch_type.lower() is 'rm' and self.ee is True:
            self.RM_EE()

    def EDF(self):
        pass

    def RM(self):
        pass

    def EDF_EE(self):
        pass

    def RM_EE(self):
        pass

    def __str__(self):
        return "Scheduler: {} {} {} {} {} {} {} ({} {})".format(self.task_count, self.exec_time, self.ap1188,
                                                                self.ap918, self.ap648, self.ap384, self.apidle,
                                                                self.sch_type, self.ee)
