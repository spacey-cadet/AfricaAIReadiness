import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Create necessary directories
Path("plots").mkdir(exist_ok=True)

# Read the data
data = pd.read_csv("data/africa_ai_readiness_trends_2019-2025_generated.csv")

# Clean and prepare data
data_clean = data.dropna(subset=['Value'])
data_clean['Year'] = pd.to_numeric(data_clean['Year'])
data_clean['Value'] = pd.to_numeric(data_clean['Value'])

# Calculate average metrics by year
yearly_metrics = data_clean.groupby(['Year', 'MetricName'])['Value'].mean().reset_index()

def generate_trend_plot(metric_name):
    plot_data = yearly_metrics[yearly_metrics['MetricName'] == metric_name]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=plot_data['Year'],
        y=plot_data['Value'],
        mode='lines+markers',
        line=dict(color='#2E86C1', width=2),
        marker=dict(color='#2E86C1', size=8),
        name=metric_name
    ))
    
    fig.update_layout(
        title=f"Trend of {metric_name} in Africa (2019-2025)",
        xaxis_title="Year",
        yaxis_title="Average Value",
        template="plotly_white",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#2C3E50'),
        xaxis=dict(
            gridcolor='#ECF0F1',
            showgrid=True
        ),
        yaxis=dict(
            gridcolor='#ECF0F1',
            showgrid=True
        )
    )
    
    return fig

# Generate plots for key metrics
metrics = [
    "InternetPenetration_Percent",
    "MobilePhoneUsage_SubscriptionsPer100",
    "BroadbandAccess_FixedSubscriptionsPer100"
]

for metric in metrics:
    fig = generate_trend_plot(metric)
    fig.write_html(f"plots/{metric.lower()}.html")

# Generate summary statistics
summary_stats = data_clean.groupby('MetricName')['Value'].agg([
    ('Mean', 'mean'),
    ('Median', 'median'),
    ('Min', 'min'),
    ('Max', 'max')
]).reset_index()

# Save summary statistics
summary_stats.to_csv("analysis/summary_statistics.csv", index=False)

print("Analysis complete! Visualizations and summary statistics have been generated.") 