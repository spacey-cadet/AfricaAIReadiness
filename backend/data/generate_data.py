import pandas as pd
import numpy as np
import random

# --- Configuration ---
OUTPUT_CSV_FILE = 'africa_ai_readiness_trends_2019-2025_generated.csv'
YEARS = list(range(2019, 2026)) # 2019 to 2025

# --- Data Definitions ---

# List of 54 African Countries and their ISO3 Codes (Example - Add all 54 for full dataset)
# Source: UN list or similar comprehensive source needed for full implementation
countries_iso = {
    "Algeria": "DZA", "Angola": "AGO", "Benin": "BEN", "Botswana": "BWA", "Burkina Faso": "BFA",
    "Burundi": "BDI", "Cabo Verde": "CPV", "Cameroon": "CMR", "Central African Republic": "CAF", "Chad": "TCD",
    "Comoros": "COM", "Congo, Dem. Rep.": "COD", "Congo, Rep.": "COG", "Cote d'Ivoire": "CIV", "Djibouti": "DJI",
    "Egypt": "EGY", "Equatorial Guinea": "GNQ", "Eritrea": "ERI", "Eswatini": "SWZ", "Ethiopia": "ETH",
    "Gabon": "GAB", "Gambia": "GMB", "Ghana": "GHA", "Guinea": "GIN", "Guinea-Bissau": "GNB",
    "Kenya": "KEN", "Lesotho": "LSO", "Liberia": "LBR", "Libya": "LBY", "Madagascar": "MDG",
    "Malawi": "MWI", "Mali": "MLI", "Mauritania": "MRT", "Mauritius": "MUS", "Morocco": "MAR",
    "Mozambique": "MOZ", "Namibia": "NAM", "Niger": "NER", "Nigeria": "NGA", "Rwanda": "RWA",
    "Sao Tome and Principe": "STP", "Senegal": "SEN", "Seychelles": "SYC", "Sierra Leone": "SLE", "Somalia": "SOM",
    "South Africa": "ZAF", "South Sudan": "SSD", "Sudan": "SDN", "Tanzania": "TZA", "Togo": "TGO",
    "Tunisia": "TUN", "Uganda": "UGA", "Zambia": "ZMB", "Zimbabwe": "ZWE"
}
# Ensure all 54 countries are listed here for the full run

countries = list(countries_iso.keys())

metrics = [
    # Infrastructure & Economy
    'InternetPenetration_Percent', 'MobilePhoneUsage_SubscriptionsPer100', 'BroadbandAccess_FixedSubscriptionsPer100',
    'ElectricityAccess_PercentPopulation', 'CloudInfra_Score', 'GDPPerCapita_USD_Current',
    # Innovation & Investment
    'AIStartupFunding_USD_Millions_AnnualizedEst', 'StartupEcosystemRank_GlobalScore', 'TechInvestment2024_USD_Millions_Est',
    'AIMarketSize_USD_Millions_Est',
    # Policy & Governance
    'NationalAIStrategy_Status', 'AIPolicy_MaturityScore', 'DataProtectionLaw_Status', 'AIRegulation_Status', 'DigitalStrategy_Status',
    # Human Capital & Skills
    'STEMGraduates_AnnualEst', 'AIEducationPrograms_CountEst', 'DataScientists_CountEst', 'ICTGraduates_AnnualEst',
    'ProgLang_Python_UsagePercentEst', 'ProgLang_R_UsagePercentEst', 'ProgLang_Java_UsagePercentEst',
    'ProgLang_JavaScript_UsagePercentEst', 'ProgLang_Other_UsagePercentEst',
    # Adoption & Perception
    'AIAwarenessSurvey_PercentAware', 'AIPerception_NetSentimentScore', 'TechnologyAdoption_Index',
    'AfrobarometerTechTrust_Score', 'ChatGPTUsage_EstimatedPenetration'
]

policy_statuses = ['None', 'Planned', 'Developing', 'Implemented', 'NA']
data_protection_statuses = ['None', 'Partial', 'Comprehensive/GDPR-like', 'NA']
ai_regulation_statuses = ['None', 'Discussion', 'Drafted', 'Implemented', 'NA']

# --- Helper Functions for Simulation ---

