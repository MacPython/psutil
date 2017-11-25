#!/usr/bin/env python

from pprint import pprint as pp
import os
import re
import requests
import errno
import concurrent.futures


URL = "http://a365fff413fe338398b6-1c8a9b3114517dc5fe17b7c3f8c63a43.r19.cf2.rackcdn.com/"
TIMEOUT = 30


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9.8 K'
    >>> bytes2human(100001221)
    '95.4 M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2f B' % (n)


def safe_makedirs(path):
    try:
        os.makedirs(path)
    except OSError as err:
        if err.errno == errno.EEXIST:
            if not os.path.isdir(path):
                raise
        else:
            raise

def get_most_recent(ls):
    assert ls
    ret = []
    ls.sort(reverse=False)  # so that higher versions are listed first
    ver = ls[0].split('-')[1]
    for item in ls:
        if item.split('-')[1] != ver:
            break
        else:
            ret.append(item)
    return ret


def download_file(url):
    local_fname = url.split('/')[-1]
    local_fname = os.path.join('dist', local_fname)
    safe_makedirs('dist')
    r = requests.get(url, stream=True, timeout=TIMEOUT)
    with open(local_fname, 'wb') as f:
        for chunk in r.iter_content(chunk_size=16384):
            if chunk:    # filter out keep-alive new chunks
                f.write(chunk)
    return local_fname


def parallel_wget(urls):
    completed = 0
    with concurrent.futures.ThreadPoolExecutor() as e:
        fut_to_url = {e.submit(download_file, url): url for url in urls}
        for fut in concurrent.futures.as_completed(fut_to_url):
            url = fut_to_url[fut]
            try:
                local_fname = fut.result()
            except Exception as _:
                exc = _
                print("error while downloading %s: %s" % (url, exc))
            else:
                completed += 1
                print("downloaded %-10s %s" % (
                    bytes2human(os.path.getsize(local_fname)), local_fname))
    return completed


def main():
    print("HTTP GET " + URL)
    req = requests.get(URL)
    req.raise_for_status()
    ls = re.findall(r"\"psutil-.*\.whl\"", req.text)
    print("found %s psutil-related files" % len(ls))
    ls = [x.strip('"') for x in ls]
    ls = get_most_recent(ls)
    print("getting the %s most recent versions" % len(ls))
    urls = [os.path.join(URL, x) for x in ls]
    parallel_wget(urls)


main()
