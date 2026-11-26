from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)                                #simply used to validate the data for the TaskFlow task example request and response models


class TaskExampleRequest(BaseModel):    #simply used to validate the data for the TaskFlow task example request model
    """Validate a proposed TaskFlow task."""

    model_config = ConfigDict(
        extra="forbid",
    )                                 #used to configure the Pydantic model to forbid any extra fields that are not defined in the model

    title: str = Field(
        min_length=3,
        max_length=100,
    )                                 #used to define the title field for the TaskFlow task example request model, with a minimum length of 3 characters and a maximum length of 100 characters

    description: str | None = Field(
        default=None,
        max_length=500,
    )                                 #used to define the description field for the TaskFlow task example request model, which is optional and has a maximum length of 500 characters

    priority: int = Field(
        default=3,
        ge=1,
        le=5,
        strict=True,
    )                                #used to define the priority field for the TaskFlow task example request model, with a default value of 3, a minimum value of 1, a maximum value of 5, and strict type checking enabled

    @field_validator("title")          #used to define a custom validator for the title field, which strips any leading or trailing whitespace and raises a ValueError if the title is less than 3 characters long
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 3:
            raise ValueError(
                "Title must contain at least 3 characters"
            )

        return value


class TaskExampleResponse(BaseModel):
    status: str
    task: TaskExampleRequest
