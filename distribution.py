import random
import math


def index(n):
    """Итератор для перебора значений выборки распределения"""
    i = 0
    while i < n:
        yield i
        i += 1

def expectedValue(t):
    """Метод расчитывает оценку математического ожидания выборки.

    Args:
        t: массив значений выборки распределения.
    Returns:
        Возвращает вещественное число. Оценку математического ожидания для
        заданной выборки случайной величины.
    """

    mu = 0
    for x in t:
        mu += x / len(t)
    return mu

def variance(t):
    """Метод вычисляет оценку дисперсии случайной величины.

    Args:
        t: массив значений выборки распределения.
        Returns:
        Возвращает вещественное число. Оценку дисперсии для
        заданной выборки случайной величины.
    """

    disp = 0
    for x in t:
        disp += pow(x, 2)

    disp = (disp - len(t) * pow(expectedValue(t), 2)) / (len(t) - 1)

    return disp

def standardDeviation(t):
    """Метод вычисляет оценку среднеквадратическое отклонения случайной
    величины

    Args:
        t: массив значений выборки распределения.
        Returns:
            Возвращает вещественное число. Оценку среднеквадратическое
            отклонения для заданной выборки случайной величины.
    """

    sigma = pow(variance(t), 0.5)
    return sigma

def confidenceInterval(t):
    """Метод вычисляет доверительный интервал случайной величины

    Args:
        t: массив значений выборки распределения.
    Returns:
        Возвращает массив длинной "2". Где значения массива - это
        границы доверительного интервала.
        Соответственно:
            x[0] - левая граница
            x[1] - правая граница
    """

    z = 1.96
    delta = z * standardDeviation(t) / pow(len(t), 0.5)

    mu = expectedValue(t)
    x = [mu - delta, mu + delta]

    return x

def statisticalDispersion(t):
    """Метод вычисляет коэффициент вариации случайной величины

    Args:
        t: массив значений выборки распределения.
    Returns:
        Возвращает вещественное число. Коэффициент вариации заданной
        случайно величины.
    """
    kv = (standardDeviation(t) / expectedValue(t) * 100.0)
    return kv




def paramN(mu, kv):
    """Расчет параметров распределения

    Returns:
        Возвращает словарь с параметрами для моделирования
        случайной величины.
    """
    param = {"alfa": mu, "beta": kv * mu}
    return param

def normalizedRandomVariable():
    """Моделирует случайное число по нормированному нормальному закону"""
    z = 0
    for i in range(12):
        z += random.random()

    return z-6.0;

def normal(mu, kv, n):
    """Метод моделирует нормальный закон распределения случайной величины

    Использует метод normalizedRandomVariable() для
    вычисления нормально нормированной случайной величины.

    Args:
        param: Словарь с параметрами

    Returns:
        Возвращает список значений распределенных по нормальному закону
    """
    param = paramN(mu, kv)
    t = []
    for i in index(n):
        t += [param["alfa"] + param["beta"] * normalizedRandomVariable()]

    return t;


 


def paramLN(mu, kv):
    """Расчет параметров распределения

    Returns:
        Возвращает словарь с параметрами для моделирования
        случайной величины.
    """

    beta = math.sqrt(math.log(1.0 + pow(kv, 2)))
    alfa = math.log(mu) - pow(beta, 2.0) / 2.0
    param = {"alfa": alfa, "beta": beta}

    return param

def normalLog(param, n):
    t = []
    for i in index(n):
        t += [param["alfa"] + param["beta"] * normalizedRandomVariable()]

    return t;

def logNormal(mu, kv, n):
    """Метод моделирует Логнормальный закон распределения случайной величины

    Использует метод normalLog() для вычисления случайной величины
    распределенной по нормального закона.

    Args:
        param: Словарь с параметрами

    Returns:
        Возвращает список значений распределенных по нормальному закону
    """
    param = paramLN(mu, kv)
    t = []
    for x in normalLog(param, n):
        t += [math.exp(x)]
    return t




def paramR(mu, kv):
    """Расчет параметров распределения

    Returns:
        Возвращает словарь с параметрами для моделирования
        случайной величины.
    """

    alfa = mu * (1 - math.sqrt(3) * kv)
    beta = mu * (1 + math.sqrt(3) * kv)
    param = {"alfa": alfa, "beta": beta}
    return param

