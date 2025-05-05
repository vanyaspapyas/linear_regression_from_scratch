from __future__ import annotations
from typing import Optional, List, Union, Tuple, Any, Self
from copy import deepcopy

class Matrix:
    '''
    Матрица для хранения числовых данных в виде матриц
    ----------
    
    Параметры
    ----------
    values: list[list[int | float]]
        Стартовые значения матрицы данных
    size: tuple(int, int)
        Размер матрицы
        
    Атрибуты
    ----------
    values: list[list[int | float]]
        Значения матрицы данных
    size: tuple(int, int)
        Текущий размер матрицы
    '''
    def __init__(self, values: List[List[Union[int, float]]], size: Optional[Tuple[int, int]] = None) -> None:
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
    
    
    def __getitem__(self, idx: Union[int, Tuple[int, int]]):
        '''
        Доступ к элементу матрицы по индексу
        ----------
        
        Параметры
        ----------
        idx: int
            Индекс элементы   
        '''
        if isinstance(idx, int):
            return self.values[idx]
        elif isinstance(idx, tuple):
            row, col = idx
            return self.values[row][col]
    
    def __setitem__(self, idx: Union[int, Tuple[int, int]], value: Union[int, float, List[Union[int, float]]]):
        '''
        Изменений значения матрицы по индексу
        ----------
        
        Параметры
        ----------
        idx: int | tuple(int, int)
            Индекс элемента
        value: int | float | list[int | float]
            Новые значения элементов матрицы
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
        Сложение матрицы с числом или другой матрицей
        ----------
        
        Параметры
        ----------
        other: Matrix | int | float
            Элемент с которым складывается исходная матрица
        
        Возвращает
        ----------
        Matrix
            Новый экземпляр матрицы
        '''
        if not isinstance(other, (Matrix, int, float)):
            raise ValueError('сложение поддерживает только Matrix, int и float типы')
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
    
    def __iadd__(self, other: Union[Matrix, int, float]) -> Self:
        '''
        Сложение матрицы с числом или другой матрицей на месте
        ----------
        
        Параметры
        ----------
        other: Matrix | int | float
            Элемент с которым складывается исходная матрицы
            
        Возвращает
        ----------
        self
        '''
        if not isinstance(other, (Matrix, int, float)):
            raise ValueError('сложение поддерживает только Matrix, int и float типы')
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
    
    def __sub__(self, other: Union[Matrix, int, float]) -> Matrix:
        '''
        Вычитание из матрицы числа или другой матрицы 
        ----------
        
        Параметры
        other: Matrix | int | float
            Элемент который вычитается из исходной матрицы
            
        Возвращает
        ----------
        Matrix
            Новый экземпляр матрицы
        '''
        if not isinstance(other, (Matrix, int, float)):
            raise ValueError('вычитание поддерживает только Matrix, int и float типы')
        result = deepcopy(self.values)
        if isinstance(other, Matrix):
            if self.size != other.size:
                raise ValueError('размеры матриц не совпадают')
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    result[i][j] -= other.values[i][j]
        elif isinstance(other, (int, float)):
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    result[i][j] -= other
        return Matrix(result)
    
    def __isub__(self, other: Union[Matrix, int, float]) -> Self:
        '''
        Вычитание из матрицы числа или другой матрицы на месте
        ----------
        
        Параметры
        other: Matrix | int | float
            Элемент который вычитается из исходной матрицы
            
        Возвращает
        ----------
        self
        '''
        if not isinstance(other, (Matrix, int, float)):
            raise ValueError('вычитание поддерживает только Matrix, int и float типы')
        if isinstance(other, Matrix):
            if self.size != other.size:
                raise ValueError('размеры матриц не совпадают')
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    self.values[i][j] -= other.values[i][j]
        elif isinstance(other, (int, float)):
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    self.values[i][j] -= other
        return self
    
    def __mul__(self, other: Union[int, float]) -> Matrix:
        '''
        Умножение матрицы на число
        ----------
        
        Параметры
        other: int | float
            Число на который умножается исходная матрицы
            
        Возвращает:
        Matrix
            Новый эземлпяр матрицы
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
        Умножение матрицы на число на месте
        ----------
        
        Параметры
        ----------
        other: int | float
            Число на который умножается исходная матрицы
        
        Возвращает
        ----------
        self
        '''
        if not isinstance(other, (int, float)):
            raise ValueError('только int и float типы')
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.values[i][j] *= other
        return self
    
    
    def __repr__(self):
        '''
        Наглядное отображение содержимого матрицы
        ----------
        
        Пример
        ----------
        [1, 2, 3, 4]\n
        [5, 6, 7, 8]\n
        [9, 10, 11, 12]\n
        [13, 14, 15, 16]\n
        '''
        return '\n'.join([str(x) for x in self.values])
    
    
    def __str__(self):
        '''
        Наглядное отображение содержимого матрицы
        Возвращает __repr__()
        '''
        return self.__repr__()
    
    
    def reshape(self, rows: int, cols: int) -> None:
        '''
        Изменение размера матрицы на месте, пустые элементы, если они имеются, заменяются нулями
        ----------
        
        Параметры
        ----------
        rows: int
            Итоговой количество строк в матрице
        cols: int
            Итоговой количество столбцов в матрицу
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
        Перемножение двух матриц между собой (self @ other)
        ----------
        
        Параметры
        ----------
        other: Matrix
            Матрица на которую умножается исходная матрица
            
        Возвращает
        ----------
        Matrix
        Новый экземпляр матрицы с результатом перемножения
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
    
    def T(self) -> None:
        '''
        Транспонирование матрицы на месте
        ----------
        '''
        self.values = [list(row) for row in zip(*self.values)]
    
    def addcol(self, other: Union[List, Tuple]) -> Self:
        '''
        Добавление заданного столбца в исходную матрицу
        
        Параметры
        ----------
        other: list | tuple
            Столбец для добавления в матрицу
            
        Возвращает
        ----------
        self
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
        Добавления новой строки в исходную матрицу
        
        Параметры
        ----------
        other: list | tuple
            Строка для добавления в матрицу
            
        Возвращает
        ----------
        self
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
        '''
        Метод для обновления информации о текущем размере матрицы
        ----------
        '''
        return len(self.values), len(self.values[0])
    
    

class ZeroMatrix(Matrix):
    '''
    Матрица необходимого размера полностью заполненная нулями
    ----------
    
    Параметры
    ----------
    size: tuple(int, int)
        Размер нулевой матрицы
    '''
    def __init__(self, size: Tuple[int, int]):
        super().__init__([[0]], size)