class EggException(Exception):
    def __init__(self):
        super().__init__(self)


class EggRegisterException(EggException):
    pass


class EggAccessViolation(EggException):
    def __str__(self):
        return f"Attempted to utilize non-existent EggData entry!\n" \
               f"Filename = {self.filename}"

    def __init__(self, egg_data):
        super().__init__()
        self.filename = egg_data.getEggFilename()
