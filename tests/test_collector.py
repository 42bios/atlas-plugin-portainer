import importlib.util,json,os,tempfile,unittest,sys
from pathlib import Path
from unittest.mock import patch,MagicMock
PLUGIN=Path(__file__).resolve().parents[1]/'worker/collector.py'
def load(name):
 spec=importlib.util.spec_from_file_location(name,PLUGIN)
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
class CollectorTests(unittest.TestCase):

    def test_portainer_stacks_roles_and_dependencies(self):
        spec = importlib.util.spec_from_file_location('portainer_collector', PLUGIN)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        data = {'/api/endpoints': [{'Id': 1, 'Name': 'Docker', 'Type': 1}], '/api/endpoints/1/docker/images/json': [{'Id': 'sha256:db', 'RepoTags': None, 'RepoDigests': ['postgres@sha256:digest']}], '/api/stacks': [{'Id': 5, 'Name': 'photos', 'EndpointId': 1}], '/api/endpoints/1/docker/containers/json?all=1': [{'Id': 'web', 'Names': ['/photos-web'], 'Image': 'caddy:2', 'Labels': {'com.docker.compose.project': 'photos', 'com.docker.compose.service': 'web', 'com.docker.compose.depends_on': 'db:service_started', 'secret': 'DO NOT EXPORT'}, 'Ports': []}, {'Id': 'db', 'Names': ['/photos-db'], 'Image': 'sha256:db', 'Labels': {'com.docker.compose.project': 'photos', 'com.docker.compose.service': 'db'}, 'Ports': []}]}
        result = module.collect(data.__getitem__, 'portainer-main')
        self.assertEqual(result['services'][0]['kind'], 'Stack')
        self.assertEqual(result['services'][1]['role'], 'Reverse proxy')
        self.assertEqual(result['services'][2]['role'], 'Database')
        self.assertEqual(result['services'][1]['host'], result['services'][0]['id'])
        self.assertEqual(result['links'][0]['type'], 'Starts after')
        self.assertNotIn('DO NOT EXPORT', json.dumps(result))
        self.assertEqual(module.role('postgres', {'atlas.role': 'Application'}), ('Application', 'Label'))

    def test_tls_pin_rejects_before_credentials_are_sent(self):
        collector_spec = importlib.util.spec_from_file_location('collector', PLUGIN)
        collector = importlib.util.module_from_spec(collector_spec)
        collector_spec.loader.exec_module(collector)
        spec = importlib.util.spec_from_file_location('portainer_runtime', PLUGIN.with_name('runtime.py'))
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {'collector': collector}):
            spec.loader.exec_module(module)
        connection = MagicMock()
        connection.sock.getpeercert.return_value = b'wrong-certificate'
        with patch.dict(os.environ, {'PORTAINER_URL': 'https://example.test:9443', 'PORTAINER_TLS_SHA256': 'a' * 64}), patch.object(module.http.client, 'HTTPSConnection', return_value=connection):
            with self.assertRaises(ValueError):
                module.request('https://example.test:9443/api/endpoints', {'X-API-Key': 'sensitive'})
        connection.request.assert_not_called()
        connection.close.assert_called_once()
