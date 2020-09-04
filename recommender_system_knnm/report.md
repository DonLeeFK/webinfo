## Web Lab3 Report

### 实验要求

根据训练数据中的用户评分信息，判断用户偏好，并为测试数据中 user-item 对进行评分。

### 代码实现

本实验的数据中，时间和标签意义不大。所以我组去掉了这两个标签，生成了一个只包含前3项的csv文件。

```python
reader = csv.reader(fin)
writer = csv.writer(fout)
count = 0
for line in reader:
    count =count + 1
    per = count/9517039
    line1 = line[:3]
    writer.writerow(line1)
```

```python
from surprise import KNNWithMeans
algorithm = KNNWithMeans(k=30, min_k=1, verbose=True)
```

本次实验使用了python库surprise，其中包含了各种聚类算法。我组选择了使用KNNWithMeans。

```python
kf = KFold(n_splits=2)
```

我们将测试数据通过KFold分成两半，进行两次训练，每次都用另一半来做测试，交叉验证，避免过拟合。

```python
for trainset, testset in kf.split(data):
	algorithm.fit(trainset)
	predictions = algo.test(testset)
	accuracy.rmse(predictions, verbose=True)
```

每次训练完成后，计算RMSE。

```python
accuracy.rmse(predictions, verbose=True)
```

至此，模型训练已经完成。只需要调用已经训练好的模型来进行预测。

 ```python
algorithm.predict(int(row[0]), int(row[1]))
 ```

### 实验结果

![](/Users/mac/Desktop/Screen Shot 2020-01-08 at 11.19.31 PM.png)

![](/Users/mac/Desktop/Screen Shot 2020-01-08 at 11.18.13 PM.png)

