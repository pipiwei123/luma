# luma
#luma-api
将lumaai使用python转为api形式进行调用
方便更快速集成接入到一些三方系统


#1、create为创建任务接口
请求示例：
curl --request POST \
  --url http://127.0.0.1:8008/create \          
  --header 'Authorization: _clck=ao5qvd|2|fmo|0|1628; _ga=GA1.1.408104221.1718518823; access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsidXNlcl91dWlkIjoiYTA1NDVkMTctOGQ4Ni00MjJiLWJjYjAtNDBlMzhjMDI0ZTFhIiwiY2xpZW50X2lkIjoiIn0sImV4cCI6MTcxOTEyMzYzM30.tn3kAjmEKpoPyNPUiq_FRjzmx8NCK88R83TavLgqjBA; refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6.eyJzdWIiOnsidXNlcl91dWlkIjoiYTA1NDVkMTctOGQ4Ni00MjJiLWJjYjAtNDBlMzhjMDI0ZTFhIiwiY2xpZW50X2lkIjoiIn0sImV4cCI6MTcxOTEyMzYzM30.tn3kAjmEKpoPyNPUiq_FRjzmx8NCK88R83TavLgqjBA; _ga_67JX7C10DX=GS1.1.1718518823.1.1.1718518833.0.0.0; _clsk=11r7jg0|1718518833560|6|0|r.clarity.ms/collect' \ 
  --header 'Content-Type:  application/json' \
  --header 'content-type: application/json' \
  --data '{
"user_prompt": "一个猫咪在跟一只狗狗打架",
"aspect_ratio": "16:9",
"expand_prompt": true
}'
响应示例：
{
	"id": "86c68665-4679-4371-8601-ff313be75c1d", 
	"prompt": "一个猫咪在跟一只狗狗打架",
	"state": "pending", 
	"created_at": "2024-06-16T07:15:09.934500Z",
	"video": null,
	"liked": null,
	"estimate_wait_seconds": null
}
#2、查询接口：status/{taskid}
请求示例：
curl --request GET \
  --url http://127.0.0.1:8008/status/660a46a5-b9cf-470b-ba53-39d1306095d3 \       
  --header 'content-type: application/json' 

taskid为create响应中的id字段
