"""
Runners to execute workflows
"""

class BaseRunner(object):
    """
    Basic runner
    """
    def __init__(self, **kwargs):
        pass

    def run(self, sig, **kwargs):
        """
        Run the function sig with arguments **kwargs
        """
        return sig(**kwargs)

class SingleThreadedRunner(BaseRunner):
    """
    Single threaded task runner
    """
    pass
