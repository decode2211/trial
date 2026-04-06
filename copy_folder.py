import shutil
import os
try:
    if not os.path.exists('fraud_detection'):
        shutil.copytree('antigravity', 'fraud_detection')
        print('Copied successfully')
except Exception as e:
    print('Error:', e)
