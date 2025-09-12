import requests

BASE = "http://127.0.0.1:5000/"

requests.post(BASE + "task/1", {"name": "Do dishes", "importance": 2, "date": "This Evening"})
requests.post(BASE + "task/2", {"name": "Take out the trash", "importance": 3, "date": "After Dinner"})
requests.post(BASE + "task/3", {"name": "Repair the garage door", "importance": 1, "date": "On Sunday"})
requests.post(BASE + "task/4", {"name": "Go to shopping", "importance": 2, "date": "Between Monday and Wednesday"})

requests.put(BASE + "task/3", {"importance": 2})

requests.delete(BASE + "task/4")

