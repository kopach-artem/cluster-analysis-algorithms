import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import kmeans
from utils import helper

def run_kmeans():
    cluster_count = cluster_count_entry.get()
    cluster_axis1 = cluster_axis1_combobox.get()
    cluster_axis2 = cluster_axis2_combobox.get()
    cluster_axis3 = cluster_axis3_combobox.get()
    method = method_combobox.get()
    count = sum(1 for combo_box in [cluster_axis1_combobox, cluster_axis2_combobox, cluster_axis3_combobox] if combo_box.get())
    
    print("Running KMeans with the following parameters:")
    print("Cluster count: ", cluster_count)
    print("Cluster axis 1: ", cluster_axis1)
    print("Cluster axis 2: ", cluster_axis2)
    print("Cluster axis 3: ", cluster_axis3)
    print("Dimensions: " + str(count) + 'D')
    print("Method: ", method)
    
    
    if method == "kmeans":
        kmeans.kmeans(data, int(cluster_count_entry.get()), cluster_axis1_combobox.get(), cluster_axis2_combobox.get(), cluster_axis3_combobox.get(), cluster_axis4_combobox.get())
    elif method == "kmeans++":
        r = 2
        # kmeanspp.KMeansPlus(data, cluster_axis1_combobox.get(), cluster_axis2_combobox.get())
    else:
        r = 1
        # dbscan.DBSCANImpl(data, cluster_axis1_combobox.get(), cluster_axis2_combobox.get())
        
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


while True:
    axis_counter = 2
    file_path = filedialog.askopenfilename(initialdir="../../data_bank/raw", title="Select CSV file", filetypes=[("CSV files", "*.csv")])
    if file_path:
        data = pd.read_csv(file_path)
        print(data.head())
    else:
        raise Exception("Sorry, you do not select any file.")

    column_names = []

    for column in data.columns:
        if data[column].dtype == 'int64' or data[column].dtype == 'float':
            column_names.append(column)

    print(column_names)

    root = tk.Tk()
    root.grid(600,400,600,400)
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
    # cluster_axis1_combobox.bind("<<ComboboxSelected>>", lambda e: toggle_axis_entry())

    cluster_axis2_label = tk.Label(root, text="Cluster Axis 2:")
    cluster_axis2_label.grid(row=2, column=0, padx=5, pady=5)
    cluster_axis2_combobox = ttk.Combobox(root, values=column_names)
    cluster_axis2_combobox.grid(row=2, column=1, padx=5, pady=5)
    # cluster_axis2_combobox.bind("<<ComboboxSelected>>", lambda e: toggle_axis_entry())

    cluster_axis3_label = tk.Label(root, text="Cluster Axis 3:")
    cluster_axis3_combobox = ttk.Combobox(root, values=column_names)
    
    cluster_axis4_label = tk.Label(root, text="Cluster Axis 4:")
    cluster_axis4_combobox = ttk.Combobox(root, values=column_names)
    
    add_axis_button = tk.Button(root, text = "Add Axis", command = add_axis_entry)
    add_axis_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)


    method_label = tk.Label(root, text="Method:")
    method_label.grid(row=5, column=0, padx=5, pady=5)
    method_combobox = ttk.Combobox(root, values=["kmeans", "kmeans++", "DBSCAN"])
    method_combobox.grid(row=5, column=1, padx=5, pady=5)

    run_button = tk.Button(root, text = "Run", command = run_kmeans)
    run_button.grid(row=8, column=0, columnspan=10, padx=5, pady=5)


    root.mainloop()
    
    ans = str(input("Do you want to comntinue? y/n: "))
    
    if ans == 'y':
        continue
    else:
        break