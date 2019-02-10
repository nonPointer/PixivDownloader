import requests
import json
import sys
import traceback
import time
import re
import os
import threading

# User-Agent
userAgent = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"

# Export Log
exportLog = False

# Export Log File
exportLogfile = "log.txt"

# Api Address
apiAddress = "https://www.pixiv.net/ajax/illust/"
authorPrefix = "https://www.pixiv.net/ajax/user/"
authorSuffix = "/profile/all"

# Cookies
# Use ";" to split each term
cookies = ""

# Threads per second
threads_per_sec = 10

# Enable Proxy
enable_proxy = False

# Enable Remote DNS Resolve via Proxies
enable_remote_dns = True

# Proxy Settings
socks5_proxy_address = "127.0.0.1"
socks5_proxy_port = "1080"

if not enable_proxy:
    proxiesDict = {}
else:
    if enable_remote_dns:
        proxiesDict = {
            'http': "socks5h://" + socks5_proxy_address + ":" + socks5_proxy_port,
            'https': "socks5h://" + socks5_proxy_address + ":" + socks5_proxy_port
        }
    else:
        proxiesDict = {
            'http': "socks5://" + socks5_proxy_address + ":" + socks5_proxy_port,
            'https': "socks5://" + socks5_proxy_address + ":" + socks5_proxy_port
        }


def print_log(content):
    print(time.strftime('%Y-%m-%d %H:%M:%S\t', time.localtime(time.time())) + content)
    sys.stdout.flush()
    if exportLog:
        f_log = open(exportLogfile, "a")
        f_log.write(time.strftime('%Y-%m-%d %H:%M:%S\t', time.localtime(time.time())) + str(content) + '\n')
        f_log.close()
    return


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)
        print_log("Folder created.")
    else:
        print_log("Folder exist!")


def work(illust_id):
    try:
        contentJSON = requests.get(apiAddress + illust_id, headers=headers, proxies=proxiesDict)
        decodeContent = json.loads(contentJSON.text)
        if decodeContent['error'] == True:
            print_log("Illustration error.")
        else:
            if not os.path.exists(foldername + "\\" + illust_id + ".png"):
                print_log("Downloading\t [" + decodeContent['body']['illustTitle'] + "]")
                # print_log("\tAuthor\t [" + decodeContent['body']['userName'] + "]")
                # print_log("\tRAW URL\t [" + decodeContent['body']['urls']['original'] + "]")
                # print_log("\tRAW URL\t [" + decodeContent['body']['urls']['regular'] + "]")
                headers1 = {
                    'Referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + i,
                    'cookie': cookies
                }

                content = requests.get(decodeContent['body']['urls']['original'], headers=headers1, proxies=proxiesDict)
                f = open(foldername + "\\" + illust_id + ".png", "wb")
                f.write(content.content)
                f.close()
            else:
                print_log("Skip\t [" + decodeContent['body']['illustTitle'] + "]")
    except:
        traceback.print_exc()


if __name__ == "__main__":

    headers = {
        "User-Agent": userAgent,
        "cookie": cookies
    }

    while True:
        # Fetch thumb list
        author_id = str(input()).strip().strip("\n")
        contentJSON = requests.get(authorPrefix + author_id + authorSuffix, headers=headers, proxies=proxiesDict)
        decodeContent = json.loads(contentJSON.text)

        # Regex Match
        try:
            illusts = re.findall("[0-9]+", str(decodeContent['body']['illusts']))
        except:
            continue
        print_log("Counter\t" + str(len(illusts)))

        print_log(str(decodeContent))

        try:
            foldername = re.findall("'userName': '(.*)', 'userImageUrl'", str(decodeContent['body']['pickup']))[0]
        except:
            try:
                foldername = re.findall("<title>「(.*)」.*</title>",
                                        requests.get("https://www.pixiv.net/member.php?id=" + author_id,
                                                     headers=headers, proxies=proxiesDict).text)[0]
            except:
                foldername = author_id

        print_log(foldername)
        mkdir(foldername)

        waitcount = 0

        # Fetch item info
        threads = []
        for i in illusts:
            illust_id = i
            t = threading.Thread(target=work, args=(illust_id,))
            t.setDaemon(False)
            t.start()
            threads.append(t)
            waitcount = waitcount + 1
            if waitcount % threads_per_sec == 0:
                time.sleep(1)
            # t.join()
        for thr in threads:
            if thr.is_alive():
                thr.join()
        print_log("Job finished.")
