import os
import requests
import subprocess as sp
from io import BytesIO

base = os.path.dirname(__file__)

tests = os.path.join(base, 'tests')

fail = False

for root, dirs, files in os.walk(tests):
    for f in files:
        if os.path.splitext(f)[1] == '.exe':
            path = os.path.join(root, f)

            proc = sp.Popen([path, '-xunitxml'], stderr=sp.PIPE, stdout=sp.PIPE)
            stdout, stderr = proc.communicate()

            print('{} returncode {}'.format(path, proc.returncode))

            if proc.returncode != 0:
                fail = True
            
            bytes_ = BytesIO(stdout)
            files = {'file': ('tests.xls', bytes_, 'application/xml', {'Expires': '0'})}
            #print(stdout)

            job_id = os.environ['APPVEYOR_JOB_ID']
            url = 'https://ci.appveyor.com/api/testresults/junit/{}'.format(job_id)
            r = requests.post(url, files=files)
            #print(r.status_code, r.text)
            print('status_code {}'.format(r.status_code))

exit(1 if fail else 0)