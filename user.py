import requests  
  

def get(ask:str):
    # 发送POST请求到Flask应用程序  
    payload = {'ask':ask}  # 你的数据  
    headers = {'Content-Type': 'application/json'}  # 设置Content-Type为json  
    
    response = requests.post('http://localhost:11451/class', json=payload, headers=headers) 
    # 从响应中获取数据并打印输出  
    print(response.json())


get('你好')
