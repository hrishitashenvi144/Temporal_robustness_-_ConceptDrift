"""
fast_download.py
Downloads DIVE_Raw_Data.zip using concurrent HTTP Range requests.
"""

import os
import sys
import time
import zipfile
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

RAW_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "raw")
URL = "https://zenodo.org/records/18519253/files/DIVE_Raw_Data.zip?download=1"
OUTPUT_ZIP = os.path.join(RAW_DIR, "DIVE_Raw_Data.zip")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

def get_file_size(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
    with urllib.request.urlopen(req) as resp:
        return int(resp.headers.get("Content-Length", 0))

def download_chunk(url, start_byte, end_byte, chunk_idx, part_file):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Range": f"bytes={start_byte}-{end_byte}"
        }
    )
    with urllib.request.urlopen(req) as resp, open(part_file, "wb") as f:
        f.write(resp.read())
    return chunk_idx, os.path.getsize(part_file)

def fast_download():
    os.makedirs(RAW_DIR, exist_ok=True)
    total_size = get_file_size(URL)
    print(f"Total size of DIVE_Raw_Data.zip: {total_size / (1024*1024):.2f} MB")
    
    num_chunks = 16
    chunk_size = total_size // num_chunks
    parts_dir = os.path.join(RAW_DIR, "_parts")
    os.makedirs(parts_dir, exist_ok=True)
    
    tasks = []
    for i in range(num_chunks):
        start = i * chunk_size
        end = (start + chunk_size - 1) if i < num_chunks - 1 else (total_size - 1)
        part_file = os.path.join(parts_dir, f"part_{i:02d}.dat")
        tasks.append((i, start, end, part_file))
        
    start_time = time.time()
    print(f"Starting parallel download with {num_chunks} threads...")
    
    with ThreadPoolExecutor(max_workers=num_chunks) as executor:
        futures = {
            executor.submit(download_chunk, URL, start, end, idx, part_file): (idx, part_file)
            for idx, start, end, part_file in tasks
        }
        completed_bytes = 0
        for future in as_completed(futures):
            idx, bytes_written = future.result()
            completed_bytes += bytes_written
            elapsed = time.time() - start_time
            pct = (completed_bytes / total_size) * 100
            spd = (completed_bytes / (1024*1024)) / max(elapsed, 0.001)
            print(f"  Completed part {idx+1}/{num_chunks} ({pct:.1f}%) - Speed: {spd:.2f} MB/s")
            
    print("Combining parts into DIVE_Raw_Data.zip...")
    with open(OUTPUT_ZIP, "wb") as outfile:
        for i in range(num_chunks):
            part_file = os.path.join(parts_dir, f"part_{i:02d}.dat")
            with open(part_file, "rb") as pf:
                outfile.write(pf.read())
            os.remove(part_file)
            
    os.rmdir(parts_dir)
    print(f"Downloaded DIVE_Raw_Data.zip ({os.path.getsize(OUTPUT_ZIP)/(1024*1024):.2f} MB in {time.time() - start_time:.1f}s)")
    
    print("Extracting DIVE_Raw_Data.zip...")
    with zipfile.ZipFile(OUTPUT_ZIP, "r") as z:
        z.extractall(RAW_DIR)
        print(f"Extracted {len(z.namelist())} files from DIVE_Raw_Data.zip")
        
    # Extract any nested zips
    for root, dirs, files in os.walk(RAW_DIR):
        for f in files:
            if f.endswith(".zip") and f != "DIVE_Raw_Data.zip":
                zp = os.path.join(root, f)
                try:
                    with zipfile.ZipFile(zp, "r") as nested_z:
                        nested_z.extractall(root)
                        print(f"Extracted nested zip: {f}")
                except Exception as e:
                    print(f"Error extracting {f}: {e}")

if __name__ == "__main__":
    fast_download()
