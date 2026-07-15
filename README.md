# GeoWaste Database Repository

This repository provides open access to the GeoWaste database together with the accompanying open-source tools developed to support the global mapping and characterisation of major dumpsites using AI, geospatial analysis, satellite-based open-burning detection, and methane emissions modelling.

These materials support the study:

**"GeoWaste database for global mapping and characterisation of major dumpsites"**  
*Maalouf et al. (2026)*

**The repository contains:**

- **GeoWaste database** – global site-level database of 200 major active dumpsites.
- **C1. GeoWaste NLP characterisation tool** – AI-assisted extraction of dumpsite characteristics from publicly available sources.
- **C2. Potentially affected population tool**– Estimates the population potentially affected around each dumpsite.
- **C3. Open burning detection tool**– Detects open burning at dumpsites using satellite observations.
- **C4. Methane emissions estimation tool** – Estimates site-level methane emissions using the IPCC methodologies.

---

> ⚠️ **IMPORTANT**

If you use the GeoWaste database or any of the accompanying code, please **cite the associated publication** (Maalouf et al., 2026). 
- The database and presented codes were developed by *Dr. Amani Maalouf*.
- Please contact Dr Amani Maalouf [amani.maalouf@smithschool.ox.ac.uk](mailto:amani.maalouf@smithschool.ox.ac.uk) to inform us about any errors, omissions or other feedback.
- For a detailed walkthrough of the methodology and analysis, please refer to the **Supplementary Information** provided in the paper.

---

## Repository components

### **GeoWaste Database**

GeoWaste is an open-access, site-level database of major uncontrolled waste disposal sites ("dumpsites") worldwide. The database was developed through a transparent and reproducible workflow integrating AI-assisted text analysis, geospatial analysis, satellite-based detection of open burning, and site-level methane emissions modelling for the global mapping and characterisation of major dumpsites.

#### Current version

Version 3.0
Released: July 2026

#### Format
The GeoWaste database is provided as a Microsoft Excel (.xlsx) workbook. Individual sheets or columns can be exported as CSV. 

#### Usage
The dataset can be opened in standard spreadsheet software or imported into Python-based workflows using commonly used libraries such as pandas or geopandas, enabling further statistical, geospatial, or visual analysis.

### **C1. GeoWaste NLP characterisation tool**

An AI-powered approach using Python, implemented in Google Colab, for characterising individual dumpsites based on precise geolocations and extracting relevant data.
- Involves **web scraping**, **text extraction**, **PDF generation**, and **data analysis**.
- Uses **OpenAI GPT-4** for processing and interpretation.
- Outputs results (attributes related to the dumpsite location) in an Excel file.

### **C2. Potentially affected population tool** 

A geospatial analysis tool, implemented in Google Earth Engine (GEE), for estimating the population speculated to be potentially affected calculated for an indicative and arbitrary 10 km radius of each dumpsite.
- Uses gridded population data (GHSL Population 2023, 100 m resolution; 2020 epoch).
- Outputs site-level population counts within the defined buffer.
 
### **C3. Open burning detection tool** 
A geospatial analysis tool, implemented in Google Earth Engine (GEE), for detecting the presence of open burning at dumpsites using satellite observations.

- Based on NASA Visible Infrared Imaging Radiometer Suite (VIIRS) active fire detections from (NOAA-20/JPSS-1) at 375 m resolution, retrieved via the NASA Fire Information for Resource Management System (FIRMS).
- Detects fire activity within dumpsite boundaries and an additional 100 m buffer to account for geolocation uncertainty.
- The open burning tool outputs presence of open burning (yes/no), open-burning detection count, VIIRS fire-detection confidence (low/nominal/high), site-level mean confidence level, and fire-type classification, derived from VIIRS (NOAA-20/JPSS-1) active fire detections for 2020–2024.

### **C4. Methane emissions estimation tool** 
A Python tool, implemented in Google Colab, for estimating methane emissions from municipal solid waste disposal in dumpsites.  
- Based on a **modified first-order decay model** per the *2019 Refinement to the 2006 IPCC Guidelines*.
- The tool processes site-specific Excel input data (parameters).
- Outputs **annual CH₄ emissions over 100 years**.

---
## License

This work is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License].  
See the (LICENSE) file for details.

---
## Read and Cite the Paper

Find the published paper [here](Journal info will be added once published).  

If you use the GeoWaste database or any of the accompanying code, please cite:

> **Proposed citation:**
> > Maalouf et al. (2026)  
> *GeoWaste database for global mapping and characterisation of major dumpsites.*  
> *(Journal info will be added once published)*


