# Operational Excellence Foundations
### ErgoPad OES
![Build Test](https://github.com/ergo-pad/ergopad-oes/actions/workflows/build_test.yml/badge.svg?branch=dev)

## Problem Statement
The ErgoPad website works most of the time. We need to increase availability of our services and reduce downtime. For this we need a proper health check and metrics service for the website with support for notifications.

## Solution
ErgoPad Operational Excellence Service aims to solve this issue with realtime error and latency metrics and a notification system. Everything OES does, depends on the ops config used.OES aims to be as flexible and configurable as possible with its JSON config model such that new services can be onboarded to the system with minimal to no code change.

## OES Architecture
Everything in OES revolves around its ops config JSON file. Let’s dive deep on config processing works for OES.
![image](https://user-images.githubusercontent.com/42897033/185749155-50d33737-abd8-44ec-8bf9-0c31f2eda21c.png)

OES Arch

OES gives its clients full flexibility on how and when notifications are dispatched. The service maintains a state for each endpoint it is registered with and the notification system is triggered when this state changes, be it for latency, errors or for any other user defined reason.

The Anatomy of a Config
Lets dissect an example config
```
{
“version”: “1.0”,
“cool_down”: 600,
	“services”: [
		{
			“url”: “https://api.ergopad.io/asset/price/ergopad”,
			“http_method”: “GET”,
			“response_matcher”: “types”,
			“response”: {
				“status”: “ok”,
				“name: “ergopad”,
				“price”: 1.28
},
“latency”: 500,
},
{
			“url”: “https://api.ergopad.io/balances”,
			“http_method”: “POST”,
                                   “payload”: {
				“addresses”: [“9i6UmaoJKWHgWkuq1EJUoYu2hrkRkxAYwQjDotHRHfGrBo16Rss”]
}
			“response_matcher”: “status_code”,
“latency”: 500,
}
	]

}
```

Configs are basically a list of services that OES must track. Each service has its url, http_method, sample payload (if any) and an expected response configuration. More on expected response configurations in later sections. Latencies are specified in milliseconds.
Default trigger for latencies is 7 point moving averages.

## Response Matchers
status_code: The “status_code” matcher only checks response status_code for 2XX. Details of the response are ignored.
types: The “types” matcher only checks response types to match.
exact: If the matcher is “exact” all values must match for the response.
others: we can define other matchers as we like. Example: charts use case

### Custom Matchers
Custom matchers allow arbitrary user defined computation including calls to other dependencies, OES will look for a python function definition with the same name and pass the response to it.
```
{
“url”: “https://api.ergopad.io/asset/price/chart/ergopad_sigusd?stepSize=1&stepUnit=d”,
	“http_method”: “GET”,
	“response_matcher”: “price_chart_matcher”,
“latency”: 500
}
```

Price chart matcher checks if the current response is stale or not. The response should be changing every 15 mins.

## Service State Store
Service state store maintains the health state for each of the services in the config. 
```
{
	“version”: “1.0”,
	“services”: [
	{
			“url”: “https://api.ergopad.io/asset/price/ergopad”,
			“violations”: [“latency”, “error”]
},
{
			“url”: “https://api.ergopad.io/balances”,
			“violations”: []
		}

]
}
```

The notification service looks for the violations and triggers the messages for discord.
