# TimeKong

![time kong](https://github.com/PurpleSun/time_kong/blob/master/time-kong-logo.png?raw=true "time kong")

Time converter between timestamp, string and datetime.


## Installation

You can install `time-kong` simply with `pip`:

```
pip install time-kong
```


## Usages

### TimeKong

Convert time between timestamp, string and datetime:

```python
from datetime import datetime

from time_kong import TimeKong

ts = 1558883766.864879
TimeKong.timestamp2string(ts, formatter="%Y-%m-%d %H:%M:%S.%f")
# '2019-05-26 23:16:06.864879'
TimeKong.timestamp2datetime(ts)
# datetime.datetime(2019, 5, 26, 23, 16, 6, 864879)

ds = '2019-05-26 23:16:06.864879'
TimeKong.string2timestamp(ds, formatter="%Y-%m-%d %H:%M:%S.%f")
# 1558883766.864879
TimeKong.string2datetime(ds, formatter="%Y-%m-%d %H:%M:%S.%f")
# datetime.datetime(2019, 5, 26, 23, 16, 6, 864879)

dt = datetime(year=2019, month=5, day=26, hour=22, minute=42, second=26, microsecond=864879)
TimeKong.datetime2timestamp(dt)
# 1558881746.864879
TimeKong.datetime2string(dt, formatter="%Y-%m-%d %H:%M:%S.%f")
# '2019-05-26 22:42:26.864879'
```

Constants included:

1. `TimeKong.NANOSECOND`
1. `TimeKong.MICROSECOND`
2. `TimeKong.MILLISECOND`
3. `TimeKong.SECOND`
4. `TimeKong.MINUTE`
5. `TimeKong.HOUR`
6. `TimeKong.DAY`
7. `TimeKong.WEEK`
8. `TimeKong.MONTH`
9. `TimeKong.YEAR`


## Author

time-kong is developed and maintained by fanwei.zeng (stayblank@gmail.com). It can be found here:

https://github.com/PurpleSun/time_kong