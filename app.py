import streamlit as st
import pandas as pd
import os

def common_message():
  st.write('''
  ### Contact:
  Jai Shree Mataji!

  For any queries or feedback, reach out to me:
  - Name: Advait Amit Kisar
  - Phone: +91 7774035501
  - Email: [advaitkisar2509@gmail.com](mailto:advaitkisar2509@gmail.com)
  
  Thank you for using this web app!
  ''')

# Custom CSS injection
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Roboto+Mono&display=swap');

/* Main title styling */
h1 {
    font-family: 'Playfair Display', serif !important;
    color: #2a3f5f !important;
    border-bottom: 2px solid #2a3f5f;
    padding-bottom: 10px;
}

/* Bhajan title styling */
.bhajan-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.8rem !important;
    color: #2a3f5f !important;
    margin: 1rem 0 !important;
}

/* Script content styling */
.script-content {
    font-family: 'Roboto Mono', monospace !important;
    font-size: 1.1rem;
    line-height: 1.6;
    white-space: pre-wrap;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 5px;
    margin-top: 15px;
}

/* Dropdown styling */
.stSelectbox > div > div {
    font-family: 'Playfair Display', serif !important;
}
</style>
""", unsafe_allow_html=True)

# Load data from Excel
@st.cache_data
def load_data():
    data = {}
    data['MR'] = pd.read_excel('Data.xlsx', sheet_name='MR')
    data['HI'] = pd.read_excel('Data.xlsx', sheet_name='HI')
    data['EN'] = pd.read_excel('Data.xlsx', sheet_name='EN')
    data['TA'] = pd.read_excel('Data.xlsx', sheet_name='TA')

    return data

data = load_data()

# App layout
st.title('Sahajayoga Bhajan Sangraha')

st.markdown('<div style="font-size: 14px; color: #777;">Designed and developed by Advait Amit Kisar</div>', unsafe_allow_html=True)

# Language selection
language = st.selectbox('Select Language', ['Marathi / मराठी (MR)', 'Hindi / हिन्दी (HI)', 'English (EN)', 'Tamil / தமிழ் (TA)'])
lang_code = language[-3:-1]  # Extracts MR/HI/EN

# Bhajan selection
df = data[lang_code]
bhajan_options = [
    f"{idx+1}. {row['Name (Roman)']} / {row['Name (Orig)']}"
    for idx, (_, row) in enumerate(df.iterrows())
]
selected_bhajan = st.selectbox('Select Bhajan', bhajan_options)

original_script = {
	'MR': 'DN',
	'HI': 'DN',
	'EN': 'EN',
	'TA': 'TA'
}

# Script selection
script_map = {
    'Original': original_script[lang_code],
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

# Display combined title
st.markdown(f"<div class='bhajan-title'>{name_roman} / {name_orig}</div>", 
            unsafe_allow_html=True)

# Construct file path
file_suffix = script_map[script]
file_path = f"Scripts/{lang_code}/{bhajan_code}-{file_suffix}.txt"

# Display content
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # st.code(content, language='text')
    # st.write(content)
    st.text(content)
else:
    st.error("File not found. Please check the file structure.")

st.markdown('<div style="margin-top: 16px;">Recommendation:</div>', unsafe_allow_html=True)
st.link_button("Check out Sahajayoga Stotra Sangraha", "https://sahajayogastotrasangraha.streamlit.app/")
common_message()
