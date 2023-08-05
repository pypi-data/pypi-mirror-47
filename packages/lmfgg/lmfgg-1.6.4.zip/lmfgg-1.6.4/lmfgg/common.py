from bs4 import BeautifulSoup
from lmf.dbv2 import db_query
import re
htmlparser="lxml" 
def to_arr(page):
    cm=["：","："]
    if page is None:return []
    soup=BeautifulSoup(page,htmlparser)
    tmp=soup.find('style')
    if tmp is not  None:tmp.clear()
    tmp=soup.find('script')
    if tmp is not  None:tmp.clear()
    arr=[]
    for w in soup.strings:
    #for w in soup.get_text('$lmf$lmf$').split("$lmf$lmf$")
            w=w.strip()
            if w=='':continue
            if len(w)==1 and w not in cm:continue
            x=re.split("[\s;；]{2,}|,|，",w)
            arr.extend(x)
    return arr 


def getpage(url,quyu):
    sql="select * from v1.t_gg where quyu='%s' and href='%s' "%(quyu,url)

    conp=['postgres','since2015','192.168.4.188','base','v1']
    df=db_query(sql,dbtype="postgresql",conp=conp)
 
    if not df.empty:
        page=df.at[0,'page']
        return page 
    return None