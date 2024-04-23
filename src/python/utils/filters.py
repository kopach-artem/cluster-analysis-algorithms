import numpy as np
import pandas as pd


def my_filter(data: pd.DataFrame, r: int, par1: str, par2: str):
    # Создаем копию DataFrame, чтобы не изменять оригинальный набор данных
    result = data.copy()

    # Маркируем строки, которые нужно удалить
    to_remove = []

    # Итерируем по каждой точке
    for i in result.index:
        if i in to_remove:
            continue

        # Текущая точка
        point = result.loc[i, [par1, par2]]

        # Находим все точки в радиусе r от текущей точки
        distances = np.sqrt(
            (result[par1] - point[par1]) ** 2 + (result[par2] - point[par2]) ** 2
        )
        # neighbors = result[(distances <= r) & (distances > 0)]

        # Если есть соседи, объединяем их
        if not (distances <= r) & (distances > 0):
            combined_point = result.append(result.loc[[i]]).mean()
            result.loc[i, [par1, par2]] = combined_point[[par1, par2]]
            to_remove.extend(result.index)

    # Удаляем соседние точки, так как они уже были объединены
    result = result.drop(to_remove)

    print(data)
    print()
    print(result)
