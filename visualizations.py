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

# Modern Kyocera-inspired color scheme
KYOCERA_PRIMARY = '#E4032E'  # Kyocera crimson red
KYOCERA_DARK = '#8B0000'     # Dark red
KYOCERA_LIGHT = '#FF6B8A'    # Light red/pink

# Modern professional color palette
MODERN_COLORS = {
    'topic_gradient_start': '#667eea',  # Purple
    'topic_gradient_end': '#764ba2',    # Deep purple
    'neutral_dark': '#2C3E50',          # Dark blue-gray
    'neutral_medium': '#95A5A6',        # Medium gray
    'neutral_light': '#ECF0F1',         # Light gray
    'accent_blue': '#3498DB',           # Bright blue
    'accent_green': '#2ECC71',          # Green
    'accent_orange': '#E67E22',         # Orange
    'accent_purple': '#9B59B6',         # Purple
    'accent_teal': '#1ABC9C',           # Teal
}

# Sophisticated brand colors (excluding Kyocera)
BRAND_COLORS = [
    '#3498DB',  # Blue - modern, trustworthy
    '#2ECC71',  # Green - growth, success
    '#E67E22',  # Orange - energy, innovation
    '#9B59B6',  # Purple - creativity, premium
    '#1ABC9C',  # Teal - balance, calm
    '#34495E',  # Dark gray - professional
    '#16A085',  # Dark teal - stability
    '#8E44AD',  # Dark purple - luxury
    '#C0392B',  # Dark red - power
    '#D35400',  # Dark orange - warmth
    '#7F8C8D',  # Gray - neutral
]

def create_color_map(brands):
    """Create modern color mapping with Kyocera highlighted"""
    color_map = {}
    other_brands = [b for b in brands if b != 'Kyocera']
    color_map['Kyocera'] = KYOCERA_PRIMARY
    for i, brand in enumerate(other_brands):
        color_map[brand] = BRAND_COLORS[i % len(BRAND_COLORS)]
    return color_map

# Get all unique brands
brands = df['Brand'].unique()
color_map = create_color_map(brands)

# ============================================================================
# 1. SANKEY DIAGRAM: Topic → Brand Flow (Interactions)
# ============================================================================
def create_sankey_diagram():
    """Create modern Sankey diagram showing flow from topics to brands"""
    print("Creating Sankey diagram...")

    # Filter out zero interactions
    df_sankey = df[df['Interactions'] > 0].copy()

    # Create node lists
    topics = sorted(df_sankey['Topic'].unique().tolist())
    brands_list = sorted(df_sankey['Brand'].unique().tolist(),
                        key=lambda x: (x != 'Kyocera', -df_sankey[df_sankey['Brand']==x]['Interactions'].sum()))

    # Create node labels with emoji indicators
    topic_labels = [f"📊 {topic}" for topic in topics]
    brand_labels = [f"{'🔴' if brand == 'Kyocera' else '🏢'} {brand}" for brand in brands_list]
    node_labels = topic_labels + brand_labels

    # Create index mappings
    topic_indices = {topic: i for i, topic in enumerate(topics)}
    brand_indices = {brand: i + len(topics) for i, brand in enumerate(brands_list)}

    # Create links with enhanced data
    sources = []
    targets = []
    values = []
    link_colors = []
    link_labels = []

    for _, row in df_sankey.iterrows():
        sources.append(topic_indices[row['Topic']])
        targets.append(brand_indices[row['Brand']])
        values.append(row['Interactions'])

        # Create sophisticated link colors
        if row['Brand'] == 'Kyocera':
            # Kyocera flows - vibrant crimson with good opacity
            link_colors.append(f'rgba(228, 3, 46, 0.5)')
        else:
            # Other brands - use their brand color with transparency
            brand_color = color_map.get(row['Brand'], MODERN_COLORS['neutral_medium'])
            # Convert hex to rgba
            rgb = tuple(int(brand_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            link_colors.append(f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.3)')

        link_labels.append(f"{row['Topic']} → {row['Brand']}<br>{row['Interactions']:,} interactions")

    # Create sophisticated node colors with gradients
    node_colors = []

    # Topic nodes - gradient purple to blue
    topic_gradient_colors = ['#667eea', '#764ba2', '#8e54e9', '#4facfe', '#667eea']
    for i, topic in enumerate(topics):
        node_colors.append(topic_gradient_colors[i % len(topic_gradient_colors)])

    # Brand nodes - use brand colors
    for brand in brands_list:
        if brand == 'Kyocera':
            node_colors.append(KYOCERA_PRIMARY)
        else:
            node_colors.append(color_map.get(brand, MODERN_COLORS['neutral_medium']))

    # Create custom hover text for nodes
    node_customdata = []
    for topic in topics:
        total = df_sankey[df_sankey['Topic'] == topic]['Interactions'].sum()
        node_customdata.append(f"{total:,} total interactions")
    for brand in brands_list:
        total = df_sankey[df_sankey['Brand'] == brand]['Interactions'].sum()
        node_customdata.append(f"{total:,} total interactions")

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=25,
            thickness=25,
            line=dict(color='white', width=2),
            label=node_labels,
            color=node_colors,
            customdata=node_customdata,
            hovertemplate='<b>%{label}</b><br>%{customdata}<extra></extra>'
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors,
            customdata=link_labels,
            hovertemplate='%{customdata}<extra></extra>'
        ),
        textfont=dict(color='white', size=12, family='Arial, sans-serif')
    )])

    fig.update_layout(
        title={
            'text': '<b>Brand Interaction Flow Analysis</b><br><sub style="font-size:14px">EU Market • Kyocera 🔴 in Focus</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': MODERN_COLORS['neutral_dark'], 'family': 'Arial, sans-serif'}
        },
        font=dict(size=13, family='Arial, sans-serif', color=MODERN_COLORS['neutral_dark']),
        height=700,
        width=1400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='#FAFAFA',
        margin=dict(l=20, r=20, t=100, b=20)
    )

    # Save outputs
    fig.write_html('output/sankey_brand_flow.html')
    print("✓ Sankey diagram saved")
    return fig

