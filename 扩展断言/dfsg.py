import random

mobile = '133'
for i in range(8):
    # print(i)
    n = str(random.randint(0, 9))
    print(n)

    mobile += n
    print(mobile)