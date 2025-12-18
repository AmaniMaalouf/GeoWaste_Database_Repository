# GeoWaste Database Repository
This repository provides open-source tools supporting the GeoWaste database: a global framework for mapping and characterising major waste dumpsites using AI, geospatial analysis, and methane emissions modelling.
It contains four codes supporting the study:

**"GeoWaste database: a global framework for mapping and characterising major dumpsites"**  
by *Maalouf et al. (2026)*

---

## About
GeoWaste provides a transparent, reproducible, site-level methodological framework for identifying and characterising uncontrolled waste disposal sites (“dumpsites”) at global scale. The workflow integrates artificial intelligence–assisted text analysis, geospatial analysis, satellite-based detection of open burning, and site-level methane emissions modelling.

> ⚠️ **IMPORTANT**

If you use any part of these codes, please **cite the paper** (Maalouf et al., 2026). 
- The database and presented codes were developed by *Dr. Amani Maalouf*.
- Please contact Dr Amani Maalouf [amani.maalouf@smithschool.ox.ac.uk](mailto:amani.maalouf@smithschool.ox.ac.uk) to inform us about any errors, omissions or other feedback.
- For a detailed walkthrough of the methodology and analysis, please refer to the **Supplementary Information** provided in the paper.

---

## Repository Contents

### **C1. GeoWaste NLP characterisation tool**

An AI-powered approach using Python, implemented in Google Colab, for characterising dumpsite based on precise geolocations and extracting relevant data.
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

This project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License].  
See the (LICENSE) file for details.

---
## Read and Cite the Paper

Find the published paper [here](Journal info will be added once published).  

If you use any code, please cite:

> **Proposed citation:**
> > Maalouf, A., Reese, S., Christiaen, C., Caldecott, B. (2026)  
> *GeoWaste database: a global framework for mapping and characterising major dumpsites.*  
> *(Journal info will be added once published)*


