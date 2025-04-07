// frontend/src/components/GeneratedContent.js
import React, { useMemo } from 'react';

const GeneratedContent = ({ content }) => {
  const formattedContent = useMemo(() => {
    return content ? JSON.stringify(content, null, 2) : '';
  }, [content]);

  if (!content) return null;

  return (
    <div className="mt-6 p-4 border rounded shadow-sm">
      <h2 className="text-lg font-semibold">Generated Content</h2>
      <pre className="whitespace-pre-wrap">{formattedContent}</pre>
    </div>
  );
};

export default GeneratedContent;