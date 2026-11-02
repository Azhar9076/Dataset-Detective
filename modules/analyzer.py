import pandas as pd

# 1. Get basic dataset information
def get_basic_info(df):
    info = {
        'total_rows' : df.shape[0],
        'total_columns' : df.shape[1],
        'missing_values' : int(df.isnull().sum().sum()),
        'duplicate_rows' : int(df.duplicated().sum()) 
    }

    return info

# 2. Identify the column types
def get_column_types(df):
    # numeric column
    numeric_column = df.select_dtypes(
        include = 'number'
    ).columns.tolist()

    # categorical column
    categorical_column = df.select_dtypes(
        include = ['object', 'category', 'bool']
    ).columns.tolist()

    # date columns
    date_column = df.select_dtypes(
            include = ['datetime']
        ).columns.tolist()
    
    return {
        'numeric' : numeric_column,
        'categorical': categorical_column,
        'date' : date_column

    }

# 3.generate numerical statiscis 
def get_numeric_summary(df):
    numeric_df = df.select_dtypes(
        include = 'number'
    )

    if numeric_df.empty:
        return None

    return numeric_df.describe()