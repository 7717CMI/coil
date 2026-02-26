"""
Generate Coiled Tubing Market data files (value.json and volume.json)
with proper segment structure for the dashboard.
"""
import json
import random
import math

random.seed(42)

# Years
YEARS = list(range(2021, 2034))

# Geography hierarchy
GEO_HIERARCHY = {
    "North America": ["U.S.", "Canada"],
    "Europe": ["U.K.", "Germany", "Italy", "France", "Spain", "Russia", "Rest of Europe"],
    "Asia Pacific": ["China", "India", "Japan", "South Korea", "ASEAN", "Australia", "Rest of Asia Pacific"],
    "Latin America": ["Brazil", "Argentina", "Mexico", "Rest of Latin America"],
    "Middle East & Africa": ["GCC", "South Africa", "Rest of Middle East & Africa"],
}

# Region share of global market (value)
REGION_SHARES = {
    "North America": 0.34,
    "Europe": 0.18,
    "Asia Pacific": 0.22,
    "Latin America": 0.10,
    "Middle East & Africa": 0.16,
}

# Country shares within regions
COUNTRY_SHARES = {
    "North America": {"U.S.": 0.82, "Canada": 0.18},
    "Europe": {"U.K.": 0.18, "Germany": 0.20, "Italy": 0.12, "France": 0.15, "Spain": 0.10, "Russia": 0.13, "Rest of Europe": 0.12},
    "Asia Pacific": {"China": 0.32, "India": 0.18, "Japan": 0.16, "South Korea": 0.10, "ASEAN": 0.12, "Australia": 0.05, "Rest of Asia Pacific": 0.07},
    "Latin America": {"Brazil": 0.38, "Argentina": 0.22, "Mexico": 0.25, "Rest of Latin America": 0.15},
    "Middle East & Africa": {"GCC": 0.55, "South Africa": 0.20, "Rest of Middle East & Africa": 0.25},
}

# Region growth rates (CAGR)
REGION_CAGR = {
    "North America": 0.052,
    "Europe": 0.048,
    "Asia Pacific": 0.072,
    "Latin America": 0.058,
    "Middle East & Africa": 0.065,
}

# === SEGMENT DEFINITIONS ===

# By Offering (hierarchical) - shares of total market
OFFERING_HIERARCHY = {
    "Products and Equipment": {
        "Coiled Tubing Strings and Pipes": 0.22,
        "Coiled Tubing Units": 0.18,
        "Reels": 0.08,
        "Injector Heads": 0.10,
        "Well Control and Pressure Control Equipment": 0.14,
        "Downhole Tools & Accessories": 0.10,
        "Pumping, Nitrogen and Fluid Support Equipment": 0.12,
        "Control, Monitoring & Instrumentation Systems": 0.06,
    },
    "Services": {
        "Well Intervention Services": 0.22,
        "Stimulation Support Services": 0.16,
        "Logging & Conveyance Services": 0.12,
        "Fishing, Milling & Remedial Services": 0.14,
        "Completion & Workover Support Services": 0.13,
        "Coiled Tubing Drilling Services": 0.12,
        "Plug & Abandonment Support Services": 0.11,
    }
}
# Products vs Services split
OFFERING_PARENT_SHARES = {
    "Products and Equipment": 0.55,
    "Services": 0.45,
}

# By Operational Task (flat)
OPERATIONAL_TASK = {
    "Circulation": 0.15,
    "Pumping": 0.18,
    "Chemical Injection": 0.10,
    "Nitrogen Lift and Nitrogen Pumping": 0.14,
    "Logging Conveyance": 0.12,
    "Perforation Conveyance": 0.10,
    "Mechanical Manipulation": 0.11,
    "Fishing and Milling": 0.10,
}

# By Material Type (flat)
MATERIAL_TYPE = {
    "Carbon Steel": 0.35,
    "Low-Alloy and High-Strength Steel": 0.25,
    "Stainless Steel": 0.18,
    "Duplex and Super Duplex Alloys": 0.13,
    "Nickel-Based and Corrosion-Resistant Alloys": 0.09,
}

