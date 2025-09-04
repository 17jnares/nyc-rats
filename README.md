# NYC Rats — Geospatial Analysis & Animated Map

This project presents an animated geospatial analysis of **NYC rat sightings** in relation to subway entrances.  
Motivated by the rise in reported sightings during the Covid-19 pandemic, the project explores whether rat movement patterns align with urban transit infrastructure.  

The analysis combines **open data ingestion**, **nearest-neighbor spatial modeling**, and **interactive visualization** to illustrate how public datasets can be leveraged to study behavioral and environmental dynamics in a city.

## 🌐 Live Demo
[➡️ View the interactive map here](https://17jnares.github.io/nyc-rats/nyc_rats_portfolio_notebook.html)

---

## 🔑 Key Skills Demonstrated
- Data ingestion from public APIs (NYC Open Data via Socrata)  
- Data cleaning, preprocessing, and temporal aggregation (`pandas`)  
- Spatial analysis using nearest-neighbor search (`scikit-learn` KDTree)  
- Geospatial visualization and animation (`plotly`, Mapbox/USGS basemaps)  
- Reproducible analysis and interactive reporting (Jupyter Notebook + HTML export)  

---

## 📂 Project Structure
```
nyc-rats/
├── notebooks/
│   └── nyc_rats_portfolio_notebook.ipynb   # main analysis + visualization
├── docs/
│   └── nyc_rats_portfolio_notebook.html    # interactive HTML (GitHub Pages)
├── README.md                               # project overview (this file)
└── requirements.txt                        # dependencies
```
