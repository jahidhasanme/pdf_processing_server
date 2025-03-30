import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ghibli_image(prompt, image_url):
    try:
        ghibli_prompt = (
            f"{extract_image_info(image_url)}, {prompt} recreate this scene in Studio Ghibli's signature animation style, incorporating these essential elements: "
            "1. Soft, diffused lighting with gentle highlights and deep, natural shadows to enhance depth and mood. "
            "2. A rich, vibrant color palette with a painterly, watercolor-like softness that brings warmth and harmony. "
            "3. Highly detailed, immersive backgrounds layered with atmospheric perspective to create a deep, living world. "
            "4. Subtle, organic textures that mimic the feel of hand-painted animation cels, adding warmth and charm. "
            "5. Expressive yet elegantly simple character designs, with clean, fluid lines that convey emotion and personality. "
            "6. A balance of realism and fantasy, capturing nature’s beauty through elements like swaying grass, drifting clouds, and dappled sunlight. "
            "The final image should embody Studio Ghibli’s signature sense of wonder, storytelling, and attention to natural details, "
            "bringing the scene to life with grace and movement."
        )

        response = client.images.generate(
            model="dall-e-3",
            prompt=ghibli_prompt,
            n=1,
            size="1024x1024",
        )

        image_url = response.data[0].url
        return image_url

    except Exception as e:
        raise RuntimeError(f"Error generating Ghibli style image: {e}")


def extract_image_info(image_url):
    try:
        print(f"Extracting image info from URL: {image_url}")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze this image and describe its key visual elements, focusing on a human figure as the main subject. Include:

Main subjects and their positions, with emphasis on the human figure as the focal point.

Color palette and lighting conditions, noting how they enhance the scene’s mood.

Environmental elements and setting, capturing the atmosphere.

Mood and atmosphere, considering how the composition evokes emotions.

Notable textures and patterns, especially those that contribute to a Studio Ghibli-style recreation.

Depth and perspective, describing how the elements create a sense of space and realism.

Be specific but concise, emphasizing details that would be crucial for a Studio Ghibli-style interpretation.""",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                    ],
                }
            ],
        )

        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"Error extracting image info: {e}")
