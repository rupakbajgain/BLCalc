"""
Contains various helper functions
"""

class TempNameGenerator:
    """
    Used to create temp names
    """
    def __init__(self, start):
        """
        Start: name start from
        """
        self.count=0
        self.start=start

    def next(self):
        """
        Returns next string
        """
        self.count += 1
        if self.count == 1:
            return self.start
        return self.start + str(self.count)
