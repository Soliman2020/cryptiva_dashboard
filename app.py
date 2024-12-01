import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# Set page config with dark theme
st.set_page_config(
    page_title="Token Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .stSelectbox [data-baseweb=select] {
            background-color: #1F2937;
        }
        .stSelectbox [data-baseweb=select] div {
            color: #FAFAFA;
        }
        .stSlider [data-baseweb=slider] {
            background-color: #1F2937;
        }
        section[data-testid="stSidebar"] {
            background-color: #1F2937;
            color: #FAFAFA;
        }
        section[data-testid="stSidebar"] .stMarkdown {
            color: #FAFAFA;
        }
        .stMarkdown {
            color: #FAFAFA;
        }
    </style>
""", unsafe_allow_html=True)

# Data
data = {
    'Token': ['RENDER', 'ICX', 'VTHO', 'BCH', 'GTC', 'XVG', 'ETC', 'ATA', 'RIF', 'GLM', 
              'IOST', 'SEI', 'SC', 'PUNDIX', 'POLYX', 'LIT', 'PHA', 'HIGH', 'QKC', 'MASK',
              'IOTX', 'FIO', 'KMD', 'BAT', 'EGLD'],
    'Current_PL_Percent': [69.42, 65.82, 63.52, 63.14, 59.85, 59.48, 59.33, 55.39, 51.12, 50.63,
                          50.49, 49.71, 44.43, 41.95, 40.94, 38.22, 36.17, 31.48, 31.38, 31.17,
                          30.92, 30.44, 29.85, 28.33, 27.91]
}
df = pd.DataFrame(data)

# Sidebar with dark theme
st.sidebar.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #1F2937;
        }
    </style>
""", unsafe_allow_html=True)

# Filter controls in sidebar
pl_range = st.sidebar.slider(
    "P/L% Range",
    min_value=float(df['Current_PL_Percent'].min()),
    max_value=float(df['Current_PL_Percent'].max()),
    value=(float(df['Current_PL_Percent'].min()), float(df['Current_PL_Percent'].max()))
)

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
            try:
                st.image(image_path, width=20)
            except Exception as e:
                st.write(f"Error loading image for {token}: {str(e)}")
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

# Display summary statistics
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Top Performers")
    st.dataframe(
        filtered_df.nlargest(5, 'Current_PL_Percent')[['Token', 'Current_PL_Percent']],
        hide_index=True
    )

with col2:
    st.markdown("### Bottom Performers")
    st.dataframe(
        filtered_df.nsmallest(5, 'Current_PL_Percent')[['Token', 'Current_PL_Percent']],
        hide_index=True
    )

with col3:
    st.markdown("### Summary Statistics")
    stats_df = pd.DataFrame({
        'Metric': ['Average P/L%', 'Median P/L%', 'Max P/L%', 'Min P/L%'],
        'Value': [
            f"{filtered_df['Current_PL_Percent'].mean():.2f}%",
            f"{filtered_df['Current_PL_Percent'].median():.2f}%",
            f"{filtered_df['Current_PL_Percent'].max():.2f}%",
            f"{filtered_df['Current_PL_Percent'].min():.2f}%"
        ]
    })
    st.dataframe(stats_df, hide_index=True)
