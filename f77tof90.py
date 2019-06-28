'''
===========================================================
f77tof90: a script for converting the Fortran 77 programs
          to Fortran 90/95 programs
Author: Di Wu
E-mail: d.wu93@aliyun.com
GitHub: https://github.com/diwu93/
Version: 0.1
Last Modified: Jun 28, 2019
===========================================================
'''

'''
Usage: python3 f77tof90.py <f77 file> <f90 file>
Requirement: Python 3.x
'''

import sys

Version = 0.1

## f77 and f90 file
filename1 = sys.argv[1]
filename2 = sys.argv[2]

f1 = open(filename1,'r')
f2 = open(filename2,'w+')

def is_comm(a):
   if a.startswith('c') or a.startswith('C'):
      return True
   elif a.lstrip().startswith('!'):
      return True
   else:
      return False

## replace the comment symbol 'c' or 'C' with '!'
## comment the characters which are beyond the 72 width
temp_str0 = []
for eachline in f1:
   eachline = eachline.expandtabs(8)
   if eachline.startswith('c') or eachline.startswith('C'):
      eachline = '!'+eachline[1:]
   if len(eachline) > 72:
      eachline = eachline[:72]+'!'+eachline[72:]
   temp_str0.append(eachline)

## solving the continuum
index_line = 0
temp_line = temp_str0.copy()
for i,eachline in enumerate(temp_str0[1:]):
   if is_comm(eachline): continue
   if len(eachline) < 6: continue
   if eachline[5] != ' ' and eachline[5] != '\n':
      line0 = temp_line[index_line]
      if '!' in line0:
         aline0 = line0.split('!',1)
         line0 = aline0[0]+'&!'+aline0[1]
      else:
         line0 = line0[:-1]+'&'+line0[-1]
      temp_line[index_line] = line0
      eachline = eachline[:5]+'&'+eachline[6:]
      temp_line[i+1] = eachline
   index_line = i + 1

## solving blanks or continuum of `if`, `goto`, `data`, `do`,
## `print` and `format`
temp_str0 = temp_line.copy()
INFO = 0
INFOdata = 0
for i,eachline in enumerate(temp_str0):
   if is_comm(eachline): continue
   if len(eachline) < 6: continue
   if INFOdata:
      line0 = eachline
      if '!' in line0: line0 = line0[:line0.index('!')]
      if not line0.endswith('&'): INFOdata = 0
      eachline = eachline[:6]+eachline[6:].replace(' ','')
   if eachline[6:].lower().lstrip().startswith('if'):
      if '!' in eachline:
         aline0 = eachline.split('!',1)
         eachline = aline0[0][:6]+aline0[0][6:].replace(' ','')+'!'+aline0[1]
      else:
         eachline = eachline[:6]+eachline[6:].replace(' ','')
      if 'goto' in eachline.lower():
         eachline = eachline.lower().replace('goto','goto ')
   elif eachline.lower().lstrip().startswith('double'):
      continue
   elif eachline[6:].lower().lstrip().startswith('do'):
      ind = eachline.lower().index('do')
      if eachline[ind+2] != ' ':
         eachline = eachline[:ind+2]+' '+eachline[ind+2:]
   elif eachline[6:].lower().replace(' ','').startswith('data(') or\
        eachline[6:].lower().lstrip().startswith('data '):
      line0 = eachline
      if '!' in line0: line0 = line0[:line0.index('!')]+'\n'
      if '&' in line0: INFOdata = 1
   elif 'goto' in eachline[6:].lower().replace(' ',''):
      line0 = eachline.lower()
      eachline = line0[:6]+line0[6:].replace(' ','').replace('goto','goto ')
   line0 = eachline
   if '!' in line0: line0 = line0[:line0.index('!')]+'\n'
   INFOp = 0
   if 'print' in line0.lower():
      ind = eachline.lower().index('print')
      if eachline[ind+5] != ' ':
         eachline = eachline[:ind+5]+' '+eachline[ind+5:]
      INFOp = 1
   if INFO:
      if line0[:-1].endswith('&'):
         eachline = line0
      else:
         INFO = 0
   if 'format' in line0.lower():
      INFO = 1
      eachline = line0
      if '&' not in line0:
         eachline = line0
         INFO = 0
   temp_line[i] = eachline

for eachline in temp_line: f2.write(eachline)
