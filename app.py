import streamlit as st
import pandas as pd
import os

# Load data from Excel
@st.cache_data
def load_data():
    data = {}
    data['MR'] = pd.read_excel('Data.xlsx', sheet_name='MR')
    data['HN'] = pd.read_excel('Data.xlsx', sheet_name='HN')
    data['EN'] = pd.read_excel('Data.xlsx', sheet_name='EN')
    return data

data = load_data()

# App layout
st.title('Bhajan Viewer')

# Language selection
language = st.selectbox('Select Language', ['Marathi (MR)', 'Hindi (HN)', 'English (EN)'])
lang_code = language[-3:-1]  # Extracts MR/HN/EN

# Bhajan selection
df = data[lang_code]
bhajan_options = [f"{row['Name (Roman)']} / {row['Name (Orig)']}" 
                 for _, row in df.iterrows()]
selected_bhajan = st.selectbox('Select Bhajan', bhajan_options)

# Script selection
script_map = {
    'Original': 'DN' if lang_code in ['MR', 'HN'] else 'EN',
    'Devanagari': 'DN',
    'English': 'EN',
    'ISO 15919 Indic': 'ISO'
}
script = st.selectbox('Select Script', list(script_map.keys()), index=0)

# Get selected bhajan details
selected_index = bhajan_options.index(selected_bhajan)
bhajan_code = df.iloc[selected_index]['Code']
name_roman = df.iloc[selected_index]['Name (Roman)']
name_orig = df.iloc[selected_index]['Name (Orig)']

# Display title
st.subheader(f"{name_roman}")
st.subheader(f"{name_orig}")

# Construct file path
file_suffix = script_map[script]
file_path = f"Scripts/{lang_code}/{bhajan_code}-{file_suffix}.txt"

# Display content
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    st.code(content, language='text')
else:
    st.error("File not found. Please check the file structure.")
