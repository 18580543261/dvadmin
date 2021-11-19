# # dvadmin 插件
import json
import os
import traceback

from git import GitCommandError

from django.conf import settings
from config.settings import PLUGINS_WEB_YAML_PATH, PLUGINS_BACKEND_YAML_PATH
# 拉取插件
from utils.apps.dvadmin.git_utils import GitRepository


def get_all_plugins():
    """
    获取所有插件字典
    :return:
    """
    plugins_dict = {}
    if os.path.exists(PLUGINS_WEB_YAML_PATH):
        with open(PLUGINS_WEB_YAML_PATH, 'r', encoding='utf-8') as doc:
            # 进行排序
            plugins_dict.update(dict(sorted(json.load(doc).items(), key=lambda x: x[1]['priority'], reverse=True)))
    else:
        print("未找到前端插件配置文件，请检查...")
    if os.path.exists(PLUGINS_WEB_YAML_PATH):
        with open(PLUGINS_BACKEND_YAML_PATH, 'r', encoding='utf-8') as doc:
            # 进行排序
            plugins_dict.update(dict(sorted(json.load(doc).items(), key=lambda x: x[1]['priority'], reverse=True)))
    else:
        print("未找到后端插件配置文件，请检查...")
    settings.PLUGINS_LIST = {plugins_name: plugins_values for plugins_name, plugins_values in plugins_dict.items() if
                             plugins_values.get('enable', None)}
    return plugins_dict


def install_update_plugins(plugins_name, data: dict):
    """
    安装插件字典
    :return:
    """
    name = data.get('name')
    if not name: return False, "插件名不能为空"
    git = data.get('git')
    if not git: return False, "插件git地址不能为空"
    tags = data.get('tags')
    if not tags: return False, "插件tags不能为空"
    type = data.get('type')
    if not type: return False, "插件type不能为空"
    enable = data.get('enable', False)

    new_data = {
        plugins_name: {
            "name": name,
            "enable": enable,
            "git": git,
            "priority": data.get('priority', 1),
            "tags": tags,
            "type": type
        }
    }
    yaml_path = PLUGINS_WEB_YAML_PATH if type == 'web' else PLUGINS_BACKEND_YAML_PATH
    with open(yaml_path, 'r', encoding='utf-8') as doc:
        plugins_dict = json.load(doc)
    plugins_dict.update(new_data)
    with open(yaml_path, "w", encoding='utf-8') as doc:
        json.dump(plugins_dict, doc, indent=2, ensure_ascii=False)
    # 校验插件是否存在，不存在下载
    plugins_exists()
    return True, ""


def delete_plugins(plugins_name):
    yaml_path = PLUGINS_WEB_YAML_PATH if type == 'web' else PLUGINS_BACKEND_YAML_PATH
    with open(yaml_path, 'r', encoding='utf-8') as doc:
        plugins_dict = json.load(doc)
    if not plugins_dict.get(plugins_name, None):
        return False, f"插件[{plugins_name}]不存在"
    plugins_dict.pop(plugins_name)
    with open(yaml_path, "w", encoding='utf-8') as doc:
        json.dump(plugins_dict, doc, indent=2, ensure_ascii=False)
    return True, ""


def plugins_initialize(plugins_name):
    def initialize_main(plugins_name):
        """
        执行 main
        :param plugins_name: 插件名称
        :return:
        """
        exec(f"""
try:
    from plugins.{plugins_name}.initialize import Initialize
    try:
        Initialize()._init()
    except Exception:
        traceback.print_exc()
except Exception as E:
    print("插件初始化数据失败，",E)
else:
    print("插件初始化 initialize 完成！")
""")

    # 校验是否为租户插件下安装插件
    if getattr(settings, 'PLUGINS_LIST', {}).get('dvadmin_tenant_backend', None):
        try:
            from django_tenants.utils import tenant_context
            from plugins.dvadmin_tenant_backend.models import Client
            for tenant in Client.objects.all():
                with tenant_context(tenant):
                    initialize_main(plugins_name)
        except Exception:
            traceback.print_exc()
            pass
    else:
        initialize_main(plugins_name)

