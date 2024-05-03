import os
from utils.helper import Helper
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def kmeans_pp(data: pd.DataFrame, par1: str, par2: str, par3: str = "", par4: str = ""):
    features = [par1, par2] + ([par3] if par3 else []) + ([par4] if par4 else [])
    data = data.dropna()
    helper = Helper()

    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    print(data_scaled)
    # statistics of scaled data
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init="k-means++")
        kmeans.fit(data_scaled)
        wcss.append(kmeans.inertia_)

    # Визуализация метода локтя
    plt.plot(range(1, 11), wcss)
    plt.title("The Elbow Method")
    plt.xlabel("Number of clusters")
    plt.ylabel("WCSS")
    plt.show()

    x = np.arange(1, 11)
    y = wcss
    dy = np.diff(y)
    dx = np.diff(x)

    optimal_clusters = np.argmin(np.diff(np.diff(wcss))) + 3

    kmeans = KMeans(n_clusters=optimal_clusters, init="k-means++", random_state=42)
    y_kmeans = kmeans.fit_predict(data_scaled)

    # Вывод информации о каждом кластере
    for cluster in range(optimal_clusters):
        data_at_cluster = data_scaled[y_kmeans == cluster]
        print(f"Cluster {cluster + 1}:")
        print(data_at_cluster)  # Вывод данных кластера

    # Опционально: Визуализация кластеров
    if len(features) == 2:
        plt.scatter(data_scaled[:, 0], data_scaled[:, 1], c=y_kmeans, cmap="viridis")
        centers = kmeans.cluster_centers_
        plt.scatter(
            centers[:, 0], centers[:, 1], c="red", s=300, alpha=0.75
        )  # Центроиды кластеров
        plt.xlabel(par1)
        plt.ylabel(par2)
        plt.title("Cluster Visualization")
    elif len(features) == 3:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(
            data_scaled[:, 0],
            data_scaled[:, 1],
            data_scaled[:, 2],
            c=y_kmeans,
            cmap="viridis",
        )
        centers = kmeans.cluster_centers_
        ax.scatter(
            centers[:, 0], centers[:, 1], centers[:, 2], c="red", s=300, alpha=0.75
        )
        ax.set_xlabel(par1)
        ax.set_ylabel(par2)
        ax.set_zlabel(par3)
        plt.title("3D Cluster Visualization")
    else:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        # print(data_scaled)
        # data_scaled = scaler.inverse_transform(data_scaled)
        # centers = scaler.inverse_transform(kmeans.cluster_centers_)
        ax.scatter(
            data_scaled[:, 0],
            data_scaled[:, 1],
            data_scaled[:, 2],
            c=y_kmeans,
            s=data_scaled[:, 3] * 100,
            cmap="viridis",
        )
        centers = kmeans.cluster_centers_
        # Центроиды
        ax.scatter(
            centers[:, 0], centers[:, 1], centers[:, 2], c="red", s=300, alpha=0.75
        )

        ax.set_xlabel(par1)
        ax.set_ylabel(par2)
        ax.set_zlabel(par3)

        # Легенда и цветовая шкала
        # plt.legend()
        cbar = plt.colorbar(ax.collections[0])  # Первая коллекция точек в графике
        cbar.set_label(par4)

        plt.title(f"4D KMeans Clustering with {optimal_clusters} Clusters")

    name_of_result = kmeans_pp.__name__ + str(len(features)) + "D"
    next_file_number = helper.find_next_file_number(name_of_result)
    filename = name_of_result + "_" + str(next_file_number) + ".png"
    plt.savefig(os.path.join(helper.target_directory, filename))
    plt.show()
