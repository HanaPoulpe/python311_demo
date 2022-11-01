def raise_except(v):
    try:
        raise ValueError(v)
    except ValueError as e:
        return e


def eg_demo():
    try:
        raise ExceptionGroup("one", [raise_except(1)])
    except ExceptionGroup as e:
        eg = e

    raise ExceptionGroup("two", [eg, raise_except(2)])


if __name__ == "__main__":
    try:
        eg_demo()
    except* ValueError as e:
        print("Catches any group containing ValueError:", e)

    try:
        eg_demo()
    except* (ValueError, ValueError) as e:
        print("Catches any group with 2 value errors", e)
    except* ValueError as e:
        print("This line should not run:", e)

    print("----")
    print("Unhandled ExceptionGroup")
    eg_demo()
