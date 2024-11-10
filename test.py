from functools import wraps

def pass_arguments(*args,**kwargs):
    def decorator(f):
        @wraps(f)
        def inner(*a,**k):
            a = a + args
            k = k|kwargs
            return f(*a,**k)
        return inner
    return decorator

@pass_arguments(a=10, b=2, c=30)
def calculate(a, b, c):
    return a ** b + c

print(calculate())