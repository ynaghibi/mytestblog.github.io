

import os
from bs4 import BeautifulSoup

def process_xhtml_file():
    # Define input and output filenames
    input_file = 'Part2.xhtml'
    output_file = 'index.html'
    
    # Custom CSS content to append
    custom_css = """
:root {
    --bg-color: #121212;
    --text-color: #e0e0e0;
    --accent-color: #bb86fc;
    --border-color: #333;
    --code-bg: #1e1e1e;
    --item-bullet: #bb86fc;
    --math-color: #f5f5f5;
    --link-color: #82b1ff;
    --link-hover: #bb86fc;
}

body {
    background-color: var(--bg-color);
    color: var(--text-color);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    padding: 20px;
    max-width: 900px;
    margin: 0 auto;
}

math {
    color: var(--math-color);
    margin: 15px 0;
    padding: 10px;
    background-color: #1e1e1e;
    border-radius: 4px;
}

div.lyx_code {
    font-family: 'Consolas', monospace;
    background-color: #252525;
    border-left: 3px solid #bb86fc;
    padding: 12px;
    border-radius: 3px;
    overflow-x: auto;
}

.lyx_code_item {
    color: #e0e0e0;
}

.toc,
.toc a,
.toc li,
.toc li a {
    color: var(--text-color);
    transition: color 0.2s ease;
}

.toc a:hover,
.toc li a:hover {
    color: var(--link-hover);
    text-decoration: underline;
}

.toc a:visited,
.toc a:active {
    color: var(--link-color);
}
"""

    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: {input_file} not found in the current directory")
            return

        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse with BeautifulSoup
        soup = BeautifulSoup(content, 'lxml')

        # Find the style tag and append custom CSS
        style_tag = soup.find('style')
        if style_tag:
            # Append the custom CSS to the existing style tag
            style_tag.append(custom_css)
        else:
            print("Warning: No <style> tag found in the document")
            new_style = soup.new_tag('style')
            new_style.string = custom_css
            soup.head.append(new_style)

        # Remove empty math tags and their parent divs if needed
        for math_tag in soup.find_all('math'):
            if not math_tag.contents or not math_tag.get_text(strip=True):
                parent = math_tag.parent
                if parent.name == 'div' and len(parent.contents) == 1:
                    parent.decompose()
                else:
                    math_tag.decompose()

        # Save to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        print(f"Successfully processed file. Output saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please check your input file format and try again.")

if __name__ == '__main__':
    process_xhtml_file()