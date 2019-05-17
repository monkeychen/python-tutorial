import os
import time

sources = ['/tmp/tmp.log']
target_dir = '/tmp/backup'
target = target_dir + os.sep + time.strftime('%Y%m%d%H%M%S') + ".zip"

if not os.path.exists(target_dir):
    os.mkdir(target_dir)

zip_cmd = 'zip -r {0} {1}'.format(target, " ".join(sources))
print("Zip command is:%s\nRunning zip cmd:\n" % zip_cmd)
if os.system(zip_cmd) == 0:
    print("Successful backup to {0}".format(target))
else:
    print("Fail to backup!")
