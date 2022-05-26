## Synthetic Data Generator (SDG)

This repository contains the utilities to generate realistic, synthetic data.

We may want to generate fake data for project proposals or POCs where clients don't or can't provide real data.


*SDG is a work in progress.*

---

####SDG Features

Below are a list of the features and functionality of SDG.

1. Name data
2. Dates, Times, and Datetimes
3. Metrics
4. Categorical data
5. Contact data
6. Intentionally missing / bad data

---

### Ideally - How to use SDG. 
1. Run gui/sdg_gui.py
2. Complete form - hit submit when finished. (This can probably move to root folder level)
3. Data is generated

### How current SDG components work
#### Gui
1. Run gui/sdg_gui.py
2. Complete form - hit submit.
3. This generates a schema in the data/input_data folder called schema.json

Notes: 
- The schema is not in the desired target format yet for ingestion into sdg.py
- Add frame to gui to take in other config details (size of data, format of output data such as csv or bq table, location of output data on prem or in cloud)
- Gui bug: If you change the data type for a row after you named it something else, the names go on top of each other.
- Gui bug: at the moment, any data can be put into each entry box. Need to enforce input to datatypes

#### sdg.py
1. config.yaml tells sdg.py which schema of data to generate, length of output data rows, and the name of output file to make.
2. config.yaml also contains the datatype (and subtype when present) to sdg utility needed to generate that data
3. Change schema for diffe
4. Run sdg.py - data is generated

SDG bugs or needed enhancements: 
- add additional means of output to config - not just local csv option but also csv to gcp or to bq table
- add ability to ingest file and preserve desired data distributions




 [link format](https://confluence.atlassian.com/x/iqyBMg)  
 **bold format**  
 *italics*
 