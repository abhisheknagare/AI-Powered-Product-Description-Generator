// frontend/src/components/ContentType.js
import React from 'react';

const ContentType = ({ selectedType, setSelectedType, platform, setPlatform }) => {
  const contentTypes = [
    { value: "all", label: "All Content" },
    { value: "product_description", label: "Product Description" },
    { value: "seo", label: "SEO Title & Description" },
    { value: "marketing", label: "Marketing Copy" },
    { value: "image_description", label: "Image Description" },
    { value: "dalle_prompt", label: "DALL·E Prompt" },
    { value: "missing_fields", label: "Fill Missing Fields" }
  ];

  const platforms = [
    { value: "email", label: "Email" },
    { value: "instagram", label: "Instagram" },
    { value: "facebook", label: "Facebook" }
  ];

  const handleTypeChange = (e) => setSelectedType(e.target.value);
  const handlePlatformChange = (e) => setPlatform(e.target.value);

  return (
    <div className="space-y-2 mt-4">
      <label className="block font-semibold">What do you want to generate?</label>
      <select
        className="w-full border px-2 py-1 rounded"
        value={selectedType}
        onChange={handleTypeChange}
      >
        {contentTypes.map(({ value, label }) => (
          <option key={value} value={value}>{label}</option>
        ))}
      </select>

      {selectedType === 'marketing' && (
        <>
          <label className="block font-semibold">Choose Platform</label>
          <select
            className="w-full border px-2 py-1 rounded"
            value={platform}
            onChange={handlePlatformChange}
          >
            {platforms.map(({ value, label }) => (
              <option key={value} value={value}>{label}</option>
            ))}
          </select>
        </>
      )}
    </div>
  );
};

export default ContentType;