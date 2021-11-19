import datetime
import os
from pathlib import Path
import environ

# ================================================= #
# ******************** 基础设置 ******************** #
# ================================================= #
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = ROOT_DIR / "apps"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))

isDocker = env.bool("DOCKER_ENV", False)
print(f'isDocker:{isDocker}')

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=['127.0.0.1'])

# ================================================= #
# ******************** 时区设置 ******************** #
# ================================================= #
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True
#语言包设置
LOCALE_PATHS = [str(ROOT_DIR / "locale")]

# For files
FILE_UPLOAD_PERMISSIONS = 0o777 #or whatever fits to your needs
# For directories
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o777




# ================================================= #
# ********************  数据库  ******************** #
# ================================================= #
DATABASES = {
    "default": env.db("DATABASE_TENANT_URL", default='',engine='django_tenants.postgresql_backend'),
}
DATABASE_ROUTERS = ['utils.apps.DBRouter']

DATABASES["default"]["ATOMIC_REQUESTS"] = True

#缓存
# CACHES = {
#     "redis":env.cache('REDIS_URL',default="rediscache://127.0.0.1:6379/1?client_class=django_redis.client.DefaultClient&password="),
#     "redis_scrapy":env.cache('REDIS_SCRAPY_URL',default="rediscache://127.0.0.1:6379/2?client_class=django_redis.client.DefaultClient&password="),
# }
# CACHES["default"] = CACHES["redis"]

#邮箱
EMAIL_CONFIG = env.email_url('EMAIL_URL', default='smtp://user@:password@localhost:25')

# ================================================= #
# ******************** api映射 ******************** #
# ================================================= #
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"


# ================================================= #
# ******************** APP ******************** #
# ================================================= #
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    'rest_framework',
    'django_filters',
    'django_comment_migrate',
    'corsheaders',
    # 'captcha',
    'drf_yasg',
]
LOCAL_APPS = [
    'apps.dvadmin.system',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

#MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.apps.dvadmin.middleware.ApiLoggingMiddleware',
]

# ================================================= #
# ******************** 文件系统 ******************** #
# ================================================= #
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(ROOT_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
# MEDIA
MEDIA_ROOT = str(ROOT_DIR / "media")
MEDIA_URL = "/media/"

# ================================================= #
# ******************** Template ******************** #
# ================================================= #
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(ROOT_DIR / "templates")],
        "OPTIONS": {
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# ================================================= #
# ******************** 日志配置 ******************** #
# ================================================= #
SERVER_LOGS_FILE = os.path.join(BASE_DIR, 'logs', 'server.log')
ERROR_LOGS_FILE = os.path.join(BASE_DIR, 'logs', 'error.log')
if not os.path.exists(os.path.join(BASE_DIR, 'logs')):
    os.makedirs(os.path.join(BASE_DIR, 'logs'))

# 格式:[2020-04-22 23:33:01][micoservice.apps.ready():16] [INFO] 这是一条日志:
# 格式:[日期][模块.函数名称():行号] [级别] 信息
STANDARD_LOG_FORMAT = '[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s'
CONSOLE_LOG_FORMAT = '[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': STANDARD_LOG_FORMAT
        },
        'console': {
            'format': CONSOLE_LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'file': {
            'format': CONSOLE_LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': SERVER_LOGS_FILE,
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 5,  # 最多备份5个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': ERROR_LOGS_FILE,
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 3,  # 最多备份3个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        }
    },
    'loggers': {
        # default日志
        '': {
            'handlers': ['console', 'error', 'file'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['console', 'error', 'file'],
            'level': 'INFO',
        },
        'scripts': {
            'handlers': ['console', 'error', 'file'],
            'level': 'INFO',
        },
        # 数据库相关日志
        'django.db.backends': {
            'handlers': [],
            'propagate': True,
            'level': 'INFO',
        },
    }
}




# ================================================= #
# ******************** 跨域设置 ******************** #
# ================================================= #
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)




# ================================================= #
# ************** REST_FRAMEWORK 配置  ************** #
# ================================================= #
REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",  # 日期时间格式配置
    'DATE_FORMAT': "%Y-%m-%d",
    'DEFAULT_FILTER_BACKENDS': (
        # 'django_filters.rest_framework.DjangoFilterBackend',
        'utils.apps.dvadmin.filters.CustomDjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',

    ),
    'DEFAULT_PAGINATION_CLASS': 'utils.apps.dvadmin.pagination.CustomPagination',  # 自定义分页
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'EXCEPTION_HANDLER': 'utils.apps.dvadmin.exception.CustomExceptionHandler',  # 自定义的异常处理
}

