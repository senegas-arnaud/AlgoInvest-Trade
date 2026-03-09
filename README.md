# AlgoInvest&Trade - Optimisation de Portefeuille d'Actions

**AlgoInvest&Trade** est un projet d'optimisation d'investissement visant à maximiser le profit d'un portefeuille d'actions avec un budget limité.

### Contexte
- **Budget maximum** : 500€ par client
- **Contrainte** : Chaque action ne peut être achetée qu'une seule fois (problème du sac à dos 0/1)
- **Objectif** : Maximiser le bénéfice total après 2 ans

### Données
- **ActionList.csv** : 20 actions (dataset de test)
- **dataset1.csv** : 1000 actions
- **dataset2.csv** : 1000 actions

---

## 🔬 Algorithmes Implémentés

### 1. Brute Force (`Brute_force.py`) - Big O(2ⁿ)

#### Principe
Teste **toutes les combinaisons possibles** pour trouver la meilleure.

#### Performance
✅ Optimal garanti  
❌ Inutilisable au-delà de 25-30 actions

---

### 2. Knapsack - Programmation Dynamique (`Optimized.py`) - Big O(n × W)

#### Principe
Décompose le problème en **sous-problèmes** et stocke les résultats intermédiaires pour éviter les recalculs.


#### Optimisations Implémentées

##### Granularité Variable
Utilise des paliers (1€, 5€, 10€) au lieu de centimes pour réduire les calculs.
Opérations = n × (budget / paliers)


##### Post-Traitement
Compense la perte de précision due à la granularité :
**Étape 1** : Retirer les actions si dépassement de budget  
**Étape 2** : Ajouter des actions si budget restant  


#### Performance
✅ Optimal (ou quasi-optimal avec granularité)  
✅ Scalable jusqu'à ~5 000 actions (avec granularité)  
⚠️ Lent sans granularité

---

### 3. Greedy - Algorithme Glouton (`Greedy.py`) - Big O(n log n)

#### Principe
Trie les actions par **ratio profit/prix décroissant** et sélectionne goulûment les meilleures jusqu'à épuisement du budget.


#### Performance
✅ Très rapide  
✅ Résultats excellents (~98-99% de l'optimal)  
✅ Scalable (millions d'actions)  
⚠️ Pas de garantie d'optimalité

---

## 🎯 Conclusion

### Quel algorithme choisir ?

#### Pour petits datasets
→ **Knapsack step=1** : Solution optimale garantie en temps raisonnable

#### Pour datasets moyens
→ **Knapsack avec granularité 1€** : 99.9% optimal, rapide

#### Pour gros datasets
→ **Greedy** : Excellent compromis vitesse/qualité

---

## 🚀 Utilisation

### Installation
```bash
pip install pandas --break-system-packages
```

### Exécution

**Brute Force :**
- Ajuster la valeur du portefeuille dans la variable "wallet"
- Sélectionner le dataset à utiliser
```bash
python Brute_force.py
```

**Knapsack Optimisé :**
- Sélectionner le dataset à utiliser
- Ajuster la valeur de step a vos besoin (Step = 1 -> Résultats optimal)
- Ajuster la valeur du portefeuille
```bash
python Optimized.py
```

**Greedy :**
- Ajuster la valeur du portefeuille dans la variable "wallet"
- Sélectionner le dataset à utiliser
```bash
python Greedy.py
```
