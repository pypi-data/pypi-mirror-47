from typing import Iterable
from urllib.parse import urljoin

import requests

from vault_cli import client, exceptions, sessions, types


class RequestsVaultClient(client.VaultClientBase):
    def _init_session(self, url: str, verify: types.VerifyOrCABundle) -> None:
        self.session = self.create_session(verify)

        self.url = urljoin(url, "v1/")

    def _full_url(self, path: str) -> str:
        url = urljoin(self.url, self.base_path)
        return urljoin(url, path)

    @staticmethod
    def handle_error(
        response: requests.Response, expected_code: int = requests.codes.ok
    ):
        if response.status_code != expected_code:
            if response.status_code == 404:
                raise exceptions.VaultSecretDoesNotExist(
                    response.status_code, response.text
                )
            raise exceptions.VaultAPIException(response.status_code, response.text)

    @staticmethod
    def create_session(verify: types.VerifyOrCABundle) -> requests.Session:
        session = sessions.Session()
        session.verify = verify
        return session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.__exit__(exc_type, exc_value, traceback)

    def _authenticate_token(self, token: str) -> None:
        self.session.headers.update({"X-Vault-Token": token})

    def _authenticate_userpass(self, username: str, password: str) -> None:
        data = {"password": password}
        response = self.session.post(
            self.url + "auth/userpass/login/" + username, json=data, headers={}
        )
        self.handle_error(response)

        json_response = response.json()
        self.session.headers.update(
            {"X-Vault-Token": json_response.get("auth").get("client_token")}
        )

    def _get_secret_and_metadata(self, path: str) -> types.JSONDict:
        url = self._full_url(path)
        response = self.session.get(url)
        self.handle_error(response)
        json_response = response.json()
        return json_response["data"]

    def get_secret(self, path: str) -> types.JSONValue:
        data = self._get_secret_and_metadata(path)
        return data["value"]

    def list_secrets(self, path: str) -> Iterable[str]:
        url = self._full_url(path).rstrip("/")
        response = self.session.get(url, params={"list": "true"})
        try:
            self.handle_error(response)
        except exceptions.VaultAPIException as exc:
            if exc.status_code == 404:
                return []
            raise
        json_response = response.json()
        return json_response["data"]["keys"]

    def _set_secret(self, path: str, value: types.JSONValue) -> None:
        url = self._full_url(path)
        response = self.session.put(url, json={"value": value})
        self.handle_error(response, requests.codes.no_content)

    def delete_secret(self, path: str) -> None:
        url = self._full_url(path)
        response = self.session.delete(url)
        self.handle_error(response, requests.codes.no_content)
