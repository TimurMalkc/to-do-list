import requests

BASE = "http://127.0.0.1:5000/"

requests.post(BASE + "task/1", {"name": "Do dishes", "importance": 2, "date": "this evening"})
requests.post(BASE + "task/2", {"name": "Take out the trash", "importance": 3, "date": "after dinner"})
requests.post(BASE + "task/3", {"name": "Repair the garage door", "importance": 1, "date": "on sunday"})
requests.delete(BASE + "task/4")

