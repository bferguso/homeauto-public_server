import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/python/publicServer")
#from publicServer.app import app as application
from app import app as application