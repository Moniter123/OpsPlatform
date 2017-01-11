import json
s = '''
{"info": [{"Function": "state.sls", "jid": "20170110143706244910", "Target": "salt-api", "Target-type": "glob", "User": "saltapi", "StartTime": "2017, Jan 10 14:37:06.244910", "Arguments": ["nginx"], "Minions": ["salt-api"], "Result": {"salt-api": {"return": {"file_|-testfile_|-/tmp/testfile_|-managed": {"comment": "File /tmp/testfile is in the correct state", "pchanges": {}, "name": "/tmp/testfile", "start_time": "14:37:06.647638", "result": true, "duration": 1567.536, "__run_num__": 0, "changes": {}, "__id__": "testfile"}}, "out": "highstate"}}}], "return": [{"salt-api": {"file_|-testfile_|-/tmp/testfile_|-managed": {"comment": "File /tmp/testfile is in the correct state", "pchanges": {}, "name": "/tmp/testfile", "start_time": "14:37:06.647638", "result": true, "duration": 1567.536, "__run_num__": 0, "changes": {}, "__id__": "testfile"}}}]}
'''

jsondata = json.loads(s)
print jsondata