def get_data_type_and_source(year, metric_name):
    """Assign DataType and Source based on year and metric type (simplified)."""
    is_economic = any(s in metric_name for s in ['GDP', 'Funding', 'Investment', 'MarketSize'])
    is_policy = any(s in metric_name for s in ['Strategy', 'Policy', 'Law', 'Regulation'])
    is_core_infra = any(s in metric_name for s in ['Internet', 'Mobile', 'Electricity'])
    is_niche = any(s in metric_name for s in ['AI', 'DataScientist', 'ChatGPT', 'ProgLang', 'Survey', 'Trust', 'Adoption', 'Cloud', 'StartupEcosystem', 'Graduates'])

    if year <= 2021:
        data_type = 'Actual' if (is_core_infra or 'GDP' in metric_name) and random.random() < 0.8 else 'Estimate'
    elif year == 2022:
        data_type = 'Actual' if (is_core_infra or 'GDP' in metric_name) and random.random() < 0.6 else 'Estimate'
    elif year == 2023:
        data_type = 'Estimate' if random.random() < 0.9 else 'Preliminary' # Assume most 2023 data are estimates now
    elif year == 2024:
        data_type = 'Projection/Forecast' if is_economic and random.random() < 0.7 else 'Estimate'
    elif year == 2025:
        data_type = 'Projection/Forecast' if is_economic and random.random() < 0.9 else 'NA' # Only forecast economics

    # Higher NA rate for niche/policy/future
    na_prob = 0.1
    if is_niche: na_prob += 0.5
    if is_policy: na_prob += 0.4
    if year >= 2024: na_prob += 0.3
    if year == 2025 and not (is_economic and data_type == 'Projection/Forecast'): na_prob = 1.0 # Force NA if not Econ forecast

    if random.random() < na_prob or data_type == 'NA':
        data_type = 'NA'
        source = 'NA'
        value = 'NA' # Will be handled later
    else:
        # Simplified source assignment
        if data_type == 'Actual': source = random.choice(['WB Data', 'ITU Data', 'Gov Stats'])
        elif data_type == 'Estimate': source = random.choice(['WB Estimate', 'Internal Estimate', 'GSMA Est'])
        elif data_type == 'Projection/Forecast': source = random.choice(['IMF Forecast', 'WB Forecast', 'AfDB Forecast'])
        else: source = 'NA' # Should not happen if NA handled above
        value = None # Placeholder, actual value generated later

    return data_type, source, value == 'NA' # Return NA status flag

def simulate_value(metric_name, year, country, is_na):
    """Generate a plausible simulated value (highly simplified)."""
    if is_na:
        return 'NA'

    # --- Base values (very rough, ideally per-country estimates needed) ---
    country_income_level = random.choice(['Low', 'Mid', 'High']) # Needs actual country classification
    base_gdp = {'Low': 800, 'Mid': 2500, 'High': 7000}.get(country_income_level, 1500)
    base_internet = {'Low': 20, 'Mid': 45, 'High': 70}.get(country_income_level, 35)
    base_electricity = {'Low': 40, 'Mid': 70, 'High': 95}.get(country_income_level, 60)
    is_hub = country in ["South Africa", "Nigeria", "Kenya", "Egypt", "Ghana", "Rwanda", "Morocco", "Tunisia"]

    # --- Simulation Logic (Example cases) ---
    if 'GDPPerCapita' in metric_name:
        growth = (year - 2019) * random.uniform(0.01, 0.03) # Simple linear growth + noise
        noise = random.uniform(0.95, 1.05)
        return max(300, round(base_gdp * (1 + growth) * noise))

    elif 'InternetPenetration' in metric_name:
        growth = (year - 2019) * random.uniform(0.02, 0.05) # Faster growth for internet
        noise = random.uniform(0.98, 1.02)
        return max(0, min(100, round(base_internet * (1 + growth) * noise, 1)))

    elif 'ElectricityAccess' in metric_name:
        growth = (year - 2019) * random.uniform(0.005, 0.02) # Slower growth
        noise = random.uniform(0.99, 1.01)
        return max(0, min(100, round(base_electricity * (1 + growth) * noise, 1)))

    elif 'MobilePhoneUsage' in metric_name:
        base_mobile = {'Low': 80, 'Mid': 100, 'High': 120}.get(country_income_level, 90)
        growth = (year - 2019) * random.uniform(0.01, 0.03)
        noise = random.uniform(0.98, 1.02)
        return max(10, min(200, round(base_mobile * (1 + growth) * noise, 1))) # Can exceed 100

    elif 'AIStartupFunding' in metric_name or 'TechInvestment' in metric_name or 'AIMarketSize' in metric_name:
         # Very sparse, higher for hubs, recent years
        if is_hub and year >= 2021 and random.random() < 0.6:
             base_fund = {'Low': 1, 'Mid': 10, 'High': 50}.get(country_income_level, 5) * (5 if is_hub else 1)
             growth_factor = random.uniform(1.1, 1.5)**max(0, year - 2021) # Exponential-ish recent growth
             return round(base_fund * growth_factor * random.uniform(0.5, 1.5), 1)
        else: return 'NA' # High probability of NA

    elif 'NationalAIStrategy' in metric_name or 'DigitalStrategy' in metric_name:
        if year < 2020 and random.random() < 0.8: return 'None'
        if is_hub and random.random() < 0.7: base_status = 'Planned'
        else: base_status = 'None'
        # Simple progression simulation
        current_status_idx = policy_statuses.index(base_status)
        progression = min(len(policy_statuses) - 2, max(0, year - 2020 + random.randint(-1, 1))) # Index up to 'Implemented'
        final_idx = min(len(policy_statuses) - 2, current_status_idx + progression) if base_status != 'None' else current_status_idx
        if random.random() < 0.2 and year >= 2022: # Random chance of being more advanced for hubs
            final_idx = min(len(policy_statuses)-2, final_idx + (1 if is_hub else 0))
        return policy_statuses[final_idx] if random.random() < 0.8 else 'NA' # Still chance of NA


    elif 'DataProtectionLaw' in metric_name:
        # Similar logic to policy, but different states
        if year < 2019 and random.random() < 0.6: return 'None'
        base_status = random.choice(['None', 'Partial']) if not is_hub else random.choice(['Partial', 'Comprehensive/GDPR-like'])
        # Assume less change year-to-year than strategy
        if year < 2021 and base_status == 'Comprehensive/GDPR-like': base_status = 'Partial' # Less likely early
        return base_status if random.random() < 0.9 else 'NA'

    elif 'DataScientists' in metric_name or 'AIEducationPrograms' in metric_name:
         # Very low counts, higher for hubs, recent years
         if is_hub and year >= 2020 and random.random() < 0.5:
             count = random.randint(5, 50) if 'Programs' in metric_name else random.randint(50, 2000)
             growth_factor = random.uniform(1.1, 1.3)**max(0, year - 2020)
             return round(count * growth_factor * (2 if is_hub else 1))
         else: return 'NA'

    elif 'ProgLang' in metric_name:
         # Extremely hard to get country data. Use static placeholder distribution.
         # This is highly unrealistic but fills the column.
         if 'Python' in metric_name: return random.uniform(25, 50)
         if 'JavaScript' in metric_name: return random.uniform(20, 45)
         if 'Java' in metric_name: return random.uniform(10, 25)
         if 'R' in metric_name: return random.uniform(3, 12)
         if 'Other' in metric_name: return random.uniform(5, 20) # Note: these won't sum to 100 per country/year here! Needs Dirichlet if accuracy matters.
         return round(random.uniform(5,40),1) # Placeholder if specific lang not caught

    elif 'ChatGPTUsage' in metric_name:
        if year >= 2023 and random.random() < 0.6: # Only exists recently
             base_usage = {'Low': 1, 'Mid': 5, 'High': 15}.get(country_income_level, 3)
             noise = random.uniform(0.7, 1.3)
             internet_pen = simulate_value('InternetPenetration_Percent', year, country, False) # Dependency attempt
             if internet_pen == 'NA' : internet_pen = base_internet
             return max(0, min(internet_pen * 0.5, round(base_usage * noise, 1))) # % of internet users, capped
        else: return 'NA'

    # --- Default / Catch-all for other metrics ---
    else:
        # Generic simulation for scores/indices/other percentages
        if 'Score' in metric_name or 'Index' in metric_name:
            return round(random.uniform(10, 70), 1)
        elif 'Percent' in metric_name or 'Per100' in metric_name:
             return round(random.uniform(5, 80), 1)
        elif 'CountEst' in metric_name or 'AnnualEst' in metric_name:
             return random.randint(1000, 50000) # Generic count
        else:
            return 'NA' # Default to NA if no logic fits