def plugins_exists():
    """
    校验插件是否存在，不存在下载
    :return:
    """
    print('检查plugins_exists')
    plugins_dict = get_all_plugins()
    plugins_dict = dict(sorted(plugins_dict.items(), key=lambda x: x[1]['priority'], reverse=False))
    for key, plugins in plugins_dict.items():
        # 启动状态的插件不存在下载
        if not plugins.get('enable'):
            continue
        # 获取插件的目录，校验插件是否存在
        yaml_path = ""
        plugins_type = plugins.get('type', None)
        if plugins_type == 'web':
            yaml_path = PLUGINS_WEB_YAML_PATH
        elif plugins_type == 'backend':
            yaml_path = PLUGINS_BACKEND_YAML_PATH
        if not yaml_path:
            continue
        plugins_path = os.path.join(os.path.split(yaml_path)[0], key)
        plugins_name = plugins.get('name')
        tags = plugins.get('tags')
        repo_url = plugins.get('git')
        # 目录不存在则下拉
        if not os.path.exists(plugins_path):
            # 进行下载
            print(f"插件[{plugins_name}]({repo_url})插件未安装，正在安装中...")
            # 插件初始化
            if plugins_type == 'backend':
                settings.INITIALIZE_LIST.append({
                    "function": plugins_initialize,
                    "kwargs": {
                        "plugins_name": key
                    }
                })
            # 从远程仓库将代码下载到上面创建的目录中
            try:
                repo = GitRepository(repo_url=repo_url, local_path=plugins_path)
            except GitCommandError as e:
                print(f"插件[{plugins_name}]git 初始化失败，请手动删除，否则无法进行更新！")
                continue
            if not repo.tags_exists(tags):
                print(f"插件[{plugins_name}]中无[{tags}]标签，请检查！")
                continue
            repo.change_to_tag(tag=tags)
            print(f"插件[{plugins_name}][{tags}]插件安装完成！")
        else:

            try:
                repo = GitRepository(repo_url=repo_url, local_path=plugins_path)
            except GitCommandError as e:
                print(f"插件[{plugins_name}]git 初始化失败，请手动删除，否则无法进行更新！")
                traceback.print_exc()
                continue
            if not repo.tags_exists(tags):
                print(f"插件[{plugins_name}]中无[{tags}]标签，请检查！")
                continue
            repo.change_to_tag(tag=tags)


def requrement(plugin_name,path):
    requirement = path

    print(f'{plugin_name}:检查依赖环境文件')
    print(f'{plugin_name}:依赖环境文件{requirement}')
    print(f'{plugin_name}:依赖环境文件{"存在" if os.path.exists(requirement) else "不存在"}')
    if os.path.exists(requirement):
        try:
            print('检查依赖环境不存在，正在安装...')
            os.system(f'pip install -r {requirement}')
        except Exception:
            traceback.print_exc()


# 检查插件状态
if not getattr(settings, 'ENABLE_PLUGINS', True):
    print("插件功能未启用...")
else:
    print("插件功能启用...")
    plugins_exists()
    with open(PLUGINS_BACKEND_YAML_PATH, 'r', encoding='utf-8') as doc:
        plugins_dict = json.load(doc)
        # 进行排序
        plugins_dict = dict(sorted(plugins_dict.items(), key=lambda x: x[1]['priority'], reverse=True))
        for plugins_name, plugins_values in plugins_dict.items():
            # 校验插件是否
            if plugins_values.get('enable', None):
                import os
                requirement = os.path.join(os.getcwd(),'plugins',plugins_name,'requirements.txt')
                requrement(plugins_name,path=requirement)
                exec(f'''
from plugins.{plugins_name} import settings as plugin_setting
from plugins.{plugins_name}.settings import *
for setting_ in dir(plugin_setting):
    if setting_.isupper():
        setattr(settings,setting_,getattr(plugin_setting, setting_))
''')
                print(f"【{plugins_values.get('name', None)}】导入成功")

print('PLUGINS_LIST',getattr(settings, 'PLUGINS_LIST', {}))
print('INITIALIZE_LIST',getattr(settings, 'INITIALIZE_LIST', {}))
print('INSTALLED_APPS',getattr(settings, 'INSTALLED_APPS', {}))
# 不是为租户模式下，新安装插件进行初始化菜单等数据，租户模式下，则在dvadmin_tenant_backend/apps 下进行初始化
if not getattr(settings, 'PLUGINS_LIST', {}).get('dvadmin_tenant_backend', None):
    print('当前为非租户模式，执行插件安装')
    [ele.get('function')(**ele.get('kwargs', {})) for ele in settings.INITIALIZE_LIST]
else:
    print('当前为租户模式，执行插件准备')
    [ele.get('function')(**ele.get('kwargs', {})) for ele in settings.INITIALIZE_LIST]