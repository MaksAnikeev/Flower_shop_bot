# -*- coding: utf-8 -*-

def hello(name):
    return 'Hello, ' + name


def sum2(x, y):
    return x + y

# прибавляет 2 к каждому элементу коллекции
def plus2(nums):
    result = []
    for num in nums:
        result.append(num + 2)
    return result

# умножает на 2 каждый элемент коллекции
def multiply2(nums):
    result = []
    for num in nums:
        result.append(num * 2)
    return result

# возводит в степень 2 каждый элемент коллекции
def exponent2(nums):
    result = []
    for num in nums:
        result.append(num ** 2)
    return result

def division(a, b):
    return a/b
