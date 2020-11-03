def total(a=5, *numbers, **phonebook):
    '''
    ---
     1
      Total function
       :param a:
    :param numbers:
    :param phonebook:
    :return:
    '''
    print("a = %d" % a)
    for single_item in numbers:
        print("single_item:", single_item)

    for x, y in phonebook.items():
        print("key = {0}, val = {1}".format(x, y))


print(total(10, 1, 2, 3, a1=11, a2=22, a3=33))
print(total.__doc__)
