#with help from chatgpt-4
import json
import requests
import hashlib
import os
import collections
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import tiktoken

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def save_json(filename,data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    return

def load_text(filename):
    return open(filename, 'r', encoding='utf-8').read()

def sitemap_to_urls_list():
    tree = ET.parse('export/sitemap.xml')
    root = tree.getroot()
    en_urls = [url.text for url in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc") if "/en/" in url.text]
    save_json("en_urls.json",en_urls)
    return

def html_to_text(html_content):
    title = ""
    description = ""
    text = ""
    soup = BeautifulSoup(html_content, 'html.parser')
    title_tag = soup.title
    if title_tag:
        title = title_tag.string
        text += "title: "+ title+ "\n"
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    if meta_tag:
        description = meta_tag.get('content')
        text += "description: "+ description +"\n"

    for script in soup(["script", "style","head","header","aside","nav"]):
        script.extract()
    
    soup_text = soup.get_text()
    lines = (line.strip() for line in soup_text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text += '\n'.join(chunk for chunk in chunks if chunk)
    return title,description,text

def export_html():
    urls_map = load_json("export/urls_map.json")
    output_html = "export/html"
    os.makedirs(output_html,exist_ok=True)
    for hashed_name,url in urls_map.items():
        response = requests.get(url)
        html_content = response.text
        html_file = os.path.join(output_html, hashed_name+".html")
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(html_content)

def convert_all_html_to_text():
    urls_map = load_json("export/urls_map.json")

    output_html = "export/html"
    output_text = "export/text"
    os.makedirs(output_text,exist_ok=True)
    files_info = collections.OrderedDict()
    count = 1
    for hashed_name,url in urls_map.items():
        print(f"{hashed_name} : {count} / {len(urls_map)}")
        html_content = ""
        html_file = os.path.join(output_html, hashed_name+".html")
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        text_file = os.path.join(output_text, hashed_name+".txt")
        title,description,text_content = html_to_text(html_content)
        files_info[hashed_name] = {
            "title":title,
            "description":description,
            "url":url,
            "path":url.split("en/")[1][:-1]
            }
        with open(text_file, 'w', encoding='utf-8') as file:
            file.write(text_content)
        count += 1

    save_json('export/files_info.json',files_info)
    return

def files_list_to_map():
    with open('export/en_urls.json', 'r') as file:
        url_list = json.load(file)
    files_map = collections.OrderedDict()
    for url in url_list:
        hashed_name = hashlib.md5(url.encode()).hexdigest()[:10]
        files_map[hashed_name] = url
    save_json('export/files_info.json',files_map)

def chunk_text(encoding,text, max_tokens = 7800):
    words = text.split()
    chunks = []
    chunk = []
    tokens_in_chunk = 0

    for word in words:
        word_tokens = len(encoding.encode(word))
        if tokens_in_chunk + word_tokens <= max_tokens:
            chunk.append(word)
            tokens_in_chunk += word_tokens
        else:
            chunks.append(' '.join(chunk))
            chunk = [word]
            tokens_in_chunk = word_tokens

    if chunk:
        chunks.append(' '.join(chunk))

    return chunks

def chunk_text_overlap(encoding, text, max_tokens=1000, overlap=200):
    words = text.split()
    chunks = []
    chunk = []
    tokens_in_chunk = 0
    current_word_index = 0

    while current_word_index < len(words):
        word = words[current_word_index]
        word_tokens = len(encoding.encode(word))
        if tokens_in_chunk + word_tokens <= max_tokens:
            chunk.append(word)
            tokens_in_chunk += word_tokens
            current_word_index += 1
        else:
            chunks.append(' '.join(chunk))

            # Handle overlap
            backtrack_tokens = 0
            while backtrack_tokens < overlap and len(chunk) > 0:
                last_word = chunk.pop()
                last_word_tokens = len(encoding.encode(last_word))
                tokens_in_chunk -= last_word_tokens
                backtrack_tokens += last_word_tokens
                current_word_index -= 1

            chunk = []
            tokens_in_chunk = 0

    if chunk:
        chunks.append(' '.join(chunk))

    return chunks

def convert_all_text_to_chunks():
    encoding = tiktoken.encoding_for_model("text-embedding-ada-002")

    files_info = load_json('export/files_info.json')
    chunks_infos = []
    chunks_only = []
    total_tokens = 0
    chunk_count = 0
    page_count = 1
    for hashed_name,file_info in files_info.items():
        text = load_text(os.path.join("export/text",hashed_name+".txt"))
        #default to 1000/200 to test with 300/50
        chunks = chunk_text_overlap(encoding,text)
        for index,chunk in enumerate(chunks):
            chunk_id = hashed_name +"-"+str(index)
            nb_tokens = len(encoding.encode(chunk))
            total_tokens += nb_tokens
            chunks_infos.append({
                "chunk_id":chunk_count,
                "chunk_uid":chunk_id,
                "file_hash":hashed_name,
                "file_path":file_info["path"],
                "nb_tokens": nb_tokens,
                "content":chunk
                })
            chunks_only.append(chunk)
            chunk_count +=1
            print(f" * chunk {chunk_count+1} from file {page_count}/{len(files_info)} {chunk_id} : {nb_tokens} tokens")
        page_count +=1
    print(f" => {len(chunks_infos)} chunks : total {total_tokens} tokens - (Ada v2 $0.0001 / 1K tokens)")
    save_json("export/chunks_infos.json",chunks_infos)
    save_json("export/chunks.json",chunks_only)
    return

if __name__ == "__main__":
    sitemap_to_urls_list()
    files_list_to_map()
    export_html()
    convert_all_html_to_text()
    convert_all_text_to_chunks()
