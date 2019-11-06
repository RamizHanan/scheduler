class Task(object):

    def __init__(self, name: str, deadline: int, wcet1188: int, wcet918: int, wcet648: int, wcet384: int):
        self.name = name
        self.deadline = deadline
        self.wcet1188 = wcet1188
        self.wcet918 = wcet918
        self.wcet648 = wcet648
        self.wcet384 = wcet384

    def __str__(self):
        return "Task: {} {} {} {} {} {}".format(self.name, self.deadline, self.wcet1188, self.wcet918, self.wcet648, self.wcet384)
