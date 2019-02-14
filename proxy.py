# requests proxy demo
import requests

# proxies = {
#     'http': 'http://127.0.0.1:1087',
#     'https': 'http://127.0.0.1:1087'
# }
proxies = {
    'http': 'http://54.194.92.235:80',
    'https': 'http://54.194.92.235:80',
}
# # url = 'http://httpbin.org/ip'
# url = 'http://httpbin.org/ip'
# r = requests.get(url, proxies=proxies)
# print(r.text)

# proxies = {
#     'http': 'http://http-pro.abuyun.com:9010',
#     'https': 'http://http-pro.abuyun.com:9010'
# }
# import base64
# user_pass = base64.b64encode('HS7DB3532N64003P:78DB08E3A5E3F1A6'.encode('utf-8')).decode()
# headers = {
#     'Proxy-Authorization': 'Basic ' + user_pass
# }
url = 'http://httpbin.org/ip'
# url = 'https://ip.cn'
r = requests.get(url, proxies=proxies)
print(r.text)



# # requests from version 2.10.0 support socks proxy
# proxies = {
#     'http': 'socks5://127.0.0.1:1087'
# }
#
#
# # tornado proxy demo
# def test(name, age):
#     """test how to write doc.
#     :param name: user's name
#     :param age: user's age
#     :return: None
#     :rtype: None
#     """
#     print(name, age)
#     return None
#
#
# """
# var pdfAsDataUri = func(data.XGL);
# var pdfAsArray = convertDataURIToBinary(pdfAsDataUri);
# DEFAULT_URL = pdfAsArray;
# """
