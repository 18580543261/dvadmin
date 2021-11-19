#流程
##1 蓝牙连接
###配网
长按按钮打开蓝牙进行配网\
wifi未连接时开灯闪烁\
wifi连接完成常亮\
服务器连接完成熄灯\
关闭蓝牙\

###方式
二维码：

###硬件提供
serial:序列号,保证每一个板子是唯一的一个值，可以采取uuid，需记录在硬件端，永久不可变更

###硬件接收
username：mqtt账户名\
password：mqtt密码\
host：47.93.23.xxx \
port：1883  \
clientid：连接mqtt服务器所需id\
wifi_name：wifi账户名\
wifi_pass：wifi密码\

##2 硬件端执行或解码
###连接
connect：通过上述蓝牙获取的参数进行连接wifi以及服务器

###订阅
subscribe：需订阅"{username}/{clientid}/#"，大括号的内容需要按参数进行修改，\
例如:\
蓝牙接收的username为：xiaodong                 \
蓝牙接收的clientid为：xxxx-ssss-zzzz-ssss      \
则订阅：xiaodong/xxxx-ssss-zzzz-ssss/#

###消息发布与接收
####注册（硬件端发布）
#####topic：
{username}/{clientid}/regist/

#####payload:
{"data":[{"code":0,"type":"lamp"},{"code":0,"type":"driver"}]} \
说明：\
code值从0开始,依次加一\
type值目前仅支持：\
lamp：灯 code: 0-max\
sensor_temperature：温度传感器 code：0-max\
sensor_lightness：光照传感器 code: 0-max\
sensor_moisture：湿度传感器 code: 0-max\
sensor_gravity：重力传感器 code: 0-max\
driver：驱动电机 code: 0-max

####状态（硬件端发布）
#####topic：
{username}/{clientid}/status/

#####payload:
{"code":0,"data":100,"type":"lamp"} \
说明：\
code为注册时的元件编号
data为该元件的状态值

####控制（硬件端接收）
#####topic：
{username}/{clientid}/control/

#####payload:
{"code":0,"data":100,"type":"lamp"} \
说明：\
code为注册时的元件编号
data为该元件的状态值

####间隔（硬件端接收）
#####topic：
{username}/{clientid}/gap/

#####payload:
{"code":0,"data":100,"type":"lamp"} \
说明：\
code为注册时的元件编号\
data为该元件隔多少时间上传一次数据，单位：毫秒