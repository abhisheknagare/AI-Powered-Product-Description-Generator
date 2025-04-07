# backend/services/llm_service.py

import os
from typing import Dict, List, Any, Optional
from fastapi import HTTPException
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-3.5-turbo"  # or "gpt-4" if available

def call_openai(prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
    """
    Make a request to the OpenAI API with error handling
    """
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant for product content generation."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error calling OpenAI API: {str(e)}")


# ----------- Prompt Generators ------------ #

def generate_product_description(product: Dict[str, Any], tone: str = "professional", 
                                length: str = "medium", style: str = "informative") -> str:
    """
    Generate a compelling, SEO-optimized product description based on product attributes
    """
    name = product.get("name", "Unnamed Product")
    desc = product.get("basic_description", "")
    features = product.get("features", [])
    materials = product.get("materials", [])
    brand = product.get("brand", "")
    price = product.get("price", "")
    category = product.get("category", "")
    subcategory = product.get("subcategory", "")
    tags = product.get("tags", [])

    prompt = f"""
You are an expert eCommerce copywriter specializing in creating compelling product descriptions.
Create a detailed, SEO-optimized product description for the following product:

Product Name: {name}
Brand: {brand}
Category: {category}
Subcategory: {subcategory}
Basic Description: {desc}
Features: {", ".join(features)}
Materials: {", ".join(materials)}
Price: ${price}
Tags: {", ".join(tags)}

Requirements:
- Tone: {tone} (maintain the brand's voice)
- Length: {length} (short: 50-100 words, medium: 100-200 words, long: 200-300 words)
- Style: {style}
- Highlight key benefits and unique selling points
- Include SEO-friendly keywords naturally
- Format with appropriate paragraphs and bullet points for readability
- Make the description compelling and conversion-focused

Respond with only the product description text.
"""

    return call_openai(prompt, temperature=0.7, max_tokens=350)


def generate_seo_elements(product: Dict[str, Any], tone: str = "professional", 
                         length: str = "standard", style: str = "persuasive") -> Dict[str, str]:
    """
    Generate SEO-optimized title and meta description for a product
    """
    name = product.get("name", "")
    desc = product.get("basic_description", "")
    brand = product.get("brand", "")
    category = product.get("category", "")
    features = product.get("features", [])
    tags = product.get("tags", [])

    prompt = f"""
You are an SEO expert for eCommerce websites. Generate optimized title and meta description for:

Product Name: {name}
Brand: {brand}
Category: {category}
Basic Description: {desc}
Key Features: {", ".join(features[:3] if len(features) > 3 else features)}
Tags: {", ".join(tags)}

Requirements:
- Tone: {tone}
- Style: {style}
- Title must be under 60 characters and include the product name and brand
- Meta description must be under 160 characters
- Include primary keywords naturally
- Make them compelling and click-worthy in search results
- Focus on benefits and value proposition

Respond in this format:
Title: ...
Meta Description: ...
"""
    response = call_openai(prompt, temperature=0.6, max_tokens=200)
    
    # Parse the response into a dictionary
    lines = response.split('\n')
    seo_elements = {}
    for line in lines:
        if line.startswith('Title:'):
            seo_elements['title'] = line.replace('Title:', '').strip()
        elif line.startswith('Meta Description:'):
            seo_elements['description'] = line.replace('Meta Description:', '').strip()
    
    return seo_elements


