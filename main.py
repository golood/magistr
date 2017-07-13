import zadacha

#test = NormalizedRandomVariable(20000, 10, 0.6)
#t = test.normal(test.param())
#print(len(t))

#plt.hist(t, 50)
#plt.show()
n = 20000

def setParam(n):
    param = {"G": [152.93, 0.1, "LN", n],   # Эксплуатационный грузооборот
             "Xp": [337, 0.07, "N", n],     # Переменные затраты на единицу грузооборота
             "Xc": [19116.8, 0.1, "G", n],  # Постоянные затраты
             "Cg": [191.3, 0.07, "R", n],   # Цена единицы перевезенного грузооборота
             "Dg": [10000, 0.1, "G", n],    # Размер инвистиций
             "In": [0, 0, "NaN", 0]}        # Величина дотаций
    return param


#def modeling(param):
#    zadacha = zadacha.Zadacha(param)
#
#    cm = zadacha.investedProfit()
#    pr = zadacha.operatingProfit(cm)


zadacha.main(setParam(n))

#seaborn.distplot(pr)
#plt.show()
