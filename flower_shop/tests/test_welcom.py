from flower_shop.welcom import sum2, hello


def test_sum2():
    assert sum2(2, 3) == 5, "ты идиот что ли? Это не работает"

def test_hello():
    assert hello('Maks') == 'Hello, Maks', "ты идиот что ли? Это не работает"