def generate_marketing_copy(product: Dict[str, Any], platform: str = "email", 
                           tone: str = "engaging", length: str = "medium", 
                           style: str = "persuasive") -> str:
    """
    Generate platform-specific marketing copy for a product
    """
    name = product.get("name", "")
    desc = product.get("basic_description", "")
    features = product.get("features", [])
    brand = product.get("brand", "")
    price = product.get("price", "")
    category = product.get("category", "")
    tags = product.get("tags", [])

    platform_prompt = {
        "email": """
Write a marketing email introducing this product. 
Include:
- Attention-grabbing subject line
- Compelling opening paragraph
- Features and benefits section
- Clear call-to-action
- Professional closing
""",
        "instagram": """
Write an Instagram caption to promote this product.
Include:
- Attention-grabbing opening line
- Benefits-focused copy
- Call-to-action
- 5-8 relevant hashtags
- Limit to 150-200 words
""",
        "facebook": """
Write a Facebook post promoting this product.
Include:
- Engaging opening that addresses the audience directly
- Value proposition and key benefits
- Social proof element (how others enjoy/benefit from it)
- Clear call-to-action
- Keep it conversational and friendly
"""
    }

    prompt = f"""
You are a marketing specialist for eCommerce brands. Write promotional content for:

Product Name: {name}
Brand: {brand}
Category: {category}
Description: {desc}
Features: {", ".join(features)}
Price: ${price}
Tags: {", ".join(tags)}

{platform_prompt.get(platform, "Write marketing copy for this product.")}

Requirements:
- Tone: {tone}
- Length: {length} (short: 50-100 words, medium: 100-200 words, long: 200-300 words)
- Style: {style}
- Focus on benefits rather than features
- Include a compelling call-to-action
- Match the writing style to the {platform} platform and audience expectations

Only respond with the {platform} marketing copy.
"""
    return call_openai(prompt, temperature=0.8, max_tokens=400)


def generate_missing_fields(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate missing product fields based on available information
    """
    prompt = f"""
You are an eCommerce product data specialist. Based on the available product information,
generate logical values for missing fields:

Product Name: {product.get('name', '')}
Brand: {product.get('brand', '')}
Price: {product.get('price', '')}
Basic Description: {product.get('basic_description', '')}
Current Category: {product.get('category', '[MISSING]')}
Current Subcategory: {product.get('subcategory', '[MISSING]')}
Current Features: {', '.join(product.get('features', ['[MISSING]']))}
Current Materials: {', '.join(product.get('materials', ['[MISSING]']))}
Current Colors: {', '.join(product.get('colors', ['[MISSING]']))}
Current Tags: {', '.join(product.get('tags', ['[MISSING]']))}

For each missing field marked [MISSING], provide logical values based on the available information.
Return in this JSON-compatible format:
Category: [single category]
Subcategory: [single subcategory]
Features: [list of 3-5 key features, comma-separated]
Materials: [list of materials, comma-separated]
Colors: [list of available colors, comma-separated]
Tags: [list of 5-8 relevant search tags, comma-separated]

Only include fields that are missing in the original data.
"""
    response = call_openai(prompt, temperature=0.6, max_tokens=300)
    
    # Parse the response into a dictionary
    result = {}
    lines = response.strip().split('\n')
    
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Convert list fields to actual lists
            if key in ['Features', 'Materials', 'Colors', 'Tags']:
                values = [item.strip() for item in value.split(',')]
                # Remove brackets if present
                if values and values[0].startswith('['):
                    values[0] = values[0][1:]
                if values and values[-1].endswith(']'):
                    values[-1] = values[-1][:-1]
                result[key.lower()] = values
            else:
                # Remove brackets if present
                if value.startswith('[') and value.endswith(']'):
                    value = value[1:-1]
                result[key.lower()] = value
    
    return result


def generate_dalle_prompt(product: Dict[str, Any]) -> str:
    """
    Generate a detailed prompt for DALL-E image generation based on product attributes
    """
    name = product.get("name", "")
    desc = product.get("basic_description", "")
    category = product.get("category", "")
    subcategory = product.get("subcategory", "")
    colors = product.get("colors", [])
    materials = product.get("materials", [])
    features = product.get("features", [])
    brand = product.get("brand", "")

    prompt = f"""
You are a product photographer and image generation expert. Create a detailed DALL-E prompt 
to generate a high-quality, professional product image for:

Product: {name}
Brand: {brand}
Category: {category}
Subcategory: {subcategory}
Basic Description: {desc}
Materials: {", ".join(materials)}
Colors: {", ".join(colors)}
Key Features: {", ".join(features)}

Your DALL-E prompt should:
1. Describe the product with vivid, specific visual details
2. Specify the style (professional product photography)
3. Include lighting details (soft, natural lighting)
4. Describe the background (minimal, contextually appropriate)
5. Include angle and perspective
6. Mention high resolution and photorealistic quality
7. Be under 200 characters for optimal DALL-E processing

Respond with ONLY the DALL-E prompt text (no explanations).
"""
    return call_openai(prompt, temperature=0.7, max_tokens=200)