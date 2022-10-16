from unittest.mock import MagicMock, patch
import unittest
import docker
from testcontainers.core.docker_client import DockerClient
from testcontainers.core.container import DockerContainer


class KafkaTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_docker_client_from_env(self):
        test_kwargs = dict(
            test_kw="test_value"
        )
        mock_docker = MagicMock(spec=docker)
        with patch("testcontainers.core.docker_client.docker", mock_docker):
            DockerClient(**test_kwargs)

        mock_docker.from_env.assert_called_with(**test_kwargs)


    def test_container_docker_client_kw(self):
        test_kwargs = dict(
            test_kw="test_value"
        )
        mock_docker = MagicMock(spec=docker)
        with patch("testcontainers.core.docker_client.docker", mock_docker):
            DockerContainer(image="", docker_client_kw=test_kwargs)

        mock_docker.from_env.assert_called_with(**test_kwargs)


if __name__ == "__main__":
    unittest.main()