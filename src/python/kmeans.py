import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import helper


def kmeans(data: pd.DataFrame, k: int, par1: str, par2: str, par3: str, par4: str):

    diff = 1
    step = 0
    threshold = 0.3

    if par3 == "":
        alg_name = "2D"
        data = data[[par1, par2]]
        centroids = data.sample(k)  # Get random centorids from data data
        plt.scatter(data[par1], data[par2], c="black")
        plt.scatter(centroids[par1], centroids[par2], c="red")
        plt.xlabel(par1)
        plt.ylabel(par2)
        plt.show()
    elif par4 == "":
        alg_name = "3D"
        data = data[[par1, par2, par3]]
        centroids = data.sample(k)  # Get random centorids from data data
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        img = ax.scatter(data[par1], data[par2], data[par3], c="black")
        centroids_img = ax.scatter(
            centroids[par1],
            centroids[par2],
            centroids[par3],
            c="red",
            marker="x",
            s=100,
            label="Centroids",
        )
        ax.set_xlabel(par1)
        ax.set_ylabel(par2)
        ax.set_zlabel(par3)
    else:
        alg_name = "4D"
        data = data[[par1, par2, par3, par4]]
        centroids = data.sample(k)  # Get random centroids from data data
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        img = ax.scatter(
            data[par1], data[par2], data[par3], c=data[par4], cmap="viridis"
        )
        centroids_img = ax.scatter(
            centroids[par1],
            centroids[par2],
            centroids[par3],
            c="red",
            marker="x",
            s=100,
            label="Centroids",
        )
        ax.set_xlabel(par1)
        ax.set_ylabel(par2)
        ax.set_zlabel(par3)

        cbar = plt.colorbar(img)
        cbar.set_label(par4)

    plt.show()

    while diff != 0 and diff > threshold and step <= 40:
        tmp_data = data
        i = 1
        for index_1, row_c in centroids.iterrows():
            eucl_distance = []
            for index_2, row_d in tmp_data.iterrows():
                d1 = (row_c[par1] - row_d[par1]) ** 2
                d2 = (row_c[par2] - row_d[par2]) ** 2
                if par4 != "":
                    d3 = (row_c[par3] - row_d[par3]) ** 2
                    d4 = (row_c[par4] - row_d[par4]) ** 2
                    d = np.sqrt(d1 + d2 + d3 + d4)
                elif par3 != "":
                    d3 = (row_c[par3] - row_d[par3]) ** 2
                    d = np.sqrt(d1 + d2 + d3)
                else:
                    d = np.sqrt(d1 + d2)
                eucl_distance.append(d)
            data.loc[:, i] = eucl_distance
            i = i + 1

        clusters = []
        for index, row in data.iterrows():
            min_dist = row[1]
            pos = 1
            for l in range(k):
                if row[l + 1] < min_dist:
                    min_dist = row[l + 1]
                    pos = l + 1
            clusters.append(pos)
        data.loc[:, "Cluster"] = clusters

        if par4 != "":
            centroids_new = data.groupby(["Cluster"]).mean()[[par1, par2, par3, par4]]
        elif par3 != "":
            centroids_new = data.groupby(["Cluster"]).mean()[[par1, par2, par3]]
        else:
            centroids_new = data.groupby(["Cluster"]).mean()[[par1, par2]]

        if step == 0:
            diff = 1
            step += 1
            print(f"Step is {step}  -  diffrence is {diff}")
        else:
            if par4 != "":
                diff = np.abs(
                    (centroids_new[par1] - centroids[par1]).sum()
                    + (centroids_new[par2] - centroids[par2]).sum()
                    + (centroids_new[par3] - centroids[par3]).sum()
                    + (centroids_new[par4] - centroids[par4]).sum()
                )
            elif par3 != "":
                diff = np.abs(
                    (centroids_new[par1] - centroids[par1]).sum()
                    + (centroids_new[par2] - centroids[par2]).sum()
                    + (centroids_new[par3] - centroids[par3]).sum()
                )
            else:
                diff = np.abs(
                    (centroids_new[par1] - centroids[par1]).sum()
                    + (centroids_new[par2] - centroids[par2]).sum()
                )
            step += 1
            print(f"Step is {step}  -  diffrence is {diff}")

        if par4 != "":
            centroids = data.groupby(["Cluster"]).mean()[[par1, par2, par3, par4]]
        elif par3 != "":
            centroids = data.groupby(["Cluster"]).mean()[[par1, par2, par3]]
        else:
            centroids = data.groupby(["Cluster"]).mean()[[par1, par2]]

    if par4 != "":
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        par4_max = data.max()[par4]
        par4_min = data.min()[par4]
        for index, row in data.iterrows():
            # print(row[par4])
            data.at[index, par4] = ((row[par4] - par4_min) / (par4_max - par4_min)) * 10
        for cluster in range(k):
            data_at_cluster = data[data["Cluster"] == cluster + 1]
            img = ax.scatter(
                data_at_cluster[par1],
                data_at_cluster[par2],
                data_at_cluster[par3],
                c=helper.random_color(),
                s=data_at_cluster[par4] ** 2,
                label=f"Cluster {cluster + 1}",
            )

        centroids_img = ax.scatter(
            centroids[par1],
            centroids[par2],
            centroids[par3],
            c="red",
            marker="X",
            s=150,
            label="Centroids",
        )

        ax.set_xlabel(par1)
        ax.set_ylabel(par2)
        ax.set_zlabel(par3)

        # cbar = plt.colorbar(img)
        cbar.set_label(par4)
    elif par3 != "":
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        for cluster in range(k):
            data_at_cluster = data[data["Cluster"] == cluster + 1]
            ax.scatter(
                data_at_cluster[par1],
                data_at_cluster[par2],
                data_at_cluster[par3],
                c=helper.random_color(),
            )
        centroids_img = ax.scatter(
            centroids[par1],
            centroids[par2],
            centroids[par3],
            c="red",
            marker="X",
            s=50,
            label="Centroids",
        )
        ax.set_xlabel(par1)
        ax.set_ylabel(par2)
        ax.set_zlabel(par3)
    else:
        for cluster in range(k):
            data_at_cluster = data[data["Cluster"] == cluster + 1]
            plt.scatter(
                data_at_cluster[par1], data_at_cluster[par2], c=helper.random_color()
            )
        plt.scatter(centroids[par1], centroids[par2], c="red")
        plt.xlabel(par1)
        plt.ylabel(par2)

    next_file_number = helper.find_next_file_number(kmeans.__name__ + alg_name)
    file_name = kmeans.__name__ + alg_name + "_" + str(next_file_number) + ".png"

    plt.savefig(os.path.join(helper.target_directory, file_name))
    plt.show()
