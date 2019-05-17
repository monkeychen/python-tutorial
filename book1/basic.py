import sys
from functools import reduce

print(sys.argv)

arr = [x for x in range(1, 11)]
val = reduce(lambda x, y: x + y, arr)
print("val = %d" % val)

a, b, c = 3, 5, None
print(a, b, c)

scores = [('a', 89, 90, 59), ('b', 99, 49, 59), ('c', 99, 60, 20)]


def handle_filter(a):
    s = sorted(a[1:])
    if s[-2] > 80 and s[0] < 60:
        return True
    if s[-1] > 90 and s[1] < 60:
        return True
    if s[-2] > 80 and sum(s) / len(s) < 60:
        return True
    return False


aa = list(filter(handle_filter, scores))
print(aa)
