# remove_useless_resource_for_flutter

### 功能: 
- [x] 删除项目中无用的文件

### 脚本执行过程
 1. 找出全部`定义资源路径的常量`，进行全局搜索
 2. 如果没有任何地方引用这些`定义资源路径的常量`，提示用户删除这些`定义资源路径的常量`
 3. 找出全部`定义Router的常量`，进行全局搜索，搜索时排除了`main.dart`这个文件
 4. 如果除了`main.dart`这个文件外，没有任何地方引用这些`定义Router的常量`，提示用户删除这些`定义Router的常量`
 5. 在指定的`搜索文件夹`中找出`没有被引用过的文件`，也就是在项目的代码中，没有使用过这个文件
 6. 提示用户需要删除这些文件，并等待用户反馈
 7. 根据用户反馈删除这些文件
 
### 用法: 
 1. 创建 env.py, 填入必须的参数
```python3
# flutter项目代码目录, 必填
project_code_dir = 'xxx/lib'

# 定义资源路径的文件， 没有填 ''
resource_define_file = 'xxx/image_path.dart'

# 定义Router的文件， 没有填 ''
router_define_file = 'xxx/router.dart'

# 在哪些目录中搜索文件
resource_dir_list = [
    'xxx//lib'
    'xxx/images',
    'xxx/images/2.0x',
    'xxx/images/3.0x',
    'xxx/lib'
]

```
 
 2. 运行脚本，删除`无用的资源定义`和`无用的router定义`
```terminal
python3 main.py
```

 3. 打开IDE，在 `main.dart` 中删除`报错的路由定义代码`，同时删除无用的 `import` 代码
```dart
import 'xxxx.dart'; // unused import
```

 5. 再次运行脚本，删除`无用的文件`
```terminal
python3 main.py
```