def de1(func):
    def _wa():
        print('装饰器1 开始')
        func()
        print('装饰器1 结束')

    return _wa


def de2(func):
    def _wa():
        print('装饰器2 开始')
        func()
        print('装饰器2 结束')

    return _wa


@de2
@de1
def main1():
    print("主函数")


def de3(func):
    def _wa(fun2):
        print('装饰器3 开始')
        print('装饰器3 结束')

    return _wa


def de4():
    def _wa():
        print('装饰器4 开始')
        print('装饰器4 结束')

    return _wa


@de3(de4)
def main2():
    print("主函数")


if __name__ == '__main__':
    # main1()
    main2()
