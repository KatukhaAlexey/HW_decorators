import os
import time
from functools import wraps


def logger(path='main.log'):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            data_of_call_function = time.strftime("%d.%m.%Y", time.localtime())
            time_of_call_function = time.strftime("%H:%M:%S", time.localtime())
            start = time.time()
            result = old_function(*args, **kwargs)
            end = time.time()
            ar = str(args)
            kwar = str(kwargs)
            if ar == '()' and kwar == '{}':
                all_args = f'Была вызвана без аргументов'
            elif ar != '()' and kwar == '{}':
                all_args = f'Была вызвана с аргументами: {args}'
            elif ar == '()' and kwar != '{}':
                all_args = f'Была вызвана с аргументами: {kwargs}'
            else:
                all_args = f'Была вызвана с аргументами: {args} {kwargs}'
            with open(path, 'a', encoding='utf-8') as file:
                file.write(f'Функция "{old_function.__name__}"\n'
                           f'\tБыла вызвана {data_of_call_function} в {time_of_call_function}\n'
                           f'\tВыполнялась {end - start} секунд\n'
                           f'\t{all_args}\n'
                           f'\tВозвратила объект: {type(result)}\n'
                           f'\tЗначение: {result}\n\n')
            return result
        return new_function
    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()
