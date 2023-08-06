import asyncio
import dataclasses
import json
import re
import sys
import time
from unittest.mock import Mock

import asynctest
import pykube
import pytest
import pytest_mock

from kopf.reactor.registries import Resource


# Make all tests in this directory and below asyncio-compatible by default.
def pytest_collection_modifyitems(items):
    for item in items:
        if asyncio.iscoroutinefunction(item.function):
            item.add_marker('asyncio')


# Substitute the regular mock with the async-aware mock in the `mocker` fixture.
@pytest.fixture(scope='session', autouse=True)
def enforce_asyncio_mocker():
    pytest_mock._get_mock_module = lambda config: asynctest


@pytest.fixture()
def resource():
    """ The resource used in the tests. Usually mocked, so it does not matter. """
    return Resource('zalando.org', 'v1', 'kopfexamples')

#
# Mocks for Kubernetes API clients (any of them). Reasons:
# 1. We do not test the clients, we test the layers on top of them,
#    so everything low-level should be mocked and assumed to be functional.
# 2. No external calls must be made under any circumstances.
#    The unit-tests must be fully isolated from the environment.
#

@pytest.fixture()
def req_mock(mocker, resource, request):

    # Pykube config is needed to create a pykube's API instance.
    # But we do not want and do not need to actually authenticate, so we mock.
    # Some fields are used by pykube's objects: we have to know them ("leaky abstractions").
    cfg_mock = mocker.patch('kopf.k8s.config.get_pykube_cfg').return_value
    cfg_mock.cluster = {'server': 'localhost'}
    cfg_mock.namespace = 'default'

    # Simulated list of cluster-defined CRDs: all of them at once. See: `resource` fixture(s).
    # Simulate the resource as cluster-scoped is there is a marker on the test.
    namespaced = not any(marker.name == 'resource_clustered' for marker in request.node.own_markers)
    res_mock = mocker.patch('pykube.http.HTTPClient.resource_list')
    res_mock.return_value = {'resources': [
        {'name': 'kopfexamples', 'kind': 'KopfExample', 'namespaced': namespaced},
    ]}

    # Prevent ANY outer requests, no matter what. These ones are usually asserted.
    req_mock = mocker.patch('requests.Session').return_value
    return req_mock


@pytest.fixture()
def stream(req_mock):
    """ A mock for the stream of events as if returned by K8s client. """
    def feed(*args):
        side_effect = []
        for arg in args:
            if isinstance(arg, (list, tuple)):
                arg = iter(json.dumps(event).encode('utf-8') for event in arg)
            side_effect.append(arg)
        req_mock.get.return_value.iter_lines.side_effect = side_effect
    return Mock(spec_set=['feed'], feed=feed)

#
# Mocks for login & checks. Used in specifialised login tests,
# and in all CLI tests (since login is implicit with CLI commands).
#

@dataclasses.dataclass(frozen=True, eq=False, order=False)
class LoginMocks:
    pykube_in_cluster: Mock
    pykube_from_file: Mock
    pykube_checker: Mock
    client_in_cluster: Mock
    client_from_file: Mock
    client_checker: Mock


@pytest.fixture()
def login_mocks(mocker):
    kubernetes = pytest.importorskip('kubernetes')

    # Pykube config is needed to create a pykube's API instance.
    # But we do not want and do not need to actually authenticate, so we mock.
    # Some fields are used by pykube's objects: we have to know them ("leaky abstractions").
    cfg_mock = mocker.patch('kopf.k8s.config.get_pykube_cfg').return_value
    cfg_mock.cluster = {'server': 'localhost'}
    cfg_mock.namespace = 'default'

    return LoginMocks(
        pykube_in_cluster=mocker.patch.object(pykube.KubeConfig, 'from_service_account'),
        pykube_from_file=mocker.patch.object(pykube.KubeConfig, 'from_file'),
        pykube_checker=mocker.patch.object(pykube.http.HTTPClient, 'get'),
        client_in_cluster=mocker.patch.object(kubernetes.config, 'load_incluster_config'),
        client_from_file=mocker.patch.object(kubernetes.config, 'load_kube_config'),
        client_checker=mocker.patch.object(kubernetes.client, 'CoreApi'),
    )

#
# Simulating that Kubernetes client library is not installed.
#

class ProhibitedImportFinder:
    def find_spec(self, fullname, path, target=None):
        if fullname == 'kubernetes' or fullname.startswith('kubernetes'):
            raise ImportError("Import is prohibited for tests.")


@pytest.fixture()
def kubernetes_uninstalled():

    # Remove any cached modules.
    preserved = {}
    for name, mod in list(sys.modules.items()):
        if name == 'kubernetes' or name.startswith('kubernetes.'):
            preserved[name] = mod
            del sys.modules[name]

    # Inject the prohibition for loading this module. And restore when done.
    finder = ProhibitedImportFinder()
    sys.meta_path.insert(0, finder)
    try:
        yield
    finally:
        sys.meta_path.remove(finder)
        sys.modules.update(preserved)

#
# Helpers for the timing checks.
#

@pytest.fixture()
def timer():
    return Timer()


class Timer(object):
    """
    A helper context manager to measure the time of the code-blocks.
    Also, supports direct comparison with time-deltas and the numbers of seconds.

    Usage:

        with Timer() as timer:
            do_something()
            print(f"Executing for {timer.seconds}s already.")
            do_something_else()

        print(f"Executed in {timer.seconds}s.")
        assert timer < 5.0
    """

    def __init__(self):
        super().__init__()
        self._ts = None
        self._te = None

    @property
    def seconds(self):
        if self._ts is None:
            return None
        elif self._te is None:
            return time.perf_counter() - self._ts
        else:
            return self._te - self._ts

    def __repr__(self):
        status = 'new' if self._ts is None else 'running' if self._te is None else 'finished'
        return f'<Timer: {self.seconds}s ({status})>'

    def __enter__(self):
        self._ts = time.perf_counter()
        self._te = None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._te = time.perf_counter()

    def __int__(self):
        return int(self.seconds)

    def __float__(self):
        return float(self.seconds)

#
# Helpers for the logging checks.
#

@pytest.fixture()
def assert_logs(caplog):
    """
    A function to assert the logs are present (by pattern).

    The listed message patterns MUST be present, in the order specified.
    Some other log messages can also be present, but they are ignored.
    """
    def assert_logs_fn(patterns, prohibited=[], strict=False):
        __traceback_hide__ = True
        remaining_patterns = list(patterns)
        for message in caplog.messages:
            # The expected pattern is at position 0.
            # Looking-ahead: if one of the following patterns matches, while the
            # 0th does not, then the log message is missing, and we fail the test.
            for idx, pattern in enumerate(remaining_patterns):
                m = re.search(pattern, message)
                if m:
                    if idx == 0:
                        remaining_patterns[:1] = []
                        break  # out of `remaining_patterns` cycle
                    else:
                        skipped_patterns = remaining_patterns[:idx]
                        raise AssertionError(f"Few patterns were skipped: {skipped_patterns!r}")
                elif strict:
                    raise AssertionError(f"Unexpected log message: {message!r}")

            # Check that the prohibited patterns do not appear in any message.
            for pattern in prohibited:
                m = re.search(pattern, message)
                if m:
                    raise AssertionError(f"Prohibited log pattern found: {message!r} ~ {pattern!r}")

        # If all patterns have been matched in order, we are done.
        # if some are left, but the messages are over, then we fail.
        if remaining_patterns:
            raise AssertionError(f"Few patterns were missed: {remaining_patterns!r}")

    return assert_logs_fn
