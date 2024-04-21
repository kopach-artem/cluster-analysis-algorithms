import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import helper

    
def kmeans(data: pd.DataFrame, k: int, par1: str, par2: str, par3: str, par4: str):

    diff = 1
    step = 0
    threshold = 0.3
    diff = 1
    
    if par3 == '':
        algName = '2D'
        data = data[[par1, par2]]
        Centroids = data.sample(k) # Get random centorids from data data
        plt.scatter(data[par1], data[par2], c = 'black')
        plt.scatter(Centroids[par1], Centroids[par2], c='red')
        plt.xlabel(par1)
        plt.ylabel(par2)
        plt.show() 
    elif par4 == '':
        algName = '3D'
        data = data[[par1, par2, par3]]
        Centroids = data.sample(k) # Get random centorids from data data
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')
        img = ax.scatter(data[par1], data[par2], data[par3], c = 'black')
        centroids_img = ax.scatter(Centroids[par1], Centroids[par2], Centroids[par3], c = 'red', marker = 'x', s=100, label='Centroids')
        ax.set_xlabel(par1)
        ax.set_ylabel(par2)
        ax.set_zlabel(par3)
    else:
        algName = '4D'
        data = data[[par1, par2, par3, par4]]
        Centroids = data.sample(k) # Get random centroids from data data
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        img = ax.scatter(data[par1], data[par2], data[par3], c = data[par4], cmap = 'viridis')
        centroids_img = ax.scatter(Centroids[par1], Centroids[par2], Centroids[par3], c = 'red', marker = 'x', s = 100, label='Centroids')
        ax.set_xlabel(par1)
        ax.set_ylabel(par2)
        ax.set_zlabel(par3)  
        
        cbar = plt.colorbar(img)
        cbar.set_label(par4)
        
    plt.show()
        
    while diff != 0 and diff > threshold and step <= 40:
        tmpX = data
        i = 1
        for index1, row_c in Centroids.iterrows():
            euclDist = []
            for index2, row_d in tmpX.iterrows():
                d1 = (row_c[par1] - row_d[par1]) ** 2
                d2 = (row_c[par2] - row_d[par2]) ** 2
                if par4 != '':
                    d3 = (row_c[par3] - row_d[par3]) ** 2
                    d4 = (row_c[par4] - row_d[par4]) ** 2
                    d = np.sqrt(d1 + d2 + d3 + d4)
                elif par3 != '':
                    d3 = (row_c[par3] - row_d[par3]) ** 2
                    d = np.sqrt(d1 + d2 + d3)
                else:
                    d = np.sqrt(d1 + d2)
                euclDist.append(d)
            data.loc[:, i] = euclDist
            i = i + 1

        clusters = []
        for index,row in data.iterrows():
            min_dist = row[1]
            pos = 1
            for i in range(k):
                if row[i + 1] < min_dist:
                    min_dist = row[i+1]
                    pos = i + 1
            clusters.append(pos)
        data.loc[:, "Cluster"] = clusters
        
        
        if par4 != '':
            CentroidsNew = data.groupby(["Cluster"]).mean()[[par1, par2, par3, par4]]
        elif par3 != '':
            CentroidsNew = data.groupby(["Cluster"]).mean()[[par1, par2, par3]]
        else:
            CentroidsNew = data.groupby(["Cluster"]).mean()[[par1, par2]]
    
        if step == 0:
            diff = 1
            step += 1
        else:
            if par4 != '':
                diff = np.abs((CentroidsNew[par1] - Centroids[par1]).sum() + (CentroidsNew[par2] - Centroids[par2]).sum() + (CentroidsNew[par3] - Centroids[par3]).sum() + (CentroidsNew[par4] - Centroids[par4]).sum())
            elif par3 != '':
                diff = np.abs((CentroidsNew[par1] - Centroids[par1]).sum() + (CentroidsNew[par2] - Centroids[par2]).sum() + (CentroidsNew[par3] - Centroids[par3]).sum())
            else:
                diff = np.abs((CentroidsNew[par1] - Centroids[par1]).sum() + (CentroidsNew[par2] - Centroids[par2]).sum())
            print(f"Step is {step}  -  diffrence is {diff}")
            step += 1
            
        
        if par4 != '':
            Centroids = data.groupby(["Cluster"]).mean()[[par1, par2, par3, par4]]
        elif par3 != '':
            Centroids = data.groupby(["Cluster"]).mean()[[par1, par2, par3]]
        else:
            Centroids = data.groupby(["Cluster"]).mean()[[par1, par2]]


    if par4 != '':
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        max4 = data.max()[par4]
        min4 = data.min()[par4]
        for index, row in data.iterrows():
            print(row[par4])
            data.at[index, par4] = ((row[par4] - min4) / (max4 - min4)) * 10
        for k in range(k):
            data_k = data[data["Cluster"] == k + 1]
            img = ax.scatter(data_k[par1], data_k[par2], data_k[par3], c = helper.random_color(), s = data_k[par4] ** 2, label = f'Cluster {k+1}')

        centroids_img = ax.scatter(Centroids[par1], Centroids[par2], Centroids[par3], c='red', marker='X', s = 150, label='Centroids')

        ax.set_xlabel(par1)
        ax.set_ylabel(par2)  
        ax.set_zlabel(par3)

        cbar = plt.colorbar(img)
        cbar.set_label(par4)
    elif par3 != '':
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')  
        for k in range(k):
            data_k = data[data["Cluster"] == k + 1]
            ax.scatter(data_k[par1], data_k[par2], data_k[par3], c = helper.random_color())
        centroids_img = ax.scatter(Centroids[par1], Centroids[par2], Centroids[par3], c = 'red', marker = 'X', s = 50, label = 'Centroids')
        ax.set_xlabel(par1)
        ax.set_ylabel(par2)
        ax.set_zlabel(par3)
    else:
        for k in range(k):
            data_k = data[data["Cluster"] == k + 1]
            plt.scatter(data_k[par1], data_k[par2], c = helper.random_color())
        plt.scatter(Centroids[par1], Centroids[par2], c = 'red')
        plt.xlabel(par1)
        plt.ylabel(par2)

    next_file_number = helper.find_next_file_number(kmeans.__name__ + algName)
    filename = kmeans.__name__ + algName + '_' + str(next_file_number) + '.png'

    plt.savefig(os.path.join(helper.target_directory, filename))
    
    plt.show()