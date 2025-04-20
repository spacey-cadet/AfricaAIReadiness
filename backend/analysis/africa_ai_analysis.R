# Load required libraries
library(tidyverse)
library(ggplot2)
library(plotly)
library(dplyr)
library(readr)

# Read the data
data <- read_csv("data/africa_ai_readiness_trends_2019-2025_generated.csv")

# Clean and prepare data
data_clean <- data %>%
  filter(!is.na(Value)) %>%
  mutate(Year = as.numeric(Year),
         Value = as.numeric(Value))

# Calculate average metrics by year
yearly_metrics <- data_clean %>%
  group_by(Year, MetricName) %>%
  summarise(AverageValue = mean(Value, na.rm = TRUE),
            .groups = 'drop')

# Create a function to generate trend plots
generate_trend_plot <- function(metric_name) {
  plot_data <- yearly_metrics %>%
    filter(MetricName == metric_name)
  
  p <- ggplot(plot_data, aes(x = Year, y = AverageValue)) +
    geom_line(color = "#2E86C1", size = 1.5) +
    geom_point(color = "#2E86C1", size = 3) +
    theme_minimal() +
    theme(
      panel.background = element_rect(fill = "white"),
      plot.background = element_rect(fill = "white"),
      text = element_text(color = "#2C3E50"),
      axis.text = element_text(color = "#2C3E50"),
      panel.grid.major = element_line(color = "#ECF0F1"),
      panel.grid.minor = element_blank()
    ) +
    labs(
      title = paste("Trend of", metric_name, "in Africa (2019-2025)"),
      x = "Year",
      y = "Average Value"
    )
  
  return(ggplotly(p))
}

# Generate plots for key metrics
internet_penetration_plot <- generate_trend_plot("InternetPenetration_Percent")
mobile_usage_plot <- generate_trend_plot("MobilePhoneUsage_SubscriptionsPer100")
broadband_plot <- generate_trend_plot("BroadbandAccess_FixedSubscriptionsPer100")

# Save plots as HTML files
htmlwidgets::saveWidget(internet_penetration_plot, "plots/internet_penetration.html")
htmlwidgets::saveWidget(mobile_usage_plot, "plots/mobile_usage.html")
htmlwidgets::saveWidget(broadband_plot, "plots/broadband.html")

# Generate summary statistics
summary_stats <- data_clean %>%
  group_by(MetricName) %>%
  summarise(
    Mean = mean(Value, na.rm = TRUE),
    Median = median(Value, na.rm = TRUE),
    Min = min(Value, na.rm = TRUE),
    Max = max(Value, na.rm = TRUE),
    .groups = 'drop'
  )

# Save summary statistics
write_csv(summary_stats, "analysis/summary_statistics.csv") 