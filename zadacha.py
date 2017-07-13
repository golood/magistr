import distribution as distr
import matplotlib.pyplot as plt
import seaborn
import math

class Zadacha(object):
    """Класс решения задачи анализа безубыточности

    В классе реализованы интерфейсы для решения задачи безубыточности на
    на предприятии(грузовые перевозки) с помощью метода Монте-Карло.

    Attributes:
       param: Словарь с исходными данными для решения задачи.
    """

    def __init__(self, param):
        self.G = self.model(param.get("G"))
        self.Xp = self.model(param.get("Xp"))
        self.Xc = self.model(param.get("Xc"))
        self.Cg = self.model(param.get("Cg"))
        self.Dg = self.model(param.get("Dg"))
        self.In = self.model(param.get("In"))
        self.n = len(self.G)

    def model(self, param):
        """Метод для моделирования исходных данных"""
        if param[2] == "N":
            return distr.normal(param[0], param[1], param[3])
        elif param[2] == "LN":
            return distr.logNormal(param[0], param[1], param[3])
        elif param[2] == "R":
            return distr.uniform(param[0], param[1], param[3])
        elif param[2] == "G":
            return distr.gamma(param[0], param[1], param[3])
        elif param[2] == "BS":
            return distr.birnbaumSaunders(param[0], param[1], param[3])
        elif param[2] == "P":
            return distr.pareto(param[0], param[1], param[3])
        else:
            return 0

    def index(self):
        """Итератор для перебора значений списка"""
        i = 0
        while i < self.n:
            yield i
            i += 1


    def investedProfit(self):
        """Расчет вложенного дохода"""
        cm = []
        for i in self.index():
            cm += [(self.Xp[i] - self.Cg[i]) * self.G[i]]
        self.CM = cm

    def operatingProfit(self):
        """Расчет операционной прибыли"""
        pr = []
        for i in self.index():
            pr += [self.CM[i] + self.In - self.Xc[i]]
        self.OP = pr

    def oprRisk(self):
        """Расчет операционного риска"""
        self.OP.sort()
        num = 0
        OP = 0

        for i in self.OP:
            if i < OP:
                num += 1

        r = num / len(self.OP)

        return r

    def oprRiskDoverInter(self, opr):
        """Расчет доверительного интервала для операционного риска"""
        dpvInter = [opr - 1.96 * math.sqrt(opr * (1 - opr) / len(self.OP)),
                    opr + 1.96 * math.sqrt(opr * (1 - opr) / len(self.OP))]
        return dpvInter

    def operacRuchag(self):
        """Расчет операционного рычага"""
        x = 0
        y = 0
        for i in self.index():
            x = x + self.CM[i]
            y = y + self.OP[i]

        m = x / y

        return m

    def opecRuchagDovInterval(self, m):
        """Расчет доверительного интервала для операционного рычага"""
        d = 0
        k = 0

        for i in self.index():
            d = d + math.pow(self.OP[i] - m * self.CM[i], 2)
            k = k + self.OP[i]

        d = math.sqrt(d)
        d = d * 1.96

        d = d / k

        delta = [m - d, m + d]

        return delta

    def pokazatelRentabel(self):
        """Расчет показателя рентабельности"""
        x = 0
        y = 0

        for i in self.index():
            x = x + self.OP[i]
            y = y + self.Dg[i]

        z = x / y * 100

        return z

    def pokazatelRentabelM(self):
        """Расчет доверительного интервала для показателя рентабельности"""
        z = []

        for i in self.index():
            z[i] = self.OP[i] / self.Dg[i]

        return z

    def srokOkupaemosti(self):
        """"Расчет срока окупаемости"""

        to = distr.expectedValue(self.Dg) / distr.expectedValue(self.OP)

        return to

    def srokOkupaemostiDovInterval(self, m):
        """Расчет доверительного интервала для срока окупаемости"""
        d = 0
        k = 0

        for i in self.index():
            d = d + math.pow(self.OP[i] - m * self.CM[i], 2)
            k = k + self.OP[i]

        d = math.sqrt(d)
        d = d * 1.96

        d = d / k

        delta = [m - d, m + d]

        return delta

    def tochkaBezub(self):
        """Матод вычисляет точку безубыточности"""
        self.TB = []

        for i in self.index():
            self.TB += [self.Xc[i] / (self.Cg[i] - self.Xp[i])]
        
    

def main(param):
    data = {  'Операционная прибыль'          : [],
              'Операционный риск(вероятность)': [],
              'Вложенный доход'               : [],
              'Операционный рычаг'            : [],
              'Показатель рентабельности'     : [],
              'Срок окупаемости'              : []
           }
    
    test = Zadacha(param)
    
    test.investedProfit()
    test.operatingProfit()
    
    data['Вложенный доход'] += ([distr.expectedValue(test.CM)]
            + [distr.confidenceInterval(test.CM)])
    data['Операционная прибыль'] += ([distr.expectedValue(test.OP)]
            + [distr.confidenceInterval(test.OP)]
            + [distr.statisticalDispersion(test.OP)])
    data['Операционный риск(вероятность)'] += ([test.oprRisk()]
            + [test.oprRiskDoverInter(test.oprRisk())])
    data['Операционный рычаг'] += ([test.operacRuchag()]
            + [test.opecRuchagDovInterval(test.operacRuchag())])
    data['Показатель рентабельности'] += ([test.pokazatelRentabel()]
            + [test.opecRuchagDovInterval(test.pokazatelRentabel())])
    data['Срок окупаемости'] += ([test.srokOkupaemosti()]
            + [test.srokOkupaemostiDovInterval(test.srokOkupaemosti())])

    test.tochkaBezub()

    for i in data:
        print(i + "  " + str(data[i]))

    proverka(data)

    graph(test.OP, test.TB)
    #seaborn.distplot(test.OP)
    #plt.show()

def proverka(data):

    for box, item in data.items():
        if item[0] > item[1][0] and item[0] < item[1][1]:
            pass
        else:
            print("Оценка мат. ожидания не попала в доверительный интервал")
            print(box + ": Посчтитан не верно")
    print("Проверка окончена")

def graph(OP, TB):
    f, ax = plt.subplots(2,1, sharex=True)
    
    ax[0].set_title("Операционная прибыль")
    ax[1].set_title('Точка езубыточности')
    
    seaborn.distplot(TB, ax=ax[1])
    seaborn.distplot(OP, ax=ax[0])
    
    plt.suptitle("Text", size=16)
    plt.show()
    