# By Tubing Outer Diameter (flat)
TUBING_DIAMETER = {
    "Up to 1.5 inch": 0.30,
    "Above 1.5 to 2.0 inch": 0.35,
    "Above 2.0 to 2.375 inch": 0.22,
    "Above 2.375 inch": 0.13,
}

# By Application (flat)
APPLICATION = {
    "Onshore": 0.65,
    "Offshore": 0.35,
}

# By Well Type (flat)
WELL_TYPE = {
    "Oil Wells": 0.32,
    "Gas Wells": 0.22,
    "Injection Wells": 0.12,
    "Horizontal and Deviated Wells": 0.15,
    "Mature Wells": 0.11,
    "HPHT Wells": 0.08,
}

# By End User (flat)
END_USER = {
    "NOCs": 0.28,
    "IOCs and Independent E&P Companies": 0.30,
    "Oilfield Service Companies": 0.22,
    "Drilling Contractors": 0.12,
    "Geothermal Operators": 0.08,
}

# Global market size in 2021 (USD Millions)
GLOBAL_VALUE_2021 = 3200  # $3.2 Billion
GLOBAL_VOLUME_2021 = 45000  # 45,000 units (thousands of meters of tubing, or service operations)

def generate_time_series(base_value, cagr, years, noise_factor=0.03):
    """Generate a time series with given CAGR and some noise."""
    series = {}
    for i, year in enumerate(years):
        growth = (1 + cagr) ** i
        noise = 1 + random.uniform(-noise_factor, noise_factor)
        val = round(base_value * growth * noise, 1)
        series[str(year)] = val
    return series

def generate_flat_segments(total_base, shares, cagr, years, segment_cagr_variation=0.015):
    """Generate data for flat segments."""
    result = {}
    for seg_name, share in shares.items():
        seg_base = total_base * share
        seg_cagr = cagr + random.uniform(-segment_cagr_variation, segment_cagr_variation)
        result[seg_name] = generate_time_series(seg_base, seg_cagr, years)
    return result

def generate_hierarchical_offering(total_base, cagr, years):
    """Generate hierarchical By Offering data with aggregated parent totals."""
    result = {}
    for parent_name, parent_share in OFFERING_PARENT_SHARES.items():
        parent_base = total_base * parent_share
        result[parent_name] = {}
        children = OFFERING_HIERARCHY[parent_name]

        # Generate child data first
        child_series_list = []
        for child_name, child_share in children.items():
            child_base = parent_base * child_share
            child_cagr = cagr + random.uniform(-0.015, 0.015)
            child_ts = generate_time_series(child_base, child_cagr, years)
            result[parent_name][child_name] = child_ts
            child_series_list.append(child_ts)

        # Add aggregated parent-level year data (sum of children)
        # _level=2 means "first segment level" in the processor's convention
        # (level 1 = total market aggregation, level 2 = first segment, level 3 = sub-segment)
        for year_str in [str(y) for y in years]:
            total = round(sum(cs[year_str] for cs in child_series_list), 1)
            result[parent_name][year_str] = total
        result[parent_name]["_aggregated"] = True
        result[parent_name]["_level"] = 2
    return result

def generate_geography_data(geo_base_value, geo_base_volume, cagr, years):
    """Generate all segment types for a geography."""
    data = {}

    # By Offering (hierarchical)
    data["By Offering"] = generate_hierarchical_offering(geo_base_value, cagr, years)

    # Flat segment types
    flat_segments = {
        "By Operational Task": OPERATIONAL_TASK,
        "By Material Type": MATERIAL_TYPE,
        "By Tubing Outer Diameter": TUBING_DIAMETER,
        "By Application": APPLICATION,
        "By Well Type": WELL_TYPE,
        "By End User": END_USER,
    }

    for seg_type, shares in flat_segments.items():
        data[seg_type] = generate_flat_segments(geo_base_value, shares, cagr, years)

    return data

