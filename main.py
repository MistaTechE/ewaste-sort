#main.py
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class InventoryMatcherApp:

  def __init__(self, root):
    self.root = root
    self.root.title("eWaste Inventory Matcher")
    self.root.geometry("900x250")
    self.root.resizable(False, False)
    self.ewaste_file = tk.StringVar()
    self.inventory_file = tk.StringVar()
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


  def process_files(self):

    ewaste = pd.read_csv(
        self.ewaste_file.get(),
        dtype=str
    ).fillna("")

    inventory = pd.read_csv(
        self.inventory_file.get(),
        dtype=str
    ).fillna("")

    # Normalize State Tags for matching
    ewaste["Match_Tag"] = (
      ewaste["State Tag"]
      .astype(str)
      .str.strip()
      .str.upper()
      .str.replace("E273", "", regex=False)
    )

    inventory["Match_Tag"] = (
      inventory["State Tag"]
      .astype(str)
      .str.strip()
      .str.upper()
      .str.replace("E273", "", regex=False)
    )

    # Match inventory records using normalized tags
    filtered_inventory = inventory[
      inventory["Match_Tag"].isin(ewaste["Match_Tag"])
    ]

    # Keep only required columns
    filtered_inventory = filtered_inventory[
      [
        "State Tag",
        "PROPERTY #",
        "DESCRIPTION",
        "SERIAL #",
        "P.O. #",
        "PROG ID",
        "COST",
        "DATE",
        "VENDOR",
        "Request for Disposal",
        "Match_Tag"
      ]
    ]

    # Find tags that were not found in inventory
    missing_tags = ewaste[
      ~ewaste["Match_Tag"].isin(inventory["Match_Tag"])
    ].copy()

    # Create missing inventory rows
    if not missing_tags.empty:

      missing_rows = pd.DataFrame(
        "?",
        index=range(len(missing_tags)),
        columns=filtered_inventory.columns
      )

      # Fill required fields
      missing_rows["Match_Tag"] = missing_tags["Match_Tag"]

      missing_rows["State Tag"] = (
        "E273" + missing_tags["Match_Tag"]
      )

      # Add missing rows to output
      filtered_inventory = pd.concat(
        [filtered_inventory, missing_rows],
        ignore_index=True
      )

    filtered_inventory["State Tag"] = (
      "E273" + filtered_inventory["Match_Tag"]
    )
    
    filtered_inventory = filtered_inventory.drop(
      columns=["Match_Tag"]
    )

    # Add disposal reason to every row
    filtered_inventory["Request for Disposal"] = (
      "Old, broken, may be used for parts"
    )

    # Write output CSV next to the inventory file
    output_file = os.path.join(
      os.path.dirname(self.inventory_file.get()),
      "Filtered_Inventory.csv"
    )

    filtered_inventory.to_csv(
      output_file,
      index=False
    )



def main():

    root = tk.Tk()

    InventoryMatcherApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
