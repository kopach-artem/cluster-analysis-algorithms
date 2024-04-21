import os
from utils import helper
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, kmeans_plusplus
from sklearn.preprocessing import StandardScaler


def kmeans_pp(data: pd.DataFrame, par1: str, par2: str):
    data = data[[par1, par2]]
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)

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

    derivative = dy / dx
    percent = wcss[0] / 100
    print(wcss)
    print(derivative)
    print(wcss[derivative.argmax()])
    print(min(wcss))
    print((wcss[derivative.argmax()] / percent) - (min(wcss) / percent))
    if (wcss[derivative.argmax()] / percent) - (min(wcss) / percent) >= 5:
        optimal_clusters = np.argmin(wcss) + 1
    else:
        optimal_clusters = derivative.argmax()
    print(optimal_clusters)
    plt.plot(x[1:], derivative)
    plt.title("Derivative of the Elbow Method")
    plt.xlabel("Number of clusters")
    plt.ylabel("Rate of change")
    plt.show()

    kmeans = KMeans(n_clusters=optimal_clusters, init="k-means++", random_state=42)
    y_kmeans = kmeans.fit_predict(data_scaled)

    # Visualising the clusters
    for i in range(1, optimal_clusters):
        data_k = data_scaled[y_kmeans == k]
    plt.scatter(
        data_scaled[y_kmeans == 0, 0],
        data_scaled[y_kmeans == 0, 1],
        s=100,
        c="red",
        label="Cluster 1",
    )
    plt.scatter(
        data_scaled[y_kmeans == 1, 0],
        data_scaled[y_kmeans == 1, 1],
        s=100,
        c="blue",
        label="Cluster 2",
    )
    plt.scatter(
        data_scaled[y_kmeans == 2, 0],
        data_scaled[y_kmeans == 2, 1],
        s=100,
        c="green",
        label="Cluster 3",
    )
    plt.scatter(
        data_scaled[y_kmeans == 3, 0],
        data_scaled[y_kmeans == 3, 1],
        s=100,
        c="cyan",
        label="Cluster 4",
    )
    plt.scatter(
        data_scaled[y_kmeans == 4, 0],
        data_scaled[y_kmeans == 4, 1],
        s=100,
        c="magenta",
        label="Cluster 5",
    )
    plt.scatter(
        kmeans.cluster_centers_[:, 0],
        kmeans.cluster_centers_[:, 1],
        s=300,
        c="yellow",
        label="Centroids",
    )
    plt.title("Clusters of customers")
    plt.xlabel(par1)
    plt.ylabel(par2)
    plt.legend()

    next_file_number = helper.find_next_file_number(KMeansPlus.__name__)
    filename = KMeansPlus.__name__ + "_" + str(next_file_number) + ".png"

    plt.savefig(os.path.join(helper.target_directory, filename))

    plt.show()
