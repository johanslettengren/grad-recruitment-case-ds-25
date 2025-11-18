# Nordic Expansion Strategy - Data Analysis

For detailed case instructions and submission requirements, follow the [instructions](INSTRUCTIONS.md).

## Project Overview

_TODO: Provide an executive summary of the work you have done._

## Environment Setup

### 1. Download the Data

The dataset required for this assessment is hosted as a GitHub Release. Download it using one of the following methods:

```bash
# Using curl (Mac/Linux)
curl -L -o data.zip https://github.com/pds-eidra/grad-recruitment-case-ds-25/releases/download/v1.0-data/data.zip
unzip data.zip -d .
rm data.zip

# Using PowerShell (Windows)
Invoke-WebRequest -Uri "https://github.com/pds-eidra/grad-recruitment-case-ds-25/releases/download/v1.0-data/data.zip" -OutFile data.zip
Expand-Archive data.zip -DestinationPath .
Remove-Item data.zip
```

### 2. Environment & Dependencies

**Dependencies -- you must install these before running:**

- python 3.11.13
- pandas 2.3.1 
- geopandas 1.0.1
- pyarrow 19.0.0 (remove?)
- fastparquet 2024.11.0
- matplotlib 3.10.0      
- seaborn 0.13.2
- numpy 2.3.1      



## Usage
**Enter the following command in the terminal**
```bash
cd scripts
python run_all.py 
````
