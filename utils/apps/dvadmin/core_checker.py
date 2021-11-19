# 初始化基类
import traceback

from django.conf import settings


class CoreChecker:
    """
    使用方法：继承此类，重写 run方法，在 run 中调用 save 进行数据初始化
    """
    plugin_name = 'default'
    requirements_list = []


    def requrement(self):
        import os
        from pathlib import Path
        requirement = os.path.join(Path(__file__).resolve(strict=True), "requirements.txt")
        print(f'{self.plugin_name}:检查依赖环境中...')
        try:
            for req in self.requirements_list:
                exec(f'import {req}')
        except ImportError:
            traceback.print_exc()
        else:
            print('检查依赖环境满足条件')
            return

        print(f'{self.plugin_name}:检查依赖环境文件')
        print(f'{self.plugin_name}:依赖环境文件{requirement}')
        print(f'{self.plugin_name}:依赖环境文件{"存在" if os.path.exists(requirement) else "不存在"}')
        if os.path.exists(requirement):
            try:
                print('检查依赖环境不存在，正在安装...')
                os.system(f'pip install -r {requirement}')
            except Exception:
                traceback.print_exc()


    def _check(self):
        self.requrement()
        self.check()

    def check(self):
        pass
        # self.migrate()
