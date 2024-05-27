from typing import List, Literal
from pydantic import BaseModel, Field

class IngredientModel(BaseModel):
    name: str = Field(
        alias='ingredient',
        description='요리에 사용될 재료의 이름을 입력해주세요!',
        min_length=1,
    )

class InputModel(BaseModel):
    ingredients: List[IngredientModel] = Field(
        alias='Ingredients',
        description='사용할 재료 목록',
    )

    llm_type: Literal['chatgpt', 'huggingface'] = Field(
        alias='Large Language Model Type',
        description='사용할 LLM 종류',
        default='chatgpt',
    )

class OutputModel(BaseModel):
    dish: str = Field(
        description='완성된 요리의 이름',
    )
    recipe: str = Field(
        description='요리 레시피',
    )
