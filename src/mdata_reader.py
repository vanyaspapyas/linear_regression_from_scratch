from __future__ import annotations
from typing import Optional, List, Union, Tuple, Any, Self
from mmath import Matrix


class DataFrame(Matrix):
    
    def __init__(self, data, labels=None):
        self.labels = labels if labels else False
        super().__init__(data)
            
    def __repr__(self):
        res = ''
        max_len = max(map(len, self.labels)) if self.labels else 8
        sep_line = '-' * ((max_len + 3) * len(self.values[0])) + '-\n'
        if self.labels:
            res += sep_line
            for name in self.labels:
                res += f'| {name:^{max_len}} '
            res += '|\n' + sep_line
        else:
            res += sep_line
        for i in range(min(5, len(self.values))):
            line_data = self.values[i]
            for number in line_data:
                res += f'| {str(number):^{max_len}} '
            res += '|\n'
        res += sep_line + f'size: {self.size[0]} rows x {self.size[1]} columns'
        return res
    
    def __str__(self):
        return self.__repr__()
    
    def __getitem__(self, idx: int | slice | str | list[str]) -> Matrix:
        '''
        Извлечение данных из таблицы
        В случае с извлечением по названию

        '''
        if not isinstance(idx, (int, slice, str, list)):
            raise ValueError('Индексы могут быть только числами, срезами или строками в случае с наличием заголовков')
        res = []
        if isinstance(idx, int):
            for i in range(len(self.values)):
                res.append([self.values[i][idx]])
        elif isinstance(idx, slice):
            for i in range(len(self.values)):
                res.append(self.values[i][idx])
        else:
            if not self.labels:
                raise ValueError('Заголовки отсутствуют')
            if isinstance(idx, str):
                idx = int(self.labels.index(idx))
                for i in range(len(self.values)):
                    res.append([self.values[i][idx]])
            else:
                for label in idx:
                    current_idx = self.labels.index(label)
                    if not res:
                        current_res = []
                        for i in range(len(self.values)):
                            current_res.append([self.values[i][current_idx]])
                        result = Matrix(current_res)
                    else:
                        current_res = []
                        for i in range(len(self.values)):
                            current_res.append(self.values[i][current_idx])
                        result.addcol(current_res)
                return result
                
        
        return Matrix(res)
            

def read_data(data, sep: str = ' ', header = True) -> DataFrame:
    with open(data, 'r') as f:
        if header:
            labels = [x for x in f.readline().strip().split(sep)]
        res = []
        for line in f:
            res.append([int(x) for x in line.strip().split(sep)])
        return DataFrame(res, labels) if header else DataFrame(res)
    