# ============================================================================
# 2. INTERACTIVE HEATMAP: Brand × Topic
# ============================================================================
def create_heatmap():
    """Create modern interactive heatmap of interactions by brand and topic"""
    print("Creating heatmap...")

    # Pivot data for heatmap
    pivot_interactions = df.pivot(index='Brand', columns='Topic', values='Interactions')
    pivot_reach = df.pivot(index='Brand', columns='Topic', values='Estimated_Reach')

    # Sort by total interactions with Kyocera on top
    pivot_interactions['Total'] = pivot_interactions.sum(axis=1)
    pivot_interactions = pivot_interactions.sort_values('Total', ascending=False)

    # Move Kyocera to top if present
    if 'Kyocera' in pivot_interactions.index:
        kyocera_row = pivot_interactions.loc[['Kyocera']]
        other_rows = pivot_interactions.drop('Kyocera')
        pivot_interactions = pd.concat([kyocera_row, other_rows])

    pivot_interactions = pivot_interactions.drop('Total', axis=1)

    # Create enhanced hover text
    hover_text = []
    for i, brand in enumerate(pivot_interactions.index):
        row_text = []
        for j, topic in enumerate(pivot_interactions.columns):
            interactions = pivot_interactions.iloc[i, j]
            reach = pivot_reach.loc[brand, topic]
            emoji = '🔴' if brand == 'Kyocera' else '🏢'
            text = f'<b>{emoji} {brand}</b><br>📊 {topic}<br>💬 Interactions: {interactions:,.0f}<br>👥 Reach: {reach:,.0f}'
            row_text.append(text)
        hover_text.append(row_text)

    # Create modern colorscale - Kyocera red gradient
    colorscale = [
        [0, '#FFFFFF'],      # White for zero
        [0.2, '#FFE5E5'],    # Very light red
        [0.4, '#FFB3B3'],    # Light red
        [0.6, '#FF6B6B'],    # Medium red
        [0.8, '#E4032E'],    # Kyocera red
        [1, '#8B0000']       # Dark red
    ]

    # Create figure
    fig = go.Figure(data=go.Heatmap(
        z=pivot_interactions.values,
        x=pivot_interactions.columns,
        y=pivot_interactions.index,
        colorscale=colorscale,
        text=hover_text,
        hovertemplate='%{text}<extra></extra>',
        colorbar=dict(
            title=dict(text='Interactions', font=dict(size=14)),
            thickness=15,
            len=0.7,
            tickfont=dict(size=11)
        ),
        xgap=2,
        ygap=2
    ))

    # Highlight Kyocera row with modern styling
    if 'Kyocera' in pivot_interactions.index:
        kyocera_idx = list(pivot_interactions.index).index('Kyocera')
        fig.add_shape(
            type='rect',
            x0=-0.5, x1=len(pivot_interactions.columns)-0.5,
            y0=kyocera_idx-0.5, y1=kyocera_idx+0.5,
            line=dict(color=KYOCERA_PRIMARY, width=4),
            fillcolor='rgba(228, 3, 46, 0.05)'
        )

    fig.update_layout(
        title={
            'text': '<b>Brand Performance Heatmap</b><br><sub style="font-size:14px">Interaction Intensity by Topic • 🔴 Kyocera Highlighted</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 22, 'color': MODERN_COLORS['neutral_dark'], 'family': 'Arial, sans-serif'}
        },
        xaxis=dict(
            title=dict(text='<b>Discussion Topics</b>', font=dict(size=14)),
            tickfont=dict(size=12),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(text='<b>Brands</b>', font=dict(size=14)),
            tickfont=dict(size=12),
            showgrid=False
        ),
        height=650,
        width=1200,
        font=dict(size=12, family='Arial, sans-serif'),
        plot_bgcolor='#FAFAFA',
        paper_bgcolor='#FAFAFA',
        margin=dict(l=120, r=20, t=100, b=80)
    )

    # Save outputs
    fig.write_html('output/heatmap_interactions.html')
    print("✓ Heatmap saved")
    return fig

