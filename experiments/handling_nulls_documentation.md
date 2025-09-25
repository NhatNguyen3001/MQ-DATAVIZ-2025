# Workflow for Handling Missing Pollution Data  

## **Step 1 – Drop bad cities (cutoff = 70%)**
- **What was done:**  
  - Calculated missing % across the 6 pollutant columns for each city.  
  - Dropped cities where the **average missingness > 70%**.  

- **Intuition:**  
  - If most of a city’s data is missing, imputing would be more guesswork than truth.  
  - Dropping these avoids bias from unreliable data while keeping cities with usable signals.  

---

## **Step 2 – Fill within each city over time**
- **What was done:**  
  - Sorted data by `country -> city -> year`.  
  - Applied **linear interpolation** between known years.  
  - Used forward/backward fill at edges.  

- **Intuition:**  
  - Pollution levels usually **change gradually year to year**.  
  - Interpolation preserves **temporal trends** without borrowing from other cities.  

---

## **Step 3 – Fill from country averages**
- **What was done:**  
  - For remaining nulls after Step 2, filled using:  
    1. **Country–year averages** (if available).  
    2. Otherwise, **overall country averages**.  

- **Intuition:**  
  - Cities in the same country share **environmental and regulatory contexts**.  
  - Country-level values preserve **geographical consistency**.  

---

## **Step 4 – Fill remaining with KNN (global imputation)**
- **What was done:**  
  - Applied **KNN imputation** on the 6 pollutant columns.  
  - Each missing value was estimated from the **nearest rows** with similar pollution patterns.  

- **Intuition:**  
  - Pollutants are often **correlated** (e.g., high PM10 often implies high PM2.5).  
  - KNN leverages **multivariate similarity** across the dataset, giving more realistic imputations than a simple mean.  

---

# Why this workflow makes sense
- **Hierarchical filling strategy**: trust **local city trends** first, then **country context**, then **global similarity**.  
- **Balanced strictness**: only the most unreliable cities were dropped.  
- **Domain-aware choices**: interpolation for time, country averages for regional consistency, KNN for cross-pollutant relationships.  