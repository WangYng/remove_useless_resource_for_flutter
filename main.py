import os
import re

from env import resource_define_file, delete_file_regular, project_code_dir, resource_dir_list


def enhance_resource_define_file():
    if os.path.exists(resource_define_file):
        define_resource_list = []
        resource_use_count_map = {}

        # 找出所有资源定义名称
        with open(resource_define_file) as file_obj:
            for line in file_obj.readlines():
                result = re.match(r'.*static const ([a-z_\-0-9]*)', line, re.I)
                if result is not None:
                    define_resource_list.append(result.group(1))
                    resource_use_count_map[result.group(1)] = 0

        # 找出资源定义名称使用的次数
        for root, dirs, files in os.walk(project_code_dir):
            for f in files:
                path = os.path.join(root, f)
                if f.startswith('.'):
                    continue
                with open(path) as file_obj:
                    file_content = file_obj.read()
                    for define_resource in define_resource_list:
                        find_count = file_content.count(define_resource)
                        if find_count != 0:
                            count = resource_use_count_map[define_resource]
                            resource_use_count_map[define_resource] = count + find_count

        # 找出无用的资源定义
        useless_resource_define_list = []
        for name in resource_use_count_map.keys():
            if resource_use_count_map[name] <= 1:
                useless_resource_define_list.append(name)

        # 删除无用的资源定义
        with open(resource_define_file) as read_file_obj:
            resource_define_file_lines = read_file_obj.readlines()

        os.remove(resource_define_file)

        with open(resource_define_file, mode='w') as write_file_obj:
            for line in resource_define_file_lines:
                useless = False
                for useless_resource_define in useless_resource_define_list:
                    if line.find(useless_resource_define) != -1:
                        useless = True
                        break
                if not useless:
                    write_file_obj.write(line)


def find_useless_resource_and_delete():
    # 找出所有资源
    resource_file_list = []
    resource_file_count_map = {}

    for resource_dir in resource_dir_list:
        for root, dirs, files in os.walk(resource_dir):
            for file in files:
                resource_file_list.append(file)
                resource_file_count_map[file] = 0
    resource_file_list = list(set(resource_file_list))

    # 找出资源使用的次数
    for root, dirs, files in os.walk(project_code_dir):
        for f in files:
            path = os.path.join(root, f)
            if f.startswith('.'):
                continue
            with open(path) as file_obj:
                file_content = file_obj.read()
                for resource_file in resource_file_list:
                    find_count = file_content.count(resource_file)
                    if find_count != 0:
                        count = resource_file_count_map[resource_file]
                        resource_file_count_map[resource_file] = count + find_count

    # 找出无用的资源
    useless_resource_file_list = []
    for name in resource_file_count_map.keys():
        if resource_file_count_map[name] < 1:
            useless_resource_file_list.append(name)

    # 删除指定的无用的资源
    for resource_dar in resource_dir_list:
        for root, dirs, files in os.walk(resource_dar):
            for f in files:
                if f in useless_resource_file_list:
                    re_result = re.match(delete_file_regular, f, re.I)
                    if re_result is not None:
                        path = os.path.join(root, f)
                        try:
                            os.remove(path)
                            print(f"删除 {path} 成功")
                        except RuntimeError:
                            print(f"删除 {path} 失败")


if __name__ == '__main__':

    # 优化资源定义文件, 删除无用的资源定义
    enhance_resource_define_file()

    # 删除指定的无用的资源
    find_useless_resource_and_delete()

    print("\n运行完成")




