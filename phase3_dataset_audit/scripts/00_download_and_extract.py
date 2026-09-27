"""
00_download_and_extract.py
Downloads official DIVE dataset files from Zenodo (DOI: 10.5281/zenodo.18519253)
and extracts them into phase3_dataset_audit/raw/ directory.
"""

import os
import sys
import zipfile
import urllib.request
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "raw")

ZENODO_FILES = [
    ("Feature_list.xlsx", "https://zenodo.org/records/18519253/files/Feature%20list.xlsx?download=1"),
    ("DIVE_Labels.zip", "https://zenodo.org/records/18519253/files/DIVE_Labels.zip?download=1"),
    ("DIVE_Preprocessed_Data.zip", "https://zenodo.org/records/18519253/files/DIVE_Preprocessed_Data.zip?download=1"),
    ("DIVE_Raw_Data.zip", "https://zenodo.org/records/18519253/files/DIVE_Raw_Data.zip?download=1"),
]

def download_file(filename, url, dest_dir):
    dest_path = os.path.join(dest_dir, filename)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
        print(f"[SKIP] {filename} already exists ({os.path.getsize(dest_path) / (1024*1024):.2f} MB).")
        return dest_path

    print(f"[DOWNLOADING] {filename} from {url}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    start_time = time.time()
    
    with urllib.request.urlopen(req) as resp, open(dest_path, "wb") as out_file:
        total_size = int(resp.headers.get("Content-Length", 0))
        downloaded = 0
        chunk_size = 1024 * 1024  # 1 MB chunk
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            out_file.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = downloaded / total_size * 100
                elapsed = time.time() - start_time
                speed = downloaded / (1024 * 1024 * max(elapsed, 0.001))
                sys.stdout.write(f"\r  -> {downloaded / (1024*1024):.1f}/{total_size / (1024*1024):.1f} MB ({percent:.1f}%) @ {speed:.2f} MB/s")
                sys.stdout.flush()
    print(f"\n[DONE] Saved {filename} ({os.path.getsize(dest_path) / (1024*1024):.2f} MB in {time.time() - start_time:.1f}s)")
    return dest_path

def extract_zip(zip_path, extract_to):
    print(f"[EXTRACTING] {os.path.basename(zip_path)} to {extract_to}...")
    with zipfile.ZipFile(zip_path, "r") as z:
        for member in z.infolist():
            # Avoid overwriting or security issues
            target_path = os.path.join(extract_to, member.filename)
            if not os.path.exists(target_path):
                z.extract(member, extract_to)
                print(f"  Extracted: {member.filename} ({member.file_size / (1024*1024):.2f} MB)")
            else:
                print(f"  Already exists: {member.filename}")

def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    for filename, url in ZENODO_FILES:
        saved_path = download_file(filename, url, RAW_DIR)
        if filename.endswith(".zip"):
            extract_zip(saved_path, RAW_DIR)

    print("\nAll downloads and extractions complete. Raw folder contents:")
    for root, dirs, files in os.walk(RAW_DIR):
        for f in files:
            p = os.path.join(root, f)
            print(f" - {os.path.relpath(p, RAW_DIR)}: {os.path.getsize(p) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
