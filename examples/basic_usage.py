from my_project import mmath as mm
from my_project import mdata_reader as mr
from my_project import ml as ml

train_data = mr.read_data('examples/train_data.txt', sep=',', header=True)
test_data = mr.read_data('examples/test_data.txt', sep=',', header=True)

target = 'length'
arg = 'width'

X_train, y_train = train_data[arg], train_data[target]
X_test, y_test = test_data[arg], test_data[target]

model = ml.Linear_Regression(learning_rate=0.0001, n_epochs=10)
model.fit(X_train, y_train)
predicts = model.predict(X_test)

def mean_absolute_error(predicts, y_test):
    test_losses_ = []
    for i in range(predicts.size[0]):
        test_losses_.append(abs(y_test[i][0] - predicts[i][0]))
    return sum(test_losses_) / len(test_losses_)

test_res = mean_absolute_error(predicts, y_test)
print(f'Средняя абсолютная ошибка модели: {test_res:.2f} ед.')