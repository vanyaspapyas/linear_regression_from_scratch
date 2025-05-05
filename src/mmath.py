from __future__ import annotations
from typing import Optional, List, Union, Tuple, Any, Self
from copy import deepcopy

class Matrix:
    '''Класс реализующий матрицы
    
    Attributes:
        values (list): Все значения
        size (tuple): Размер матрицы
    
    '''
    def __init__(self, values: List[List[Union[int, float]]], size: Optional[tuple] = None) -> None:
        '''
        Инициализация матрицы
        
        Args:
            values (list): Начальные значения матрицы
            size (tuple): Размеры матрицы
        '''
        if not values:
            raise ValueError('values должно быть матрицей')
        
        if not all(len(row) == len(values[0]) for row in values):
            raise ValueError('все строки матрицы должны быть одинаковой длины')
        
        rows, cols = len(values), len(values[0])
        
        if size is None:
            self.values = deepcopy(values)
            self.size = (rows, cols)
            
        if size and (not isinstance(size, (tuple)) or len(size) != 2):
            raise ValueError('size должен быть кортежем из 2ух положительных чисел')
        elif size:
            self.size = size
            
            new_rows, new_cols = self.size
            flat_matrx = [elem for row in values for elem in row]
        
            self.values = []
            idx = 0
            for _ in range(new_rows):
                row = []
                for _ in range(new_cols):
                    if idx < len(flat_matrx):
                        row.append(flat_matrx[idx])
                        idx += 1
                    else:
                        row.append(0)
                self.values.append(row)
    
    
    def __getitem__(self, idx: int):
        '''
        Доступ к элементу матрицы по индексу
        '''
        return self.values[idx]
    
    def __setitem__(self, idx: Union[int, Tuple[int, int]], value: Union[int, float, List[Union[int, float]]]):
        '''
        Изменений значения матрицы по индексу
        '''
        if isinstance(idx, tuple):
            if not isinstance(value, (int, float)):
                raise TypeError("Для элемента значение должно быть int или float")
            row, col = idx
            self.values[row][col] = value
        else:
            if not isinstance(value, list):
                raise TypeError("Для строки значение должно быть списком")
            if len(value) != len(self.values[0]):
                raise ValueError("Длина списка не совпадает с шириной матрицы")
            self.values[idx] = value
    
    def __add__(self, other: Union[Matrix, int, float]) -> Matrix:
        '''
        Сложение двух матриц 
        
        Args:
            other (matrix): матрица для сложения с исходной матрицей
            
        Returns:
            Matrix: возвращает результат в виде нового экземпляра матрицы
        '''
        result = deepcopy(self.values)
        if isinstance(other, Matrix):
            if self.size != other.size:
                raise ValueError('размеры матриц не совпадают')
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    result[i][j] += other.values[i][j]
        elif isinstance(other, (int, float)):
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    result[i][j] += other
        return Matrix(result)
    
    def __iadd__(self, other: Union[Matrix, int, float]) -> 'Matrix':
        '''
        Сложение двух матриц на месте
        
        Args:
            other (matrix): матрица для сложения с исходной матрицей
        '''
        if isinstance(other, Matrix):
            if self.size != other.size:
                raise ValueError('размеры матриц не совпадают')
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    self.values[i][j] += other[i][j]
        elif isinstance(other, (int, float)):
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    self.values[i][j] += other
        return self
    
    
    def __mul__(self, other: Union[int, float]) -> Matrix:
        '''
        Умножение матрицы на скаляр
        
        Args:
            other (int | float): скаляр для умножения
            
        Returns: 
            Matrix: возвращает результат в виде нового экземпляра матрицы
        '''
        result = deepcopy(self.values)
        if not isinstance(other, (int, float)):
            raise ValueError('только int и float типы')
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                result[i][j] *= other
        return Matrix(result)
    
    
    def __imul__(self, other: Union[int, float]) -> Self:
        '''
        Умножение матрицы на скаляр на месте
        
        Args:
            other (int | float): скаляр для умножения 
        '''
        if not isinstance(other, (int, float)):
            raise ValueError('только int и float типы')
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.values[i][j] *= other
        return self
    
    
    def __repr__(self):
        return '\n'.join([str(x) for x in self.values])
    
    
    def __str__(self):
        return self.__repr__()
    
    
    def reshape(self, rows: int, cols: int) -> None:
        '''Изменение размера матрицы на месте, пустые элементы заменяются нулём
        
        Args:
            size (tuple): итоговый размер матрицы
        '''
        flat_matrx = [elem for row in self.values for elem in row]
        
        updated_values = []
        idx = 0
        for _ in range(rows):
            row = []
            for _ in range(cols):
                if idx < len(flat_matrx):
                    row.append(flat_matrx[idx])
                    idx += 1
                else:
                    row.append(0)
            updated_values.append(row)  
        self.values = updated_values 
    
        
    def matmul(self, other: Matrix) -> Matrix:
        '''
        Умножение двух матрицы
        
        Args:
            other (Matrix): матрица 'B' для перемножения типа AxB
        
        Returns:
            Matrix: возвращает результат в виде нового экземляра матрицы
        '''
        
        if not isinstance(other, Matrix):
            raise ValueError('только для матриц')
        if self.size[1] != other.size[0]:
            raise ValueError('размеры матриц не совпадают')
        result = ZeroMatrix(size=(self.size[0], other.size[1]))
        for i in range(self.size[0]):
            for j in range(other.size[1]):
                for k in range(self.size[1]):
                    result.values[i][j] += self.values[i][k] * other.values[k][j]

        return Matrix(result.values)
    

    
    def T(self) -> Self:
        '''
        Транспонирование матрицы
        '''
        
        self.values = [list(row) for row in zip(*self.values)]
        
        return self
    
    def addcol(self, other: Union[List, Tuple]) -> Self:
        '''
        Добавление заданного столбца(column) в исходную матрицу
        
        Args:
            other (List | Tuple): столбец для добавления
        '''
        if not isinstance(other, (list, tuple)):
            raise ValueError('только list ил tuple')
        if len(other) != len(self.values):
            raise ValueError('размеры не совпадают')
        
        extra_col = self.size[1]
        
        result = ZeroMatrix((self.size[0], self.size[1] + 1))
        for i in range(result.size[0]):
            for j in range(result.size[1]):
                if j == extra_col:
                    result[i][j] = other[i]
                else:
                    result.values[i][j] = self.values[i][j]
        self.values = deepcopy(result.values)
        self.size = self._update_size()
        
        return self
    
    
    def addrow(self, other: Union[List, Tuple]) -> Self:
        '''
        Добавления новой строки(row) в исходную матрицу
        
        Args:
            other (List | Tuple): строка для добавления
            
        Returns:
            Self
        '''
        
        if not isinstance(other, (list, tuple)):
            raise ValueError('только list ил tuple')
        if len(other) != len(self.values[0]):
            raise ValueError('размеры не совпадают')
        
        extra_row = self.size[0]
        
        result = ZeroMatrix((self.size[0] + 1, self.size[1]))
        for i in range(result.size[0]):
            for j in range(result.size[1]):
                if i == extra_row:
                    result[i][j] = other[i]
                else:
                    result.values[i][j] = self.values[i][j]
        self.values = deepcopy(result.values)
        self.size = self._update_size()
        
        return self
                
    def _update_size(self):
        return len(self.values), len(self.values[0])
    
    

class ZeroMatrix(Matrix):
    def __init__(self, size):
        super().__init__([[0]], size)
        