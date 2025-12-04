"""
Create a single-file interactive dashboard with all visualizations
This creates ONE HTML file that works anywhere - perfect for presentations!
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

# Import all the functions from visualizations.py
exec(open('visualizations.py').read())

print("\n" + "="*60)
print("CREATING INTERACTIVE PRESENTATION DASHBOARD")
print("="*60 + "\n")

# Generate all figures
print("Generating visualizations...")
fig1 = create_sankey_diagram()
fig2 = create_heatmap()
fig3 = create_kyocera_comparison()
fig4 = create_topic_breakdown()
fig5 = create_scatter_plot()
fig6 = create_kyocera_market_share()

# Create HTML with all visualizations
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Brand Interaction Analysis - EU Market</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 50px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        .tabs {
            display: flex;
            background: #f5f5f5;
            border-bottom: 2px solid #ddd;
            overflow-x: auto;
        }
        .tab {
            padding: 15px 25px;
            cursor: pointer;
            border: none;
            background: transparent;
            font-size: 14px;
            font-weight: 600;
            color: #666;
            transition: all 0.3s;
            white-space: nowrap;
        }
        .tab:hover {
            background: #e0e0e0;
        }
        .tab.active {
            background: white;
            color: #667eea;
            border-bottom: 3px solid #667eea;
        }
        .tab-content {
            display: none;
            padding: 20px;
            animation: fadeIn 0.3s;
        }
        .tab-content.active {
            display: block;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .chart-container {
            width: 100%;
            min-height: 600px;
        }
        .description {
            background: #f9f9f9;
            padding: 15px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }
        .description h3 {
            color: #667eea;
            margin-bottom: 8px;
        }
        .footer {
            text-align: center;
            padding: 20px;
            background: #f5f5f5;
            color: #666;
            font-size: 14px;
        }
        .kyocera-highlight {
            color: #FF0000;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Brand Interaction Analysis</h1>
            <p>EU Market Overview - Focus on <span class="kyocera-highlight">Kyocera</span></p>
        </div>

        <div class="tabs">
            <button class="tab active" onclick="showTab(0)">🌊 Flow Analysis</button>
            <button class="tab" onclick="showTab(1)">🔥 Heatmap</button>
            <button class="tab" onclick="showTab(2)">📊 Kyocera vs All</button>
            <button class="tab" onclick="showTab(3)">📈 By Topic</button>
            <button class="tab" onclick="showTab(4)">🎯 Reach vs Engagement</button>
            <button class="tab" onclick="showTab(5)">📍 Market Share</button>
        </div>

        <div id="content0" class="tab-content active">
            <div class="description">
                <h3>Sankey Flow Diagram</h3>
                <p>Visualizes the flow of interactions from topics to brands. <span class="kyocera-highlight">Kyocera flows are highlighted in red</span>. Wider flows indicate higher interaction volumes.</p>
            </div>
            <div id="chart1" class="chart-container"></div>
        </div>

        <div id="content1" class="tab-content">
            <div class="description">
                <h3>Interaction Heatmap</h3>
                <p>Matrix view showing brand performance across all topics. <span class="kyocera-highlight">Kyocera row is outlined in red</span>. Darker colors indicate more interactions.</p>
            </div>
            <div id="chart2" class="chart-container"></div>
        </div>

        <div id="content2" class="tab-content">
            <div class="description">
                <h3>Kyocera Competitive Analysis</h3>
                <p>Direct comparison of <span class="kyocera-highlight">Kyocera (red bars)</span> against all competitors across four key metrics: interactions, reach, results, and comments.</p>
            </div>
            <div id="chart3" class="chart-container"></div>
        </div>

        <div id="content3" class="tab-content">
            <div class="description">
                <h3>Topic-by-Topic Breakdown</h3>
                <p>Detailed analysis of top 6 brands for each topic. <span class="kyocera-highlight">Kyocera is always shown in red</span>. Click legend items to toggle brands on/off.</p>
            </div>
            <div id="chart4" class="chart-container"></div>
        </div>

        <div id="content4" class="tab-content">
            <div class="description">
                <h3>Reach vs Interactions Scatter Plot</h3>
                <p>Explores the relationship between engagement and reach. <span class="kyocera-highlight">Kyocera points highlighted in red</span>. Bubble size represents number of results.</p>
            </div>
            <div id="chart5" class="chart-container"></div>
        </div>

        <div id="content5" class="tab-content">
            <div class="description">
                <h3>Kyocera Market Share by Topic</h3>
                <p>Shows <span class="kyocera-highlight">Kyocera's percentage</span> of total interactions for each topic. Identifies strengths and growth opportunities.</p>
            </div>
            <div id="chart6" class="chart-container"></div>
        </div>

        <div class="footer">
            <p>Interactive Brand Interaction Dashboard | EU Market Analysis | Kyocera Focus</p>
            <p style="margin-top: 5px; font-size: 12px;">Tip: Hover over charts for details, click-drag to zoom, double-click to reset</p>
        </div>
    </div>

    <script>
        // Chart data
        const charts = [
            """ + fig1.to_json() + """,
            """ + fig2.to_json() + """,
            """ + fig3.to_json() + """,
            """ + fig4.to_json() + """,
            """ + fig5.to_json() + """,
            """ + fig6.to_json() + """
        ];

        // Render all charts
        charts.forEach((chart, index) => {
            Plotly.newPlot('chart' + (index + 1), chart.data, chart.layout, {responsive: true});
        });

        // Tab switching
        function showTab(index) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });

            // Show selected tab
            document.getElementById('content' + index).classList.add('active');
            document.querySelectorAll('.tab')[index].classList.add('active');

            // Trigger resize for proper rendering
            window.dispatchEvent(new Event('resize'));
        }

        // Handle keyboard navigation
        document.addEventListener('keydown', (e) => {
            const currentTab = document.querySelector('.tab.active');
            const currentIndex = Array.from(document.querySelectorAll('.tab')).indexOf(currentTab);

            if (e.key === 'ArrowRight' && currentIndex < 5) {
                showTab(currentIndex + 1);
            } else if (e.key === 'ArrowLeft' && currentIndex > 0) {
                showTab(currentIndex - 1);
            }
        });
    </script>
</body>
</html>
"""

# Save the dashboard
output_file = 'output/presentation_dashboard.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\n" + "="*60)
print("✓ PRESENTATION DASHBOARD CREATED!")
print("="*60)
print(f"\nFile created: {output_file}")
print("\nThis single HTML file contains ALL 6 visualizations with tabs.")
print("\nHow to use:")
print("  1. Open in any web browser - works offline!")
print("  2. Navigate with tabs or arrow keys")
print("  3. Present directly from browser (F11 for fullscreen)")
print("  4. OR link from PowerPoint for interactive access")
print("\n✨ This file is completely self-contained and portable!")
