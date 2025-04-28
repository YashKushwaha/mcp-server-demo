import requests

class MCPClient:
    def __init__(self, server_url):
        self.server_url = server_url.rstrip("/")

    def call(self, tool_name, params):
        url = f"{self.server_url}/tool/{tool_name}"
        response = requests.post(url, json=params)
        response.raise_for_status()
        return response.json()

    def get(self, resource_path):
        # resource_path example: 'greeting://John'
        path = resource_path.replace("greeting://", "greeting/")
        url = f"{self.server_url}/resource/{path}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

# Example usage
if __name__ == "__main__":
    client = MCPClient("http://172.23.48.126:6277")

    result = client.call("add", {"a": 5, "b": 7})
    print(result)

    greeting = client.get("greeting://John")
    print(greeting)
