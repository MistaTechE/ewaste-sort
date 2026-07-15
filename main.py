#main.py
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class InventoryMatcherApp:

  def __init__(self, root):
    self.root = root
    self.root.title("eWaste Inventory Matcher")
    self.root.geometry("900x300")
    self.root.resizable(False, False)
    self.ewaste_file = tk.StringVar()
    self.inventory_file = tk.StringVar()
    self.output_file = tk.StringVar()
    self.build_gui()

  def build_gui(self):

    padding = {'padx': 10, 'pady': 8}
    ttk.Label(
        self.root,
        text="eWaste Inventory Matcher",
        font=("Segoe UI", 16, "bold")
    ).grid(row=0, column=0, columnspan=3, pady=15)

    ttk.Label(self.root, text="eWaste CSV").grid(row=1, column=0, sticky="w", **padding)

    ttk.Entry(
        self.root,
        textvariable=self.ewaste_file,
        width=60
    ).grid(row=1, column=1)

    ttk.Button(
        self.root,
        text="Browse",
        command=self.select_ewaste
    ).grid(row=1, column=2)

    ttk.Label(self.root, text="Inventory CSV").grid(row=2, column=0, sticky="w", **padding)

    ttk.Entry(
        self.root,
        textvariable=self.inventory_file,
        width=60
    ).grid(row=2, column=1)

    ttk.Button(
        self.root,
        text="Browse",
        command=self.select_inventory
    ).grid(row=2, column=2)

    ttk.Label(self.root, text="Output CSV").grid(row=3, column=0, sticky="w", **padding)

    ttk.Entry(
        self.root,
        textvariable=self.output_file,
        width=60
    ).grid(row=3, column=1)

    ttk.Button(
        self.root,
        text="Save As",
        command=self.select_output
    ).grid(row=3, column=2)

    ttk.Button(
        self.root,
        text="Process Files",
        command=self.process_files
    ).grid(row=4, column=0, columnspan=3, pady=20)

    self.status = ttk.Label(
        self.root,
        text="Ready",
        foreground="blue"
    )

    self.status.grid(row=5, column=0, columnspan=3)

  def select_ewaste(self):
    filename = filedialog.askopenfilename(
      title="Select eWaste CSV",
      filetypes=[("CSV Files", "*.csv")]
    )
    if filename:
      self.ewaste_file.set(filename)

  def select_inventory(self):
    filename = filedialog.askopenfilename(
        title="Select Inventory CSV",
        filetypes=[("CSV Files", "*.csv")]
    )
    if filename:
      self.inventory_file.set(filename)

  def select_output(self):
    filename = filedialog.asksaveasfilename(
      title="Save Output As",
      defaultextension=".csv",
      filetypes=[("CSV Files", "*.csv")],
      initialfile="Filtered_Inventory.csv"
    )
    if filename:
      self.output_file.set(filename)


  def process_files(self):

    ewaste = pd.read_csv(
        self.ewaste_file.get(),
        dtype=str
    ).fillna("")

    inventory = pd.read_csv(
        self.inventory_file.get(),
        dtype=str
    ).fillna("")

    # Clean State Tags
    ewaste["State Tag"] = ewaste["State Tag"].str.strip()
    inventory["State Tag"] = inventory["State Tag"].str.strip()

    # Match inventory records to eWaste State Tags
    filtered_inventory = inventory[
        inventory["State Tag"].isin(ewaste["State Tag"])
    ]

    # Write output CSV
    filtered_inventory.to_csv(
        self.output_file.get(),
        index=False
    )



def main():

    root = tk.Tk()

    InventoryMatcherApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
