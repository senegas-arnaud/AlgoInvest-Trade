import pandas
import math
import time
import tracemalloc

csv_action = pandas.read_csv("Data/ActionList.csv", delimiter=",")
csv_action["profit"] = csv_action["profit"].str.replace("%", "").astype(float)
data1 = pandas.read_csv("Data/dataset1.csv", delimiter=",")
data2 = pandas.read_csv("Data/dataset2.csv", delimiter=",")

class Optimized():
    def __init__(self, data):
        self.data_original = self.clean_data(data)
        
        self.csv_action = self.data_original.copy()
        self.csv_action['price_rounded'] = self.csv_action['price'].apply(math.ceil).astype(int)
         
        self.actions = list(self.csv_action.itertuples())
        self.stockage = {}
    
    def clean_data(self, data):
        data_cleaned = data[
            (data['price'] > 0) &
            (data['profit'] > 0)
        ].copy()
        
        print(f"📊 Actions totales : {len(data)}")
        print(f"❌ Actions filtrées : {len(data) - len(data_cleaned)}\n")
        
        return data_cleaned
    
    def opti_algo(self, wallet):
        nombre_actions = len(self.actions)
        
        if nombre_actions == 0:
            return (0, [])
        
        for budget in range(wallet + 1):
            self.stockage[(0, budget)] = (0, [])
        
        for index_action in range(1, nombre_actions + 1):
            current_action = self.actions[index_action - 1]
            cost = current_action.price_rounded 
            profit = current_action.price * (current_action.profit / 100) 
            
            for budget in range(wallet + 1):
                profit_without, combinaison_without = self.stockage[(index_action - 1, budget)]

                if cost <= budget:
                    profit_leftover, combinaison_leftover = self.stockage[(index_action - 1, budget - cost)]
                    profit_with = profit + profit_leftover
                    combinaison_with = [current_action.name] + combinaison_leftover
                else:
                    profit_with = 0
                    combinaison_with = []
                
                if profit_with > profit_without:
                    self.stockage[(index_action, budget)] = (profit_with, combinaison_with)
                else:
                    self.stockage[(index_action, budget)] = (profit_without, combinaison_without)

        return self.stockage[(nombre_actions, wallet)]
        
    
    def display_result(self, wallet):
        start_time = time.time()

        profit_total, best_combinaison = self.opti_algo(wallet)

        end_time = time.time() 
        execution_time = end_time - start_time
        
        if not best_combinaison:
            print("Aucune solution trouvée")
            return [], 0, 0
        
        cost_total_real = sum(
            action.price
            for action in self.actions 
            if action.name in best_combinaison
        )
        
        
        print(f"🎯 Meilleure combinaison : {len(best_combinaison)} actions : {best_combinaison}")
        print(f"💰 Bénéfice total : {profit_total:.2f}€")
        print(f"💳 Coût total (réel) : {cost_total_real:.2f}€")
        print(f"💵 Budget restant : {wallet - cost_total_real:.2f}€")
        print(f"⏱️ Temps d'exécution : {execution_time:.2f} secondes\n")
        
        
        return best_combinaison, profit_total, cost_total_real

    def memory_calculation(self):
        tracemalloc.start()
        self.opti_algo(500)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"Current memory usage: {current / 10**6:.2f} MB; Peak memory usage: {peak / 10**6:.2f} MB")


algo = Optimized(data1)
algo.display_result(500)
algo.memory_calculation()