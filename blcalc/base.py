"""
Base class for all data based objects
> Contains datas as dictionary for ease
"""
# Just wrapper over dict for now

class Base(dict):
    """
    Base class of BLCalc
    """
    def get(self):
        """
        Get datas as seriliazable value
        """
        return self

    def set(self, obj):
        """
        Add new object to base data
        """
        self.update(obj)
