#!/bin/sh
openssl ecparam -genkey -name secp384r1 -noout -out new-private.pem
openssl ec -in new-private.pem -pubout -out new-public.pem