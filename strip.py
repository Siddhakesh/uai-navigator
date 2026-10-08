import re
with open(r's:\mini p\Mini Project\uai-welcome-chatbot.html', 'r', encoding='utf-8') as f:
    content = f.read()
content = re.sub(r'data:image/[^;]+;base64,[a-zA-Z0-9+/=]+', 'base64_img', content)
with open(r's:\mini p\Mini Project\uai-welcome-chatbot-clean.html', 'w', encoding='utf-8') as f:
    f.write(content)
