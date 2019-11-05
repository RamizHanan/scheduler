class Task(object):
    def __init__(self, name: str, deadline: int, ap1188: int, ap918: int, ap648: int, ap384: int):
        self.name = name
        self.deadline = deadline
        self.ap1188 = ap1188
        self.ap918 = ap918
        self.ap648 = ap648
        self.ap384 = ap384

    def __str__(self):
        return "Task: {} {} {} {} {} {}".format(self.name, self.deadline, self.ap1188, self.ap918, self.ap648, self.ap384)
