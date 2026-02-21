# CineMatch | Streamlit Movie Recommendation Engine

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://cinematch-streamlit.streamlit.app)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

CineMatch is a high-performance, content-based movie recommender system built with Streamlit. It combines advanced natural language processing (NLP) with an interactive web interface to demonstrate the power of vector similarity in information retrieval.

**🚀 Live Streamlit App**: [https://cinematch-streamlit.streamlit.app](https://cinematch-streamlit.streamlit.app)

---

## Core Features

### 1. Vector Similarity Engine
*   **Methodology**: Uses **Cosine Similarity** on high-dimensional movie metadata vectors.
*   **Tag Fusion**: Combines plot overviews, genres, keywords, cast, and directors into unique textual signatures.
*   **3D Manifold Visualization**: Projects the 5000-D feature space into an interactive 3D manifold using **Truncated SVD** for latent cluster analysis.

### 2. Explainable AI (XAI)
*   **Transparency**: Every recommendation includes a mathematical breakdown of why it was chosen.
*   **Feature Attribution**: Visualizes shared metadata features between the query and recommended movies.

### 3. Experimental Evaluation
*   **Ablation Study**: Benchmarks different vectorization strategies (**Bag-of-Words**, **TF-IDF**, and **SBERT**).
*   **Precision@10**: Evaluates accuracy using Genre Overlap as a scientific proxy for relevance.

### 4. Enterprise-Grade Reliability
*   **API Load Balancing**: Implements random round-robin rotation between multiple TMDB API keys to maximize image loading throughput.
*   **Resilient Fallbacks**: Multi-stage poster fetching strategy (Direct ID -> Title Search -> High-end Placeholder).

---

## Project Structure

```text
├── streamlit_app.py        # Main Streamlit Application
├── requirements.txt        # Python Dependencies (includes Streamlit)
├── config.py              # TMDB API Configuration
├── README.md              # Project Documentation
└── data/                  # Essential JSON Data Files
    ├── movies.json        # Movie Metadata (4,800+ titles)
    ├── recommendations.json # Pre-computed Recommendations
    ├── manifold.json      # 3D SVD Visualization Data
    └── evaluation.json    # Benchmark Metrics
```

---

## Deployment

### Streamlit Cloud (Recommended)
The app is deployed on Streamlit Cloud and automatically updates when pushed to the `master` branch.

**🚀 Live App**: [https://cinematch-streamlit.streamlit.app](https://cinematch-streamlit.streamlit.app)

### Local Development
To run the app locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/kram2006/cinematch_streamlit.git
   cd cinematch_streamlit
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

### Environment Variables
Set up TMDB API keys in `config.py` or as environment variables for poster fetching functionality.

---

## Author
**K RAMA KRISHNA NARASIMHA CHOWDARY**  
*Research Status: ONLINE*

---
© 2026 CineMatch Research Project. Released under the MIT License.
