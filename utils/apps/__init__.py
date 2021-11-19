from django.views.decorators.csrf import csrf_exempt
from django.db import connection, models, transaction
from rest_framework.views import APIView
from django.urls import path


class API(APIView):
    root_path = None

    # @classmethod
    # def as_view(cls, **initkwargs):
    #     """
    #     Store the original class on the view function.
    #
    #     This allows us to discover information about the view when we do URL
    #     reverse lookups.  Used for breadcrumb generation.
    #     """
    #     if isinstance(getattr(cls, 'queryset', None), models.query.QuerySet):
    #         def force_evaluation():
    #             raise RuntimeError(
    #                 'Do not evaluate the `.queryset` attribute directly, '
    #                 'as the result will be cached and reused between requests. '
    #                 'Use `.all()` or call `.get_queryset()` instead.'
    #             )
    #
    #         cls.queryset._fetch_all = force_evaluation
    #
    #     view = super().as_view(**initkwargs)
    #     view.cls = cls
    #     view.initkwargs = initkwargs
    #
    #     # Note: session based authentication is explicitly CSRF validated,
    #     # all other authentication is CSRF exempt.
    #     return csrf_exempt(view)

    def as_api(self,*args,**kwargs):
        if self.root_path:
            p_ = self.root_path
        elif len(args):
            p_ = args[0]
        elif hasattr(kwargs,'path'):
            p_ = kwargs.get('path')
        else:
            p_ = self.__class__.__name__.lower()

        p_ = p_
        return path(p_, self.as_view())


class DBRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'scrapy':
            return 'mongodb'
        else:
            return 'default'

    def db_for_write(self, model, **hints):
        """写数据库"""
        return "default"


    def allow_relation(self, obj1, obj2, **hints):
        """是否运行关联操作"""
        return True