from fastapi import APIRouter

from app.core.errors import AppError  #provides a custom exception class for handling application-specific errors

from app.schemas.task_example import (
    TaskExampleRequest,
    TaskExampleResponse,
)                                          #provides Pydantic models for validating and serializing the request and response data for the TaskFlow task example endpoint


router = APIRouter(
    prefix="/examples",
    tags=["Learning Examples"],
)


@router.get("/projects/{project_id}")
async def get_example_project(project_id: int):

    example_projects = {
        1: "TaskFlow Development",
        2: "AWS Deployment",
        3: "Docker Learning",
    }

    if project_id not in example_projects:
        raise AppError(
            status_code=404,
            code="PROJECT_NOT_FOUND",
            message="Project not found",
        )

    return {
        "id": project_id,
        "name": example_projects[project_id],
    }

@router.post(
    "/validate-task",
    response_model=TaskExampleResponse,
)
async def validate_task(
    task: TaskExampleRequest,
):
    return TaskExampleResponse(
        status="validated",
        task=task,
    )