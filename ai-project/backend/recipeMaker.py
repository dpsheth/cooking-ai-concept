from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Endpoint to generate a recipe based on ingredients and dietary preferences
@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    data = request.json
    ingredients = data.get("ingredients", "")
    dietary_preferences = data.get("preferences", "")

    if not ingredients:
        return jsonify({"error": "Ingredients are required"}), 400

    # Generate the recipe using the Gemini model
    if dietary_preferences:
        prompt = f"Ingredients:\n{ingredients}\n\nDietary Preferences:\n{dietary_preferences}\n\nRecipe:"
    else:
        prompt = f"Ingredients:\n{ingredients}\n\nRecipe:"

    try:
        result = model.generate_content(prompt)
        answer = result.text.strip()

        # Clean up and enforce line breaks
        formatted_answer = (
            answer.replace("##", "\n##")  # Ensure headers start on new lines
            .replace(" 1.", "\n1.")       # Ensure numbered lists start on new lines
            .replace("\n\n", "\n")        # Remove excessive blank lines
            .strip()
        )
        formatted_answer = '\n'.join([line.strip() for line in formatted_answer.splitlines() if line.strip()])

        return jsonify({"recipe": formatted_answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to modify the recipe based on a suggestion
@app.route('/modify_recipe', methods=['POST'])
def modify_recipe():
    data = request.json

    # Log incoming data to check what is received
    print("Received data:", data)

    recipe = data.get("recipe")
    suggestion = data.get("suggestion")

    if not recipe or not suggestion:
        print(f"Missing data - recipe: {recipe}, suggestion: {suggestion}")
        return jsonify({"error": "Both recipe and suggestion are required"}), 400

    # Construct the prompt for modifying the recipe
    prompt = (
        f"Original Recipe:\n{recipe}\n\n"
        f"Suggested Modification: {suggestion}\n\n"
        f"Modify the recipe by incorporating the suggested changes. Provide the updated recipe:"
    )

    try:
        result = model.generate_content(prompt)
        modified_recipe = result.text.strip()

        # Clean up and format the modified recipe
        formatted_recipe = (
            modified_recipe.replace("##", "\n##")  # Ensure headers start on new lines
            .replace(" 1.", "\n1.")               # Ensure numbered lists start on new lines
            .replace("\n\n", "\n")                 # Remove excessive blank lines
            .strip()
        )

        return jsonify({"modifiedRecipe": formatted_recipe})

    except Exception as e:
        print(f"Error during recipe modification: {str(e)}")
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