def generate_geography_volume_data(geo_base_volume, cagr, years):
    """Generate all segment types for a geography (volume)."""
    # Volume uses same structure but different base and integer values
    data = {}

    # By Offering (hierarchical) - volume
    result = {}
    for parent_name, parent_share in OFFERING_PARENT_SHARES.items():
        parent_base = geo_base_volume * parent_share
        result[parent_name] = {}
        children = OFFERING_HIERARCHY[parent_name]

        child_series_list = []
        for child_name, child_share in children.items():
            child_base = parent_base * child_share
            child_cagr = cagr + random.uniform(-0.015, 0.015)
            series = generate_time_series(child_base, child_cagr, years, noise_factor=0.04)
            rounded = {k: round(v) for k, v in series.items()}
            result[parent_name][child_name] = rounded
            child_series_list.append(rounded)

        # Add aggregated parent-level year data (sum of children)
        for year_str in [str(y) for y in years]:
            total = round(sum(cs[year_str] for cs in child_series_list))
            result[parent_name][year_str] = total
        result[parent_name]["_aggregated"] = True
        result[parent_name]["_level"] = 2

    data["By Offering"] = result

    # Flat segment types
    flat_segments = {
        "By Operational Task": OPERATIONAL_TASK,
        "By Material Type": MATERIAL_TYPE,
        "By Tubing Outer Diameter": TUBING_DIAMETER,
        "By Application": APPLICATION,
        "By Well Type": WELL_TYPE,
        "By End User": END_USER,
    }

    for seg_type, shares in flat_segments.items():
        seg_data = {}
        for seg_name, share in shares.items():
            seg_base = geo_base_volume * share
            seg_cagr = cagr + random.uniform(-0.015, 0.015)
            series = generate_time_series(seg_base, seg_cagr, years, noise_factor=0.04)
            seg_data[seg_name] = {k: round(v) for k, v in series.items()}
        data[seg_type] = seg_data

    return data

def main():
    value_data = {}
    volume_data = {}

    for region, countries in GEO_HIERARCHY.items():
        region_cagr = REGION_CAGR[region]
        region_share = REGION_SHARES[region]

        region_value_base = GLOBAL_VALUE_2021 * region_share
        region_volume_base = GLOBAL_VOLUME_2021 * region_share

        # Generate region data
        value_data[region] = generate_geography_data(region_value_base, region_volume_base, region_cagr, YEARS)
        volume_data[region] = generate_geography_volume_data(region_volume_base, region_cagr, YEARS)

        # Add "By Country" for regions
        country_shares = COUNTRY_SHARES[region]
        value_data[region]["By Country"] = {}
        volume_data[region]["By Country"] = {}
        for country in countries:
            c_share = country_shares[country]
            c_base_val = region_value_base * c_share
            c_base_vol = region_volume_base * c_share
            c_cagr = region_cagr + random.uniform(-0.01, 0.01)
            value_data[region]["By Country"][country] = generate_time_series(c_base_val, c_cagr, YEARS)
            vol_series = generate_time_series(c_base_vol, c_cagr, YEARS, noise_factor=0.04)
            volume_data[region]["By Country"][country] = {k: round(v) for k, v in vol_series.items()}

        # Generate country data
        for country in countries:
            c_share = country_shares[country]
            c_cagr = region_cagr + random.uniform(-0.008, 0.008)
            c_value_base = region_value_base * c_share
            c_volume_base = region_volume_base * c_share

            value_data[country] = generate_geography_data(c_value_base, c_volume_base, c_cagr, YEARS)
            volume_data[country] = generate_geography_volume_data(c_volume_base, c_cagr, YEARS)

    # Write files
    with open("public/data/value.json", "w") as f:
        json.dump(value_data, f, indent=2)

    with open("public/data/volume.json", "w") as f:
        json.dump(volume_data, f, indent=2)

    # Print summary
    print("Generated Coiled Tubing Market data:")
    print(f"  Geographies: {len(value_data)}")
    print(f"  Segment types per geography: {len(list(value_data.values())[0])}")
    for st in list(value_data.values())[0].keys():
        segs = list(value_data[list(value_data.keys())[0]][st].keys())
        print(f"    {st}: {len(segs)} segments")
    print(f"  Years: {YEARS[0]}-{YEARS[-1]}")
    print(f"  Value file: public/data/value.json")
    print(f"  Volume file: public/data/volume.json")

if __name__ == "__main__":
    main()
