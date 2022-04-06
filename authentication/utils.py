WORDS = ['минута', 'минуты', 'минут']

def mul_of_num(number, words=WORDS):
    n = abs(number) % 100
    n1 = n % 10
    if n > 10 and n < 20:
        return words[2]
    if n1 > 1 and n1 < 5:
        return words[1]
    if n1 == 1:
        return words[0]
    return words[2]
