# backend/services/product_service.py

from . import llm_service

def generate_all_content(product_data):
    return {
        "product_description": llm_service.generate_product_description(product_data),
        "seo": llm_service.generate_seo_elements(product_data),
        "marketing_copy": {
            "email": llm_service.generate_marketing_copy(product_data, platform="email"),
            "instagram": llm_service.generate_marketing_copy(product_data, platform="instagram"),
            "facebook": llm_service.generate_marketing_copy(product_data, platform="facebook")
        },
        "missing_fields": llm_service.generate_missing_fields(product_data),
        "image_description": llm_service.generate_image_description(product_data),
        "dalle_prompt": llm_service.generate_dalle_prompt(product_data)
    }


def generate_single_content(product_data, content_type, platform=None):
    content_generators = {
        "product_description": lambda: llm_service.generate_product_description(product_data),
        "seo": lambda: llm_service.generate_seo_elements(product_data),
        "marketing": lambda: llm_service.generate_marketing_copy(product_data, platform),
        "missing_fields": lambda: llm_service.generate_missing_fields(product_data),
        "image_description": lambda: llm_service.generate_image_description(product_data),
        "dalle_prompt": lambda: llm_service.generate_dalle_prompt(product_data)
    }
    
    generator = content_generators.get(content_type)
    return generator() if generator else "Invalid content type."
# def generate_single_content(product_data, content_type, platform=None):
#     if content_type == "product_description":
#         return llm_service.generate_product_description(product_data)
#     elif content_type == "seo":
#         return llm_service.generate_seo_elements(product_data)
#     elif content_type == "marketing":
#         return llm_service.generate_marketing_copy(product_data, platform)
#     elif content_type == "missing_fields":
#         return llm_service.generate_missing_fields(product_data)
#     elif content_type == "image_description":
#         return llm_service.generate_image_description(product_data)
#     elif content_type == "dalle_prompt":
#         return llm_service.generate_dalle_prompt(product_data)
#     else:
#         return "Invalid content type."