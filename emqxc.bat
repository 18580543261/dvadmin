cd emqx/bin
set ip=192.168.123.116:8181/api/mqtt/
set auth=axfw34y235wrq234t4ersgw4t
cmd /c emqx_ctl resources create "web_hook" -i "resource:connect" -c "{\"url\": \"http://%ip%/device/connect/\", \"headers\": {\"HTTP_AUTHORIZATION\":\"%auth%\"}, \"method\": \"POST\"}"
cmd /c emqx_ctl resources create "web_hook" -i "resource:disconnect" -c "{\"url\": \"http://%ip%/device/disconnect/\", \"headers\": {\"HTTP_AUTHORIZATION\":\"%auth%\"}, \"method\": \"POST\"}"
cmd /c emqx_ctl resources create "web_hook" -i "resource:deliver" -c "{\"url\": \"http://%ip%/device/deliver/\", \"headers\": {\"HTTP_AUTHORIZATION\":\"%auth%\"}, \"method\": \"POST\"}"
cmd /c emqx_ctl resources create "web_hook" -i "resource:ack" -c "{\"url\": \"http://%ip%/device/ack/\", \"headers\": {\"HTTP_AUTHORIZATION\":\"%auth%\"}, \"method\": \"POST\"}"
cmd /c emqx_ctl resources create "web_hook" -i "resource:drop" -c "{\"url\": \"http://%ip%/device/drop/\", \"headers\": {\"HTTP_AUTHORIZATION\":\"%auth%\"}, \"method\": \"POST\"}"
cmd /c emqx_ctl resources create "web_hook" -i "resource:subscribe" -c "{\"url\": \"http://%ip%/device/subscribe/\", \"headers\": {\"HTTP_AUTHORIZATION\":\"%auth%\"}, \"method\": \"POST\"}"
cmd /c emqx_ctl resources create "web_hook" -i "resource:unsubscribe" -c "{\"url\": \"http://%ip%/device/unsubscribe/\", \"headers\": {\"HTTP_AUTHORIZATION\":\"%auth%\"}, \"method\": \"POST\"}"

cmd /c emqx_ctl rules create "SELECT * FROM \"$events/client_connected\"" "[{\"name\":\"data_to_webserver\",\"params\": {\"$resource\":  \"resource:connect\"}}]" -i "connect" -d "client_connected"
cmd /c emqx_ctl rules create "SELECT * FROM \"$events/client_disconnected\"" "[{\"name\":\"data_to_webserver\",\"params\": {\"$resource\":  \"resource:disconnect\"}}]" -i "disconnect" -d "client_disconnected"
cmd /c emqx_ctl rules create "SELECT * FROM \"$events/message_delivered\"" "[{\"name\":\"data_to_webserver\",\"params\": {\"$resource\":  \"resource:deliver\"}}]" -i "deliver" -d "message_delivered"
cmd /c emqx_ctl rules create "SELECT * FROM \"$events/message_acked\"" "[{\"name\":\"data_to_webserver\",\"params\": {\"$resource\":  \"resource:ack\"}}]" -i "ack" -d "message_acked"
cmd /c emqx_ctl rules create "SELECT * FROM \"$events/message_dropped\"" "[{\"name\":\"data_to_webserver\",\"params\": {\"$resource\":  \"resource:drop\"}}]" -i "drop" -d "message_dropped"
cmd /c emqx_ctl rules create "SELECT * FROM \"$events/session_subscribed\"" "[{\"name\":\"data_to_webserver\",\"params\": {\"$resource\":  \"resource:subscribe\"}}]" -i "subscribe" -d "session_subscribed"
cmd /c emqx_ctl rules create "SELECT * FROM \"$events/session_unsubscribed\"" "[{\"name\":\"data_to_webserver\",\"params\": {\"$resource\":  \"resource:unsubscribe\"}}]" -i "unsubscribe" -d "session_unsubscribed"