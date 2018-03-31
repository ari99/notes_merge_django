import sys
import os
def checkIp4Nums(arr):
  for a in arr:
    try:
      b = int(a)
    except ValueError:
      return False
  return True

def checkIp6Nums(arr):
  for a in arr:
    for c in range(0,len(a)):
      try:
        b = int(a[c])
      except ValueError:
        return False
  return True

def  checkIPs(ip_array):
  result = []
  for ip in ip_array:
    if "." in  ip:
      if checkIp4Nums(ip.split(".")):
        result.append("IPv4")
    if ":" in ip:
      if checkIp6Nums(ip.split(":")):
        result.append("IPv6")
    result.append("Neither")
  return result






def  maxDifference(a):
  max=0
  least=a[0]
  most=a[1]
  for num in a:
    if num<least:
      least = num
    if num>most:
      most = num
  return most - least




