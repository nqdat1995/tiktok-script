import requests

def getid(sec_user_id, max_cursor):
    url = f"https://www-hj.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id={sec_user_id}&max_cursor={max_cursor}"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "vi",
        "cache-control": "no-cache",
        "origin": "https://www.douyin.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.douyin.com/",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    cookies = {
        "ttwid": "1|OopEWR-Ay9UO6hA5eOwqqOltjOuTgeW0WUKh-5sPnak|1736430899|7c00e0c030cd3549a4adbc4ad0c38eb626480bb1b82d4a9d709306a9987d696c",
        "UIFID_TEMP": "c4a29131752d59acb78af076c3dbdd52744118e38e80b4b96439ef1e20799db0631480ed3caa78a3cdc859dfd07bf02237d58fe3c4291a522577f3fb16eada33d32c0d7283f28a93f4ae9157f64f88c890b21abea096a9e760656cb6570a38c521a53fabdf8060f200ccbe2a910d68d0",
    }
    
    try:
        res = requests.get(url, headers=headers, cookies=cookies)
        print(f"Response Status: {res.status_code}")
        print(f"Response Content: {res.text[:500]}")  # Print first 500 characters for debugging
        
        if res.status_code == 200:
            return res.json()
        else:
            return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}

def save_to_file(text, filename="douyin-video-links.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

def run():
    result = []
    has_more = 1
    #sec_user_id = "MS4wLjABAAAA0-PwDh2_qM3ByLNzHA9szJaitks-QRY65w3czIXHipM"  # Kênh mèo
    sec_user_id = "MS4wLjABAAAAgHRTHEoERbW0q5mBVCjysdCBd7Gh9rVUXskIDByGQXo"  # Replace with actual user ID
    
    max_cursor = 0
    
    while has_more == 1:
        moredata = getid(sec_user_id, max_cursor)
        has_more = moredata.get("has_more", 0)
        max_cursor = moredata.get("max_cursor", 0)
        
        for item in moredata.get("aweme_list", []):
            url = item.get("video", {}).get("play_addr", {}).get("url_list", [""])[0]
            if url.startswith("https"):
                result.append(url)
            else:
                result.append(url.replace("http", "https"))
            print(f"Number of videos: {len(result)}")
    
    save_to_file("\n".join(result))

run()
