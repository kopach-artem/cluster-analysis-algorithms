import numpy as np
import pandas as pd


def my_filter(data: pd.DataFrame, r: int, par1: str, par2: str):
    result = data.copy()
    to_modify = []
    indexes_to_drop = []

    print(result)

    for index_1, row_r in result.iterrows():
        for index_2, row_n in result.iterrows():
            if (
                index_1 >= index_2
                or index_1 in indexes_to_drop
                or index_2 in indexes_to_drop
            ):
                continue

            distances = np.sqrt(
                (row_r[par1] - row_n[par1]) ** 2 + (row_r[par2] - row_n[par2]) ** 2
            )
            if distances < r:
                par1_aver = (row_r[par1] + row_n[par1]) / 2
                par2_aver = (row_r[par2] + row_n[par2]) / 2
                to_modify.append({par1: par1_aver, par2: par2_aver, "Modified": True})
                indexes_to_drop.extend([index_1, index_2])

    result = result.drop(indexes_to_drop).reset_index(drop=True)

    modify_points = pd.DataFrame(to_modify)
    result = result._append(modify_points, ignore_index=True)
    return result


# data = pd.read_csv("../../data_bank/raw/proba.csv")
# filtered_data = my_filter(data, 200, "ApplicantIncome", "LoanAmount")
# print(filtered_data)
