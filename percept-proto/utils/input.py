def import_from_string(import_string):
    import_split = import_string.split(".")
    import_class = import_split[-1]
    module_path = ".".join(import_split[:-1])
    mod = __import__(module_path, fromlist=[import_class])
    klass = getattr(mod, import_class)
    return klass