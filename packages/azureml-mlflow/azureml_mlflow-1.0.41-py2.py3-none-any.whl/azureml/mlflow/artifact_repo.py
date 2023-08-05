# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""**AzureMLflowArtifactRepository** provides a class to up/download artifacts to storage backends in Azure."""

import logging
import os

import mlflow
from mlflow.entities import FileInfo
from mlflow.store.artifact_repo import ArtifactRepository

from .utils import artifact_uri_decomp, _EXP_NAME, _RUN_ID
from .run_artifacts_extension_client import RunArtifactsExtensionClient
from six.moves.urllib import parse

logger = logging.getLogger(__name__)


class AzureMLflowArtifactRepository(ArtifactRepository):
    """Define how to upload (log) and download potentially large artifacts from different storage backends."""

    def __init__(self, artifact_uri):
        """
        Construct an AzureMLflowArtifactRepository object.

        This object is used with any of the functions called from mlflow or from
        the client which have to do with artifacts.

        :param artifact_uri: Azure URI. This URI is never used within the object,
            but is included here, as it is included in ArtifactRepository as well.
        :type artifact_uri: str
        """
        logger.debug("Initializing the AzureMLflowArtifactRepository")
        parsed_artifacts_url = parse.urlparse(artifact_uri)
        parsed_artifacts_path = artifact_uri_decomp(parsed_artifacts_url.path)
        experiment_name = parsed_artifacts_path[_EXP_NAME]
        logger.debug("AzureMLflowArtifactRepository for experiment {}".format(experiment_name))
        run_id = parsed_artifacts_path[_RUN_ID]
        logger.debug("AzureMLflowArtifactRepository for run id {}".format(run_id))
        self._run_id = run_id

        aml_store = mlflow.tracking.MlflowClient().store
        logger.debug("Using the service context for the tracking uri {}".format(aml_store.__class__.__name__))
        self.run_artifacts = RunArtifactsExtensionClient(aml_store.service_context, experiment_name)

    def log_artifact(self, local_file, artifact_path=None):
        """
        Log a local file as an artifact.

        Optionally takes an ``artifact_path``, which renames the file when it is
        uploaded to the ArtifactRepository.

        :param local_file: Absolute or relative path to the artifact locally.
        :type local_file: str
        :param artifact_path: Path to a file in the AzureML run's outputs, to where the artifact is uploaded.
        :type artifact_path: str
        """
        dest_path = self._normalize_slashes(self._build_dest_path(local_file, artifact_path))
        self.run_artifacts.upload_artifact(local_file, self._run_id, dest_path)

    def log_artifacts(self, local_dir, artifact_path=None):
        """
        Log the files in the specified local directory as artifacts.

        Optionally takes an ``artifact_path``, which specifies the directory of
        the AzureML run under which to place the artifacts in the local directory.

        :param local_dir: Directory of local artifacts to log.
        :type local_dir: str
        :param artifact_path: Directory within the run's artifact directory in which to log the artifacts.
        :type artifact_path: str
        """
        dest_path = self._normalize_slashes(self._build_dest_path(local_dir, artifact_path))
        local_dir = self._normalize_slash_end(local_dir)
        dest_path = self._normalize_slash_end(dest_path)

        self.run_artifacts.upload_dir(local_dir,
                                      self._run_id,
                                      lambda fpath: dest_path + fpath[len(local_dir):])

    def list_artifacts(self, path):
        """
        Return all the artifacts for this run_uuid directly under path.

        If path is a file, returns an empty list. Will error if path is neither a
        file nor directory. Note that list_artifacts will not return valid
        artifact sizes from Azure.

        :param path: Relative source path that contain desired artifacts
        :type path: str
        :return: List of artifacts as FileInfo listed directly under path.
        """
        # get and filter by paths
        artifacts = []
        for file_path in self.run_artifacts.get_file_paths(self._run_id):
            if path is None or file_path[:len(path)] == path:
                artifacts.append(file_path)

        # create fileinfos
        fileInfos = []
        for artifact in artifacts:
            fileInfos.append(FileInfo(
                path=artifact,
                is_dir=False,
                file_size=-1  # TODO: artifact size retrieval is not supported in Azure
            ))

        return fileInfos

    def download_artifacts(self, artifact_path):
        """
        Download an artifact file or directory to a local directory if applicable.

        Returns a local path for it. The caller is responsible for managing the
        lifecycle of the downloaded artifacts. Downloaded artifacts are stored
        relative to the returned path with the same relative path they are
        requested from the artifact repository.

        :param artifact_path: Relative source path to the desired artifact.
        :type artifact_path: str
        :return: Full path to the directory which contains the path to the desired artifact.
        """
        artifact_path = artifact_path

        # list all artifacts which have artifact_path as prefix
        artifacts = []
        for file in self.run_artifacts.get_file_paths(self._run_id):
            if file[:len(artifact_path)] == artifact_path:
                artifacts.append(file)

        for artifact in artifacts:
            self._download_file(artifact, artifact)

        if os.path.isfile(artifact_path):
            return os.path.abspath(os.path.dirname(artifact_path))

        return os.path.abspath(artifact_path)

    def _download_file(self, remote_file_path, local_path):
        """
        Download the file at the specified relative remote path and save it at the specified local path.

        :param remote_file_path: Source path to the remote file, relative to the
        root directory of the artifact repository.
        :type remote_file_path: str
        :param local_path: The path to which to save the downloaded file.
        :type local_path: str
        """
        self.run_artifacts.download_artifact(self._run_id, remote_file_path, local_path)

    @staticmethod
    def _build_dest_path(local_path, artifact_path):
        return artifact_path if artifact_path else os.path.basename(local_path)

    @staticmethod
    def _normalize_slashes(path):
        return "/".join(path.split("\\"))

    @staticmethod
    def _normalize_slash_end(path):
        return path if path[-1] == "/" else path + "/"
