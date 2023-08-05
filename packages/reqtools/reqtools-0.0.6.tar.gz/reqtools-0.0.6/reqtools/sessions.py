# -*- coding: utf-8 -*-

import json
import logging

import curlify
from requests import Session


logger = logging.getLogger(__name__)


class RemoteApiSession(Session):
    __attrs__ = Session.__attrs__ + ['_base_url', '_prefix']

    def __init__(self, base_url: str, *, prefix: str = None):
        super(RemoteApiSession, self).__init__()

        self._base_url = base_url
        self._prefix = prefix

    def __repr__(self):
        return f'{self.__class__.__name__}({self.url})'

    @property
    def base_url(self):
        return self._base_url

    @property
    def prefix(self):
        return self._prefix

    @property
    def url(self):
        if self.prefix:
            return self._glue_parts(self._base_url, self._prefix)
        return self._base_url

    def _build_url(self, url_path: str):
        if self._prefix:
            url_path = self._glue_parts(self._prefix, url_path)
        return self._glue_parts(self._base_url, url_path)

    def _glue_parts(self, part1, part2: str):
        return part1.rstrip('/') + '/' + part2.lstrip('/')

    def request(self, method: str, url_path: str, **kwargs):
        url = self._build_url(url_path)
        logger.info(f'Performing "{method}" request to "{url}"')

        if kwargs:
            for k, v in kwargs.items():
                if v is not None:
                    message = json.dumps(v, ensure_ascii=False, indent=4)
                    logger.info(f'Request param "{k}": {message}')

        resp = super(RemoteApiSession, self).request(method, url, **kwargs)
        logger.info(curlify.to_curl(resp.request))
        logger.info(f'Response status code is "{resp.status_code}"')

        try:
            message = json.dumps(resp.json(), ensure_ascii=False, indent=4)
            logger.info('\n' + message)
        except ValueError:
            logger.info('\n' + resp.text)

        headers = json.dumps({k: v for k, v in resp.headers.items()})
        logger.info(f'Headers: {headers}')

        total_seconds = resp.elapsed.total_seconds()
        logger.info(f'Response time is "{total_seconds}" seconds')

        return resp
