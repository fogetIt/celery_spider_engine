
```python
import os
import sys
file_path = sys.argv[0]  # 获取执行入口文件（绝对）路径
# 获取文件名
file_name = os.path.splitext(os.path.basename(file_path))[0]
```
