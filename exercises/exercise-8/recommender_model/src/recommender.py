import pandas as pd

from surprise import SVD
from surprise import Reader
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import train_test_split
from surprise import dump

def train_and_package_model(data_path, model_output_path):
  df_ratings = pd.read_csv(data_path)
  reader = Reader(rating_scale=(1, 5))
  data = Dataset.load_from_df(df_ratings[['userId','movieId','rating']], reader)
  trainset, testset = train_test_split(data, test_size=.25)
  
  algo = SVD(n_factors=10, n_epochs=10, lr_all=0.001, reg_all=0.01, verbose=True)
  
  algo.fit(trainset)
    
  predictions = algo.test(testset)
  rmse = accuracy.rmse(predictions)
  print(f"Model trained with RMSE {rmse}")
  
  
  dump.dump(file_name=model_output_path, algo=algo, verbose=1)
  print(f"Model outputted to {model_output_path}")
  

if __name__ == "__main__":
  train_and_package_model('./data/ml-latest/ratings.csv', './models/model_SVD.pkl')