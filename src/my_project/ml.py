from __future__ import annotations
from typing import Optional, List, Union, Tuple, Any, Self
import my_project.mmath as mm 

class Linear_Regression:
    '''
    Линейная регрессия
    ----------
    
    Параметры
    ----------
    learning_rate: float
        Скорость обучения между 0 и 1
    n_epochs: int
        Количество эпох
        
    Атрибуты
    ----------
    w_: Matrix
        Веса после обучения
    b_: Matrix
        Смещение после обучения
    losses_: list[int | float]
        Значения потерь на каждой из эпох обучения
    '''
    
    def __init__(self, learning_rate: float = 0.01, n_epochs: int = 100):
        self.learning_rate = learning_rate
        self.n_epochs = n_epochs
        
    
    def fit(self, X: mm.Matrix, y: mm.Matrix):
        '''
        Обучение модели
        ----------
        
        Параметры
        ----------
        X: Matrix
            Матрица содержащая обучающие данные
        y: Matrix
            Вектор целевых значений для обучающих данных
        '''
        
        self.w_ = mm.ZeroMatrix(size=(X.size[1], 1))
        self.b_ = 0.0
        self.losses_ = []
        
        for epoch in range(self.n_epochs):
            lr_input = self.activation(X)
            errors = y - lr_input
            self.w_ += self.learning_rate * 2.0 * X.T().matmul(errors) / X.size[0]
            self.b_ += self.learning_rate * 2.0 * errors.mean()
            loss = (errors**2).mean()
            self.losses_.append(loss)
            
    def activation(self, X):
        return X.matmul(self.w_) + self.b_
    
    def predict(self, X):
        return self.activation(X) if isinstance(X, mm.Matrix) else self.activation(mm.Matrix([X]))
    