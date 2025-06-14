import requests

API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VybmFtZSI6InVnenVpOTkiLCJDb21pZCI6bnVsbCwiUm9sZWlkIjpudWxsLCJpc3MiOiJ0bWFwaSIsInN1YiI6InVnenVpOTkiLCJhdWQiOlsiIl0sImlhdCI6MTc0OTgzODcwNn0.GQcqv2-ZrFmpyTSqoCvIA0BLJYuhp7-h0Ogsl7foIWs"
url = "https://tmapi.top/api/ali/item-list/search"
headers = {"Authorization": API_TOKEN}
params = {
    "keyword": "韩版 女装",
    "sortType": "salesVolumeDesc",
    "pageSize": 10,
    "days": 10,
    "page": 1
}

res = requests.get(url, headers=headers, params=params)
print("Status:", res.status_code)
print(res.text)
