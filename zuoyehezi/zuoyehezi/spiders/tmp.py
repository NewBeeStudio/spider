# coding: utf-8
import os, re
from bs4 import BeautifulSoup

txt = """
<html>
<body>
<span style="color:#46b789;margin-right:5px;margin-left: 5px ">...</span>
<p>
<span new="" style="font-family:;" times="">It’s hard to believe____ the way out of the forest without the help of the local guide.</span>
</p>
<p>
<span new="" style="font-family:;" times="">A．</span>
<span new="" style="font-family:;" times=""> what they were able to find</span>   
<span new="" style="font-family:;" times="">B．what were they able to find</span></p>
<p><span new="" style="font-family:;" times="">C． how they were able to find</span>   
<span new="" style="font-family:;" times="">D． how were they able to find</span></p><p></p></body></html>
	  """
txt = re.sub(r"(?:</span>|<span.*?>|<p>|</p>|</body>|</html>|\n|\t)", '', txt)
c = '．'
tmpList = txt.split('A'+c)
tmpText = tmpList[1]
# tmpList = tmpText.split("D.")
ans = tmpList[1]

# print txt.encode('ascii', 'ignore').decode('ascii')
print ans
# def replaceFunc(match):
# 	return re.search(match).group(1)

# test = re.search(r"A\.(.*)B\.(.*)C\.(.*)D\.(.*)<body>$", txt, flags=re.S)
# test = re.sub(r"A(.+?)B", replaceFunc, txt, flags = re.S)
# print test