def uniform(mu, kv, n):
    """Метод моделирует Равномерный закон распределения случайной величины

    Args:
        param: Словарь с параметрами

    Returns:
        Возвращает список значений распределенных по нормальному закону
    """
    param = paramR(mu, kv)
    t = []
    for i in index(n):
        t += [param["alfa"] + random.random() * (param["beta"] - param["alfa"])]
    return t



def paramG(mu, kv):
    """Расчет параметров распределения

    Returns:
        Возвращает словарь с параметрами для моделирования
        случайной величины.
    """
    alfa = 1 / pow(kv, 2)
    beta = alfa / mu
    param = {"alfa": alfa, "beta": beta}
    return param

def gammaVspom(param):
    """Вспомогательный метод реализует алгоритм расчета случайной величины"""
    if 0 < param["alfa"] and param["alfa"] < 1:
        while True:
            a = pow(random.random(), 1 / param["alfa"])
            b = pow(random.random(), 1 / (1 - param["alfa"]))
            c = a + b
            if c <= 1:
                d = a / c
                return (-d * math.log(random.random())) / param["beta"]
    elif 1 <= param["alfa"] and param["alfa"] < 5:
        a = math.trunc(param["alfa"])
        b = param["alfa"] - a
        while True:
            r = 1
            for i in range(math.trunc(a)):
                r *= random.random()
            c = -(param["alfa"] / a) * math.log(r)
            if random.random() <= pow(c / param["alfa"], b) * \
                        math.exp(-b * (c / param["alfa"] - 1)):
                return c / param["beta"]
    elif param["alfa"] >= 5:
        b = param["alfa"] - math.trunc(param["alfa"])
        r = random.random()
        if r >= b:
            for i in range(math.trunc(param["alfa"] - 1)):
                r *= random.random()
            return -math.log(r) / param["beta"]
        else:
            for i in range(math.trunc(param["alfa"])):
                r *= random.random()
            return -math.log(r) / param["beta"]

def gamma(mu, kv, n):
    """Метод моделирует Гамма закон распределения случайной величины

    Args:
        param: Словарь с параметрами

    Returns:
        Возвращает список значений распределенных по нормальному закону
    """
    param = paramG(mu, kv)
    t = []
    for i in index(n):
        t += [gammaVspom(param)]
    return t



def paramBS(mu, kv):
    """Расчет параметров распределения

    Returns:
        Возвращает словарь с параметрами для моделирования
        случайной величины.
    """
    beta = math.sqrt((mu + math.sqrt(math.pow(mu, 2) + 3 * math.pow(kv*mu, 2)))
            / (2 * math.pow(kv*mu, 2)))
    alfa = beta * mu - 0.5 / beta
    param = {"alfa": alfa, "beta": beta}
    return param

def birnbaumSaunders(mu, kv, n):
    """Метод моделирует Бирнбаум-Саундерса закон распределения
    случайной величины

    Args:
        param: Словарь с параметрами

    Returns:
        Возвращает список значений распределенных по нормальному закону
    """
    param = paramBS(mu, kv)
    t = []
    for i in index(n):
        z = normalizedRandomVariable()
        a1 = param["alfa"] / param["beta"]
        a2 = z / param["beta"]
        t += [a1 + 0.5 * pow(a2, 2) + a2 * math.sqrt(a1 + 0.25 * pow(a2, 2))]
    return t



def paramP(mu, kv):
    """Расчет параметров распределения

    Returns:
        Возвращает словарь с параметрами для моделирования
        случайной величины.
    """
    alfa = 2 * pow(kv, 2) / (pow(kv, 2) - 1)
    beta = (alfa - 1) * mu
    param = {"alfa": alfa, "beta": beta}
    return param


def pareto(mu, kv, n):
    """Метод моделирует Парето закон распределения случайной величины

    Args:
        param: Словарь с параметрами

    Returns:
        Возвращает список значений распределенных по нормальному закону
    """
    param = paramP(mu, kv)
    t = []
    for i in index(n):
        t += [param["beta"] * (1 / pow(1 - random.random(), 1 / param["alfa"]) - 1)]
    return t
