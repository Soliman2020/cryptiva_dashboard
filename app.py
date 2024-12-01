import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page config with dark theme
st.set_page_config(
    page_title="Token Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for dark theme
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #262730;
    }
    
    /* Metric containers */
    div[data-testid="stMetricValue"] {
        color: #FAFAFA;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FAFAFA !important;
    }
    
    /* DataFrames */
    .dataframe {
        background-color: #262730;
        color: #FAFAFA;
    }
    
    /* Slider */
    .stSlider {
        background-color: #262730;
    }
    </style>
    """, unsafe_allow_html=True)

# Title with emoji
st.title("📊 Token Performance Dashboard")
st.markdown('<hr style="border: 2px solid #4A4A4A;">', unsafe_allow_html=True)

# Data
data = {
    'Token': ['RENDER', 'ICX', 'VTHO', 'BCH', 'GTC', 'XVG', 'ETC', 'ATA', 'RIF', 'GLM', 
              'IOST', 'SEI', 'SC', 'PUNDIX', 'POLYX', 'LIT', 'PHA', 'HIGH', 'QKC', 'MASK',
              'IOTX', 'FIO', 'KMD', 'BAT', 'EGLD'],
    'Current_PL_Percent': [69.42, 65.82, 63.52, 63.14, 59.85, 59.48, 59.33, 55.39, 51.12, 50.63,
                          50.49, 49.71, 44.43, 41.95, 40.94, 38.22, 36.17, 31.48, 31.38, 31.17,
                          30.13, 24.21, 23.91, 17.94, 16.04]
}
df = pd.DataFrame(data)

# Sidebar with dark theme
st.sidebar.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #262730;
    }
    </style>
    """, unsafe_allow_html=True)
st.sidebar.header("Filters")

# Performance Range Filter
pl_range = st.sidebar.slider(
    "Filter by P/L%",
    min_value=float(df['Current_PL_Percent'].min()),
    max_value=float(df['Current_PL_Percent'].max()),
    value=(float(df['Current_PL_Percent'].min()), float(df['Current_PL_Percent'].max()))
)

# Function to display token with image
def display_token_option(token):
    col1, col2 = st.columns([1, 4])
    with col1:
        image_path = f"token_images/{token.lower()}.png"
        if os.path.exists(image_path):
            st.image(image_path, width=20)
    with col2:
        st.write(token)

# Token Selection with images
st.sidebar.write("Select Tokens")
token_container = st.sidebar.container()
all_tokens = df['Token'].unique()
selected_tokens = []

# Create checkboxes for each token with images
for token in all_tokens:
    token_col1, token_col2 = token_container.columns([1, 4])
    with token_col1:
        image_path = f"token_images/{token.lower()}.png"
        if os.path.exists(image_path):
            st.image(image_path, width=20)
    with token_col2:
        if st.checkbox(token, value=True, key=f"token_{token}"):
            selected_tokens.append(token)

if not selected_tokens:  # If no tokens selected, select all by default
    selected_tokens = list(all_tokens)

# Filter data
filtered_df = df[
    (df['Current_PL_Percent'].between(pl_range[0], pl_range[1])) &
    (df['Token'].isin(selected_tokens))
].sort_values('Current_PL_Percent', ascending=True)

# Main chart taking full width
fig = go.Figure()
fig.add_trace(go.Bar(
    y=filtered_df['Token'],
    x=filtered_df['Current_PL_Percent'],
    orientation='h',
    text=filtered_df['Current_PL_Percent'].round(2).astype(str) + '%',
    textposition='outside',
    marker=dict(color='#00CA8E'),  # Bright green for contrast
    textfont=dict(color='#FAFAFA')
))

fig.update_layout(
    title={
        'text': "Token Performance (P/L%)",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(color='#FAFAFA')
    },
    xaxis_title="P/L%",
    height=500,  # Reduced height to make room for stats below
    showlegend=False,
    plot_bgcolor='#0E1117',
    paper_bgcolor='#0E1117',
    margin=dict(l=0, r=0, t=40, b=0),
    xaxis=dict(
        gridcolor='#1F2937',
        zerolinecolor='#1F2937',
        tickfont=dict(color='#FAFAFA')
    ),
    yaxis=dict(
        gridcolor='#1F2937',
        zerolinecolor='#1F2937',
        tickfont=dict(color='#FAFAFA')
    )
)

st.plotly_chart(fig, use_container_width=True)

# Add spacing
st.markdown("<br>", unsafe_allow_html=True)

# Statistics sections in three columns at the bottom
st.markdown("""
    <div style='background-color: #262730; padding: 10px; border-radius: 10px; margin-bottom: 15px;'>
    <h2 style='color: #FAFAFA; text-align: center; margin-bottom: 10px; font-size: 20px;'>Performance Analytics</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    # Summary Statistics
    st.markdown("""
        <div style='background-color: #262730; padding: 8px; border-radius: 8px; margin-bottom: 10px;'>
        <h3 style='color: #FAFAFA; text-align: center; margin: 0; font-size: 16px;'>Summary Statistics</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Metrics in 2x2 grid
    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        st.metric("Average P/L%", f"{filtered_df['Current_PL_Percent'].mean():.2f}%")
        st.metric("Min P/L%", f"{filtered_df['Current_PL_Percent'].min():.2f}%")
    with metric_col2:
        st.metric("Max P/L%", f"{filtered_df['Current_PL_Percent'].max():.2f}%")
        st.metric("# of Tokens", len(filtered_df))

with col2:
    # Top Performers
    st.markdown("""
        <div style='background-color: #262730; padding: 8px; border-radius: 8px; margin-bottom: 10px;'>
        <h3 style='color: #FAFAFA; text-align: center; margin: 0; font-size: 16px;'>Top Performers</h3>
        </div>
    """, unsafe_allow_html=True)
    top_performers = filtered_df.nlargest(5, 'Current_PL_Percent')
    st.dataframe(
        top_performers[['Token', 'Current_PL_Percent']].style
        .format({'Current_PL_Percent': '{:.2f}%'})
        .set_properties(**{
            'background-color': '#262730',
            'color': '#FAFAFA',
            'font-size': '13px'
        }),
        hide_index=True,
        height=200
    )

with col3:
    # Bottom Performers
    st.markdown("""
        <div style='background-color: #262730; padding: 8px; border-radius: 8px; margin-bottom: 10px;'>
        <h3 style='color: #FAFAFA; text-align: center; margin: 0; font-size: 16px;'>Bottom Performers</h3>
        </div>
    """, unsafe_allow_html=True)
    bottom_performers = filtered_df.nsmallest(5, 'Current_PL_Percent')
    st.dataframe(
        bottom_performers[['Token', 'Current_PL_Percent']].style
        .format({'Current_PL_Percent': '{:.2f}%'})
        .set_properties(**{
            'background-color': '#262730',
            'color': '#FAFAFA',
            'font-size': '13px'
        }),
        hide_index=True,
        height=200
    )
