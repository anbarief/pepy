import pytest

from pepy.domain.model import Project
from pepy.infrastructure import container
from pepy.infrastructure.db_repository import DBProjectRepository
from tests.tools.stub import ProjectStub, ProjectDownloadsStub


@pytest.fixture()
def project_repository():
    conn = container.db_connection
    with conn.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE projects CASCADE")
    yield DBProjectRepository(conn)


def test_find_project(project_repository: DBProjectRepository):
    project = ProjectStub.create()
    project_repository.save_projects([project])
    result = project_repository.find(project.name)
    assert isinstance(result, Project)
    assert project.name.name == result.name.name
    assert project.downloads.value == result.downloads.value


def test_update_downloads(project_repository: DBProjectRepository):
    project = ProjectStub.create()
    project_repository.save_projects([project])
    project_downloads = ProjectDownloadsStub.create(name=project.name)
    project_repository.update_downloads([project_downloads])
    result = project_repository.find(project.name)
    assert project_downloads.downloads.value + project.downloads.value == result.downloads.value


def test_retrieve_last_downloads(project_repository: DBProjectRepository):
    project = ProjectStub.create()
    project_repository.save_projects([project])
    project_downloads = ProjectDownloadsStub.create_consecutive(project.name)
    project_repository.save_day_downloads(project_downloads)
    assert project_downloads == project_repository.last_downloads(project.name)
