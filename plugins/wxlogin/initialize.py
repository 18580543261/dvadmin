# 初始化
from django.conf import settings

from apps.dvadmin.system.models import MenuButton, Menu
from utils.apps.dvadmin.core_initialize import CoreInitialize


class Initialize(CoreInitialize):
    creator_id = "456b688c-8ad5-46de-bc2e-d41d8047bd42"
    migrate_list = ['wxlogin']
    requirements_list = []

    def init_menu(self):
        pass
        """
        初始化菜单表
        """
        # self.menu_data = [
        #     {"id": "b02a2224-efc9-4329-9033-7380ac38fb20", "name": "定时任务", "sort": 8, "icon": "hourglass-2",
        #      "web_path": "/task", "component": "dvadmin_plugins/dvadmin_mqtt_iot_web/task/index",
        #      "component_name": "task", "parent_id": "54f769b0-3dff-416c-8102-e55ec44827cc"},
        #     {"id": "b02a2224-efc9-4329-9033-7380ac38fb21", "name": "定时任务详情", "sort": 8, "icon": "map-o",
        #      "web_path": "/taskDetail", "component": "dvadmin_plugins/dvadmin_mqtt_iot_web/taskDetail/index",
        #      "component_name": "taskDetail", "parent_id": "54f769b0-3dff-416c-8102-e55ec44827cc", "visible": 0},
        # ]
        # self.save(Menu, self.menu_data, "菜单表")

    def init_menu_button(self):
        pass
        """
        初始化菜单权限表
        """
        # self.menu_button_data = [
        #     {'id': 'ca8125a6-2868-435b-a6c6-99ce1ef5d9e4', 'menu_id': 'b02a2224-efc9-4329-9033-7380ac38fb20',
        #      'name': '查询', 'value': 'Search', 'api': '/api/dvadmin_mqtt_iot/cron/', 'method': 0},
        #     {'id': '74224c4d-52fe-4624-bf32-5dc432199803', 'menu_id': 'b02a2224-efc9-4329-9033-7380ac38fb20',
        #      'name': '新增', 'value': 'Create', 'api': '/api/dvadmin_mqtt_iot/cron/', 'method': 1},
        #     {'id': '399cd210-fa76-461b-aa5d-8be40b71b3f6', 'menu_id': 'b02a2224-efc9-4329-9033-7380ac38fb20',
        #      'name': '编辑', 'value': 'Update', 'api': '/api/dvadmin_mqtt_iot/cron/{id}/', 'method': 2},
        #     {'id': '64352645-ae18-46be-87b0-e8dc8137a645', 'menu_id': 'b02a2224-efc9-4329-9033-7380ac38fb20',
        #      'name': '删除', 'value': 'Delete', 'api': '/api/dvadmin_mqtt_iot/cron/{id}/', 'method': 3},
        #     {'id': '70a17263-00fa-4299-b9dc-df84f54cafc6', 'menu_id': 'b02a2224-efc9-4329-9033-7380ac38fb20',
        #      'name': '单例', 'value': 'Retrieve', 'api': '/api/dvadmin_mqtt_iot/cron/{id}/', 'method': 0},
        #     {'id': 'ca3125a6-2868-435b-a6c6-99ce1ef5d9e4', 'menu_id': 'b02a2224-efc9-4329-9033-7380ac38fb21',
        #      'name': '查询', 'value': 'Search', 'api': '/api/dvadmin_mqtt_iot/task/', 'method': 0},
        #     {'id': '74424c4d-52fe-4624-bf32-5dc432199803', 'menu_id': 'b02a2224-efc9-4329-9033-7380ac38fb21',
        #      'name': '新增', 'value': 'Create', 'api': '/api/dvadmin_mqtt_iot/task/', 'method': 1},
        #     {'id': '397cd210-fa76-461b-aa5d-8be40b71b3f6', 'menu_id': 'b02a2224-efc9-4329-9033-7380ac38fb21',
        #      'name': '编辑', 'value': 'Update', 'api': '/api/dvadmin_mqtt_iot/task/{id}/', 'method': 2},
        #     {'id': '64852645-ae18-46be-87b0-e8dc8137a645', 'menu_id': 'b02a2224-efc9-4329-9033-7380ac38fb21',
        #      'name': '删除', 'value': 'Delete', 'api': '/api/dvadmin_mqtt_iot/task/{id}/', 'method': 3},
        #     {'id': '70017263-00fa-4299-b9dc-df84f54cafc6', 'menu_id': 'b02a2224-efc9-4329-9033-7380ac38fb21',
        #      'name': '单例', 'value': 'Retrieve', 'api': '/api/dvadmin_mqtt_iot/task/{id}/', 'method': 0}]
        #
        # self.save(MenuButton, self.menu_button_data, "菜单权限表")

    def init(self):
        self.init_menu()
        self.init_menu_button()


