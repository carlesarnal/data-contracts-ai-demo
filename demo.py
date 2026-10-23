"""Structural publication versus semantic feature checks; no model needed."""
import argparse
import json
import math
import time
import urllib.error
import urllib.request
import uuid


def seconds(value, unit):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError('duration must be numeric, not boolean')
    if not math.isfinite(value) or value < 0:
        raise ValueError('duration must be finite and nonnegative')
    if unit not in {'s', 'ms'}:
        raise ValueError('unit must be explicitly s or ms')
    return value if unit == 's' else value / 1000


def request(base, path, body=None, method='GET', expected=(200, 201, 204)):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(base + '/apis/registry/v3' + path, data=data,
                                 method=method, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            status, raw = response.status, response.read()
    except urllib.error.HTTPError as error:
        status, raw = error.code, error.read()
    if status not in expected:
        raise AssertionError(f'{method} {path}: HTTP {status}: {raw.decode()}')
    return status, json.loads(raw) if raw else None


def content(schema):
    return {'content': json.dumps(schema), 'contentType': 'application/json'}


def registry_check(base):
    for attempt in range(60):
        try:
            request(base, '/system/info')
            break
        except (OSError, AssertionError):
            if attempt == 59:
                raise
            time.sleep(2)
    group = 'feature-lab-' + uuid.uuid4().hex
    schema = {'type': 'record', 'name': 'Duration', 'fields': [
        {'name': 'duration', 'type': 'long'}, {'name': 'unit', 'type': 'string'}]}
    path = f'/groups/{group}/artifacts/duration'
    request(base, '/groups', {'groupId': group}, 'POST')
    try:
        request(base, f'/groups/{group}/artifacts', {
            'artifactId': 'duration', 'artifactType': 'AVRO',
            'firstVersion': {'version': '1', 'content': content(schema)}}, 'POST')
        request(base, path + '/rules', {'ruleType': 'COMPATIBILITY', 'config': 'BACKWARD'}, 'POST')
        compatible = dict(schema, fields=schema['fields'] + [
            {'name': 'source', 'type': ['null', 'string'], 'default': None}])
        request(base, path + '/versions', {'version': '2', 'content': content(compatible)}, 'POST')
        incompatible = dict(schema, fields=compatible['fields'] + [{'name': 'required_new', 'type': 'string'}])
        status, error = request(base, path + '/versions', {
            'version': '3', 'content': content(incompatible)}, 'POST', expected=(400, 409, 422))
        if 'compatib' not in json.dumps(error).lower():
            raise AssertionError(f'Not a compatibility rejection: {error}')
        request(base, path + '/versions/3', expected=(404,))
        _, accepted = request(base, path + '/versions/2/content')
        assert accepted == compatible, 'accepted content changed after rejection'
        print(json.dumps({'structural_check': 'passed', 'rejection_http': status,
                          'rejected_version_absent': True, 'accepted_content_preserved': True}))
    finally:
        request(base, f'/groups/{group}', method='DELETE')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--registry')
    args = parser.parse_args()
    assert seconds(30, 's') == seconds(30000, 'ms') == 30
    assert 30000 != seconds(30000, 'ms'), 'fixture must detect omitted normalization'
    print(json.dumps({'semantic_check': 'passed', 's_input': 30, 'ms_input': 30000,
                      'expected_seconds': 30, 'unconverted_input_rejected_by_invariant': True}))
    if args.registry:
        registry_check(args.registry.rstrip('/'))
