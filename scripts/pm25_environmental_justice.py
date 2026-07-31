# GIS540_Final_Project
# North Carolina Air Quality and Environmental Justice Analysis
# This script processes EPA pollution data, census income data, and coal power plant locations
# to create GIS layers for analysis in ArcGIS Pro that highlight air quality and environmental justice 
# concerns in regard to proximity to coal power plants in North Carolina.
# Usage Instructions:
# Run this script in ArcGIS Pro Python window or as a script tool. 
# When prompted provide paths to the following data:
# 1. Folder containing EPA pollution CSV files
# 2. Census income CSV file
# 3. Census shapefile
# 4. Coal power plants CSV file
# 5. North Carolina county boundary shapefile
# Output shapefiles will be created in the specified output folder and automatically added to the ArcGIS Pro project.

# Author: Kyle Scavo
# Date: November 16th, 2024

# Import necessary modules
import arcpy
import os
import csv
print("Modules imported.")

# User-defined functions
def filter_pollution_data(input_folder, state_name, parameter_name):
    """Filters pollution data CSV files for a specific state and parameter."""
    """Arguments:"""
    """           input_folder (str): Folder containing pollution CSV files"""
    """           state_name (str): Name of the state to filter for"""
    """           parameter_name (str): Name of the pollution parameter to filter for"""
    """Returns:"""
    """           list: Filtered pollution records"""
    filtered_records = []
    file_list = os.listdir(input_folder)
    
    for filename in file_list:
        if filename.lower().endswith('.csv'):
            filepath = os.path.join(input_folder, filename)
            with open(filepath, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['State Name'] == state_name and row['Parameter Name'] == parameter_name:
                        filtered_records.append(row)
    return filtered_records

def calculate_county_averages(filtered_records):
    """Calculates overall county averages from filtered pollution records."""
    """Arguments:"""
    """           filtered_records (list): List of filtered pollution records"""
    """Returns:"""
    """           dict: County-wise overall averages"""
    county_data = {}
    
    for row in filtered_records:
        county_name = row["County Name"]
        if county_name not in county_data:
            county_data[county_name] = [] 
        # Collect available quarterly values
        max_val_avg = []
        for field in ["1st Max Value", "2nd Max Value", "3rd Max Value", "4th Max Value"]:
            value = row[field].strip()
            if value != '':
                try:
                    max_val_avg.append(float(value))
                except ValueError:
                    continue 
        # Calculate site-year average if we have at least one value
        if len(max_val_avg) > 0:
            site_year_average = sum(max_val_avg) / len(max_val_avg)
            county_data[county_name].append(site_year_average)
    
    county_pm25_averages = {}
    for county_name in county_data:
        site_year_averages = county_data[county_name]
        county_overall_average = sum(site_year_averages) / len(site_year_averages)
        county_pm25_averages[county_name] = county_overall_average
    
    return county_pm25_averages
def add_layer_to_map(layer_path):
    """Adds a layer to the current ArcGIS Pro map."""
    """Arguments:"""
    """           layer_path (str): Path to the layer to be added"""
    """           layer_name (str): Name of the layer to be added"""
    """Returns:"""
    """           None"""
    try: # research and cited from esri documentation
        aprx = arcpy.mp.ArcGISProject("CURRENT") # utilizes ArcGISProject class to create a project object/uses CURRENT as a keyoword to reference the open project
        map_obj = aprx.listMaps()[0] # utilize listMaps to get maps returned in the ArcGISProject above - calls only the initial map made in the aprx
        map_obj.addDataFromPath(layer_path) # add layer to a map in a project (providing local path or URL)
        print(f"Layer added to map: {layer_path}")
    except Exception as e:
        print(f"Error adding layer to map: {e}")
# Pollution Data Class
class PollutionData:
    """Class to handle pollution data processing."""
    """Attributes:"""
    """           state (str): State name (North Carolina)"""
    """           parameter (str): Pollution parameter name ('PM2.5 - Local Conditions')"""
    """           records (list): Filtered pollution records"""
    """           county_averages (dict): County-wise overall averages"""
    def __init__(self, state, parameter): # Constructor - initializes state and parameter - ask if needed to be reviewed
        """ Initializes PollutionData with state and parameter."""
        """ Arguments:"""
        """           state (str): State name for filtering"""
        """           parameter (str): Pollution parameter name for filtering"""
        self.state = state
        self.parameter = parameter
        self.records = []
        self.county_averages = {}
    def add_records(self, record):
        """ Adds filtered pollution records."""
        """ Arguments:"""
        """           records (dict): List of filtered pollution records"""
        self.records.append(record)
    def calc_averages(self, averages_dict):
        """ Calculates county-wise overall averages."""
        self.county_averages = averages_dict
    def get_record_count(self):
        """ Returns the count of filtered records."""
        return len(self.records)
    def get_county_averages(self):
        """ Returns the number of counties with calculated averages."""
        return len(self.county_averages)

# Main script execution
# Get the data from the user(using arcpy.GetParameterAsText for script tool GUI stuff)
pollution_data_folder = arcpy.GetParameterAsText(0) or input("Provide the pollution data folder: ").strip('"')
census_income_csv = arcpy.GetParameterAsText(1) or input("Provide the census income CSV file: ").strip('"')
census_shapefile = arcpy.GetParameterAsText(2) or input("Provide the census shapefile: ").strip('"')
coal_power_plants_csv = arcpy.GetParameterAsText(3) or input("Provide the coal power plants CSV file: ").strip('"')
nc_county_boundary = arcpy.GetParameterAsText(4) or input("Provide the North Carolina county boundary shapefile: ").strip('"')
output_folder = arcpy.GetParameterAsText(5) or input("Provide the output folder: ").strip('"')
print("Data paths received.")

# Set Environment settings
arcpy.env.overwriteOutput = True
arcpy.env.workspace = output_folder
print("Environment settings configured.")

# Filter EPA pollution data for NC
pm25_data = PollutionData("North Carolina", "PM2.5 - Local Conditions")

filtered_records = filter_pollution_data(pollution_data_folder, pm25_data.state, pm25_data.parameter)
print("Filtering pollution data for North Carolina PM2.5...")

for record in filtered_records:
    pm25_data.add_records(record)
print(f"Filtered records count: {pm25_data.get_record_count()}")

# Calculate county averages using max values
county_average_values = calculate_county_averages(pm25_data.records)

pm25_data.calc_averages(county_average_values)
print(f"Calculated county averages for {pm25_data.get_county_averages()} counties.")

# Create PM 2.5 Layer
print("Creating PM2.5 layer...")
pm25_fc = os.path.join(output_folder, "PM25_Counties.shp")
arcpy.CopyFeatures_management(nc_county_boundary, pm25_fc)
arcpy.AddField_management(pm25_fc, "PM25_Avg", "DOUBLE")
print("Updating PM2.5 averages in shapefile...")

cursor = arcpy.da.UpdateCursor(pm25_fc, ["County", "PM25_Avg"])
for row in cursor:
    county_name = row[0]
    if county_name in pm25_data.county_averages:
        row[1] = pm25_data.county_averages[county_name]
        cursor.updateRow(row)
del cursor
print("PM2.5 layer created successfully.")
add_layer_to_map(pm25_fc)
# Process Census Income Data
income_tracts = {}
print("Processing census income data...")
try:
    with open(census_income_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            geoid_original = row['geoid'].strip()
            median_income_val = row['B19013001'].strip()

            if geoid_original.startswith('14000US'):
                geoid = geoid_original.replace('14000US', '1400000US')
            else:
                geoid = geoid_original
 # Had to talk with my dad about why this error kept happening - Appears that the GEOID has inconsistent formatting between the census data sources where 
 # some are shorter (14 characters) and some are longer (16 characters) 
 # The census TIGER/Line shapefiles use the longer format, so we need to standardize to that for joining purposes
            if median_income_val != '':
                try:
                    median_income = float(median_income_val)
                    income_tracts[geoid] = median_income
                except ValueError:
                    continue
    print(f"Census income data processed: {len(income_tracts)} tracts")
except Exception as e:
    print(f"Error processing census income data: {e}")
# Create Income Layer
income_fc = os.path.join(output_folder, "Census_Tracts_Income.shp")
arcpy.CopyFeatures_management(census_shapefile, income_fc)
arcpy.AddField_management(income_fc, "Med_Income", "DOUBLE")
print("Updating median income in census tracts shapefile...")

cursor = arcpy.da.UpdateCursor(income_fc, ['GEOIDFQ', 'Med_Income'])
updated_count = 0
for row in cursor:
    geoid = row[0]
    if geoid in income_tracts:
        row[1] = income_tracts[geoid]
        cursor.updateRow(row)
        updated_count += 1
del cursor
print(f"Income layer created successfully.")
add_layer_to_map(income_fc)

# Create Coal Plant Layer
coal_fc = os.path.join(output_folder, "Coal_Power_Plants_NC.shp")
print("Creating coal power plants layer...")

arcpy.management.XYTableToPoint(
    in_table=coal_power_plants_csv,
    out_feature_class=coal_fc,
    x_field="Plant longitude",
    y_field="Plant latitude",
    coordinate_system=arcpy.SpatialReference(4326)
)
print("Coal power plants layer created successfully.")

# Clip coal plants to NC boundary
coal_fc_clipped = os.path.join(output_folder, "Coal_Power_Plants_NC_Clipped.shp")
print("Clipping coal plants to NC boundary...")

arcpy.analysis.Clip(
    in_features=coal_fc,
    clip_features=nc_county_boundary,
    out_feature_class=coal_fc_clipped
)
print("Coal plants clipped to NC boundary.")
add_layer_to_map(coal_fc_clipped)

# Create 3-mile buffer around clipped coal plants
buffer_fc = os.path.join(output_folder, "Coal_Power_Plants_Buffer.shp")
print("Creating 3-mile buffer...")

arcpy.analysis.Buffer(
    in_features=coal_fc_clipped,
    out_feature_class=buffer_fc,
    buffer_distance_or_field="3 Miles"
)
print("3-mile buffer created successfully.")

# Clip buffer to NC boundary
buffer_fc_clipped = os.path.join(output_folder, "Coal_Power_Plants_Buffer_Clipped.shp")
print("Clipping buffer to NC boundary...")

arcpy.analysis.Clip(
    in_features=buffer_fc,
    clip_features=nc_county_boundary,
    out_feature_class=buffer_fc_clipped
)
print("Buffer clipped to NC boundary.")
add_layer_to_map(buffer_fc_clipped)
print("Done!")
