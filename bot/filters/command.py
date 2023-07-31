from aiogram.filters.command import Command


class CommandFilter(Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ignore_case = True
        self.prefix = '/!'
