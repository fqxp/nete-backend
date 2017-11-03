from nete.util.json_util import default_serialize, note_object_hook
import json
import requests


class NotFound(Exception):
    pass


class NeteClient:

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def list(self):
        return self._get('/notes').json(object_hook=note_object_hook)

    def get_note(self, note_id):
        return self._get('/notes/{}', note_id).json(object_hook=note_object_hook)

    def create_note(self, note):
        return self._post(
            '/notes',
            data=json.dumps(note, default=default_serialize)
            ).json(object_hook=note_object_hook)

    def update_note(self, note):
        response = self._put(
            '/notes/{}', note['id'],
            data=json.dumps(note, default=default_serialize))

    def delete_note(self, note_id):
        response = self._delete('/notes/{}', note_id)

    def _get(self, path, *args, **kwargs):
        request = requests.Request(
            'GET',
            self._url(path, *args, **kwargs))
        return self._send(request)

    def _post(self, path, data, *args, **kwargs):
        request = requests.Request(
            'POST',
            self._url(path, *args, **kwargs),
            data=data)
        return self._send(request)

    def _put(self, path, data, *args, **kwargs):
        request = requests.Request(
            'PUT',
            self._url(path, *args, **kwargs),
            data=data)
        return self._send(request)

    def _delete(self, path, *args, **kwargs):
        request = requests.Request(
            'DELETE',
            self._url(path, *args, **kwargs))
        return self._send(request)

    def _send(self, request):
        response = self.session.send(request.prepare())
        if response.status_code == 404:
            raise NotFound('URL {} not found'.format(request.url))
        return response

    def _url(self, path, *args, **kwargs):
        path = path.lstrip('/').format(*args, **kwargs)
        return '{base_url}/{path}'.format(
            base_url=self.base_url,
            path=path)