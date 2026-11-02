import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def create_histogram(df, column):
    fig , ax = plt.subplots(figsize=(8,4))

    sns.histplot(
        data=df,
        x = column,
        kde=True,
        ax=ax
    )

    ax.set_title(f'Distribution of {column}')
    ax.set_xlabel(column)
    ax.set_ylabel('Frequency')

    return fig

def create_barchart(df,column):
    fig , ax = plt.subplots(figsize=(8,4))

    df[column].value_counts().head(10).plot(
        kind = 'bar',
        ax = ax
    )

    ax.set_title(f'Distribution of {column}')
    ax.set_xlabel(column)
    ax.set_ylabel('Count')

    plt.xticks(rotation=45)

    return fig

def create_scatter_plot(df, x_column, y_column):
    fig , ax = plt.subplots(figsize=(8,4))
    
    sns.scatterplot(
            data=df,
            x = x_column,
            y = y_column,
            ax=ax
    )
    
    ax.set_title(f'{x_column} vs {y_column}')
   
    return fig

def create_heatmap(df, selected_columns):

    numeric_df = df[selected_columns]

    if numeric_df.shape[1] < 2:
        return None

    fig, ax = plt.subplots(figsize=(8, 4))

    correlation = numeric_df.corr()

    sns.heatmap(
        correlation,
        annot=True,
        cmap='coolwarm',
        fmt='.2f',
        ax=ax
    )

    ax.set_title('Correlation Heatmap')

    return fig