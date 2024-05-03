import os
from utils.helper import Helper
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from mpl_toolkits.mplot3d import Axes3D


def dbscan_clustering(data: pd.DataFrame, par1: str, par2: str, par3: str, par4: str):
    features = [par1, par2] + ([par3] if par3 else []) + ([par4] if par4 else [])
    data = data[features].dropna()
    helper = Helper()

    # Пересмотрите параметры масштабирования и DBSCAN
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    print("Scaled data:", data_scaled)

    # Подбор параметра eps, возможно, через NearestNeighbors или исходя из доменного знания
    eps_value = 0.1  # Значение eps должно быть адаптировано к распределению данных
    min_samples_value = 1

    dbscan = DBSCAN(eps=eps_value, min_samples=min_samples_value)
    labels = dbscan.fit_predict(data)
    unique_labels = np.unique(labels)

    print(f"Unique labels (clusters and noise): {unique_labels}")

    if len(features) == 2:
        plt.scatter(
            data_scaled[:, 0], data_scaled[:, 1], c=labels, cmap="viridis", marker="o"
        )
        plt.colorbar()
        plt.xlabel(par1)
        plt.ylabel(par2)
        plt.title("2D DBSCAN Clustering")
    elif len(features) == 3:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(
            data_scaled[:, 0],
            data_scaled[:, 1],
            data_scaled[:, 2],
            c=labels,
            cmap="viridis",
            marker="o",
        )
        ax.set_xlabel(par1)
        ax.set_ylabel(par2)
        ax.set_zlabel(par3)
        plt.title("3D DBSCAN Clustering")
    elif len(features) == 4:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(
            data_scaled[:, 0],
            data_scaled[:, 1],
            data_scaled[:, 2],
            c=labels,
            s=data_scaled[:, 3] * 100,
            cmap="viridis",
        )
        ax.set_xlabel(par1)
        ax.set_ylabel(par2)
        ax.set_zlabel(par3)
        cbar = plt.colorbar(ax.collections[0])
        cbar.set_label(par4)
        plt.title("4D DBSCAN Clustering")

    name_of_result = dbscan_clustering.__name__ + str(len(features)) + "D"
    next_file_number = helper.find_next_file_number(name_of_result)
    filename = name_of_result + "_" + str(next_file_number) + ".png"
    plt.savefig(os.path.join(helper.target_directory, filename))
    plt.show()
