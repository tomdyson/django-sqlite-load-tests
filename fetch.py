# fetch.py
import requests
import sys

def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename

def main():
    if len(sys.argv) != 2:
        print('Usage: python fetch.py <url>')
        sys.exit(1)
    
    url = sys.argv[1]
    download_file(url)

if __name__ == "__main__":
    main()
