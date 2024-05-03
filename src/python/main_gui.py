import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import numpy as np
import pandas as pd
import kmeans
import kmeanspp
import dbscan
from utils import filters
from scipy.spatial.distance import pdist


def run_clusterisation():
    cluster_count = (
        "" if cluster_count_entry.get() == "" else int(cluster_count_entry.get())
    )
    cluster_axis1 = cluster_axis1_combobox.get()
    cluster_axis2 = cluster_axis2_combobox.get()
    cluster_axis3 = cluster_axis3_combobox.get()
    cluster_axis4 = cluster_axis4_combobox.get()
    method = method_combobox.get()
    count = sum(
        1
        for combo_box in [
            cluster_axis1_combobox,
            cluster_axis2_combobox,
            cluster_axis3_combobox,
        ]
        if combo_box.get()
    )

    print("Running KMeans with the following parameters:")
    print("Cluster count: ", cluster_count)
    print("Cluster axis 1: ", cluster_axis1)
    print("Cluster axis 2: ", cluster_axis2)
    print("Cluster axis 3: ", cluster_axis3)
    print("Dimensions: " + str(count) + "D")
    print("Method: ", method)

    if cluster_axis4 != "":
        data_n = data[[cluster_axis1, cluster_axis2, cluster_axis3, cluster_axis4]]
    elif cluster_axis3 != "":
        data_n = data[[cluster_axis1, cluster_axis2, cluster_axis3]]
    else:
        data_n = data[[cluster_axis1, cluster_axis2]]

    # Рассчитываем попарные расстояния
    dist_matrix = pdist(data_n, "euclidean")

    # Находим квантиль 0.05 распределения расстояний
    radius = np.percentile(dist_matrix, 0.75)

    filtered_data = filters.process_data(
        data_n, radius, cluster_axis1, cluster_axis2, cluster_axis3, cluster_axis4
    )

    if method == "kmeans":
        kmeans.kmeans(
            filtered_data,
            cluster_count,
            cluster_axis1,
            cluster_axis2,
            cluster_axis3,
            cluster_axis4,
        )
    elif method == "kmeans++":
        kmeanspp.kmeans_pp(
            filtered_data, cluster_axis1, cluster_axis2, cluster_axis3, cluster_axis4
        )
    else:
        print(data)
        dbscan.dbscan_clustering(
            data, cluster_axis1, cluster_axis2, cluster_axis3, cluster_axis4
        )

    root.destroy()


def add_axis_entry():
    global axis_counter
    axis_counter += 1
    if axis_counter == 3:
        cluster_axis3_label.grid(row=3, column=0, padx=5, pady=5)
        cluster_axis3_combobox.grid(row=3, column=1, padx=5, pady=5)
    elif axis_counter == 4:
        cluster_axis4_label.grid(row=4, column=0, padx=5, pady=5)
        cluster_axis4_combobox.grid(row=4, column=1, padx=5, pady=5)
    else:
        print("Cannot add more than 4 clustering axes.")


def on_combobox_select(event):
    selected_option = event.widget.get()
    # Update all other comboboxes to exclude the selected option
    comboboxes = [
        cluster_axis1_combobox,
        cluster_axis2_combobox,
        cluster_axis3_combobox,
        cluster_axis4_combobox,
    ]
    for cb in comboboxes:
        if cb is not event.widget:
            current_value = cb.get()
            cb["values"] = [x for x in column_names if x != selected_option]
            if current_value == selected_option:
                cb.set("")  # Clear selection if it's the same as the newly selected


column_names = []
while True:
    axis_counter = 2
    file_path = filedialog.askopenfilename(
        initialdir="../../data_bank/raw",
        title="Select CSV file",
        filetypes=[("CSV files", "*.csv")],
    )
    if file_path:
        data = pd.read_csv(file_path)
        print(data.head())
    else:
        raise Exception("Sorry, you do not select any file.")
    column_names.append("")
    for column in data.columns:
        if data[column].dtype == "int64" or data[column].dtype == "float":
            column_names.append(column)

    print(column_names)

    root = tk.Tk()
    root.grid(600, 400, 600, 400)
    root.title("Parameters")

    root.columnconfigure(0, minsize=200)  # Cluster Count column
    root.columnconfigure(1, minsize=400)

    cluster_count_label = tk.Label(root, text="Cluster Count:")
    cluster_count_label.grid(row=0, column=0, padx=5, pady=5)
    cluster_count_entry = tk.Entry(root)
    cluster_count_entry.grid(row=0, column=1, padx=5, pady=5)

    cluster_axis1_label = tk.Label(root, text="Cluster Axis 1:")
    cluster_axis1_label.grid(row=1, column=0, padx=5, pady=5)
    cluster_axis1_combobox = ttk.Combobox(root, values=column_names)
    cluster_axis1_combobox.grid(row=1, column=1, padx=5, pady=5)

    cluster_axis2_label = tk.Label(root, text="Cluster Axis 2:")
    cluster_axis2_label.grid(row=2, column=0, padx=5, pady=5)
    cluster_axis2_combobox = ttk.Combobox(root, values=column_names)
    cluster_axis2_combobox.grid(row=2, column=1, padx=5, pady=5)

    cluster_axis3_label = tk.Label(root, text="Cluster Axis 3:")
    cluster_axis3_combobox = ttk.Combobox(root, values=column_names)

    cluster_axis4_label = tk.Label(root, text="Cluster Axis 4:")
    cluster_axis4_combobox = ttk.Combobox(root, values=column_names)

    cluster_axis1_combobox.bind("<<ComboboxSelected>>", on_combobox_select)
    cluster_axis2_combobox.bind("<<ComboboxSelected>>", on_combobox_select)
    cluster_axis3_combobox.bind("<<ComboboxSelected>>", on_combobox_select)
    cluster_axis4_combobox.bind("<<ComboboxSelected>>", on_combobox_select)

    add_axis_button = tk.Button(root, text="Add Axis", command=add_axis_entry)
    add_axis_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    method_label = tk.Label(root, text="Method:")
    method_label.grid(row=5, column=0, padx=5, pady=5)
    method_combobox = ttk.Combobox(root, values=["kmeans", "kmeans++", "DBSCAN"])
    method_combobox.grid(row=5, column=1, padx=5, pady=5)

    run_button = tk.Button(root, text="Run", command=run_clusterisation)
    run_button.grid(row=8, column=0, columnspan=10, padx=5, pady=5)

    root.mainloop()

    ans = str(input("Do you want to continue? y/n: "))

    if ans == "y":
        column_names.clear()
        continue
    else:
        break
