    // frontend/src/App.js
    
    import React, { useState } from 'react';
    import './styles/App.css';
    import ProductForm from './components/ProductForm';
    import ContentType from './components/ContentType';
    import StyleOptions from './components/StyleOptions';
    import GeneratedContent from './components/GeneratedContent';
    import { generateAllContent, generateSingleContent } from './services/api';

    function App() {
    const [generatedContent, setGeneratedContent] = useState(null);
    const [selectedType, setSelectedType] = useState("all");
    const [platform, setPlatform] = useState("email");

    const [tone, setTone] = useState("default");
    const [length, setLength] = useState("medium");
    const [style, setStyle] = useState("standard");

    const handleProductSubmit = async (product) => {
        if (selectedType === "all") {
        const result = await generateAllContent(product, tone, length, style);
        setGeneratedContent(result);
        } else {
        const result = await generateSingleContent(product, selectedType, platform, tone, length, style);
        setGeneratedContent({ [selectedType]: result });
        }
    };

    return (
        <div className="max-w-3xl mx-auto p-6 space-y-6">
        <h1 className="text-2xl font-bold">🧠 AI Product Description Generator</h1>
        <ContentType
            selectedType={selectedType}
            setSelectedType={setSelectedType}
            platform={platform}
            setPlatform={setPlatform}
        />
        <StyleOptions tone={tone} setTone={setTone} length={length} setLength={setLength} style={style} setStyle={setStyle} />
        <ProductForm onSubmit={handleProductSubmit} />
        <GeneratedContent content={generatedContent} />
        </div>
    );
    }

    export default App;