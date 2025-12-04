"""
Generate static PNG images from the visualizations
Requires: Chrome browser installed + kaleido package
"""

import subprocess
import sys

# Check if kaleido is installed
try:
    import kaleido
except ImportError:
    print("Installing kaleido...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "kaleido"])
    import kaleido

# Now run the main visualization script but with PNG export enabled
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

# Import all the functions from visualizations.py
exec(open('visualizations.py').read())

print("\n" + "="*60)
print("GENERATING STATIC PNG IMAGES")
print("="*60 + "\n")

# Create output directory
os.makedirs('output/png', exist_ok=True)

# Generate each visualization and save as PNG
print("Generating PNG images...")

try:
    # Sankey
    fig = create_sankey_diagram()
    fig.write_image('output/png/sankey_brand_flow.png', width=1200, height=600, scale=2)
    print("✓ Sankey PNG saved")

    # Heatmap
    fig = create_heatmap()
    fig.write_image('output/png/heatmap_interactions.png', width=1000, height=600, scale=2)
    print("✓ Heatmap PNG saved")

    # Kyocera comparison
    fig = create_kyocera_comparison()
    fig.write_image('output/png/kyocera_comparison.png', width=1400, height=800, scale=2)
    print("✓ Kyocera comparison PNG saved")

    # Topic breakdown
    fig = create_topic_breakdown()
    fig.write_image('output/png/topic_breakdown.png', width=1200, height=600, scale=2)
    print("✓ Topic breakdown PNG saved")

    # Scatter plot
    fig = create_scatter_plot()
    fig.write_image('output/png/scatter_reach_interactions.png', width=1000, height=600, scale=2)
    print("✓ Scatter plot PNG saved")

    # Market share
    fig = create_kyocera_market_share()
    fig.write_image('output/png/kyocera_market_share.png', width=900, height=500, scale=2)
    print("✓ Market share PNG saved")

    print("\n" + "="*60)
    print("✓ ALL PNG IMAGES GENERATED!")
    print("="*60)
    print("\nPNG files saved in: output/png/")
    print("These can be directly inserted into PowerPoint")

except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nMake sure Chrome browser is installed!")
    print("On Linux: sudo apt-get install chromium-browser")
    print("On Mac: Download from google.com/chrome")
    print("On Windows: Download from google.com/chrome")
