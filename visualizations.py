"""
Brand Interaction Visualization Tool
Focus on Kyocera and competitor brands across different EU topics
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# Load data
df = pd.read_csv('data.csv')

# Define color scheme with Kyocera highlighted
KYOCERA_COLOR = '#FF0000'  # Red to highlight Kyocera
OTHER_COLORS = px.colors.qualitative.Set3

def create_color_map(brands):
    """Create color mapping with Kyocera highlighted"""
    color_map = {}
    other_brands = [b for b in brands if b != 'Kyocera']
    color_map['Kyocera'] = KYOCERA_COLOR
    for i, brand in enumerate(other_brands):
        color_map[brand] = OTHER_COLORS[i % len(OTHER_COLORS)]
    return color_map

# Get all unique brands
brands = df['Brand'].unique()
color_map = create_color_map(brands)

# ============================================================================
# 1. SANKEY DIAGRAM: Topic → Brand Flow (Interactions)
# ============================================================================
def create_sankey_diagram():
    """Create Sankey diagram showing flow from public to topics to brands"""
    print("Creating Sankey diagram...")

    # Filter out zero interactions
    df_sankey = df[df['Interactions'] > 0].copy()

    # Topic name mapping
    topic_names = {
        'Topic_1': 'Digital Printing Solutions',
        'Topic_2': 'Document Solutions',
        'Topic_3': 'Printing Experience Personalisation',
        'Topic_4': 'Technologies and Workflow Optimisation',
        'Topic_5': 'Employment'
    }

    # Create node lists with Public as the first node
    public_node = ['General Public']
    topics = sorted(df_sankey['Topic'].unique().tolist())
    topic_labels = [topic_names.get(t, t) for t in topics]
    brands_list = df_sankey['Brand'].unique().tolist()

    # Create node labels: Public + Topics + Brands
    node_labels = public_node + topic_labels + brands_list

    # Create index mappings
    public_index = 0
    topic_indices = {topic: i + 1 for i, topic in enumerate(topics)}
    brand_indices = {brand: i + 1 + len(topics) for i, brand in enumerate(brands_list)}

    # Calculate total interactions per topic for Public → Topic flows
    topic_totals = df_sankey.groupby('Topic')['Interactions'].sum().to_dict()

    # Create links
    sources = []
    targets = []
    values = []
    link_colors = []

    # Add Public → Topic flows
    for topic in topics:
        sources.append(public_index)
        targets.append(topic_indices[topic])
        values.append(topic_totals[topic])
        link_colors.append('rgba(100, 150, 250, 0.3)')  # Blue for public flows

    # Add Topic → Brand flows
    for _, row in df_sankey.iterrows():
        sources.append(topic_indices[row['Topic']])
        targets.append(brand_indices[row['Brand']])
        values.append(row['Interactions'])

        # Highlight Kyocera flows
        if row['Brand'] == 'Kyocera':
            link_colors.append('rgba(255, 0, 0, 0.4)')
        else:
            link_colors.append('rgba(100, 100, 100, 0.2)')

    # Create node colors
    node_colors = ['rgba(100, 200, 255, 0.9)']  # Public in bright blue
    node_colors += ['rgba(100, 150, 200, 0.8)'] * len(topics)  # Topics in blue
    for brand in brands_list:
        if brand == 'Kyocera':
            node_colors.append('rgba(255, 0, 0, 0.8)')  # Kyocera in red
        else:
            node_colors.append('rgba(150, 150, 150, 0.6)')  # Others in gray

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=node_labels,
            color=node_colors
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors
        )
    )])

    fig.update_layout(
        title={
            'text': 'Public → Topic → Brand Interaction Flow (EU Market)<br><sub>General public drives topic conversations | Kyocera highlighted in red</sub>',
            'x': 0.5,
            'xanchor': 'center'
        },
        font=dict(size=12),
        height=700,
        width=1400
    )

    # Save outputs
    fig.write_html('output/sankey_brand_flow.html')
    print("✓ Sankey diagram saved")
    return fig

# ============================================================================
# 2. INTERACTIVE HEATMAP: Brand × Topic
# ============================================================================
def create_heatmap():
    """Create interactive heatmap of interactions by brand and topic"""
    print("Creating heatmap...")

    # Pivot data for heatmap
    pivot_interactions = df.pivot(index='Brand', columns='Topic', values='Interactions')
    pivot_reach = df.pivot(index='Brand', columns='Topic', values='Estimated_Reach')

    # Sort by total interactions
    pivot_interactions['Total'] = pivot_interactions.sum(axis=1)
    pivot_interactions = pivot_interactions.sort_values('Total', ascending=False)
    pivot_interactions = pivot_interactions.drop('Total', axis=1)

    # Create hover text with both metrics
    hover_text = []
    for i, brand in enumerate(pivot_interactions.index):
        row_text = []
        for j, topic in enumerate(pivot_interactions.columns):
            interactions = pivot_interactions.iloc[i, j]
            reach = pivot_reach.loc[brand, topic]
            text = f'<b>{brand}</b><br>{topic}<br>Interactions: {interactions:,.0f}<br>Reach: {reach:,.0f}'
            row_text.append(text)
        hover_text.append(row_text)

    # Create figure
    fig = go.Figure(data=go.Heatmap(
        z=pivot_interactions.values,
        x=pivot_interactions.columns,
        y=pivot_interactions.index,
        colorscale='YlOrRd',
        text=hover_text,
        hovertemplate='%{text}<extra></extra>',
        colorbar=dict(title='Interactions')
    ))

    # Highlight Kyocera row
    if 'Kyocera' in pivot_interactions.index:
        kyocera_idx = list(pivot_interactions.index).index('Kyocera')
        fig.add_shape(
            type='rect',
            x0=-0.5, x1=len(pivot_interactions.columns)-0.5,
            y0=kyocera_idx-0.5, y1=kyocera_idx+0.5,
            line=dict(color='red', width=3)
        )

    fig.update_layout(
        title={
            'text': 'Brand Interactions Heatmap by Topic<br><sub>Kyocera highlighted with red border</sub>',
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Topic',
        yaxis_title='Brand',
        height=600,
        width=1000,
        font=dict(size=11)
    )

    # Save outputs
    fig.write_html('output/heatmap_interactions.html')
    print("✓ Heatmap saved")
    return fig

# ============================================================================
# 3. KYOCERA-FOCUSED COMPARISON
# ============================================================================
def create_kyocera_comparison():
    """Create visualizations focused on Kyocera vs competitors"""
    print("Creating Kyocera comparison charts...")

    # Calculate total metrics by brand
    brand_totals = df.groupby('Brand').agg({
        'Interactions': 'sum',
        'Estimated_Reach': 'sum',
        'Results': 'sum',
        'Comments': 'sum'
    }).reset_index()

    brand_totals = brand_totals.sort_values('Interactions', ascending=True)

    # Create colors
    colors = [KYOCERA_COLOR if brand == 'Kyocera' else 'lightgray' for brand in brand_totals['Brand']]

    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Total Interactions', 'Estimated Reach',
                       'Total Results', 'Total Comments'),
        specs=[[{'type': 'bar'}, {'type': 'bar'}],
               [{'type': 'bar'}, {'type': 'bar'}]]
    )

    # Interactions
    fig.add_trace(
        go.Bar(
            x=brand_totals['Interactions'],
            y=brand_totals['Brand'],
            orientation='h',
            marker_color=colors,
            name='Interactions',
            showlegend=False,
            text=brand_totals['Interactions'],
            textposition='auto'
        ),
        row=1, col=1
    )

    # Reach
    fig.add_trace(
        go.Bar(
            x=brand_totals['Estimated_Reach'],
            y=brand_totals['Brand'],
            orientation='h',
            marker_color=colors,
            name='Reach',
            showlegend=False,
            text=brand_totals['Estimated_Reach'],
            textposition='auto'
        ),
        row=1, col=2
    )

    # Results
    fig.add_trace(
        go.Bar(
            x=brand_totals['Results'],
            y=brand_totals['Brand'],
            orientation='h',
            marker_color=colors,
            name='Results',
            showlegend=False,
            text=brand_totals['Results'],
            textposition='auto'
        ),
        row=2, col=1
    )

    # Comments
    fig.add_trace(
        go.Bar(
            x=brand_totals['Comments'],
            y=brand_totals['Brand'],
            orientation='h',
            marker_color=colors,
            name='Comments',
            showlegend=False,
            text=brand_totals['Comments'],
            textposition='auto'
        ),
        row=2, col=2
    )

    fig.update_layout(
        title={
            'text': 'Kyocera vs Competitors: Total Metrics Across All Topics<br><sub>Kyocera highlighted in red</sub>',
            'x': 0.5,
            'xanchor': 'center'
        },
        height=800,
        width=1400,
        showlegend=False,
        font=dict(size=10)
    )

    # Save outputs
    fig.write_html('output/kyocera_comparison.html')
    print("✓ Kyocera comparison saved")
    return fig

# ============================================================================
# 4. TOPIC-BY-TOPIC BREAKDOWN WITH KYOCERA FOCUS
# ============================================================================
def create_topic_breakdown():
    """Create stacked bar chart showing Kyocera's position in each topic"""
    print("Creating topic breakdown...")

    # Get top 6 brands by total interactions
    top_brands = df.groupby('Brand')['Interactions'].sum().nlargest(6).index.tolist()

    # Ensure Kyocera is included
    if 'Kyocera' not in top_brands:
        top_brands = ['Kyocera'] + top_brands[:5]

    df_filtered = df[df['Brand'].isin(top_brands)]

    fig = go.Figure()

    for brand in top_brands:
        brand_data = df_filtered[df_filtered['Brand'] == brand]
        color = KYOCERA_COLOR if brand == 'Kyocera' else color_map.get(brand, 'gray')

        fig.add_trace(go.Bar(
            name=brand,
            x=brand_data['Topic'],
            y=brand_data['Interactions'],
            marker_color=color,
            text=brand_data['Interactions'],
            textposition='auto',
            hovertemplate='<b>%{fullData.name}</b><br>Topic: %{x}<br>Interactions: %{y:,}<extra></extra>'
        ))

    fig.update_layout(
        title={
            'text': 'Brand Interactions by Topic (Top 6 Brands)<br><sub>Kyocera highlighted in red</sub>',
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Topic',
        yaxis_title='Number of Interactions',
        barmode='group',
        height=600,
        width=1200,
        font=dict(size=11),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )

    # Save outputs
    fig.write_html('output/topic_breakdown.html')
    print("✓ Topic breakdown saved")
    return fig

# ============================================================================
# 5. REACH VS INTERACTIONS SCATTER PLOT
# ============================================================================
def create_scatter_plot():
    """Create scatter plot showing reach vs interactions with Kyocera highlighted"""
    print("Creating scatter plot...")

    # Filter out zeros
    df_scatter = df[(df['Interactions'] > 0) | (df['Estimated_Reach'] > 0)].copy()

    # Add size based on results
    df_scatter['Size'] = df_scatter['Results'] * 2 + 5

    # Create colors
    df_scatter['Color'] = df_scatter['Brand'].apply(
        lambda x: KYOCERA_COLOR if x == 'Kyocera' else 'rgba(100, 100, 100, 0.5)'
    )

    fig = px.scatter(
        df_scatter,
        x='Interactions',
        y='Estimated_Reach',
        color='Brand',
        size='Size',
        hover_data=['Topic', 'Results', 'Comments'],
        color_discrete_map=color_map,
        title='Interaction Reach vs Engagement by Brand<br><sub>Kyocera in red | Bubble size = Results</sub>',
        labels={'Interactions': 'Number of Interactions',
                'Estimated_Reach': 'Estimated Reach'}
    )

    # Update traces to emphasize Kyocera
    fig.update_traces(
        marker=dict(line=dict(width=1, color='DarkSlateGrey')),
        selector=dict(mode='markers')
    )

    fig.update_layout(
        height=600,
        width=1000,
        font=dict(size=11),
        title_x=0.5
    )

    # Save outputs
    fig.write_html('output/scatter_reach_interactions.html')
    print("✓ Scatter plot saved")
    return fig

# ============================================================================
# 6. KYOCERA MARKET SHARE BY TOPIC
# ============================================================================
def create_kyocera_market_share():
    """Calculate and visualize Kyocera's market share per topic"""
    print("Creating Kyocera market share analysis...")

    # Calculate market share by topic
    topic_totals = df.groupby('Topic')['Interactions'].sum()
    kyocera_data = df[df['Brand'] == 'Kyocera'].set_index('Topic')

    market_share = []
    for topic in df['Topic'].unique():
        total = topic_totals[topic]
        kyocera_val = kyocera_data.loc[topic, 'Interactions'] if topic in kyocera_data.index else 0
        share = (kyocera_val / total * 100) if total > 0 else 0
        market_share.append({
            'Topic': topic,
            'Kyocera_Share': share,
            'Kyocera_Interactions': kyocera_val,
            'Total_Interactions': total
        })

    df_share = pd.DataFrame(market_share).sort_values('Kyocera_Share', ascending=True)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_share['Kyocera_Share'],
        y=df_share['Topic'],
        orientation='h',
        marker_color=KYOCERA_COLOR,
        text=[f"{val:.1f}%" for val in df_share['Kyocera_Share']],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Kyocera Share: %{x:.1f}%<br>Kyocera Interactions: %{customdata[0]:,}<br>Total Interactions: %{customdata[1]:,}<extra></extra>',
        customdata=df_share[['Kyocera_Interactions', 'Total_Interactions']].values
    ))

    fig.update_layout(
        title={
            'text': 'Kyocera Market Share by Topic<br><sub>Percentage of total interactions</sub>',
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Market Share (%)',
        yaxis_title='Topic',
        height=500,
        width=900,
        font=dict(size=11)
    )

    # Save outputs
    fig.write_html('output/kyocera_market_share.html')
    print("✓ Kyocera market share saved")
    return fig

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == '__main__':
    import os

    # Create output directory
    os.makedirs('output', exist_ok=True)

    print("=" * 60)
    print("BRAND INTERACTION VISUALIZATION TOOL")
    print("Focus: Kyocera in EU Market")
    print("=" * 60)
    print()

    # Generate all visualizations
    try:
        create_sankey_diagram()
        create_heatmap()
        create_kyocera_comparison()
        create_topic_breakdown()
        create_scatter_plot()
        create_kyocera_market_share()

        print()
        print("=" * 60)
        print("✓ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("Output files (interactive HTML):")
        print("    - output/sankey_brand_flow.html")
        print("    - output/heatmap_interactions.html")
        print("    - output/kyocera_comparison.html")
        print("    - output/topic_breakdown.html")
        print("    - output/scatter_reach_interactions.html")
        print("    - output/kyocera_market_share.html")
        print()
        print("To use in PowerPoint:")
        print("  1. RECOMMENDED: Open HTML file in browser, take screenshot")
        print("  2. INTERACTIVE: Insert > Get Add-ins > 'Web Viewer' to embed HTML")
        print("  3. Can also open in browser and use browser's print-to-PDF feature")

    except Exception as e:
        print(f"✗ Error generating visualizations: {e}")
        import traceback
        traceback.print_exc()
