import json
import os
import re
from datetime import datetime

def clean_html(raw_html):
    # Remove script and style elements
    cleanr = re.compile('<script.*?</script>', re.DOTALL)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile('<style.*?</style>', re.DOTALL)
    raw_html = re.sub(cleanr, '', raw_html)
    
    # Replace <p> with newlines
    raw_html = raw_html.replace('</p>', '\n\n')
    raw_html = raw_html.replace('<br>', '\n')
    
    # Simple regex to remove other tags (keep it simple as "text is fine")
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    
    # Decode HTML entities
    cleantext = cleantext.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    
    return cleantext.strip()

with open('note_api_data_page2.json', 'r') as f:
    data = json.load(f)

contents = data.get('data', {}).get('contents', [])

if not os.path.exists('articles'):
    os.makedirs('articles')

for note in contents:
    title = note.get('name', 'No Title')
    pub_date_str = note.get('publishAt', '')
    body_html = note.get('body', '')
    link = note.get('noteUrl', '')
    
    # Parse date
    try:
        pub_date = datetime.strptime(pub_date_str, "%Y-%m-%dT%H:%M:%S%z")
        date_prefix = pub_date.strftime("%Y-%m-%d")
        display_date = pub_date.strftime("%Y年%m月%d日")
    except:
        date_prefix = "0000-00-00"
        display_date = pub_date_str

    # Clean body
    body_text = clean_html(body_html)
    
    # Create file content
    file_content = f"# {title}\n\n"
    file_content += f"公開日: {display_date}\n"
    file_content += f"リンク: {link}\n\n"
    file_content += "---\n\n"
    file_content += body_text
    
    # Safe filename
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    filename = f"articles/{date_prefix}-{safe_title}.md"
    
    with open(filename, 'w') as f:
        f.write(file_content)
    
    print(f"Created: {filename}")
