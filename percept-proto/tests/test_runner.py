from utils.registry import registry

def run_all_tests():
    for item in registry:
        item_cls = item.cls
        if hasattr(item_cls, 'tester') and hasattr(item_cls, 'test_cases'):
            tester = item_cls.tester()
            yield tester.run, item_cls, item_cls.test_cases

