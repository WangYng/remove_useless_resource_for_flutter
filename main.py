import os
import re

from env import resource_define_file, project_code_dir, resource_dir_list, router_define_file


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
                print("%s" % name)

        # 提示用户删除
        if len(useless_resource_define_list) > 0:
            while True:
                is_delete = input("是否删除以上无用的资源定义 (Y/N):")
                if is_delete == "Y" or is_delete == "y":
                    break
                elif is_delete == "N" or is_delete == "n":
                    return
                else:
                    print("请输入Y(同意)或者N(不同意)")

        # 读取资源定义文件内容
        with open(resource_define_file) as read_file_obj:
            resource_define_file_lines = read_file_obj.readlines()

        # 删除资源定义文件
        os.remove(resource_define_file)

        # 重建资源定义文件内容
        with open(resource_define_file, mode='w') as write_file_obj:
            for line in resource_define_file_lines:
                useless = False
                for useless_resource_define in useless_resource_define_list:
                    if line.find(useless_resource_define) != -1:
                        useless = True
                        break
                if not useless:
                    write_file_obj.write(line)


def enhance_router_define_file():
    if os.path.exists(router_define_file):
        define_router_list = []
        router_use_count_map = {}

        # 找出所有路由定义名称
        with open(router_define_file) as file_obj:
            for line in file_obj.readlines():
                result = re.match(r'.*static const ([a-z_\-0-9]*)', line, re.I)
                if result is not None:
                    router_name = result.group(1)
                    define_router_list.append(router_name)
                    router_use_count_map[router_name] = 0

        # 找出路由定义名称使用的次数
        for root, dirs, files in os.walk(project_code_dir):
            for f in files:
                path = os.path.join(root, f)
                if f.startswith('.'):
                    continue
                if f.startswith('main.dart'):
                    continue
                with open(path) as file_obj:
                    file_content = file_obj.read()
                    for define_router in define_router_list:
                        find_count = file_content.count(define_router)
                        if find_count != 0:
                            count = router_use_count_map[define_router]
                            router_use_count_map[define_router] = count + find_count

        # 找出无用的路由定义
        useless_router_define_list = []
        for name in router_use_count_map.keys():
            if router_use_count_map[name] <= 1:
                useless_router_define_list.append(name)
                print("%s" % name)

        # 提示用户删除
        if len(useless_router_define_list) > 0:
            while True:
                is_delete = input("是否删除以上无用的路由定义 (Y/N):")
                if is_delete == "Y" or is_delete == "y":
                    break
                elif is_delete == "N" or is_delete == "n":
                    return
                else:
                    print("请输入Y(同意)或者N(不同意)")

        # 读取路由定义文件内容
        with open(router_define_file) as read_file_obj:
            router_define_file_lines = read_file_obj.readlines()

        # 删除路由定义文件
        os.remove(router_define_file)

        # 重建路由定义文件内容
        with open(router_define_file, mode='w') as write_file_obj:
            for line in router_define_file_lines:
                useless = False
                for useless_router_define in useless_router_define_list:
                    if line.find(useless_router_define) != -1:
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
                if str(file) != 'main.dart':
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
            print(name)

    # 提示用户删除
    if len(useless_resource_file_list) > 0:
        while True:
            is_delete = input("是否删除以上无用的文件 (Y/N):")
            if is_delete == "Y" or is_delete == "y":
                # 删除指定的无用的资源
                for resource_dar in resource_dir_list:
                    for root, dirs, files in os.walk(resource_dar):
                        for f in files:
                            if f in useless_resource_file_list:
                                path = os.path.join(root, f)
                                try:
                                    os.remove(path)
                                    print(f"删除 {path} 成功")
                                except RuntimeError:
                                    print(f"删除 {path} 失败")
                return
            elif is_delete == "N" or is_delete == "n":
                return
            else:
                print("请输入Y(同意)或者N(不同意)")


if __name__ == '__main__':
    # 优化资源定义文件, 删除无用的资源定义
    enhance_resource_define_file()

    # 优化路由定义文件, 删除无用的路由定义
    enhance_router_define_file()

    # 删除无用的资源
    find_useless_resource_and_delete()

    print("\n脚本运行完成")
