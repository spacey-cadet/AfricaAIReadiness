import wbgapi as wb
import pandas as pd
import json
from pathlib import Path

def fetch_africa_data():
    # List of relevant indicators
    indicators = {
        'SP.POP.TOTL': 'Population, total',
        'SE.TER.GRAD.ZS': 'Tertiary education graduates',
        'GB.XPD.RSDV.GD.ZS': 'Research and development expenditure',
        'IT.NET.USER.ZS': 'Internet users',
        'NY.GDP.PCAP.CD': 'GDP per capita'
    }
    
    # Get data for all African countries
    data = {}
    for indicator, name in indicators.items():
        df = wb.data.DataFrame(
            indicator,
            economy=wb.region.members('AFR'),
            time=range(2015, 2024)
        )
        data[name] = df.to_dict()
    
    # Save to JSON file
    output_path = Path(__file__).parent.parent / 'data' / 'africa_data.json'
    with open(output_path, 'w') as f:
        json.dump(data, f)
    
    return "Data fetched and saved successfully"

if __name__ == "__main__":
    fetch_africa_data()
