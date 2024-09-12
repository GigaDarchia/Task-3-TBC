import json
import threading
import time
import requests
from concurrent.futures import ThreadPoolExecutor

start_time = time.time()

with open("posts.json", "w") as f:
    f.write("[\n")

file_lock = threading.Lock()
first_entry = True

def get_posts(post_id, lock):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response = requests.get(url)
    data = response.json()

    global first_entry
    with lock:
        with open("posts.json", "a") as f:
            if not first_entry:
                f.write(",\n")
            json.dump(data, f, indent=4)
            first_entry = False


with ThreadPoolExecutor(max_workers=10) as executor:
    for i in range(1, 78):
        thread = executor.submit(get_posts, i, file_lock)

with open("posts.json", "a") as f:
    f.write("\n]")


print(f"Time needed: {time.time() - start_time}")
