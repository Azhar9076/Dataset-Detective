import pandas as pd


def missing_summary(df):
    missing = df.isnull().sum()

    summary = pd.DataFrame(
        {
            'column': missing.index,
            'Missing Value' : missing.values,
            'Missing Percentage' : (
                missing.values / len(df) * 100
            ).round(2) if len(df) > 0 else 0
        }
    )

    return summary

def remove_dulicates(df):
    return df.drop_duplicates()

def handle_missing_values(df, method):
    cleaned_df = df.copy()

    if method == 'Remove Rows':
        cleaned_df = cleaned_df.dropna()
    
    elif method == 'Fill with Mean':
        numeric_column = cleaned_df.select_dtypes(
            include = 'number'
        ).columns

        cleaned_df[numeric_column] = cleaned_df[numeric_column].fillna(cleaned_df[numeric_column].mean())

    elif method == 'Fill with Median':
        numeric_column = cleaned_df.select_dtypes(
                    include = 'number'
        ).columns
        
        cleaned_df[numeric_column] = cleaned_df[numeric_column].fillna(cleaned_df[numeric_column].median())
    
    elif method == 'Fill with Mode':
        for column in cleaned_df.columns:
            if not cleaned_df[column].mode().empty:
                cleaned_df[column] = cleaned_df[column].fillna(cleaned_df[column].mode()[0])

    return cleaned_df        
