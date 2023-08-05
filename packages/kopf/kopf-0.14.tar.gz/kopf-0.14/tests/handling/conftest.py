"""
Testing the handling of events on the top level.

As input:

* Mocked cause detection, with the cause artificially simulated for each test.
  The proper cause detection is tested elsewhere (see ``test_detection.py``).
* Registered handlers in a global registry. Each handler is a normal function,
  which calls a mock -- to ease the assertions.

As output, we check mocked calls on the following:

* ``asyncio.sleep()`` -- for delays.
* ``kopf.k8s.patching.patch_obj()`` -- for patch content.
* ``kopf.k8s.events.post_event()`` -- for events posted.
* Handler mocks -- whether they were or were not called with specific arguments.
* Captured logs.

The above inputs & outputs represent the expected user scenario
rather than the specific implementation of it.
Therefore, we do not mock/spy/intercept anything within the handling routines
(except for cause detection), leaving it as the implementation details.
Specifically, this internal chain of calls happens on every event:

* ``causation.detect_cause()`` -- tested separately in ``/tests/causation/``.
* ``handle_cause()``
* ``execute()``
* ``_execute()``
* ``_call_handler()``
* ``invocation.invoke()`` -- tested separately in ``/tests/invocations/``.

Some of these aspects are tested separately to be sure they indeed execute
all possible cases properly. In the top-level event handling, we assume they do,
and only check for the upper-level behaviour, not all of the input combinations.
"""
import copy
import dataclasses
from typing import Callable
from unittest.mock import Mock

import pytest
from kubernetes.client.rest import ApiException  # to avoid mocking it

import kopf
from kopf.reactor.causation import Cause


@dataclasses.dataclass(frozen=True, eq=False)
class K8sMocks:
    patch_obj: Mock
    post_event: Mock
    asyncio_sleep: Mock


@pytest.fixture(autouse=True)
def k8s_mocked(mocker):
    """ Prevent any actual K8s calls."""

    # TODO: consolidate with tests/k8s/conftest.py:client_mock()
    client_mock = mocker.patch('kubernetes.client')
    client_mock.rest.ApiException = ApiException  # to be raises and caught

    # We mock on the level of our own K8s API wrappers, not the K8s client.
    return K8sMocks(
        patch_obj=mocker.patch('kopf.k8s.patching.patch_obj'),
        post_event=mocker.patch('kopf.k8s.events.post_event'),
        asyncio_sleep=mocker.patch('asyncio.sleep'),
    )


@pytest.fixture(autouse=True)
def clear_default_registry():
    old_registry = kopf.get_default_registry()
    new_registry = kopf.GlobalRegistry()
    kopf.set_default_registry(new_registry)
    try:
        yield new_registry
    finally:
        kopf.set_default_registry(old_registry)


@pytest.fixture()
def registry(clear_default_registry):
    return clear_default_registry


@dataclasses.dataclass(frozen=True, eq=False, order=False)
class HandlersContainer:
    create_mock: Mock
    update_mock: Mock
    delete_mock: Mock
    create_fn: Callable
    update_fn: Callable
    delete_fn: Callable


@pytest.fixture()
def handlers(clear_default_registry):
    create_mock = Mock(return_value=None)
    update_mock = Mock(return_value=None)
    delete_mock = Mock(return_value=None)

    @kopf.on.create('zalando.org', 'v1', 'kopfexamples', id='create_fn', timeout=600)
    async def create_fn(**kwargs):
        return create_mock(**kwargs)

    @kopf.on.update('zalando.org', 'v1', 'kopfexamples', id='update_fn', timeout=600)
    async def update_fn(**kwargs):
        return update_mock(**kwargs)

    @kopf.on.delete('zalando.org', 'v1', 'kopfexamples', id='delete_fn', timeout=600)
    async def delete_fn(**kwargs):
        return delete_mock(**kwargs)

    return HandlersContainer(
        create_mock=create_mock,
        update_mock=update_mock,
        delete_mock=delete_mock,
        create_fn=create_fn,
        update_fn=update_fn,
        delete_fn=delete_fn,
    )


@pytest.fixture()
def extrahandlers(clear_default_registry, handlers):
    create_mock = Mock(return_value=None)
    update_mock = Mock(return_value=None)
    delete_mock = Mock(return_value=None)

    @kopf.on.create('zalando.org', 'v1', 'kopfexamples', id='create_fn2')
    async def create_fn2(**kwargs):
        return create_mock(**kwargs)

    @kopf.on.update('zalando.org', 'v1', 'kopfexamples', id='update_fn2')
    async def update_fn2(**kwargs):
        return update_mock(**kwargs)

    @kopf.on.delete('zalando.org', 'v1', 'kopfexamples', id='delete_fn2')
    async def delete_fn2(**kwargs):
        return delete_mock(**kwargs)

    return HandlersContainer(
        create_mock=create_mock,
        update_mock=update_mock,
        delete_mock=delete_mock,
        create_fn=create_fn2,
        update_fn=update_fn2,
        delete_fn=delete_fn2,
    )


@pytest.fixture()
def cause_mock(mocker, resource):

    # Use everything from a mock, but use the passed `patch` dict as is.
    # The event handler passes its own accumulator, and checks/applies it later.
    def new_detect_fn(**kwargs):

        # Avoid collision of our mocked values with the passed kwargs.
        original_event = kwargs.pop('event', None)
        original_body = kwargs.pop('body', None)
        event = mock.event if mock.event is not None else original_event
        body = copy.deepcopy(mock.body) if mock.body is not None else original_body

        # Pass through kwargs: resource, logger, patch, diff, old, new.
        # I.e. everything except what we mock: event & body.
        cause = Cause(
            event=event,
            body=body,
            **kwargs)

        # Needed for the k8s-event creation, as they are attached to objects.
        body.setdefault('apiVersion', f'{resource.group}/{resource.version}')
        body.setdefault('kind', 'KopfExample')  # TODO: resource.???
        body.setdefault('metadata', {}).setdefault('namespace', 'some-namespace')
        body.setdefault('metadata', {}).setdefault('name', 'some-name')
        body.setdefault('metadata', {}).setdefault('uid', 'some-uid')

        return cause

    # Substitute the real cause detector with out own mock-based one.
    mocker.patch('kopf.reactor.causation.detect_cause', new=new_detect_fn)

    # The mock object stores some values later used by the factory substitute.
    mock = mocker.Mock(spec_set=['event', 'body'])
    mock.event = None
    mock.body = {'metadata': {'namespace': 'ns1', 'name': 'name1'}}
    return mock
