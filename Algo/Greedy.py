import pandas
import time

csv_action = pandas.read_csv("Data/ActionList.csv", delimiter=",")
csv_action["profit"] = csv_action["profit"].str.replace("%", "").astype(float)
data1 = pandas.read_csv("Data/dataset1.csv", delimiter=",")
data2 = pandas.read_csv("Data/dataset2.csv", delimiter=",")

class Greedy():
    def __init__(self, csv_action):
        self.csv_action = csv_action

    def clean_data(self, data):
        data_cleaned = data[
            (data['price'] > 0) &
            (data['profit'] > 0)
        ].copy()
        
        print(f"📊 Actions totales : {len(data)}")
        print(f"❌ Actions filtrées : {len(data) - len(data_cleaned)}\n")
        
        return data_cleaned
        
    def greed_algo(self):
        start_time = time.time()
        sorted_actions = self.csv_action.sort_values(by="profit", ascending=False)
        wallet = 500
        total_cost = 0
        total_benefit = 0
        best_combinaison = []
        
        for action in sorted_actions.itertuples():
            if total_cost + action.price <= wallet:
                total_cost += action.price
                total_benefit += action.price * (action.profit / 100)
                best_combinaison.append(action.name)
        
        end_time = time.time() 
        execution_time = end_time - start_time

        print(f"🎯 Meilleure combinaison : {len(best_combinaison)} actions : {best_combinaison}")
        print(f"💰 Bénéfice total : {total_benefit:.2f}€")
        print(f"💳 Coût total (réel) : {total_cost:.2f}€")
        print(f"💵 Budget restant : {wallet - total_cost:.2f}€")
        print(f"⏱️ Temps d'exécution : {execution_time:.2f} secondes\n")


        

algo = Greedy(data2)
algo.clean_data(data2)
algo.greed_algo()