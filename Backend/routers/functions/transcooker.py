import os
import json
from fastapi import APIRouter, FastAPI
from models.transcooker import InputModel, OutputModel
from llm.chat import build
from llm.store import LLMStore

# Configure API router
router = APIRouter(
    tags=['functions'],
)

# Configure metadata
NAME = os.path.basename(__file__)[:-3]

# Configure resources
store = LLMStore()

###############################################
#                   Actions                   #
###############################################

@router.post(f'/func/{NAME}', response_model=OutputModel)
async def call_recipe_generator(model: InputModel) -> OutputModel:
    # Create a LLM chain
    chain = build(
        name=NAME,
        llm=store.get(model.llm_type),
    )

    ingredients_list = ", ".join([ingredient.name for ingredient in model.ingredients])
    input_context = f'''
        # Recipe Ingredients
        * Ingredients: {ingredients_list}
    '''

    llm_response = chain.invoke({'input_context': input_context})

    # Log llm_response for debugging
    print(f"LLM Response: {llm_response}")

    # Assuming the response is plain text
    dish, recipe = parse_llm_response(llm_response)

    return OutputModel(
        dish=dish,
        recipe=recipe
    )

def parse_llm_response(response: str) -> (str, str):
    # Check if the response contains a detailed recipe
    if "요리 이름" in response:
        # Extract dish and recipe from the response
        dish_start_index = response.find("요리 이름") + len("요리 이름")
        dish_end_index = response.find("\n", dish_start_index)
        dish = response[dish_start_index:dish_end_index].strip()

        recipe_start_index = response.find("조리 순서") + len("조리 순서")
        recipe = response[recipe_start_index:].strip()

        return dish, recipe
    else:
        # Return default values
        return "Unknown Dish", "Recipe not available"



# Initialize FastAPI app
app = FastAPI()

# Include the router
app.include_router(router)

# Run the FastAPI app with Uvicorn if this script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
