import os
import pandas as pd
from surprise import SVD
from surprise import KNNWithMeans
from surprise import Dataset
from surprise import Reader
from surprise import dump
from surprise.model_selection import train_test_split
from surprise.model_selection import cross_validate
from surprise import accuracy
from surprise.model_selection import KFold

df = pd.read_csv('train.csv', encoding='utf-8')
reader = Reader(rating_scale=(0, 5))
data = Dataset.load_from_df(df, reader)

print('Reading finished!')

kf = KFold(n_splits=2)
algo = KNNWithMeans(k=30, min_k=1, verbose=True)

count = 0
for trainset, testset in kf.split(data):
    count = count + 1
    print('Training round: ' + str(count))
    # 训练并测试算法
    print('Training')
    algo.fit(trainset)
    print('Train completed!')
    #if count is 1:
        #break
    print('Variating')
    predictions = algo.test(testset)
    print('Variation completed!')

    # 计算并打印 RMSE（均方根误差，Root Mean Squared Error）
    accuracy.rmse(predictions, verbose=True)

# 保存模型
dump.dump('saved_model_knnm.model', algo=algo, verbose=1)

# 生成结果
fo = open('submission.txt', 'w', encoding='utf-8')
with open('test.txt', 'r', encoding='utf-8') as f:
    for line in f:
        row = line.split(',')
        fo.write(str(algo.predict(int(row[0]), int(row[1])).est) + '\n')
fo.close()