# ============================================================================
# 3. KYOCERA-FOCUSED COMPARISON
# ============================================================================
def create_kyocera_comparison():
    """Create modern visualizations focused on Kyocera vs competitors"""
    print("Creating Kyocera comparison charts...")

    # Calculate total metrics by brand
    brand_totals = df.groupby('Brand').agg({
        'Interactions': 'sum',
        'Estimated_Reach': 'sum',
        'Results': 'sum',
        'Comments': 'sum'
    }).reset_index()

    brand_totals = brand_totals.sort_values('Interactions', ascending=True)

    # Create sophisticated colors with gradient effect
    colors = []
    for brand in brand_totals['Brand']:
        if brand == 'Kyocera':
            colors.append(KYOCERA_PRIMARY)
        else:
            colors.append(MODERN_COLORS['neutral_medium'])

    # Create subplots with modern styling
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            '<b>💬 Total Interactions</b>',
            '<b>👥 Estimated Reach</b>',
            '<b>📊 Total Results</b>',
            '<b>💭 Total Comments</b>'
        ),
        specs=[[{'type': 'bar'}, {'type': 'bar'}],
               [{'type': 'bar'}, {'type': 'bar'}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.10
    )

    # Enhanced bar styling function
    def create_bar(x_data, y_data, colors, row, col, format_suffix=''):
        text_vals = [f"{v:,.0f}{format_suffix}" for v in x_data]
        fig.add_trace(
            go.Bar(
                x=x_data,
                y=y_data,
                orientation='h',
                marker=dict(
                    color=colors,
                    line=dict(color='white', width=1.5)
                ),
                showlegend=False,
                text=text_vals,
                textposition='outside',
                textfont=dict(size=11, family='Arial, sans-serif'),
                hovertemplate='<b>%{y}</b><br>Value: %{x:,.0f}<extra></extra>'
            ),
            row=row, col=col
        )

    # Add all bars
    create_bar(brand_totals['Interactions'], brand_totals['Brand'], colors, 1, 1)
    create_bar(brand_totals['Estimated_Reach'], brand_totals['Brand'], colors, 1, 2)
    create_bar(brand_totals['Results'], brand_totals['Brand'], colors, 2, 1)
    create_bar(brand_totals['Comments'], brand_totals['Brand'], colors, 2, 2)

    # Update all axes
    fig.update_xaxes(
        showgrid=True,
        gridcolor='rgba(200, 200, 200, 0.3)',
        gridwidth=1,
        zeroline=True,
        zerolinecolor='rgba(200, 200, 200, 0.5)',
        tickfont=dict(size=10)
    )
    fig.update_yaxes(
        showgrid=False,
        tickfont=dict(size=11)
    )

    fig.update_layout(
        title={
            'text': '<b>Kyocera Competitive Analysis</b><br><sub style="font-size:14px">Total Metrics Across All Topics • 🔴 Kyocera vs Competitors</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': MODERN_COLORS['neutral_dark'], 'family': 'Arial, sans-serif'}
        },
        height=900,
        width=1500,
        showlegend=False,
        font=dict(size=12, family='Arial, sans-serif', color=MODERN_COLORS['neutral_dark']),
        plot_bgcolor='#FAFAFA',
        paper_bgcolor='#FAFAFA',
        margin=dict(l=120, r=100, t=120, b=60)
    )

    # Update subplot title styling
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(size=15, family='Arial, sans-serif', color=MODERN_COLORS['neutral_dark'])

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
        color = KYOCERA_PRIMARY if brand == 'Kyocera' else color_map.get(brand, 'gray')

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
            'text': '<b>Topic Breakdown Analysis</b><br><sub style="font-size:14px">Top 6 Brands by Interaction Volume • 🔴 Kyocera in Focus</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 22, 'color': MODERN_COLORS['neutral_dark'], 'family': 'Arial, sans-serif'}
        },
        xaxis=dict(
            title=dict(text='<b>Discussion Topics</b>', font=dict(size=14)),
            tickfont=dict(size=12),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(text='<b>Number of Interactions</b>', font=dict(size=14)),
            tickfont=dict(size=11),
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.3)'
        ),
        barmode='group',
        height=650,
        width=1300,
        font=dict(size=12, family='Arial, sans-serif', color=MODERN_COLORS['neutral_dark']),
        plot_bgcolor='#FAFAFA',
        paper_bgcolor='#FAFAFA',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(size=12),
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor=MODERN_COLORS['neutral_light'],
            borderwidth=1
        ),
        margin=dict(l=80, r=40, t=120, b=80)
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
        lambda x: KYOCERA_PRIMARY if x == 'Kyocera' else 'rgba(100, 100, 100, 0.5)'
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
        title={
            'text': '<b>Engagement Efficiency Analysis</b><br><sub style="font-size:14px">Reach vs Interactions • Bubble Size = Results • 🔴 Kyocera Highlighted</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 22, 'color': MODERN_COLORS['neutral_dark'], 'family': 'Arial, sans-serif'}
        },
        xaxis=dict(
            title=dict(text='<b>Number of Interactions</b>', font=dict(size=14)),
            tickfont=dict(size=11),
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.3)'
        ),
        yaxis=dict(
            title=dict(text='<b>Estimated Reach</b>', font=dict(size=14)),
            tickfont=dict(size=11),
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.3)'
        ),
        height=650,
        width=1200,
        font=dict(size=12, family='Arial, sans-serif', color=MODERN_COLORS['neutral_dark']),
        plot_bgcolor='#FAFAFA',
        paper_bgcolor='#FAFAFA',
        legend=dict(
            font=dict(size=11),
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor=MODERN_COLORS['neutral_light'],
            borderwidth=1
        ),
        margin=dict(l=80, r=40, t=120, b=80)
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
        marker=dict(
            color=df_share['Kyocera_Share'],
            colorscale=[
                [0, '#FFE5E5'],
                [0.25, '#FFB3B3'],
                [0.5, '#FF6B6B'],
                [0.75, KYOCERA_PRIMARY],
                [1, KYOCERA_DARK]
            ],
            line=dict(color='white', width=2),
            showscale=False
        ),
        text=[f"<b>{val:.1f}%</b>" for val in df_share['Kyocera_Share']],
        textposition='outside',
        textfont=dict(size=13, family='Arial, sans-serif'),
        hovertemplate='<b>🔴 Kyocera in %{y}</b><br>Market Share: %{x:.1f}%<br>Kyocera Interactions: %{customdata[0]:,}<br>Total Interactions: %{customdata[1]:,}<extra></extra>',
        customdata=df_share[['Kyocera_Interactions', 'Total_Interactions']].values
    ))

    fig.update_layout(
        title={
            'text': '<b>Kyocera Market Dominance</b><br><sub style="font-size:14px">Share of Total Interactions by Topic • 🔴 Performance Overview</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 22, 'color': MODERN_COLORS['neutral_dark'], 'family': 'Arial, sans-serif'}
        },
        xaxis=dict(
            title=dict(text='<b>Market Share (%)</b>', font=dict(size=14)),
            tickfont=dict(size=11),
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.3)',
            range=[0, max(df_share['Kyocera_Share']) * 1.15]
        ),
        yaxis=dict(
            title=dict(text='<b>Discussion Topics</b>', font=dict(size=14)),
            tickfont=dict(size=12),
            showgrid=False
        ),
        height=550,
        width=1100,
        font=dict(size=12, family='Arial, sans-serif', color=MODERN_COLORS['neutral_dark']),
        plot_bgcolor='#FAFAFA',
        paper_bgcolor='#FAFAFA',
        margin=dict(l=150, r=100, t=120, b=80)
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
