import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Import 
from modules.analyzer import(
    get_basic_info,
    get_column_types,
    get_numeric_summary
)

from modules.visualizer import (
    create_barchart,
    create_heatmap,
    create_histogram,
    create_scatter_plot
)

from modules.cleaner import (
    missing_summary,
    remove_dulicates,
    handle_missing_values
)

from pathlib import Path

@st.cache_data
def load_dataset(file):
    return pd.read_csv(file)


def load_css(file_name: str) -> None:
    css = Path(__file__).parent / file_name
    st.markdown(f"<style>{css.read_text()}</style>", unsafe_allow_html=True)

load_css("style.css")

# Page Configuration
st.set_page_config(
    page_title='Dataset Detective',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'About':'dataset analyzer'
    }
)

# Page logo
st.sidebar.image('assets/dataset-detective-logo-B.png', use_container_width=True)

# application title
st.title('Dataset Detective')

# Description
st.write(
    'Analyze your datasets and discover meaningfull insights'
)

# sidebar
st.sidebar.title('Navigation')
page = st.sidebar.radio(
    'Select Section',
    ['Dashboard', 'Data Analysis', 'Data Visualization', 'Data Cleaning']
)

# welcome message
st.success('Welcome to the Dataset Detective..')

# Page
if page == 'Dashboard':
    st.subheader('Dashboard')
    st.write("Upload and explore your datasets.")

    st.subheader('Upload the file')
    
    # file upload section
    upload_file = st.file_uploader(
        'Upload the Csv file Of Dataset',
        type=['csv']
    )

    if upload_file is not None:
        # df = pd.read_csv(upload_file)
        df = load_dataset(upload_file)

        # use session state for maintaining session between ui and user
        st.session_state['dataset'] = df
                
        st.success('Your Dataset uploaded sucessfully..')
        st.subheader('Preview your dataset')
        st.dataframe(df.head())
    else :
        st.error('Please upload a CSV file to start analysis.')    

elif page == 'Data Analysis':
    st.subheader('Data Analysis')
    st.write("Analyze your dataset using statistical methods.")

    if 'dataset' in st.session_state:
        
        df = st.session_state['dataset'] 
        
        # information
        info = get_basic_info(df)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric('Total rows', info['total_rows'])
        col2.metric('Total columns', info['total_columns'])
        col3.metric('Missing values', info['missing_values'])
        col4.metric('Duplicate rows', info['duplicate_rows'])

        st.divider()

        # Column Classification
        st.subheader('Column Classification')
        col_type = get_column_types(df)
        st.write('Numerical Column', col_type['numeric'])
        st.write('Categorical Column', col_type['categorical'])
        st.write('Date Column', col_type['date'])

        st.divider()

        # Statistical summary
        st.subheader('Statistical Summary')
        state = get_numeric_summary(df)

        if state is not None:
            st.dataframe(state)
        else :
            st.write('There no numerical column')    
    else:
        st.warning('Please fisrt upload your Csv file')        


elif page == 'Data Visualization':
    st.subheader('Date Visualization')
    st.write("Create charts and graphs from your dataset.")

    if 'dataset' in st.session_state:
        df = st.session_state['dataset']

        # numeric column
        numeric_column = df.select_dtypes(
            include = 'number'
        ).columns.tolist()
        
        # categorical column
        categorical_column = df.select_dtypes(
            include = ['object', 'category', 'bool']
        ).columns.tolist()

        # Chart Option
        chart_type = st.selectbox(
            'Select Chart Option',
            ['Histogram', 'Bar Chart', 'Scatter Plot', 'Correlation Heatmap']
        )

        # option
        if chart_type == 'Histogram':
            if numeric_column:
                column = st.selectbox (
                    'Select Your Numerical Column',
                    numeric_column
                )

                fig = create_histogram(df, column)

                st.pyplot(fig)
                plt.close(fig)

            else :
                st.warning('No numerical in your dataset')    

        elif chart_type == 'Bar Chart':
            if categorical_column:
                column = st.selectbox(
                    'Select Your Categorical Colun',
                    categorical_column
                )

                fig = create_barchart(df, column)

                st.pyplot(fig)
                plt.close(fig)
            else:
                st.warning('No Categorical in your dataset')
        
        elif chart_type == 'Scatter Plot':
            if len(numeric_column) >= 2:
                col1 , col2 = st.columns(2)

                with col1:
                    x_column = st.selectbox(
                        'x-axis',
                        numeric_column
                    )
                with col2:
                    y_column = st.selectbox(
                        'y-axis',
                        numeric_column
                    )   

                fig = create_scatter_plot(df, x_column, y_column)
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.warning('Atleast 2 numerical column required')
        elif chart_type == 'Correlation Heatmap':

            if len(numeric_column) >= 2:
                selected_column = st.multiselect(
                    'Select columns for correlation analysis',
                    numeric_column,
                    default = numeric_column
                )    

                if len(selected_column) >= 2:
                    fig = create_heatmap(df, selected_column)
                    st.pyplot(fig)
                    plt.close(fig)  
            else :
                st.warning('Please select at least two numerical column')        
    else:
        st.warning('Please fisrt upload your Csv file') 


elif page == 'Data Cleaning':

    st.subheader('Data Cleaning')
    st.write("Handle missing values and duplicate records.")

    if 'dataset' in st.session_state:

        df = st.session_state['dataset']

        miss_df = missing_summary(df)

        st.subheader('Missing Values Summary')
        st.dataframe(miss_df)

        method = st.selectbox(
            'Select Your Option',
            [
                'Remove Rows',
                'Fill with Mean',
                'Fill with Median',
                'Fill with Mode'
            ]
        )

        if st.button('Apply Missing Value Cleaning'):

            cleaned_df = handle_missing_values(df, method)

            st.session_state['cleaned_df'] = cleaned_df

            st.success('Missing values handled successfully!')

        st.subheader('Remove Duplicate Rows')

        if st.button('Remove Duplicates'):

            cleaned_df = remove_dulicates(df)

            st.session_state['cleaned_df'] = cleaned_df

            st.success('Duplicates removed successfully!')

            st.write('Rows Before Cleaning:', len(df))
            st.write('Rows After Cleaning:', len(cleaned_df))

        # Retrieve cleaned dataset from session state
        if 'cleaned_df' in st.session_state:

            cleaned_df = st.session_state['cleaned_df']

            st.subheader('Download Clean Dataset and Preview Dataset')

            option = st.selectbox(
                'Select Your Option',
                ['Preview', 'Download']
            )

            if option == 'Preview':

                st.dataframe(cleaned_df)

            elif option == 'Download':

                csv = cleaned_df.to_csv(
                    index=False
                ).encode('utf-8')

                st.download_button(
                    label='Download Cleaned CSV',
                    data=csv,
                    file_name='cleaned_dataset.csv',
                    mime='text/csv'
                )

        else:
            st.info('Please apply a cleaning operation first.')

    else:
        st.warning('Please upload first CSV file.')


else:
    st.error('You choose something wrong!')    

