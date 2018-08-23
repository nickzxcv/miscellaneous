import csv
import subprocess
import re
import sys

ianaciphers={}
openssl_ciphers={}

# based on this nice helpful article http://www.woolie.co.uk/article/mapping-openssl-ciphers-to-iana-cipher-suite-registy/

# IANA cipher suite names https://www.iana.org/assignments/tls-parameters/tls-parameters-4.csv
with open('20160930-tls-parameters-4.csv', 'r') as ianafile:
    csv_ianaciphers = csv.reader(ianafile, delimiter=',', quotechar='"')
    for row in csv_ianaciphers:
        ianaciphers[row[1]]=row[0]

openssl_cipher_output=subprocess.check_output(['openssl', 'ciphers', '-V'])
openssl_cipher_list=re.findall(
    '^\s+(0x[0-9A-F][0-9A-F],0x[0-9A-F][0-9A-F]) - ([0-9A-Z\-]+)\s+',
    openssl_cipher_output,
    re.DOTALL|re.MULTILINE)

for ciphersuite in openssl_cipher_list:
    openssl_ciphers[ciphersuite[0]]=ciphersuite[1]

# Apple ATS allowable ciphers from:
# https://developer.apple.com/library/content/documentation/General/Reference/InfoPlistKeyReference/Articles/CocoaKeys.html#//apple_ref/doc/uid/TP40009251-SW57
apple_ATS_allowable_ciphers=[
    'TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384',
    'TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256',
    'TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384',
    'TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA',
    'TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256',
    'TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA',
    'TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384',
    'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256',
    'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384',
    'TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256',
    'TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA',
]

separator=''
for applecipher in apple_ATS_allowable_ciphers:
    sys.stdout.write("{}{}".format(separator, openssl_ciphers[ianaciphers[applecipher]]))
    separator=':'
