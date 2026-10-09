import json
import os
from pathlib import Path
import runpy
import sys
config_path=Path(os.environ['ADDIN_CONFIG_FILE'])
config=json.loads(config_path.read_text())
credential=os.environ['ADDIN_CREDENTIAL_FILE']
os.environ['RUN_ONCE']='true'
sys.path.insert(0,str(Path(__file__).parent/'worker'))
os.environ.update(PORTAINER_URL=config['upstreamUrl'],PORTAINER_TLS_SHA256=config.get('tlsFingerprint',''),PORTAINER_TOKEN_FILE=credential)
runpy.run_path(str(Path(__file__).parent/'worker/runtime.py'),run_name='__main__')
