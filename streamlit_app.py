import streamlit as st
import json
import pickle
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import os
from config import TMDB_API_KEYS

# Page configuration
st.set_page_config(
    page_title="CineMatch - Movie Recommendation Engine",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #1e2139;
        color: #ffffff;
        border: 1px solid #3d4466;
    }
    .stSelectbox > div > div > select {
        background-color: #1e2139;
        color: #ffffff;
    }
    .movie-card {
        background-color: #1e2139;
        border: 1px solid #3d4466;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    .feature-tag {
        background-color: #3d4466;
        color: #ffffff;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
        margin: 2px;
        display: inline-block;
    }
    .score-badge {
        background-color: #ff3e3e;
        color: #ffffff;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load movies and recommendations data"""
    try:
        with open('data/movies.json', 'r', encoding='utf-8') as f:
            movies = json.load(f)
        
        with open('data/recommendations.json', 'r', encoding='utf-8') as f:
            recommendations = json.load(f)
            
        with open('data/manifold.json', 'r', encoding='utf-8') as f:
            manifold = json.load(f)
            
        return movies, recommendations, manifold
    except FileNotFoundError:
        st.error("Data files not found. Please run export_data.py first.")
        return [], [], []

# TMDB API functions
def get_tmdb_poster(movie_id):
    """Get movie poster from TMDB API"""
    api_keys = TMDB_API_KEYS
    base_url = "https://api.themoviedb.org/3/movie/"
    poster_base = "https://image.tmdb.org/t/p/w500/"
    
    for api_key in api_keys:
        try:
            url = f"{base_url}{movie_id}?api_key={api_key}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('poster_path'):
                    return poster_base + data['poster_path']
        except:
            continue
    
    return "https://placehold.co/500x750/0e1117/ffffff.png?text=NO+IMAGE"

def get_movie_by_title(title, movies):
    """Find movie by title"""
    for movie in movies:
        if movie['title'].lower() == title.lower():
            return movie
    return None

# Main app
def main():
    movies, recommendations, manifold = load_data()
    
    if not movies:
        st.error("No data available. Please check your data files.")
        return
    
    # Header
    st.markdown("""
    # 🎬 CineMatch
    ### Advanced Movie Recommendation Engine
    Powered by Vector Similarity & Explainable AI
    """)
    
    # Sidebar
    st.sidebar.markdown("## 🔍 Search Movies")
    
    # Movie search
    movie_titles = [movie['title'] for movie in movies]
    selected_movie = st.sidebar.selectbox(
        "Select a movie:",
        options=movie_titles,
        index=0 if movie_titles else None
    )
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Recommendations", "📊 Analysis", "🌐 3D Manifold"])
    
    with tab1:
        if selected_movie:
            st.markdown(f"## Recommendations for **{selected_movie}**")
            
            # Get movie info
            movie_info = get_movie_by_title(selected_movie, movies)
            if movie_info:
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    poster_url = get_tmdb_poster(movie_info['id'])
                    st.image(poster_url, width=200)
                
                with col2:
                    st.markdown(f"### {movie_info['title']}")
                    genres = movie_info.get('genres', [])
                    if genres:
                        st.markdown("**Genres:** " + " ".join([f"`{g}`" for g in genres]))
            
            # Get recommendations
            if selected_movie in recommendations:
                recs = recommendations[selected_movie][:10]  # Top 10
                
                st.markdown("### 🎯 Top 10 Recommendations")
                
                for i, rec in enumerate(recs, 1):
                    with st.container():
                        st.markdown(f"#### {i}. {rec['title']}")
                        
                        col1, col2, col3 = st.columns([1, 2, 1])
                        
                        with col1:
                            poster_url = get_tmdb_poster(rec['id'])
                            st.image(poster_url, width=150)
                        
                        with col2:
                            # Feature breakdown
                            st.markdown("**Feature Breakdown:**")
                            features_html = ""
                            for feature in rec['features'][:5]:  # Top 5 features
                                feature_name = feature['f'].replace('_', ' ').title()
                                feature_count = feature['c']
                                features_html += f'<span class="feature-tag">{feature_name}: {feature_count}</span>'
                            st.markdown(features_html, unsafe_allow_html=True)
                        
                        with col3:
                            st.markdown(f'<div class="score-badge">Score: {rec["score"]:.4f}</div>', 
                                      unsafe_allow_html=True)
                        
                        st.divider()
            else:
                st.warning("No recommendations available for this movie.")
        else:
            st.info("Please select a movie from the sidebar to see recommendations.")
    
    with tab2:
        st.markdown("## 📊 Recommendation Analysis")
        
        if selected_movie and selected_movie in recommendations:
            recs = recommendations[selected_movie]
            
            # Score distribution
            scores = [rec['score'] for rec in recs]
            titles = [rec['title'][:20] + "..." if len(rec['title']) > 20 else rec['title'] for rec in recs]
            
            fig = go.Figure(data=[
                go.Bar(x=titles[:10], y=scores[:10], 
                       marker_color='#ff3e3e',
                       hovertemplate='<b>%{x}</b><br>Score: %{y:.4f}<extra></extra>')
            ])
            
            fig.update_layout(
                title="Recommendation Scores (Top 10)",
                xaxis_title="Movies",
                yaxis_title="Similarity Score",
                height=500,
                plot_bgcolor='#1e2139',
                paper_bgcolor='#0e1117',
                font=dict(color='#ffffff')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Feature analysis
            st.markdown("### 🔍 Feature Analysis")
            
            # Collect all features
            all_features = {}
            for rec in recs[:10]:
                for feature in rec['features']:
                    feature_name = feature['f']
                    feature_count = feature['c']
                    if feature_name in all_features:
                        all_features[feature_name] += feature_count
                    else:
                        all_features[feature_name] = feature_count
            
            # Sort and display top features
            sorted_features = sorted(all_features.items(), key=lambda x: x[1], reverse=True)[:15]
            
            feature_names = [f[0].replace('_', ' ').title() for f in sorted_features]
            feature_counts = [f[1] for f in sorted_features]
            
            fig2 = go.Figure(data=[
                go.Bar(x=feature_counts, y=feature_names,
                       orientation='h',
                       marker_color='#3d4466',
                       hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>')
            ])
            
            fig2.update_layout(
                title="Top Shared Features",
                xaxis_title="Total Count",
                yaxis_title="Features",
                height=600,
                plot_bgcolor='#1e2139',
                paper_bgcolor='#0e1117',
                font=dict(color='#ffffff'),
                yaxis={'categoryorder': 'total ascending'}
            )
            
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        st.markdown("## 🌐 3D Manifold Visualization")
        
        if manifold:
            # Extract coordinates and movie info
            x_coords = [point['x'] for point in manifold]
            y_coords = [point['y'] for point in manifold]
            z_coords = [point['z'] for point in manifold]
            movie_titles_manifold = [point['title'] for point in manifold]
            
            # Create 3D scatter plot
            fig3 = go.Figure(data=[go.Scatter3d(
                x=x_coords,
                y=y_coords,
                z=z_coords,
                mode='markers',
                marker=dict(
                    size=5,
                    color='#ff3e3e',
                    opacity=0.8
                ),
                text=movie_titles_manifold,
                hovertemplate='<b>%{text}</b><br>X: %{x:.2f}<br>Y: %{y:.2f}<br>Z: %{z:.2f}<extra></extra>'
            )])
            
            fig3.update_layout(
                title="Movie Similarity Manifold (3D SVD Projection)",
                scene=dict(
                    xaxis_title='Component 1',
                    yaxis_title='Component 2',
                    zaxis_title='Component 3',
                    bgcolor='#1e2139',
                    xaxis=dict(backgroundcolor='#1e2139', gridcolor='#3d4466'),
                    yaxis=dict(backgroundcolor='#1e2139', gridcolor='#3d4466'),
                    zaxis=dict(backgroundcolor='#1e2139', gridcolor='#3d4466')
                ),
                height=700,
                plot_bgcolor='#0e1117',
                paper_bgcolor='#0e1117',
                font=dict(color='#ffffff')
            )
            
            st.plotly_chart(fig3, use_container_width=True)
            
            st.markdown("""
            **About this visualization:**
            - This 3D manifold shows the high-dimensional movie feature space projected to 3D using Truncated SVD
            - Movies that are closer together have similar content and metadata
            - The visualization helps identify clusters of similar movies
            """)
        else:
            st.warning("Manifold data not available.")

if __name__ == "__main__":
    main()
