import os
import pytest

import logging

log = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def mazer_args_for_test(tmpdir_factory):
    return ['mazer']


@pytest.fixture(autouse=True)
def inject_mazer_home(monkeypatch):
    _mazer_home = os.path.join(os.path.dirname(__file__), '_mazer_home')

    monkeypatch.setattr("ansible_galaxy.config.defaults.MAZER_HOME",
                        _mazer_home)
    # log.debug('monkeypatched MAZER_HOME to %s', _mazer_home)


@pytest.fixture
def galaxy_context(tmpdir):
    # FIXME: mock
    server = {'url': 'http://localhost:8000',
              'ignore_certs': False,
              'api_key': None,
              }
    collections_path = tmpdir.mkdir('collections')

    from ansible_galaxy.models.context import GalaxyContext

    return GalaxyContext(server=server, collections_path=collections_path.strpath)
