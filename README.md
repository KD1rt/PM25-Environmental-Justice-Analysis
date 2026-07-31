# PM2.5 Environmental Justice Analysis

## Overview

This project demonstrates a Python and ArcPy workflow developed to automate the preparation of environmental and demographic datasets for air quality and environmental justice analysis in North Carolina. The workflow integrates EPA PM2.5 monitoring data, U.S. Census income data, coal power plant locations, and county boundaries to generate GIS-ready feature classes for analysis within ArcGIS Pro.

## Problem

Environmental justice analyses often require data from multiple agencies, each using different formats, schemas, and geographic units. Preparing these datasets manually is repetitive, time-consuming, and increases the potential for inconsistencies before spatial analysis can begin.

## Solution

This workflow automates the preprocessing of multiple datasets by filtering EPA PM2.5 monitoring records, calculating county-level PM2.5 averages, processing census income data, creating coal power plant feature classes from CSV coordinates, generating three-mile buffer zones, clipping outputs to the study area, and automatically loading the resulting layers into ArcGIS Pro.

## Workflow

1. Import Source Data
2. Process Environmental Data
3. Create GIS Layers
4. Perform Spatial Analysis
5. Generate GIS Deliverables

## Technologies

* Python
* ArcPy
* ArcGIS Pro
* EPA Air Quality Data
* U.S. Census Data
* CSV Processing
* Spatial Analysis

## Skills Demonstrated

* GIS Automation
* Python Development
* ArcPy Scripting
* Object-Oriented Programming
* Spatial Data Processing
* Data Integration
* Environmental GIS
* Feature Class Creation
* Buffer Analysis
* Geoprocessing

## Results

The workflow produces GIS-ready feature classes representing county-level PM2.5 averages, census tract median income, coal power plant locations, and associated buffer zones. By automating preprocessing and geoprocessing tasks, the project creates a repeatable workflow that improves efficiency and consistency while supporting environmental justice and air quality analyses.

## Repository Structure

```text
scripts/
images/
sample_data/
README.md
requirements.txt
LICENSE
```

## Future Improvements

* Support additional EPA pollutants (O₃, NO₂, SO₂).
* Allow configurable study areas and buffer distances.
* Export results directly to ArcGIS Online.
* Generate automated map layouts and summary reports.
* Expand the workflow to support regional or multi-state analyses.
