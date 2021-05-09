import re

# text = '9@gmail.com'
# if re.match(r'[0-9a-zA-Z_]{0,19}@[qq,gmail,]{1,5}.[co,net,cn]{1,3}$', text):
#     print('Right!')
# else:
#     print('Please reset')


# text = '9@163.cn'
# res = re.match('[0-9a-zA-Z_]{0,19}@[qq,163,gamil]{1,5}.[com,cn,net]{1,3}', text)
# print(res.group(1))
# print(res.group(2))


# num = '19821959308'
# res = re.match('^1[3689]{1}\d{9}', num)
# print(res.group())


import time

flag = True


def timer(tc):
    def wrapper(func):
        def inner(*args, **kwargs):
            if tc:
                s = time.perf_counter()

                res = func(*args, **kwargs)

                e = time.perf_counter()
                print(f"耗时: {e - s} 秒")

            else:
                res = func(*args, **kwargs)

            return res

        return inner

    return wrapper


@timer(flag)
def task(*args, **kwargs):
    time.sleep(3)


if __name__ == '__main__':
    task()
