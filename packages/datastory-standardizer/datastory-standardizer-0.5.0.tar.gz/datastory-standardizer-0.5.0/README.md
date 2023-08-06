# Standardizer

Standardizer acts as a single source of truth for Datastory's core data. It includes a Python package for harmonizing datasets.

## Usage

**Harmonize country identifiers**

```python
import Standardizer as sd
import pandas as pd

sample = pd.DataFrame([
    {'country': 'Sverige', 'gdp': 40},
    {'country': 'USA', 'gdp': 50},
    {'country': 'Vietnam', 'gdp': 30},
])

# Add country ID's based on country names
name_id_map = sd.mappings.country.name_to_id(lang='sv')
sample['id'] = sample.country.map(name_id_map)

# Add region column based on country ID's
id_region_map = sd.mappings.country.id_to_region()
sample['region'] = sample.id.map(id_region_map)
```

**Merge DDF packages**

```python
# Name of DDF package directories
ddfs = ['elections-data', 'gdp-data']

# Destination of merged DDF package
dest_dir = 'elections-gdp-data'

# Perform the merge
sd.merge(ddfs, dest_dir)
```

**Merge DDF packages with filters**

You might want to specify which concepts to include from the source packages in the destination package. Just pass a list of all concepts (entities, datapoints, time, booleans, etc.) with the `include` argument.

```python
sd.merge(ddfs, dest_dir, include=['gdp', 'country', 'year'])
```