# ================================================= #
# ******************** JWT配置  ******************** #
# ================================================= #
SIMPLE_JWT = {
    # token有效时长
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=7),
    # token刷新后的有效时间
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),
    # 设置前缀
    'AUTH_HEADER_TYPES': ('JWT',),
    'ROTATE_REFRESH_TOKENS': True
}

# ================================================= #
# ************** 登录方式配置  ************** #
# ================================================= #
AUTHENTICATION_BACKENDS = [
    'utils.apps.dvadmin.backends.CustomBackend'
]
AUTH_USER_MODEL = 'system.Users'
# username_field
USERNAME_FIELD = 'username'
EMAIL_FIELD = 'email'
# PASSWORDS
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ====================================#
# ****************swagger************#
# ====================================#
SWAGGER_SETTINGS = {
    # 基础样式
    'SECURITY_DEFINITIONS': {
        "basic": {
            'type': 'basic'
        }
    },
    # 如果需要登录才能够查看接口文档, 登录的链接使用restframework自带的.

    'LOGIN_URL': 'apiLogin/',
    # 'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
    # 'DOC_EXPANSION': None,
    # 'SHOW_REQUEST_HEADERS':True,
    # 'USE_SESSION_AUTH': True,
    # 'DOC_EXPANSION': 'list',
    # 接口文档中方法列表以首字母升序排列
    'APIS_SORTER': 'alpha',
    # 如果支持json提交, 则接口文档中包含json输入框
    'JSON_EDITOR': True,
    # 方法列表字母排序
    'OPERATIONS_SORTER': 'alpha',
    'VALIDATOR_URL': None,
    'AUTO_SCHEMA_TYPE': 2,  # 分组根据url层级分，0、1 或 2 层
    'DEFAULT_AUTO_SCHEMA_CLASS': 'utils.apps.dvadmin.swagger.CustomSwaggerAutoSchema',
}

# ================================================= #
# **************** 验证码配置  ******************* #
# ================================================= #
CAPTCHA_STATE = True
CAPTCHA_IMAGE_SIZE = (160, 60)  # 设置 captcha 图片大小
CAPTCHA_LENGTH = 4  # 字符个数
CAPTCHA_TIMEOUT = 1  # 超时(minutes)
CAPTCHA_OUTPUT_FORMAT = '%(image)s %(text_field)s %(hidden_field)s '
CAPTCHA_FONT_SIZE = 40  # 字体大小
CAPTCHA_FOREGROUND_COLOR = '#0033FF'  # 前景色
CAPTCHA_BACKGROUND_COLOR = '#F5F7F4'  # 背景色
CAPTCHA_NOISE_FUNCTIONS = (
    'captcha.helpers.noise_arcs',  # 线
    'captcha.helpers.noise_dots',  # 点
)
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge' #字母验证码
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'  # 加减乘除验证码

# ================================================= #
# ******************** 其他配置 ******************** #
# ================================================= #
# 插件yaml地址
PLUGINS_WEB_YAML_PATH = os.path.join(BASE_DIR, os.path.pardir, os.path.pardir, "frontend","dvadminpro", "src", "views", "dvadmin_plugins", "config.json")
PLUGINS_BACKEND_YAML_PATH = os.path.join(BASE_DIR, "plugins", "config.json")

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
API_LOG_ENABLE = True
# API_LOG_METHODS = 'ALL' # ['POST', 'DELETE']
API_LOG_METHODS = ['POST', 'UPDATE', 'DELETE', 'PUT']  # ['POST', 'DELETE']
API_MODEL_MAP = {
    "/token/": "登录模块",
    "/api/login/": "登录模块",
    "/api/plugins_market/plugins/": "插件市场",
}
# 表前缀
TABLE_PREFIX = "dvadmin_"
DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_TIMEZONE = 'Asia/Shanghai'  # celery 时区问题
# 静态页面压缩
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
# 初始化需要执行的列表，用来初始化后执行
INITIALIZE_LIST = []
READYCHECK_LIST = []
INITIALIZE_RESET_LIST = []
# 导入租户数据
SHARED_APPS = []
TENANT_APPS = [
    'django.contrib.contenttypes',
]



