import numpy as np
import matplotlib.pyplot as plt


# Données d'exemple
X = [31, 36, 37, 40, 41, 44, 49, 50, 51, 52, 53, 55, 57, 58, 59, 61, 62, 66, 67, 71, 73, 74, 81, 87, 91, 96, 110, 112, 113, 115, 127, 129, 133, 146, 157, 160, 172, 173, 181, 189, 191, 193, 210, 215, 222, 224, 225, 260, 268]
Y = [1025.44, 560.63, 1528.17, 1778.27, 2432.93, 825.5, 1741.69, 2494.03, 1069.89, 1229.69, 1083.62, 1434.43, 1659.02, 5583.65, 1169.57, 916.02, 1352.44, 1619.45, 1409.86, 3371.53, 1985.2, 2224.74, 3110.18, 3857.14, 2363.32, 2402.41, 2439.95, 2295.32, 2548.73, 2453.13, 2864.73, 3226.7, 3172.77, 3687.84, 6756.66, 3152.43, 3732.31, 3711.98, 7361.23, 4274.5, 3566.82, 4021.45, 4364.57, 4028.01, 5285.04, 5313.24, 5559.79, 5857.81, 5779.58]


# Etape 1 : Calcul des moyennes
mean_X = sum(X) / len(X)
mean_Y = sum(Y) / len(Y)


# Etape 2 : Calcul des différences X - moyenne et Y - moyenne
X_diff = [x - mean_X for x in X]
Y_diff = [y - mean_Y for y in Y]




# Etape 3 : Calcul du numérateur (somme des produits des écarts)
num = sum(xd * yd for xd, yd in zip(X_diff, Y_diff))


# Etape 4 : Calcul du dénominateur (les variances de X et Y)
denom_X = sum(xd ** 2 for xd in X_diff)
denom_Y = sum(yd ** 2 for yd in Y_diff)


# Etape 5 : Calcul du coefficient de corrélation
correlation = num / (np.sqrt(denom_X) * np.sqrt(denom_Y))
print("Coefficient de corrélation de Pearson :", correlation)


# Calcul de la pente (a) et de l'ordonnée à l'origine (b)
a = num / denom_X
b = mean_Y - a * mean_X


# Etape 6 : Tracer la droite de régression
Y_pred = [a * x + b for x in X]


# Estimation du nombre de ventes pour un chiffre d'affaires de 1250 eur
chiffre_affaires = 1250
nb_ventes_estime = (chiffre_affaires - b) / a
print("Estimation du nombre de ventes pour un chiffre d'affaires de 1250 eur :", nb_ventes_estime)
print(a, b)


# Tracer les points et la droite de régression
plt.scatter(X, Y, color='blue', label='Données')
plt.plot(X, Y_pred, color='red', label='Droite de régression')
plt.xlabel('NbVentes')
plt.ylabel('Somme - CA')
plt.title('Droite de régression')
plt.legend()
plt.show()