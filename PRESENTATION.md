---
marp: true
theme: default
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# Demographic Data Analysis for Retail
## Johan Slettengren

---

**Data cleaning and aggregation**

---

**Population density across Sweden**

<img src="output/log_beftotalt_map.png" width="20%">

---

**Conditions**

- Population density: at least 5000 people in a 5km^2 square
- Growing population: positive linear slope over past 10 years
- Non-aging population: share of 65+ not growing over past 10 years
- Family-influx: population of young children growing over past 10 years

---

**Percentage of areas that fullfill the criteria**

<img src="output/filter_stages.png" width="40%">

---
**Spread of areas that fullfill all the criteria**

<img src="output/ind_map.png" width="20%">

---

**Allocation of candidate areas across municipalities**

<img src="output/candidates_over_muns.png" width="50%">

---

**Allocation and customer mix for top 5 candidates**

<img src="output/allocation.png" width="60%">

---

**Historical evolution and linear interpolation**

<img src="output/forecast.png" width="80%">

---

See the Marpit Markdown syntax [here](https://marpit.marp.app/markdown).