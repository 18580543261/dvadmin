import datetime
import time

# 注意类名必须是以Middleware结尾。
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

cache_key = 'visit_info'

def save_to_cache(result):
    t = datetime.timedelta(days=7)
    cache.add(cache_key,result,7*24*60*60)

class VisitMiddleware(MiddlewareMixin):
    """ 访问统计 """

    def __init__(self, get_response):
        super().__init__(get_response)

    def __call__(self, request):
        # 获取request属性，
        request_meta = request.META
        response = self.get_response(request)

        # 对要获取的参数进行判断，防止因没有参数而抛出异常
        HTTP_PARAMS = {'get': dict(request.GET), 'post': dict(request.POST)}
        # ip地址
        if request_meta.get("HTTP_X_FORWARDED_FOR"):
            ip = request_meta["HTTP_X_FORWARDED_FOR"]
        else:
            ip = request_meta["REMOTE_ADDR"]
        # 起始路径，可以统计在网站内部的访问记录，如：从A到B,起始路径就是A
        if request_meta.get('HTTP_REFERER'):
            HTTP_REFERER = request_meta['HTTP_REFERER']
        else:
            HTTP_REFERER = False
        # 目标路径，就是上面说到的B
        if request_meta.get('PATH_INFO'):
            PATH_INFO = request_meta['PATH_INFO']
        else:
            PATH_INFO = False
        # User-agent，这一项也可以用来过滤请求
        if request_meta.get('HTTP_USER_AGENT'):
            HTTP_USER_AGENT = request_meta['HTTP_USER_AGENT']
        else:
            HTTP_USER_AGENT = False
        # 请求方式
        if request_meta.get('REQUEST_METHOD'):
            REQUEST_METHOD = request_meta['REQUEST_METHOD']
        else:
            REQUEST_METHOD = False
        # 连接方式，
        if request_meta.get('HTTP_CONNECTION'):
            HTTP_CONNECTION = request_meta['HTTP_CONNECTION']
        else:
            HTTP_CONNECTION = False
        # 响应码
        response_code = response.status_code
        visit_time = time.strftime("%Y-%m-%d %H:%M:%S")
        # 组装数据，添加访问时间visit_time
        info_list = {
            'IP': ip,
            'HTTP_PARAMS': HTTP_PARAMS,
            'HTTP_REFERER': HTTP_REFERER,
            'PATH_INFO': PATH_INFO,
            'HTTP_USER_AGENT': HTTP_USER_AGENT,
            'REQUEST_METHOD': REQUEST_METHOD,
            'HTTP_CONNECTION': HTTP_CONNECTION,
            'response_code': response_code,
            'visit_time': visit_time
        }

        # 调用存储数据库函数，存入数据库
        save_to_cache(info_list)
        return response