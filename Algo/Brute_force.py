import pandas
import time
import tracemalloc

csv_action = pandas.read_csv("Data/ActionList.csv", delimiter=",")
csv_action["profit"] = csv_action["profit"].str.replace("%", "").astype(float)
data1 = pandas.read_csv("Data/dataset1.csv", delimiter=",")
data2 = pandas.read_csv("Data/dataset2.csv", delimiter=",")

class Brute_force():
    def __init__(self, csv_action):
        self.csv_action = csv_action

    def generate_combinations(self, actions):
        all_combinations = [[]]

        for action in actions:
            new_combinations = []
            for existing in all_combinations:
                new_combinations.append(existing + [action]) 
            all_combinations = all_combinations + new_combinations

        return all_combinations[1:]

    def bf_algo(self, silent=False):
        start_time = time.time()
        wallet = 500
        best_benefit = 0
        best_combination = []
        best_cost = 0
        actions = list(self.csv_action.itertuples())

        all_combinations = self.generate_combinations(actions)

        for combination in all_combinations:
            total_cost = 0
            total_benefit = 0

            for action in combination:
                total_cost += action.price
                total_benefit += action.price * (action.profit / 100)

            if total_cost <= wallet and total_benefit > best_benefit:
                best_benefit = total_benefit
                best_combination = [action.name for action in combination]
                best_cost = total_cost

        end_time = time.time()
        execution_time = end_time - start_time

        if not silent:
            print(f"🎯 Meilleure combinaison : {best_combination}")
            print(f"📋 Nombre d'actions : {len(best_combination)}")
            print(f"💰 Bénéfice total : {best_benefit:.2f}€")
            print(f"💳 Coût total : {best_cost:.2f}€")
            print(f"💵 Budget restant : {wallet - best_cost:.2f}€\n")
            print(f"⏱️ Temps d'exécution : {execution_time:.2f} secondes")

    def clean_data(self, data):
        data_cleaned = data[
            (data['price'] > 0) &
            (data['profit'] > 0)
        ].copy()

        print(f"📊 Actions totales : {len(data)}")
        print(f"❌ Actions filtrées : {len(data) - len(data_cleaned)}\n")

        return data_cleaned
    
    def memory_calculation(self):
        tracemalloc.start()
        self.bf_algo(silent=True)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"🧠 Consommation actuelle de la mémoire: {current / 10**6:.2f} MB; Pic de consommation: {peak / 10**6:.2f} MB\n")


algo = Brute_force(csv_action)
algo.clean_data(csv_action)
algo.bf_algo()
algo.memory_calculation()