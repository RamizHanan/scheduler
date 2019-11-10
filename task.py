class Task(object):

    def __init__(self, name: str, deadline: int, wcet1188: int, wcet918: int, wcet648: int, wcet384: int):
        self.name = name
        self.deadline = int(deadline)
        self.wcet1188 = int(wcet1188)
        self.wcet918 = int(wcet918)
        self.wcet648 = int(wcet648)
        self.wcet384 = int(wcet384)
        self.wcet = self.wcet1188
        self.ap = None

    def __str__(self):
        return "Task: {} {} {} {} {} {}".format(self.name, self.deadline, self.wcet1188, self.wcet918, self.wcet648, self.wcet384)
