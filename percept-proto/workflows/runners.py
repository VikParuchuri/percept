class BaseRunner(object):
    def __init__(self, **kwargs):
        pass

    def run(self, sig, **kwargs):
        return sig(**kwargs)

class SingleThreadedRunner(BaseRunner):
    pass
