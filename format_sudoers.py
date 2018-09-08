import os, sys, shutil, re

text = '''\
##
## User privilege specification
##
root ALL=(ALL)  ALL
%admin  ALL=(ALL) ALL
%admin  ALL=(ALL)    ALL
   

#
%admin  ALL=(ALL)  NOPASSWD: ALL 
%admin  ALL=(ALL) NOPASSWD: ALL  
%admin  ALL=(ALL)    NOPASSWD: ALL\
'''

# 
def unique(lines):
    result = []
    for x in lines:
        # keep comments and empty lines
        if re.match(r"^(#|\s)",x) or not x in result:
            result.append(x)
    return result

# format space
def format_line(m):
    result = re.sub('\s+','\t',m.group(0).upper().strip())
    return result

text = re.sub('^(%admin\s+.*)$',format_line,text,flags=re.IGNORECASE | re.MULTILINE)
print(text)
print('---')
lines = unique(text.split('\n'))
text = '\n'.join(lines)
print(text)
