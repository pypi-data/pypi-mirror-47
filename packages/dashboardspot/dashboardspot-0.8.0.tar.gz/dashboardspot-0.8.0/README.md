# DashboardSpot Python

# Examples
```python
from dashboardspot import DashboardSpot

ds = DashboardSpot('your_api_key')
ds.hit('new sale')
ds.hit('new sale', data="blue shirt")
ds.hit('new sale', data="red shirt", count=2, timestamp=1559746170)
```
