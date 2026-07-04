import pandas as pd
import matplotlib.pyplot as plt
from utils import *
######################################################
##### Plotting Functions ####
# These functions are designed to be flexible and reusable for various types of plots. They can be extended to include more customization options as needed.
# Each function takes a DataFrame and the necessary parameters to create the desired plot, such as column names for the x and y axes, titles, labels, and whether to stack bars in a bar chart.
######################################################

def plot_bar(df:pd.DataFrame, x_col:str, y_col:str, title:str="", xlabel:str="", ylabel:str="", stacked:bool=False, msglvl=0):
    df.plot(kind="bar", x=x_col, y=y_col, stacked=stacked, xlabel=xlabel, ylabel=ylabel, title=title)

def plot_line(df:pd.DataFrame, x_col:str, y_col:str, title:str="", xlabel:str="", ylabel:str="", fsize=12):
    df.plot(kind="line", x=x_col, y=y_col, xlabel=xlabel, ylabel=ylabel, title=title)
    config_plot(plt.gca(), title, xlabel, ylabel, fontsize=fsize)

def plot_scatter(df:pd.DataFrame, x_col:str, y_col:str, title:str="", xlabel:str="", ylabel:str=""):
    df.plot(kind="scatter", x=x_col, y=y_col, xlabel=xlabel, ylabel=ylabel, title=title)

def plot_box(df:pd.DataFrame, x_col:str, y_col:str, title:str="", xlabel:str="", ylabel:str=""):
    df.plot(kind="box", x=x_col, y=y_col, xlabel=xlabel, ylabel=ylabel, title=title)

def plot_2d_scatter_colored(data: pd.DataFrame, x_label: str, y_label: str, z_label: str, title: str = "2D Scatter Plot with Color",msglvl=0):
    # Input validation: Check if DataFrame is valid
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a Pandas DataFrame.")
    if data.empty:
        raise ValueError("DataFrame cannot be empty.")

    # Input validation: Check if columns exist
    if not all(col in data.columns for col in [x_label, y_label, z_label]):
        missing_columns = [col for col in [x_label, y_label, z_label] if col not in data.columns]
        raise ValueError(f"Columns not found in DataFrame: {', '.join(missing_columns)}")

    # Input validation: Check for numeric data in selected columns
    for col in [x_label, y_label, z_label]:
        if not pd.api.types.is_numeric_dtype(data[col]):
            raise ValueError(f"Column '{col}' must contain numeric data.")

    # Create the 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    # Get the data from the DataFrame columns
    x_data = data[x_label]
    y_data = data[y_label]
    z_data = data[z_label]

    # Use z_data for color mapping.  Normalize to the range 0-1.
    norm = plt.Normalize(vmin=z_data.min(), vmax=z_data.max())
    colors = plt.cm.viridis(norm(z_data))  # Use 'viridis' colormap

    # Create the scatter plot, passing the colors
    ax.scatter(x_data, y_data, c=colors, marker='.')

    # Set the labels for the axes
    ax.set_xlabel(x_label, fontsize=16)
    ax.set_ylabel(y_label, fontsize=16)
    # ax.set_zlabel(z_label)

    # Set the title of the plot
    ax.set_title(title,fontsize=24)

    # Add a colorbar to show the mapping between z-values and colors
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
    sm.set_array([])  # You need to set an array, but it can be empty
    fig.colorbar(sm, ax=ax, label=z_label) # Add label to colorbar

    # Add grid lines for better readability
    ax.grid(True)

def create_3d_scatter_plot(df, x_col, y_col, z_col, title="3D Scatter Plot"):
    # Check if the input is a Pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a Pandas DataFrame.")

    # Check if the specified columns exist in the DataFrame
    if not all(col in df.columns for col in [x_col, y_col, z_col]):
        raise ValueError(f"Columns '{x_col}', '{y_col}', and '{z_col}' must exist in the DataFrame.  The columns in the dataframe are: {df.columns}")

    # Create the 3D plot
    fig = plt.figure(figsize=(10, 8))  # Adjust figure size as needed
    ax = fig.add_subplot(111, projection='3d')  # Create 3D axes

    # Get the data from the DataFrame columns
    x_data = df[x_col]
    y_data = df[y_col]
    z_data = df[z_col]

    # Create the scatter plot
    ax.scatter(x_data, y_data, z_data, c='b', marker='o')  # 'b' for blue, 'o' for circle

    # Set the labels for the axes
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_zlabel(z_col)

    # Set the title of the plot
    ax.set_title(title)

    # Add gridlines
    ax.grid(True)


def save_plot(outfile:str="",odir:str="",msglvl=0):
    console_log(f"Saving Plot --> {outfile}",msglvl+1,"pass")
    plt.savefig(f"{odir}/{outfile}.png")
    plt.savefig(f"{odir}/{outfile}_transp.png",transparent=True)
    plt.close()

def save_df(df:pd.DataFrame,outfile:str="",odir:str="",msglvl=0):
    console_log(f"Saving DataFrame --> {outfile}",msglvl+1,"pass")
    df.to_csv(f"{odir}/{outfile}.csv", index=False)

def config_plot(ax, title="", xlabel="", ylabel="", zlabel="", fontsize=12, msglvl=0):
    # Set the labels for the axes
    plt.title(title, fontsize=24)
    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    if zlabel != "":
        ax.set_zlabel(zlabel, fontsize=fontsize)

    # Set the title of the plot
    ax.set_title(title, fontsize=fontsize)

    # Add grid lines for better readability
    ax.grid(True)
    plt.legend(loc='best')

if __name__ == "__main__":

    # Plotting Line Plot Example
    x_data = [1, 2, 3, 4, 5]
    y_data = [2, 3, 5, 7, 11]
    df = pd.DataFrame({"X": x_data, "Y": y_data})
    plot_line(df, "X", "Y", title="Sample Line Plot", xlabel="X-axis", ylabel="Y-axis")

    # Plotting Bar Plot Example
    plot_bar(df, "X", "Y", title="Sample Bar Plot", xlabel="X-axis", ylabel="Y-axis", stacked=False)

    # Plotting Stacked Bar Plot Example
    plot_bar(df, "X", "Y", title="Sample Stacked Bar Plot", xlabel="X-axis", ylabel="Y-axis", stacked=True)

    # Plotting Scatter Plot Example
    plot_scatter(df, "X", "Y", title="Sample Scatter Plot", xlabel="X-axis", ylabel="Y-axis")

    # Plotting Box Plot Example
    plot_box(df, "X", "Y", title="Sample Box Plot", xlabel="X-axis", ylabel="Y-axis")

    # Plotting 2D Scatter Plot with Color Example
    z_data = [10, 20, 30, 40, 50]
    df["Z"] = z_data
    plot_2d_scatter_colored(df, "X", "Y", "Z", title="Sample 2D Scatter Plot with Color")

    # Plotting 3D Scatter Plot Example
    create_3d_scatter_plot(df, "X", "Y", "Z", title="Sample 3D Scatter Plot")

    plt.show()