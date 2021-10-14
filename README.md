# better_flutter_build

### 功能: 
- [x] 自动删除无用的资源文件

### 用法: 
 1. 创建 env.py, 填入必须的参数
```python3
# flutter项目代码目录
project_code_dir = 'xxx/lib'

# 定义资源的文件
resource_define_file = 'xxx/image_path.dart'

# flutter项目资源目录列表
resource_dir_list = [
    'xxx/images',
    'xxx/images/2.0x',
    'xxx/images/3.0x'
]

delete_file_regular = r'test.*'
```
 
 2. 运行脚本
```terminal
python3 main.py
```