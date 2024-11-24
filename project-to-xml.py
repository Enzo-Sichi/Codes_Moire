import os

def create_xml_from_project(project_path):
    """Convert a project directory into the required XML format."""
    xml_parts = ['<documents>']
    index = 1
    
    for root, _, files in os.walk(project_path):
        for file in files:
            # Skip common files/directories you might want to exclude
            if any(skip in file for skip in ['.git', '__pycache__', '.pyc', '.env']):
                continue
                
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Create relative path from project root
                relative_path = os.path.relpath(file_path, project_path)
                
                xml_parts.append(f'<document index="{index}">')
                xml_parts.append(f'<source>{relative_path}</source>')
                xml_parts.append('<document_content>')
                xml_parts.append(content)
                xml_parts.append('</document_content>')
                xml_parts.append('</document>')
                
                index += 1
            except UnicodeDecodeError:
                print(f"Skipping binary file: {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    xml_parts.append('</documents>')
    return '\n'.join(xml_parts)

# Usage
if __name__ == "__main__":
    # project_path = input("Enter the path to your project directory: ")
    project_path = "C:/Users/enzo/Documents/01_Enzo/04_Moire/Codes_Moire/Moire_streamlit_app"
    output_path = "project_dump.xml"
    
    xml_content = create_xml_from_project(project_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
        
    print(f"XML dump created at: {output_path}")

