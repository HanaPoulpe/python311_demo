class MyClass:
    def __init__(self):
        self.my_attribute = None


def main():
    o = MyClass()

    print(o.missing_attribute)


if __name__ == '__main__':
    main()
