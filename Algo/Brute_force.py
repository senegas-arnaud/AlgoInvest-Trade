import pandas
from itertools import combinations
import time
import tracemalloc

csv_action = pandas.read_csv("Data/ActionList.csv", delimiter=",")
csv_action["profit"] = csv_action["profit"].str.replace("%", "").astype(float)
data1 = pandas.read_csv("Data/dataset1.csv", delimiter=",")
data2 = pandas.read_csv("Data/dataset2.csv", delimiter=",")

class Brute_force():
    def __init__(self, csv_action):
        self.csv_action = csv_action

    def bf_algo(self):
        start_time = time.time()
        wallet = 500
        best_benefit = 0
        best_combination = []
        best_cost = 0
        actions = list(self.csv_action.itertuples())

        for size in range(1, len(actions) + 1):
            for combination in combinations(actions, size):
                total_cost = sum(action.price for action in combination)

                if total_cost <= wallet:
                    total_benefit = sum(action.price * (action.profit / 100) for action in combination)

                    if total_benefit > best_benefit:
                        best_benefit = total_benefit
                        best_combination = [action.name for action in combination]
                        best_cost = total_cost

        end_time = time.time() 
        execution_time = end_time - start_time

        print(f"Meilleure combinaison : {best_combination}")    
        print(f"Coût total : {best_cost}€")
        print(f"Bénéfice total : {best_benefit}€")
        print(f"Temps d'exécution : {execution_time:.2f} secondes")
    
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
        self.bf_algo()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"Current memory usage: {current / 10**6:.2f} MB; Peak memory usage: {peak / 10**6:.2f} MB")
        
        
algo = Brute_force(csv_action)
algo.clean_data(csv_action)
print(algo.bf_algo())
algo.memory_calculation()