import requests

# 测试DeepSeek API连接
def test_deepseek_api():
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "Hello"
                }
            ],
            "temperature": 0.1,
            "max_tokens": 100
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer sk-2f494a13f27f410c8e93ba5132763466"
        }
        print("测试DeepSeek API连接...")
        response = requests.post(url, json=data, headers=headers, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        if response.status_code == 200:
            print("API连接成功！")
        else:
            print("API连接失败！")
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")

if __name__ == "__main__":
    test_deepseek_api()
