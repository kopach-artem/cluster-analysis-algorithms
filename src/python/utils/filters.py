import numpy as np
import pandas as pd


def my_filter(data: pd.DataFrame, r: int, par1: str, par2: str):
    result = data.drop_duplicates([par1, par2])[[par1, par2]]
    modified = False
    result["Modified"] = modified
    # print(result)

    for index_1, row_r in result.iterrows():
        for index_2, row_n in result.iterrows():
            distances = np.sqrt(
                (row_r[par1] - row_n[par1]) ** 2 + (row_r[par2] - row_n[par2]) ** 2
            )
            if (
                index_1 >= index_2 or modified or distances >= r
            ):  # Avoid repeat comparisons
                continue
            else:
                par1_aver = (row_r[par1] + row_n[par1]) // 2
                par2_aver = (row_r[par2] + row_n[par2]) // 2
                modify_point = {
                    par1: par1_aver,
                    par2: par2_aver,
                    "Modified": True,
                }
                result.drop(index_1, inplace=True)
                result.drop(index_2, inplace=True)
                result = result._append(modify_point, ignore_index=True)

    return result


data = pd.read_csv("../../../data_bank/raw/clustering.csv")
my_filter(data, 7, "ApplicantIncome", "LoanAmount")
