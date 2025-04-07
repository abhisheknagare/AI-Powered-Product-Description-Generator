// frontend/src/components/ProductForm.js
import React, { useState, useCallback } from "react";
import { generateDescription, generateSEO, generateMarketing, generateImagePrompt } from "../services/api";

const ProductForm = () => {
  const [product, setProduct] = useState({
    name: "",
    basic_description: "",
    features: [],
    materials: [],
    brand: "",
    price: ""
  });

  const [tone, setTone] = useState("friendly");
  const [length, setLength] = useState("medium");
  const [style, setStyle] = useState("casual");

  const [generatedContent, setGeneratedContent] = useState({
    description: "",
    seo: "",
    marketing: "",
    imagePrompt: ""
  });

  const { description, seo, marketing, imagePrompt } = generatedContent;

  const handleChange = useCallback((e) => {
    const { name, value } = e.target;
    setProduct(prevProduct => ({ ...prevProduct, [name]: value }));
  }, []);

  const handleGenerate = useCallback(async () => {
    try {
      // Use Promise.all to run API calls in parallel
      const [desc, seoResult, marketingResult, imgPrompt] = await Promise.all([
        generateDescription(product, tone, length, style),
        generateSEO(product, tone, length, style),
        generateMarketing(product, "email", tone, length, style),
        generateImagePrompt(product)
      ]);

      setGeneratedContent({
        description: desc,
        seo: seoResult,
        marketing: marketingResult,
        imagePrompt: imgPrompt
      });
    } catch (error) {
      console.error("Error generating content:", error);
    }
  }, [product, tone, length, style]);

  const inputFields = [
    { name: "name", placeholder: "Product Name" },
    { name: "basic_description", placeholder: "Basic Description" },
    { name: "brand", placeholder: "Brand" },
    { name: "price", placeholder: "Price" }
  ];

  const resultSections = [
    { title: "Description", content: description, type: "text" },
    { title: "SEO", content: seo, type: "json" },
    { title: "Marketing", content: marketing, type: "text" },
    { title: "Image Prompt", content: imagePrompt, type: "text" }
  ];

  return (
    <div className="p-4 space-y-4 max-w-xl mx-auto">
      {inputFields.map(field => (
        <input
          key={field.name}
          className="border p-2 w-full"
          name={field.name}
          placeholder={field.placeholder}
          onChange={handleChange}
        />
      ))}

      <button className="bg-blue-600 text-white p-2 rounded" onClick={handleGenerate}>
        Generate Content
      </button>

      {resultSections.map(section => (
        section.content && (
          <div key={section.title}>
            <h2 className="font-bold">{section.title}:</h2>
            {section.type === "json" ? (
              <pre>{JSON.stringify(section.content, null, 2)}</pre>
            ) : (
              <p>{section.content}</p>
            )}
          </div>
        )
      ))}
    </div>
  );
};

export default ProductForm;