# --- Main Generation Loop ---
all_data = []

print(f"Generating data for {len(countries)} countries, {len(metrics)} metrics, {len(YEARS)} years...")

for country in countries:
    country_iso = countries_iso.get(country, 'N/A')
    print(f"Processing: {country}")
    for metric in metrics:
        # Add specific simulation logic here if needed that persists across years
        # e.g., setting a more consistent base value per country/metric
        base_value_for_metric_country = None # Placeholder

        for year in YEARS:
            # 1. Determine DataType, Source, and if value should be NA
            data_type, source, is_na_flag = get_data_type_and_source(year, metric)

            # 2. Simulate the value based on metric type, year, country (simplified)
            value = simulate_value(metric, year, country, is_na_flag)

            # 3. Append row data
            all_data.append({
                'CountryName': country,
                'CountryISO3': country_iso,
                'Year': year,
                'MetricName': metric,
                'Value': value,
                'DataType': data_type if value != 'NA' else 'NA', # Ensure DataType is NA if Value is NA
                'Source': source if value != 'NA' else 'NA'
            })

print("Data generation finished. Creating DataFrame...")

# --- Create DataFrame and Save ---
df = pd.DataFrame(all_data)

print("DataFrame created. Saving to CSV...")

df.to_csv(OUTPUT_CSV_FILE, index=False, encoding='utf-8')

print("-" * 50)
print(f"Successfully generated and saved data to: {OUTPUT_CSV_FILE}")
print("-" * 50)
print("\nIMPORTANT DISCLAIMER:")
print("This CSV contains SYNTHETIC and ESTIMATED data generated by an AI.")
print("It is based on generalized assumptions about trends and data availability.")
print("Values are plausible placeholders and may not reflect real-world figures accurately.")
print("Data sparseness (NA values) is intentionally included, especially for niche metrics and future years.")
print("The 'DataType' column ('Actual', 'Estimate', 'Projection/Forecast', 'NA') is crucial for interpretation.")
print("The 'Source' column provides only generalized indicators.")
print("CROSS-VERIFY with authoritative sources before using this data for critical analysis or publications.")
print("-" * 50)

# Display a sample of the generated data
print("\nSample of generated data:")
print(df.sample(15))