#!/usr/bin/env python
import sys
import urllib2
import logging
from lxml import etree


def _query(word):
    url = 'http://m.youdao.com/dict?le=eng&q=' + word
    logging.debug('url: %s' % url)
    response = urllib2.urlopen(url)
    html = response.read()
    logging.debug('html: %s' % html)
    return html


def _pretty(html):
    tree = etree.HTML(html.decode('utf-8', 'replace'))

    deletes = ['//*[@id="doc2"]/div[3]', '//*[@id="hd"]', '//*[@id="ft"]', '//*[@id="outer"]', '//*[@id="dictNav"]',
               '//*[@id="ec"]/h2',
               '//*[@id="bd"]/div[@class="content-wrp dict-container closed"]', '//*[@id="blng_sents_part"]/div/ul/li/div[1]', '//*[@id="ec"]/h2/a']

    for d in deletes:
        elements = tree.xpath(d)
        for e in elements:
            e.getparent().remove(e)

    result = etree.tostring(tree)
    logging.debug('result: %s' % result)

    return result


def main():
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s [%(lineno)d][%(levelname)s] %(message)s')
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    if len(sys.argv) != 2:
        logging.error('error args length')
        return

    html = _query(sys.argv[1])

    result = _pretty(html)
    # logging.info(result)
    print(result)


if __name__ == '__main__':
    main()
