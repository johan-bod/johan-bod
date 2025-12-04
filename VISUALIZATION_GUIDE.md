# Brand Interaction Visualization Guide

## Overview
This project visualizes brand interactions across different topics in the EU market, with a **special focus on Kyocera**. The visualizations show the flow of interactions, market share, and competitive positioning.

## Data Structure
The dataset (`data.csv`) contains:
- **Topics**: 5 different discussion topics (Topic_1 through Topic_5)
- **Brands**: Kyocera, Epson, Xerox, Canon, Ricoh, Konica Minolta, Hyland, Lexmark, Docuware, Open Text, Laserfiche, KDA
- **Metrics**:
  - Results: Number of posts/results found
  - Interactions: Total engagement (likes, shares, comments)
  - Comments: Number of comments
  - Estimated Reach: Estimated audience reach

## Visualizations Generated

### 1. Sankey Diagram (`sankey_brand_flow.html`)
**Purpose**: Shows the flow of interactions from topics to brands

**Features**:
- Visual flow representation from left (topics) to right (brands)
- Kyocera flows highlighted in **red**
- Width of flows proportional to interaction volume
- Interactive: Hover to see exact numbers

**Best for**: Understanding which topics drive interactions for each brand

---

### 2. Interactive Heatmap (`heatmap_interactions.html`)
**Purpose**: Matrix view of brand performance across topics

**Features**:
- Rows = Brands, Columns = Topics
- Color intensity = Number of interactions (darker = more interactions)
- Kyocera row highlighted with **red border**
- Hover shows interactions AND estimated reach

**Best for**: Quick comparison of brand strength across topics

---

### 3. Kyocera Comparison (`kyocera_comparison.html`)
**Purpose**: Direct comparison of Kyocera vs all competitors

**Features**:
- 4 metrics side-by-side: Interactions, Reach, Results, Comments
- Kyocera bars in **red**, competitors in gray
- Shows total aggregated performance across all topics

**Best for**: Executive summary of Kyocera's competitive position

---

### 4. Topic Breakdown (`topic_breakdown.html`)
**Purpose**: Detailed view of top 6 brands across each topic

**Features**:
- Grouped bar chart by topic
- Shows top 6 brands by interaction volume
- Kyocera always included and highlighted in **red**
- Interactive legend (click to toggle brands on/off)

**Best for**: Topic-by-topic competitive analysis

---

### 5. Reach vs Interactions Scatter (`scatter_reach_interactions.html`)
**Purpose**: Relationship between engagement and reach

**Features**:
- X-axis: Number of interactions
- Y-axis: Estimated reach
- Bubble size: Number of results
- Kyocera points in **red**
- Hover to see topic details

**Best for**: Identifying high-efficiency campaigns (high reach with low interaction or vice versa)

---

### 6. Kyocera Market Share (`kyocera_market_share.html`)
**Purpose**: Kyocera's share of interactions per topic

**Features**:
- Shows percentage of total interactions captured by Kyocera
- Sorted by market share
- Hover to see absolute numbers

**Best for**: Identifying topics where Kyocera dominates or needs improvement

---

## How to Use in PowerPoint

### Option 1: Screenshots (RECOMMENDED - Easiest)
1. Open any HTML file in your web browser (Chrome, Firefox, Edge)
2. Interact with the visualization to show the desired view
3. Take a screenshot (Windows: Win+Shift+S, Mac: Cmd+Shift+4)
4. Paste into PowerPoint slide

### Option 2: Interactive Embed (Modern PowerPoint)
1. In PowerPoint, go to `Insert` > `Get Add-ins`
2. Search for "Web Viewer" and install it
3. Use Web Viewer to embed the HTML file
4. The visualization will remain **fully interactive** in presentation mode!

### Option 3: Print to PDF
1. Open HTML in browser
2. Right-click > Print > Save as PDF
3. Insert PDF into PowerPoint as an object

### Option 4: Export from Browser
1. Open HTML file in browser
2. Use browser's built-in "Export" or "Share" features
3. Many browsers allow saving as image or PDF

---

## Running the Visualizations

### First Time Setup
```bash
# Install required packages
pip install -r requirements.txt
```

### Generate All Visualizations
```bash
# Run the visualization script
python visualizations.py
```

This will create all 6 HTML files in the `output/` directory.

---

## Customization

### Changing Topic Names
The data currently uses generic names (Topic_1, Topic_2, etc.). To use real topic names:

1. Open `data.csv`
2. Replace Topic_1, Topic_2, etc. with actual topic names
3. Re-run `python visualizations.py`

### Adding More Data
To add more topics or update data:

1. Edit `data.csv` following the same format
2. Each row needs: Topic, Brand, Results, Interactions, Comments, Estimated_Reach
3. Re-run the script

### Color Scheme
The visualizations use:
- **Red (#FF0000)**: Kyocera (always highlighted)
- **Blue tones**: Topics (in Sankey diagram)
- **Gray/Light colors**: Competitor brands
- **YlOrRd (Yellow-Orange-Red)**: Heatmap intensity

To change colors, edit the `KYOCERA_COLOR` and `OTHER_COLORS` variables in `visualizations.py`.

---

## Technical Details

**Language**: Python 3.11+

**Libraries**:
- `plotly`: Interactive visualizations
- `pandas`: Data manipulation
- `numpy`: Numerical operations

**Output Format**: HTML5 with embedded JavaScript (Plotly.js)

**Browser Compatibility**: All modern browsers (Chrome, Firefox, Safari, Edge)

---

## Visualization Summary Table

| Visualization | Type | Interactive | Best Use Case | Kyocera Focus |
|--------------|------|-------------|---------------|---------------|
| Sankey Flow | Flow Diagram | ✅ | Show topic-to-brand flow | Red flows |
| Heatmap | Matrix | ✅ | Quick comparison across topics | Red border |
| Kyocera Comparison | Bar Chart | ✅ | Direct competitive analysis | Red bars |
| Topic Breakdown | Grouped Bars | ✅ | Detailed per-topic analysis | Red bars |
| Scatter Plot | Bubble Chart | ✅ | Reach vs engagement analysis | Red bubbles |
| Market Share | Horizontal Bar | ✅ | Kyocera's dominance per topic | 100% focus |

---

## Data Quality Notes

- Some brands have zero interactions in certain topics (shown as 0 or empty)
- The visualizations automatically filter out zero-value flows in Sankey diagram
- All metrics are aggregated across the EU market
- Topic names should be updated to reflect actual discussion themes

---

## Troubleshooting

**Problem**: Visualizations don't show in browser
- **Solution**: Make sure you're opening the HTML files from the `output/` directory

**Problem**: Can't embed in PowerPoint
- **Solution**: Use screenshot method (Option 1) - works with all PowerPoint versions

**Problem**: Data doesn't match images
- **Solution**: Update `data.csv` with exact values from your source data

---

## Contact
For questions about the visualizations or data updates, refer to the main repository README.

---

**Generated**: December 2025
**Focus Market**: European Union
**Primary Brand**: Kyocera
