import sys
import os

sys.path.insert(0, '/app')
os.chdir('/app')

from config.wsgi import application