import types


class InterfaceLifeCycle(object):
    def __getattribute__(self, attr):

        method = object.__getattribute__(self, attr)

        if isinstance(method, types.MethodType) or isinstance(method, types.FunctionType):
            def wrapper(*args, **kwargs):
                if 'db' in kwargs.keys():
                    try:
                        return method(*args, **kwargs)
                    except Exception as e:
                        raise e
                else:
                    return method(*args, **kwargs)

            return wrapper
        else:
            return method
