import inspect


class Testowa:

    def test(self, a, b, c=None):
        pass

for i in inspect.getmembers(Testowa):
    if i[0] == 'test':
        print(i)


