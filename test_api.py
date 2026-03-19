#!/usr/bin/env python3
"""
测试Google Custom Search API
"""
import requests
import sys

# 从命令行参数获取API密钥和搜索引擎ID
if len(sys.argv) != 3:
    print("用法: python test_api.py <API_KEY> <CSE_ID>")
    sys.exit(1)

API_KEY = sys.argv[1]
CSE_ID = sys.argv[2]

# 构建请求
url = "https://www.googleapis.com/customsearch/v1"
params = {
    'key': API_KEY,
    'cx': CSE_ID,
    'q': '字节跳动 商业化',
    'num': 5
}

print("=" * 60)
print("测试Google Custom Search API")
print("=" * 60)
print(f"API URL: {url}")
print(f"搜索引擎ID: {CSE_ID}")
print(f"搜索查询: {params['q']}")
print("=" * 60)

try:
    response = requests.get(url, params=params, timeout=10)
    print(f"\n📡 HTTP状态码: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ 请求失败")
        print(f"响应内容: {response.text}")
        sys.exit(1)
    
    data = response.json()
    
    print(f"\n📊 搜索信息:")
    search_info = data.get('searchInformation', {})
    print(f"  - 总结果数: {search_info.get('totalResults', 0)}")
    print(f"  - 搜索时间: {search_info.get('searchTime', 0)} 秒")
    
    items = data.get('items', [])
    print(f"\n📋 返回结果数: {len(items)} 条")
    
    if items:
        print(f"\n✅ 成功！前3条结果：")
        for i, item in enumerate(items[:3], 1):
            print(f"\n{i}. {item.get('title', '')}")
            print(f"   URL: {item.get('link', '')}")
            print(f"   摘要: {item.get('snippet', '')[:100]}...")
    else:
        print(f"\n⚠️  API返回成功但没有结果")
        print(f"完整响应: {data}")

except Exception as e:
    print(f"\n❌ 异常: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
