# VNDB Thigh-highs
This module provide one VNDB api implementation. It aims to provide some high level features to easily use VNDB api.

## Quick start

```
from vndb_thigh_highs import VNDB
from vndb_thigh_highs.models import VN

vndb = VNDB()
vns = vndb.get_vn(VN.id == 17)
```
