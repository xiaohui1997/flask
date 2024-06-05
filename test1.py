import requests

cookies = {
    'XSRF-TOKEN': 'eyJpdiI6IkE1K3B4RldCeVhnRytLcXg5VDR1Z3c9PSIsInZhbHVlIjoiSXVkZXNTamlGQXR6RjJBV2FUZmxaVjdBVTFzUU1yZ0dodHc1eHM4aXFnK2hBS1hOejVFaWFFdXk2aDlxNlFvWnZuVTR3VTRXYWRCTE5tdjg1T1UxY05NU1l6aDhXazZaTjFyZ0NhMWlUNktQRUtZaVR0NEhTK2FOVHpBTUFiM0kiLCJtYWMiOiI4ZGY1MjNhMDI5YjNlZTkyMzExN2NlOTZkZTNjN2Y3YWVlMTM4NWYyZDkxNmY2MDllMTU0YTljY2Y0ZWEyZmVhIiwidGFnIjoiIn0%3D',
    'ar_cf_session': 'hbiF3aetyU0cyplZ6fsu6cpSjNjAMzcSpETiN06L',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'XSRF-TOKEN=eyJpdiI6IkE1K3B4RldCeVhnRytLcXg5VDR1Z3c9PSIsInZhbHVlIjoiSXVkZXNTamlGQXR6RjJBV2FUZmxaVjdBVTFzUU1yZ0dodHc1eHM4aXFnK2hBS1hOejVFaWFFdXk2aDlxNlFvWnZuVTR3VTRXYWRCTE5tdjg1T1UxY05NU1l6aDhXazZaTjFyZ0NhMWlUNktQRUtZaVR0NEhTK2FOVHpBTUFiM0kiLCJtYWMiOiI4ZGY1MjNhMDI5YjNlZTkyMzExN2NlOTZkZTNjN2Y3YWVlMTM4NWYyZDkxNmY2MDllMTU0YTljY2Y0ZWEyZmVhIiwidGFnIjoiIn0%3D; ar_cf_session=hbiF3aetyU0cyplZ6fsu6cpSjNjAMzcSpETiN06L',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

proxies = {
  'http': 'http://fanye:fanye@1997@47.236.76.143:8089',
}

response = requests.get('https://cfwebs.xyz/admin/login', cookies=cookies, headers=headers, proxies=proxies)

print(response.text)