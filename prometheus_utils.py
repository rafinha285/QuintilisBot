import requests

def check_server_status(prometheus_url):
    query = 'up{job="minecraft-plugin"} == 0'  # Consulta para verificar se o servidor Minecraft está caído
    params = {'query': query}
    response = requests.get(prometheus_url, params=params)
    if response.status_code == 200:
        data = response.json()
        result = data['data']['result']
        if result and result[0]['value'][1] == '0':
            return True  # O servidor Minecraft está caído
    return False  # O servidor Minecraft está funcionando normalmente