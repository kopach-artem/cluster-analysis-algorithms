from tkinter import filedialog
import pandas as pd
import numpy as np


def my_filter(data: pd.DataFrame, r: int, par1: str, par2: str, par3: str, par4: str):
    result = data.copy()
    to_modify = []
    indexes_to_drop = set()
    result["Modified"] = False
    processed = set()

    for index_1, row_r in result.iterrows():
        if index_1 in processed or pd.isna(row_r[par1]) or pd.isna(row_r[par2]):
            continue

        current_group = [index_1]
        for index_2, row_n in result.iterrows():
            if (
                index_1 != index_2
                and index_2 not in processed
                and not (pd.isna(row_n[par1]) or pd.isna(row_n[par2]))
            ):
                d_x = (row_r[par1] - row_n[par1]) ** 2
                d_y = (row_r[par2] - row_n[par2]) ** 2
                if par4 != "":
                    d_z = (row_r[par3] - row_n[par3]) ** 2
                    d_t = (row_r[par4] - row_n[par4]) ** 2
                    distance = np.sqrt(d_x + d_y + d_z + d_t)
                elif par3 != "":
                    d_z = (row_r[par3] - row_n[par3]) ** 2
                    distance = np.sqrt(d_x + d_y + d_z)
                else:
                    distance = np.sqrt(d_x + d_y)

                if distance < r:
                    current_group.append(index_2)

        processed.update(current_group)

        if len(current_group) > 1:
            group_data = result.loc[current_group]
            avg_par1 = group_data[par1].dropna().mean()
            avg_par2 = group_data[par2].dropna().mean()
            if par4 != "":
                avg_par3 = group_data[par3].dropna().mean()
                avg_par4 = group_data[par4].dropna().mean()
                if not (
                    np.isnan(avg_par1)
                    or np.isnan(avg_par2)
                    or np.isnan(avg_par3)
                    or np.isnan(avg_par4)
                ):
                    to_modify.append(
                        {
                            par1: avg_par1,
                            par2: avg_par2,
                            par3: avg_par3,
                            par4: avg_par4,
                            "Modified": True,
                        }
                    )
                    indexes_to_drop.update(current_group)
            elif par3 != "":
                avg_par3 = group_data[par3].dropna().mean()
                if not (np.isnan(avg_par1) or np.isnan(avg_par2) or np.isnan(avg_par3)):
                    to_modify.append(
                        {
                            par1: avg_par1,
                            par2: avg_par2,
                            par3: avg_par3,
                            "Modified": True,
                        }
                    )
                    indexes_to_drop.update(current_group)
            else:
                if not (np.isnan(avg_par1) or np.isnan(avg_par2)):
                    to_modify.append({par1: avg_par1, par2: avg_par2, "Modified": True})
                    indexes_to_drop.update(current_group)

    result = result.drop(indexes_to_drop).reset_index(drop=True)
    modify_points = pd.DataFrame(to_modify)
    result = pd.concat([result, modify_points], ignore_index=True)

    return result


def remove_outliers(data: pd.DataFrame):
    for column in data.columns:
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        data = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
    return data


def remove_duplicates(data: pd.DataFrame):
    return data.drop_duplicates()


def process_data(
    data: pd.DataFrame, r: int, par1: str, par2: str, par3: str, par4: str
):
    data_r_duplicates = remove_duplicates(data)
    print(data_r_duplicates)
    data_r_outliers = remove_outliers(data_r_duplicates)
    print(data_r_outliers)
    filtered_data = my_filter(data_r_outliers, r, par1, par2, par3, par4)

    if par3 == "":
        filtered_data = filtered_data[[par1, par2]]
    elif par4 == "":
        filtered_data = filtered_data[[par1, par2, par3]]
    else:
        filtered_data = filtered_data[[par1, par2, par3, par4]]
    print(filtered_data)
    return filtered_data


"""Test"""
# file_path = filedialog.askopenfilename(
#     initialdir="../../../data_bank/raw",
#     title="Select CSV file",
#     filetypes=[("CSV files", "*.csv")],
# )
# if file_path:
#     data = pd.read_csv(file_path)
# print(data)
# remove_duplic = remove_duplicates(data[["ApplicantIncome", "LoanAmount"]])
# print(remove_duplic)
# remove_outl = remove_outliers(remove_duplic)
# print(remove_outl)
# filtered_data = my_filter(
#     remove_outl,
#     10,
#     "ApplicantIncome",
#     "LoanAmount",
# )
# print(filtered_data)
