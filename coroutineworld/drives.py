
class Drive:
    def __init__(self):
        self.level = 0  # the least amount of drive
        self.event_type = NotImplemented

    def up(self):
        self.level += 1

    def reset(self):
        self.level = 0


class Hunger(Drive):
    def __init__(self):
        super().__init__()

        self.event_type = 'eating'


class Thirst(Drive):
    def __init__(self):
        super().__init__()

        self.event_type = 'drinking'


class Fatigue(Drive):
    def __init__(self):
        super().__init__()

        self.event_type = 'sleeping'
