def include(func):
    # inner1 is a Wrapper function in
    # which the argument is called

    # inner function can access the outer local
    # functions like in this case "func"
    def inner1(*args):
        # print(func.__name__)
        # calling the actual function now
        # inside the wrapper function.
        # print(dir(func))
        func(*args)
       #  print("This is after function execution")

    return inner1
