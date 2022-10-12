import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns



class Plots:

    def plot_hist(df: pd.DataFrame, column: str, color: str) -> None:
        """
        Plots the histogram of a given dataset with specific columns and colors
        Parameters
        ---------------
        df: Dataframe to be processed
        column: column to be plotted
        color: color of the histogram

        """
        sns.displot(data=df, x=column, color=color,
                    kde=True, height=7, aspect=2)
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.show()
    def plot_hist_all(df: pd.DataFrame):
        """
        Plot the histogram of all of the features in the dataset with numerical values
        
        Parameters
        -----------------------
        df: Dataframe to be processed
        """
        sns.set()
        num_feats = list(df.select_dtypes(
            include=['int64', 'float64', 'int32']).columns)
        df[num_feats].hist(figsize=(20, 20))

    def plot_bar(df: pd.DataFrame, x_col: str, y_col: str, title: str, xlabel: str, ylabel: str) -> None:
        """Plots the column with bargraph
        Parameters
        ------------------
        df: Dataframe to be processed
        x_col: x value of the column to be plotted.
        y_col: y value of the column to be plotted.
        title: title of the plot to be
        xlabel: x axis label of the plot
        ylabel: y axis label of the plot
        """
        plt.figure(figsize=(12, 7))
        sns.barplot(data=df, x=x_col, y=y_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.yticks(fontsize=14)
        plt.xlabel(xlabel, fontsize=16)
        plt.ylabel(ylabel, fontsize=16)
        plt.show()

    def plot_box(df: pd.DataFrame, x_col: str, title: str) -> None:
        """
        Plots a box plot of a given columns.

        Parameters:
        ----------------------
        df: Dataframe to be processed
        box: Plot a box plot.
        x_col: x-axis column
        title: Title of the plot
        """
        plt.figure(figsize=(12, 7))
        sns.boxplot(data=df, x=x_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.show()

    def plot_box_multi(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> None:
        """Plots multiple columns with boxgraphs
        Parameters
        ------------------
        df: Dataframe to be processed
        x_col: x value of the column to be plotted.
        y_col: y value of the column to be plotted.
        title: title of the plot to be

        """
        plt.figure(figsize=(12, 7))
        sns.boxplot(data=df, x=x_col, y=y_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()

    def plot_scatter(df: pd.DataFrame, x_col: str, y_col: str, title: str, hue: str, style: str) -> None:
        """Plots scatter graph of the given columns
        Parameters
        ------------------
        df: Dataframe to be processed
        x_col: x value of the column to be plotted.
        y_col: y value of the column to be plotted.
        title: title of the plot to be
        hue: category column
        style: additional category of column
        """
        plt.figure(figsize=(12, 7))
        sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue, style=style)
        plt.title(title, size=20)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()

    def plot_count(df: pd.DataFrame, column: str) -> None:
        """Plots count graph of the given column
        Parameters
        ------------------
        df: Dataframe to be processed
        x_col: x value of the column to be plotted.
        y_col: y value of the column to be plotted.
        title: title of the plot to be
        hue: category column
        style: additional category of column
        """
        plt.figure(figsize=(12, 7))
        sns.countplot(data=df, x=column)
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.show()

    def plot_heatmap(df: pd.DataFrame, title: str, cbar=False) -> None:
        """Plots the heatmap graph of the given column
        Parameters
        ------------------
        df: Dataframe to be processed
        title: title of the plot to be
        """

        plt.figure(figsize=(13, 8))
        sns.heatmap(df, annot=True, cmap='viridis', vmin=0,
                    vmax=1, fmt='.2f', linewidths=.7, cbar=cbar)
        plt.title(title, size=20, fontweight='bold')
        plt.show()

    def plot_heatmap_from_correlation(correlation, title: str):
        """Plots heatmap of the features based on correlation matrix result
        Parameters
        -------------------
        title: Title of the plot
        correlation: correlation matrix
        """
        plt.figure(figsize=(14, 9))
        sns.heatmap(correlation)
        plt.title(title, size=18, fontweight='bold')
        plt.show()

    def plot_subplots(x: str, y: str, xtitle: str, ytitle: str)->None:
        """Plots the subplots of the data.
        Parameters
        --------------------
        x: str
        y: str
        ytitle:
        xtitle:
        """
        sns.set(style="whitegrid")
        fig, axes = plt.subplots(nrows=1, ncols=2)
        fig.set_size_inches(25, 8)
        x.hist(ax=axes[0], alpha=0.3, color='green', bins=20)
        y.hist(ax=axes[1], alpha=0.3, color='yellow', bins=20)
        axes[0].set_title(xtitle, size=20)
        axes[1].set_title(ytitle, size=20)
        # self.logger.info(
        #     'Plotting a subplots')
        plt.show()