import openai
import os
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ghibli_image(prompt, image_url):
    try:
        ghibli_prompt = (
            f"{prompt}, create this scene in a natural, hand-drawn style inspired by Studio Ghibli. "
            "The image should evoke the warmth and organic feeling of hand-drawn art, with soft colors, gentle shading, "
            "and vibrant, whimsical details. Focus on creating an authentic, hand-crafted atmosphere, where the brushstrokes "
            "feel intentional and the scene feels alive with a natural flow. The characters should have exaggerated features but "
            "should not be overdrawn or overly stylized. Ensure the world around them feels grounded and magical in a realistic way."
        )

        response = client.images.generate(
            model="dall-e-3",
            prompt=ghibli_prompt,
            n=1, 
            size="1024x1024"
        )

        image_url = response.data[0].url
        return image_url
    
    except Exception as e:
        raise RuntimeError(f"Error generating Ghibli style image: {e}")

def extract_image_info(image_url):
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Describe the details and key points of this image. What emotions, objects, and themes are present in the image?",
                        },
                        {
                            "type": "input_image",
                            "image_url": image_url,
                        },
                    ],
                }
            ],
        )
        return response.output_text
    
    except Exception as e:
        raise RuntimeError(f"Error extracting image info: {e}")

