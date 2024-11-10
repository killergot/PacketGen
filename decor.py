from functools import wraps

def except_catch(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            result = method(self, *args, **kwargs)
            return result
        except Exception as e:
            print(f"Что-то пошло не так при исполнении {method.__name__}")
            return None
    return wrapper

def except_catch_packet(packet_name : str):
    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            try:
                result = method(self, *args, **kwargs)
                return result
            except Exception as e:
                print(f"Ошибка при создании {packet_name} пакета")
                print(e)
                return None

        return wrapper
    return decorator