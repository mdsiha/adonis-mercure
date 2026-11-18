import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Preformatted, KeepTogether, NextPageTemplate)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Circle, PolyLine
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

D='/usr/share/fonts/truetype/dejavu/'
for n,f in [('DV','DejaVuSans.ttf'),('DV-B','DejaVuSans-Bold.ttf'),('DVM','DejaVuSansMono.ttf'),('DVM-B','DejaVuSansMono-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(n,D+f))
addMapping('DV',0,0,'DV');addMapping('DV',1,0,'DV-B');addMapping('DV',0,1,'DV');addMapping('DV',1,1,'DV-B')
addMapping('DVM',0,0,'DVM');addMapping('DVM',1,0,'DVM-B');addMapping('DVM',0,1,'DVM');addMapping('DVM',1,1,'DVM-B')

INK=colors.HexColor('#1f2937'); MUTED=colors.HexColor('#6b7280')
BLUE=colors.HexColor('#2563eb'); LBLUE=colors.HexColor('#dbeafe')
GREEN=colors.HexColor('#16a34a'); LGREEN=colors.HexColor('#dcfce7')
ORANGE=colors.HexColor('#ea580c'); LORANGE=colors.HexColor('#ffedd5')
PURPLE=colors.HexColor('#7c3aed'); LPURPLE=colors.HexColor('#ede9fe')
RED=colors.HexColor('#dc2626'); LRED=colors.HexColor('#fee2e2')
GREY=colors.HexColor('#f3f4f6'); DARK=colors.HexColor('#111827')
YEL=colors.HexColor('#fef3c7')

S={}
S['body']=ParagraphStyle('body',fontName='DV',fontSize=9.3,leading=14,textColor=INK,spaceAfter=5)
S['h1']=ParagraphStyle('h1',parent=S['body'],fontName='DV-B',fontSize=19,leading=24,textColor=BLUE,spaceBefore=4,spaceAfter=8)
S['h2']=ParagraphStyle('h2',parent=S['body'],fontName='DV-B',fontSize=12.5,leading=17,textColor=DARK,spaceBefore=9,spaceAfter=4)
S['h3']=ParagraphStyle('h3',parent=S['body'],fontName='DV-B',fontSize=10,leading=14,textColor=PURPLE,spaceBefore=5,spaceAfter=2)
S['small']=ParagraphStyle('small',parent=S['body'],fontSize=8,leading=11,textColor=MUTED)
S['bul']=ParagraphStyle('bul',parent=S['body'],leftIndent=13,bulletIndent=3,spaceAfter=2.5)
S['cell']=ParagraphStyle('cell',parent=S['body'],fontSize=8.3,leading=11.5,spaceAfter=0)
S['cellb']=ParagraphStyle('cellb',parent=S['cell'],fontName='DV-B')
S['cellh']=ParagraphStyle('cellh',parent=S['cell'],fontName='DV-B',textColor=colors.white)
S['code']=ParagraphStyle('code',fontName='DVM',fontSize=7.4,leading=9.8,textColor=colors.HexColor('#e5e7eb'))
S['q']=ParagraphStyle('q',parent=S['body'],fontName='DV-B',textColor=BLUE,spaceBefore=7,spaceAfter=2)
S['cover1']=ParagraphStyle('c1',fontName='DV-B',fontSize=30,leading=36,textColor=colors.white)
S['cover2']=ParagraphStyle('c2',fontName='DV',fontSize=13,leading=19,textColor=colors.HexColor('#dbeafe'))

def P(t,s='body'): return Paragraph(t,S[s])
def H1(t): return P(t,'h1')
def H2(t): return P(t,'h2')
def H3(t): return P(t,'h3')
def B(items): return [Paragraph(i,S['bul'],bulletText='•') for i in items]
def M(t): return '<font face="DVM" color="#be123c">%s</font>'%t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

W=A4[0]-36*mm
def code(txt,title=None):
    pre=Preformatted(txt.strip('\n'),S['code'])
    rows=[]
    if title: rows.append([Paragraph('<font color="#9ca3af" face="DVM" size="7">%s</font>'%title,S['cell'])])
    rows.append([pre])
    t=Table(rows,colWidths=[W])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DARK),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),5),('ROUNDEDCORNERS',[5,5,5,5])]))
    return [t,Spacer(1,6)]
def callout(label,text,bg,fg):
    inner=[Paragraph('<b><font color="%s">%s</font></b>'%(fg.hexval().replace('0x','#'),label),S['cell']),Spacer(1,2),Paragraph(text,S['body'])]
    t=Table([[inner]],colWidths=[W])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('LINEBEFORE',(0,0),(0,-1),3,fg),('LEFTPADDING',(0,0),(-1,-1),10),
        ('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),2)]))
    return [t,Spacer(1,7)]
def kid(t): return callout('Simple explanation (“like I am 5”)',t,LORANGE,ORANGE)
def tip(t): return callout('Remember for the interview',t,LGREEN,GREEN)
def warn(t): return callout('Warning / trap',t,LRED,RED)
def table(rows,widths,head=True):
    data=[[Paragraph(str(c),S['cellh'] if (head and i==0) else S['cell']) for c in r] for i,r in enumerate(rows)]
    t=Table(data,colWidths=widths,repeatRows=1 if head else 0)
    st=[('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#d1d5db')),
        ('TOPPADDING',(0,0),(-1,-1),3.5),('BOTTOMPADDING',(0,0),(-1,-1),3.5),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5)]
    if head: st.append(('BACKGROUND',(0,0),(-1,0),BLUE))
    for i in range(1,len(rows)):
        if i%2==0: st.append(('BACKGROUND',(0,i),(-1,i),GREY))
    t.setStyle(TableStyle(st)); return [t,Spacer(1,8)]

# ---------- drawing helpers ----------
def box(d,x,y,w,h,lines,fill=LBLUE,stroke=BLUE,size=8.5,bold_first=True,tc=INK):
    d.add(Rect(x,y,w,h,rx=5,ry=5,fillColor=fill,strokeColor=stroke,strokeWidth=1.2))
    n=len(lines); lh=size+3; top=y+h/2+(n-1)*lh/2-size*0.35
    for i,l in enumerate(lines):
        fn='DV-B' if (i==0 and bold_first) else 'DV'
        d.add(String(x+w/2,top-i*lh,l,fontName=fn,fontSize=size if i==0 else size-1,fillColor=tc,textAnchor='middle'))
def arrow(d,x1,y1,x2,y2,color=INK,label=None,dash=None,lx=0,ly=4,size=7,anchor='middle'):
    ln=Line(x1,y1,x2,y2,strokeColor=color,strokeWidth=1.3)
    if dash: ln.strokeDashArray=dash
    d.add(ln)
    a=math.atan2(y2-y1,x2-x1); s=6
    p=[x2,y2,x2-s*math.cos(a-0.4),y2-s*math.sin(a-0.4),x2-s*math.cos(a+0.4),y2-s*math.sin(a+0.4)]
    d.add(Polygon(p,fillColor=color,strokeColor=color))
    if label: d.add(String((x1+x2)/2+lx,(y1+y2)/2+ly,label,fontName='DV',fontSize=size,fillColor=color,textAnchor=anchor))
def txt(d,x,y,t,size=8,color=INK,bold=False,anchor='start'):
    d.add(String(x,y,t,fontName='DV-B' if bold else 'DV',fontSize=size,fillColor=color,textAnchor=anchor))

def fig(d,caption):
    t=Table([[d],[Paragraph('<i>%s</i>'%caption,S['small'])]],colWidths=[W])
    t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('BOX',(0,0),(-1,0),0.5,colors.HexColor('#e5e7eb')),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)]))
    return [KeepTogether([t]),Spacer(1,8)]

# D1 big picture
def d_big():
    d=Drawing(W,190)
    box(d,10,110,120,60,['Browser','(React, Vue, JS…)','EventSource'],LGREEN,GREEN)
    box(d,W-130,110,120,60,['App AdonisJS','+ this package','adonis-mercure'],LBLUE,BLUE)
    box(d,W/2-60,10,120,55,['Mercure Hub','(external server)','« the post office »'],LORANGE,ORANGE)
    arrow(d,W-70,110,W/2+45,65,BLUE)
    txt(d,W-10,88,'① POST /.well-known/mercure',7,BLUE,anchor='end')
    txt(d,W-10,78,'(JWT admin + topic + data)',7,BLUE,anchor='end')
    arrow(d,W/2-45,65,70,110,ORANGE,'② pushes live (SSE)',lx=-62,ly=2,size=7)
    arrow(d,W-130,150,130,150,PURPLE,None,dash=[3,2])
    txt(d,W/2,155,'③ (private) the app gives a « subscriber » JWT token',7.5,PURPLE,anchor='middle')
    arrow(d,130,128,W-130,128,GREEN,None,dash=[2,2])
    txt(d,W/2,118,'(the browser subscribes to the hub: GET + topic)',7,GREEN,anchor='middle')
    return d
# D2 polling/sse/ws
def d_proto():
    d=Drawing(W,150)
    cols=[('Polling','“Anything new?”',RED,LRED),('SSE (Mercure)','“I listen, talk anytime”',GREEN,LGREEN),('WebSocket','Pipe in both directions',PURPLE,LPURPLE)]
    cw=(W-20)/3
    for i,(t,sub,c,l) in enumerate(cols):
        x=i*(cw+10)
        d.add(Rect(x,5,cw,140,rx=6,ry=6,fillColor=l,strokeColor=c))
        txt(d,x+cw/2,128,t,10,c,True,'middle'); txt(d,x+cw/2,116,sub,6.8,INK,False,'middle')
        cx1,cx2=x+22,x+cw-22
        d.add(Line(cx1,25,cx1,105,strokeColor=INK,strokeDashArray=[2,2])); d.add(Line(cx2,25,cx2,105,strokeColor=INK,strokeDashArray=[2,2]))
        txt(d,cx1,10,'Client',7,INK,True,'middle'); txt(d,cx2,10,'Server',7,INK,True,'middle')
        if i==0:
            for k,yy in enumerate([95,75,55,35]):
                arrow(d,cx1,yy,cx2,yy,RED,'nothing?' if k<3 else 'yes!',size=6.5,ly=2)
        if i==1:
            arrow(d,cx1,95,cx2,95,GREEN,'I subscribe',size=6.5,ly=2)
            for yy,l in [(75,'msg 1'),(55,'msg 2'),(35,'msg 3')]:
                arrow(d,cx2,yy,cx1,yy,GREEN,l,size=6.5,ly=2)
        if i==2:
            arrow(d,cx1,95,cx2,95,PURPLE,'hello',size=6.5,ly=2)
            arrow(d,cx2,75,cx1,75,PURPLE,'msg',size=6.5,ly=2)
            arrow(d,cx1,55,cx2,55,PURPLE,'msg',size=6.5,ly=2)
            arrow(d,cx2,35,cx1,35,PURPLE,'msg',size=6.5,ly=2)
    return d
# D3 architecture
def d_arch():
    d=Drawing(W,250)
    box(d,W/2-70,205,140,36,['MercureProvider','boot() → container.singleton'],LPURPLE,PURPLE,8)
    box(d,W/2-70,135,140,40,['Mercure','(facade: send, ping…)'],LBLUE,BLUE,9)
    box(d,10,60,140,44,['Publisher','publish() → fetch POST'],LORANGE,ORANGE,8.5)
    box(d,W-150,60,140,44,['TokenGenerator','generate() → JWT (jws)'],LGREEN,GREEN,8.5)
    box(d,W/2-70,5,140,38,['MercureConfig','endpoint, adminToken, jwt…'],GREY,MUTED,8)
    box(d,W-135,195,125,50,['MercureContract','(TypeScript interface)'],YEL,colors.HexColor('#ca8a04'),8)
    box(d,10,195,125,50,['FakeMercure','(fake for tests)'],LRED,RED,8)
    arrow(d,W/2,205,W/2,175,PURPLE,'new Mercure(config)',lx=45,ly=-2)
    arrow(d,W/2-40,135,100,104,BLUE,'send()',lx=-20,ly=4)
    arrow(d,W/2+40,135,W-100,104,BLUE,'generate…()',lx=22,ly=4)
    arrow(d,80,60,W/2-30,43,MUTED,'reads config',lx=-10,ly=-10,size=6.5)
    arrow(d,W-80,60,W/2+30,43,MUTED,'reads config',lx=10,ly=-10,size=6.5)
    arrow(d,W-72,195,W/2+50,175,colors.HexColor('#ca8a04'),None,dash=[3,2])
    txt(d,W-50,182,'implements',6.5,colors.HexColor('#ca8a04'),anchor='middle')
    arrow(d,72,195,W/2-50,175,RED,None,dash=[3,2])
    txt(d,50,182,'implements',6.5,RED,anchor='middle')
    return d
# D4 sequence send
def d_seq():
    d=Drawing(W,240)
    names=['Your code','Mercure','Publisher','Mercure Hub']
    xs=[50,160,280,410]
    cols=[GREEN,BLUE,ORANGE,PURPLE]
    for x,n,c in zip(xs,names,cols):
        box(d,x-42,210,84,24,[n],colors.white,c,8.5)
        d.add(Line(x,210,x,8,strokeColor=c,strokeDashArray=[3,3]))
    def msg(i,j,y,t,c=INK,dash=None):
        arrow(d,xs[i],y,xs[j],y,c,None,dash)
        txt(d,(xs[i]+xs[j])/2,y+3,t,6.8,c,anchor='middle')
    msg(0,1,190,"send('/orders/42', {status})")
    msg(1,2,168,'publish(topics, data, opts)')
    d.add(Rect(xs[2]-4,128,8,34,fillColor=LORANGE,strokeColor=ORANGE))
    txt(d,xs[2]+8,150,'URLSearchParams',6.5,ORANGE); txt(d,xs[2]+8,140,'+ anti-freeze timer',6.5,ORANGE)
    msg(2,3,120,'POST + Bearer adminToken',PURPLE)
    msg(3,2,92,'200 OK  « urn:uuid:… »',PURPLE,[3,2])
    msg(2,1,70,'return id',ORANGE,[3,2])
    msg(1,0,48,'return id',BLUE,[3,2])
    txt(d,xs[3]+6,50,'sends to subscribers',6.5,PURPLE)
    d.add(Rect(W-318,14,312,12,fillColor=colors.white,strokeColor=None))
    txt(d,W-8,17,'If it fails: MercurePublishError / TimeoutError / ConnectionError',6.8,RED,anchor='end')
    return d
# D5 timeline
def d_time():
    d=Drawing(W,160)
    d.add(Line(15,75,W-15,75,strokeColor=MUTED,strokeWidth=2))
    ev=[('1.0.12','Aug 2024','First version',1),('2.0.0','May 2026','Rewrite:\nFake, ping,\nerrors, fetch',-1),('2.0.1','May 2026','Security',1),('2.1.x','May 2026','npm rename,\ntimeout',-1),('2.2.0','Nov 2026','expiresIn,\nConnectionError,\nv7',1),('3.0.0','Nov 2026','send()\nreturns the id',-1)]
    n=len(ev)
    for i,(v,dt,t,s) in enumerate(ev):
        x=40+i*(W-80)/(n-1)
        c=[GREEN,BLUE,RED,PURPLE,ORANGE,DARK][i]
        d.add(Circle(x,75,6,fillColor=c,strokeColor=colors.white,strokeWidth=1.5))
        y=112 if s>0 else 55
        txt(d,x,y+ (14 if s>0 else -2),v,9,c,True,'middle')
        txt(d,x,y+(5 if s>0 else -11),dt,6.5,MUTED,False,'middle')
        for k,l in enumerate(t.split('\n')):
            txt(d,x,(y+ (-6 if s>0 else -22))-k*8 if False else (y-6-k*8 if s>0 else y-22-k*8)+(0 if s>0 else 0),l,6.8,INK,False,'middle')
    return d
# D6 cookie flow
def d_cookie():
    d=Drawing(W,230)
    names=['Browser','App AdonisJS','Mercure Hub']
    xs=[60,230,400]; cols=[GREEN,BLUE,ORANGE]
    for x,n,c in zip(xs,names,cols):
        box(d,x-50,200,100,24,[n],colors.white,c,8.5); d.add(Line(x,200,x,8,strokeColor=c,strokeDashArray=[3,3]))
    def msg(i,j,y,t,c=INK,dash=None):
        arrow(d,xs[i],y,xs[j],y,c,None,dash); txt(d,(xs[i]+xs[j])/2,y+3,t,6.8,c,anchor='middle')
    msg(0,1,180,'GET /orders/42/subscribe',GREEN)
    d.add(Rect(xs[1]-4,138,8,36,fillColor=LBLUE,strokeColor=BLUE)); txt(d,xs[1]+8,158,'generateSubscribeToken()',6.5,BLUE)
    txt(d,xs[1]+8,148,'→ JWT {subscribe:[topic]}',6.5,BLUE)
    msg(1,0,125,'Set-Cookie: __Secure-mercure_access_token=JWT',BLUE,[3,2])
    msg(0,2,95,'EventSource(url + ?topic=…, withCredentials)',GREEN)
    txt(d,xs[2]-4,80,'checks the JWT signature',6.5,ORANGE,anchor='end')
    msg(2,0,60,'SSE stream open…',ORANGE,[3,2])
    msg(2,0,35,'data: {"status":"shipped"}',ORANGE)
    return d
# D7 errors
def d_err():
    d=Drawing(W,150)
    box(d,W/2-60,112,120,30,['Error','(native JavaScript)'],GREY,MUTED,8.5)
    box(d,W/2-60,66,120,30,['MercureError','parent class'],LBLUE,BLUE,8.5)
    arrow(d,W/2,112,W/2,96,MUTED); 
    items=[('ConfigError','invalid config',PURPLE,LPURPLE),('PublishError','hub answers non-2xx',RED,LRED),('TimeoutError','too slow (5 s)',ORANGE,LORANGE),('ConnectionError','hub unreachable',GREEN,LGREEN)]
    bw=(W-30)/4
    for i,(t,s,c,l) in enumerate(items):
        x=5+i*(bw+7); box(d,x,6,bw,34,['Mercure'+t,s],l,c,7.5)
        arrow(d,x+bw/2,40,W/2+(i-1.5)*18,66,c)
    return d
# D8 boot flow
def d_boot():
    d=Drawing(W,130)
    steps=[('node ace\nconfigure','You install',GREEN,LGREEN),('configure.ts','creates config,\n.env, rcfile',BLUE,LBLUE),('Adonis\nstartup','reads adonisrc',PURPLE,LPURPLE),('Provider.boot()','declares\nsingleton',ORANGE,LORANGE),('import service\n(1st time)','container.make\n→ new Mercure',RED,LRED)]
    n=len(steps); bw=82; gap=(W-n*bw)/(n-1)
    for i,(a,b,c,l) in enumerate(steps):
        x=i*(bw+gap)
        d.add(Rect(x,40,bw,70,rx=5,ry=5,fillColor=l,strokeColor=c,strokeWidth=1.2))
        for k,t in enumerate(a.split('\n')): txt(d,x+bw/2,95-k*10,t,7.5,c,True,'middle')
        for k,t in enumerate(b.split('\n')): txt(d,x+bw/2,70-k*9,t,6.8,INK,False,'middle')
        txt(d,x+bw/2,26,str(i+1),11,c,True,'middle')
        if i<n-1: arrow(d,x+bw+2,75,x+bw+gap-2,75,INK)
    return d
# D9 JWT
def d_jwt():
    d=Drawing(W,95)
    parts=[('HEADER','{"alg":"HS256"}',LRED,RED),('PAYLOAD','{"mercure":{"subscribe":[…]}, "exp":…}',LPURPLE,PURPLE),('SIGNATURE','HMAC(secret, header.payload)',LBLUE,BLUE)]
    ws=[110,225,W-335-30]
    x=0
    for (t,s,l,c),w in zip(parts,ws):
        box(d,x,25,w,50,[t,s],l,c,8.5); x+=w+15
    txt(d,W/2,8,'The hub computes the signature again with the same secret. If it matches, the token is real.',7.2,MUTED,anchor='middle')
    return d


# ---------- Document (English, B1) ----------
def vocab(pairs):
    cells=[[Paragraph('<b>%s</b>'%e,S['cell']),Paragraph('= %s'%f,S['cell'])] for e,f in pairs]
    # 2 columns of pairs
    rows=[]
    for i in range(0,len(cells),2):
        a=cells[i]; b=cells[i+1] if i+1<len(cells) else ['','']
        rows.append(a+b)
    t=Table(rows,colWidths=[W*0.2,W*0.3,W*0.2,W*0.3])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LPURPLE),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),
        ('LEFTPADDING',(0,0),(-1,-1),6),('LINEBEFORE',(0,0),(0,-1),3,PURPLE)]))
    head=Paragraph('<b><font color="#7c3aed">Key vocabulary (EN = FR)</font></b>',S['cell'])
    return [head,Spacer(1,2),t,Spacer(1,7)]

# ======== CANADA / SENIOR EDITION BLOCK (EN) ========
import re as _re
def bt(t): return _re.sub(r'`([^`]+)`',lambda m: M(m.group(1)),t)
def trade(t): return callout('Technical Trade-offs & Production Impact',bt(t),LPURPLE,PURPLE)
TRADE=[
"""<b>Build vs Buy: delegating real time to an external hub.</b><br/>
• <b>Gain</b>: the application stays <i>stateless</i>; no long-lived connections inside the Node process; the hub scales independently of the app.<br/>
• <b>Cost</b>: one more infrastructure component to operate (deployment, monitoring, HA, upgrades), an extra network hop and a new point of failure (a SPOF if you run a single instance).<br/>
• <b>Production impact</b>: real time must be designed to <i>degrade gracefully</i>. If the hub goes down, the app keeps serving requests and the UI falls back to a manual refresh or polling.""",
"""<b>SSE vs WebSocket: server cost, memory, load balancing.</b><br/>
• <b>SSE</b> is plain HTTP: it goes through existing proxies, CDNs and WAFs; reconnection and <i>Last-Event-ID</i> are built in; authentication works with ordinary cookies and headers; HTTP/2 multiplexes several streams over one TCP connection. There is no application-level heartbeat or framing to write, so less code and less per-connection memory on the server.<br/>
• <b>SSE limits</b>: unidirectional (client → server stays normal HTTP requests); UTF-8 text only; on HTTP/1.1, about 6 connections per domain per browser (so use HTTP/2, or a single EventSource with several topics); behind nginx you must disable `proxy_buffering` and raise `proxy_read_timeout`.<br/>
• <b>Load balancing</b>: long-lived connections make the distribution uneven after a <i>rolling deploy</i> and cause a <i>thundering herd</i> when clients reconnect (add client-side jitter). WebSocket often needs sticky sessions and its own heartbeat.<br/>
• <i>Orders of magnitude (memory per connection, file-descriptor limits) must be validated with a load test (k6, Artillery): the repo contains no benchmark.</i>""",
"""<b>Topic granularity: per resource or per user?</b><br/>
• <b>One topic per resource</b> (`/orders/42`): precise targeting and fine-grained ACLs through the JWT, but high cardinality; the `subscribe` list in the JWT grows, and the token travels in a cookie (about 4 KB limit) or a header.<br/>
• <b>One topic per user</b> (`/users/1`): few topics and a tiny token, but the fan-out logic (who receives what) moves into application code.<br/>
• The Mercure protocol supports <i>topic selectors</i> (URI templates, wildcards) to keep tokens small, at the price of a wider authorization surface: check it against the <i>least privilege</i> principle.""",
"""<b>Stateless JWT vs server-side sessions.</b><br/>
• <b>Gain</b>: the hub verifies the signature locally, with no call to the database or the app: no coupling, trivial horizontal scaling.<br/>
• <b>Cost</b>: no revocation before `exp`. A stolen token stays valid until it expires. Mitigation: short TTL (a few minutes), an endpoint that issues a fresh token, and secret rotation after an incident.<br/>
• <b>In this package</b>: `expiresIn` is optional and by default the token never expires. This is a DX-over-security compromise; in production I would make a TTL mandatory or set a sensible default.""",
"""<b>Fail-fast at boot vs fault tolerance.</b><br/>
• `defineConfig()` crashes at startup if the config is invalid: the error is caught at deploy time (failing readiness probe, rolling update halted, automatic rollback) instead of on the first user request.<br/>
• <b>Deliberate choice</b>: the provider does <i>not</i> `ping()` the hub at boot. Otherwise a hub outage would block every deployment of the app, although real time is not critical. Invalid config is a developer bug (fail-fast); an unavailable hub is an operational incident (graceful degradation).""",
"""<b>5-second default timeout: why, and at what price.</b><br/>
• `send()` is often called on the critical path of a user HTTP request. Without a timeout, a slow hub piles up pending requests, blows up p99 latency and can trigger a <i>cascading failure</i>.<br/>
• 5 s is a generous default: for an API with a p99 SLO under 500 ms, lower `http.timeout` (for example 1000 ms). `timeout: 0` disables the protection: avoid it in production.<br/>
• Better still: move publishing off the critical path (queued job, <i>outbox pattern</i>) so hub latency never affects the user.""",
"""<b>Test double (FakeMercure) vs mocking `fetch`.</b><br/>
• The <i>fake</i> is extra code to maintain and it can <i>drift</i> from real behavior. In return, application tests express intent (“topic X received Y”) and do not depend on the HTTP shape (URL, form encoding, headers).<br/>
• Mocking `fetch` costs no code, but couples every test to the transport implementation: an internal change in the package would break the tests of all its users.<br/>
• The package keeps both levels: a `fetch` mock to test <i>Publisher</i> (that is the boundary) and `FakeMercure` for consumers. A <i>contract test</i> against a real hub (Docker) would limit the drift risk.""",
]
FW_ROWS=[['Concept in this package','Universal pattern','AdonisJS (here)','NestJS','Express / Fastify'],
['MercureProvider + container.singleton','IoC container, DI, <b>Singleton</b> scope, <i>composition root</i>','Provider.boot() registers a lazy singleton','Module provider (<code>useFactory</code>), singleton scope by default','Express: instance exported from a module. Fastify: <code>fastify.decorate()</code> in a plugin'],
['MercureContract + FakeMercure','<b>Dependency Inversion</b> (DIP), <b>Strategy</b> pattern, <b>test double</b>','interface + <code>container.swap()</code>','<code>overrideProvider()</code> in <code>Test.createTestingModule</code>','Manual injection (parameter / factory) or overriding the decoration in tests'],
['configure.ts + stubs + codemods','<b>CLI scaffolding</b>, <b>AST</b> modification (codemods)','<code>node ace configure</code> (codemods)','Schematics (<code>nest g</code>)','<code>create-*</code>, jscodeshift / ts-morph, or manual steps'],
['defineConfig() (boot-time validation)','<b>Fail-fast</b> typed configuration','<code>defineConfig</code> + <code>start/env.ts</code>','<code>ConfigModule.forRoot({ validate })</code> (Joi / zod)','zod, envalid; <code>@fastify/env</code> (JSON Schema)'],
['services/mercure.ts','<b>Facade</b> / service locator (lazy singleton)','service import','Constructor injection (no facade)','Import of a singleton module or <code>fastify.mercure</code>'],
['MercureError hierarchy','Typed domain errors, <b>error boundary</b>','<code>instanceof</code> + global handler','Exception filters (<code>@Catch</code>)','Error middleware / <code>setErrorHandler</code>'],
['Publisher: fetch + AbortController','Outbound call with a <b>timeout</b> (deadline propagation)','native <code>fetch</code>','<code>HttpModule</code> (axios) or RxJS <code>timeout()</code>','<code>undici</code> / <code>fetch</code> + signal'],
['peerDependency @adonisjs/core','<b>Peer dependency</b>: the host provides the framework','<code>^6.2 || ^7</code>','<code>@nestjs/common</code> as a peer','<code>express</code> / <code>fastify</code> as a peer'],
]
FW_CODE_NEST='''// ILLUSTRATIVE (not in the repo): reusing the core in NestJS
@Module({
  providers: [{ provide: 'MERCURE', useFactory: () => new Mercure(defineConfig(config)) }],
  exports: ['MERCURE'],
})
export class MercureModule {}

// Fastify
fastify.decorate('mercure', new Mercure(defineConfig(config)))

// Express
export const mercure = new Mercure(defineConfig(config))   // a module is a singleton'''
def qa(n,q,d,j,l):
    return [KeepTogether([P('Q%d. %s'%(n,q),'q'),P('<b><font color="#16a34a">Direct answer (30 s)</font></b> — '+bt(d))]),
            P('<b><font color="#2563eb">Technical justification</font></b> — '+bt(j)),
            P('<b><font color="#ea580c">Limit / Possible improvement</font></b> — '+bt(l))]
QA_CA=[
("System design: how would you handle 50,000 simultaneous connections with this setup?",
 "The package is not the bottleneck: the application only sends one short POST per event. The 50,000 long-lived connections are carried by the Mercure hub, which scales horizontally behind a load balancer, not by the Node workers.",
 "Points of attention: (1) file-descriptor limits (`ulimit -n`) and memory per connection on the hub; (2) one EventSource per tab with several topics, over HTTP/2, to avoid the ~6 connections per domain limit of HTTP/1.1; (3) proxy: `proxy_buffering off`, a high `proxy_read_timeout`, heartbeats; (4) several hub instances need a shared <i>transport</i> (depending on the hub edition: Bolt locally, or an HA edition with an external transport): check the docs of the deployed version; (5) after a deploy or an outage, a mass reconnection (<i>thundering herd</i>): client-side jitter and slow rolling deploys.",
 "The repo has no load test or benchmark: I would not promise a number without testing (k6/Artillery with 50k simulated clients, hub memory and CPU metrics). On the package side, `sendBatch` (roadmap) would reduce the number of POSTs under heavy publishing."),
("SSE or WebSocket: which one would you pick in production, and why?",
 "SSE when the flow is mostly server → client (notifications, statuses, dashboards): it is standard HTTP, simpler to operate and to secure. WebSocket when you need low-latency bidirectional traffic (games, collaborative editing).",
 "Costs: SSE reuses the existing HTTP infrastructure (proxies, WAF, cookie auth), reconnection and `Last-Event-ID` are native, and there is no application protocol to maintain. WebSocket often needs sticky sessions, an application heartbeat, and explicit handling of reconnection and backpressure. Both use one long-lived connection per client; the difference is operational complexity.",
 "SSE limits: unidirectional, UTF-8 only, per-domain connection limit on HTTP/1.1. If the need becomes bidirectional, keep SSE for push and use HTTP requests for upstream, or migrate to WebSocket."),
("`send()` is called inside a user request and the hub is slow or down: what happens?",
 "The call is bounded by a timeout (5 s by default, `http.timeout`) and fails with a typed error: `MercureTimeoutError`, `MercureConnectionError` or `MercurePublishError`. The caller decides what to do: ignore, log or retry.",
 "Without a timeout, requests pile up, p99 explodes and a cascading failure becomes possible. The real issue is the <i>dual write</i>: if the database transaction commits but the publish fails, state and notifications diverge. Solutions: publish after the commit and treat failure as acceptable degradation, or use an <i>outbox pattern</i> (write the event to the database in the same transaction, then a worker publishes it with retry).",
 "5 s is too long for an aggressive p99 SLO: configure it (for example 1 s) or move publishing off the critical path with a queue (BullMQ, etc.). The package provides neither retry nor a circuit breaker (see next question)."),
("The package has no retry. How would you implement it properly?",
 "A wrapper around `send()` with <i>exponential backoff + jitter</i>, limited to a few attempts, that retries only transient errors: `MercureTimeoutError`, `MercureConnectionError`, and `MercurePublishError` with a 5xx status (possibly 429). No retry on 4xx such as 401/403/400: those are config or payload bugs.",
 "Typed errors make the retry policy trivial to write without parsing text. You need a <i>retry budget</i> (total duration below the request SLO); otherwise retry asynchronously through a queue. Delivery semantics: a retry can duplicate a message (at-least-once); passing a stable `id` lets clients deduplicate. To avoid hammering a sick hub, add a <i>circuit breaker</i> (for example opossum): after N failures, short-circuit and degrade.",
 "It should live in the package (roadmap item “Retry with backoff”) with an option such as `retry: { attempts, baseDelay, retryOn }`, plus a test double able to simulate outages (`failNext(error)`), which `FakeMercure` cannot do today. Note also that the hub does not guarantee deduplication: consumers must be idempotent."),
("Observability: what would you measure and how?",
 "A latency histogram around `send()`, an error counter per class (`MercureTimeoutError`, `MercureConnectionError`, `MercurePublishError` + status), the number of published messages, and an OpenTelemetry span per call. Alerts on error rate and p99 latency.",
 "Typed errors give clean metric labels (controlled cardinality). `ping()` works as a health probe, but beware: using it as a <i>liveness</i> probe would restart the whole app whenever the hub goes down. Expose it as a “degraded” <i>readiness</i> signal or in an informational health endpoint, consistent with graceful degradation. For logs: `MercurePublishError.responseBody` is truncated to 200 characters so that sensitive data does not leak.",
 "Today the package emits no logs or metrics: you instrument through an application-level wrapper. Improvement: accept a logger and hooks (`onPublish`, `onError`) or expose events so Prometheus / OpenTelemetry can plug in without a hard dependency."),
("Security: which JWT vulnerabilities do you know, and how does the package protect against them?",
 "Main ones: <b>`alg: none`</b>, <b>algorithm confusion</b> (HS256 vs RS256), <b>weak secrets</b> (offline brute force on HS256), <b>tokens without expiry</b>, <b>overly broad claims</b> (wildcard), and <b>tokens in the URL</b> (leaked in logs). The package enforces an algorithm allow-list (HS/RS 256-384-512, never `none`) and a secret of at least 32 characters, both checked at boot.",
 "Token verification is done by the hub, not by the package: we only <i>sign</i>. The admin token (`publish: [\"*\"]`) must never leave the server (<i>least privilege</i>); subscriber tokens should list precise topics with a short TTL (`expiresIn`). The secret comes from the environment, never from the code; `configure.ts` leaves the values empty on purpose.",
 "Remaining weaknesses: `expiresIn` is optional (no default), there is no revocation before `exp`, and no secret rotation. Improvements: mandatory TTL, `kid` support for key rotation, and a regression test proving that a token signed with another algorithm is rejected."),
("A subscriber token is visible on the client: what are the risks and how do you reduce them?",
 "The main risk is token theft (XSS, malicious extension, logs). Limit the impact with a minimal-scope token (precise topics), a short TTL, and delivery through an `HttpOnly` cookie rather than storing it in JavaScript.",
 "`EventSource` cannot send an `Authorization` header, so there are two options: a cookie set by the app (with `response.plainCookie`, because `response.cookie` signs the value and the hub would reject it) or a `fetch`-based library with a Bearer header. An `HttpOnly` cookie cannot be read by JavaScript: an XSS cannot exfiltrate it, although it can still send authenticated requests from the page. Never pass the token in the query string (it ends up in logs and referrers).",
 "A stolen token stays valid until expiry (no revocation): hence the short TTL and a renewal endpoint. Defense in depth: strict CSP, input sanitization, and monitoring of abnormal access on the hub."),
("CORS and `__Secure-` cookies: what can go wrong with `EventSource`?",
 "If the hub is on another origin, you need `withCredentials: true` on the client and, on the hub, a CORS configuration that lists the exact origin and allows credentials: a `*` wildcard is rejected when credentials are used. A `__Secure-` cookie requires HTTPS and the `Secure` attribute.",
 "The cookie must reach the hub: same <i>site</i> (for example `app.example.com` and `hub.example.com`, with `domain: '.example.com'`); `SameSite=Lax` is enough between subdomains of the same site, whereas a hub on a different site needs `SameSite=None; Secure`. The `__Host-` prefix is impossible for a cookie shared across subdomains (it forbids the `Domain` attribute). In local HTTP development, use a cookie name without the prefix and `secure: false`.",
 "A frequently forgotten point: the route that issues the token must check that the user is allowed to subscribe to that topic (access control / IDOR). The README example builds the topic from `params.id` without this check: in production, verify authorization before calling `generateSubscribeToken`."),
("Why create a `FakeMercure` instead of mocking `fetch` in the client application?",
 "Because `fetch` is an implementation detail of the package. A test double at the level of the <i>contract</i> (`MercureContract`) tests business intent (“topic `/orders/42` received `{status:'shipped'}`”) and stays stable if the transport changes.",
 "With a `fetch` mock, every test would know the URL, the `x-www-form-urlencoded` encoding, the headers and the shape of the response: an internal refactor would break all consumers. `FakeMercure` implements the same interface (checked by the compiler) and is plugged in with `container.swap()`, so application code does not change (Dependency Inversion). It compares data through `JSON.parse(JSON.stringify())` to reflect what the hub would really receive.",
 "Risk of drift between the fake and the real thing: `FakeMercure` always returns `'fake-token'`, `ping()` is always `true`, and it simulates no failure. Improvements: a contract test run against both implementations, an integration test with a real hub in Docker (Testcontainers), and `failNext(error)` to test error paths."),
("You changed `send()` to return an id instead of a `Response` (v3.0.0). How did you handle this breaking change?",
 "It was a deliberate breaking change: a major version (SemVer 3.0.0), an explicit CHANGELOG entry with migration instructions, and a reminder that classes implementing `MercureContract` must change their return type.",
 "Returning a `Response` leaked a transport detail into the public API and forced every caller to read the body. Returning a domain value (the id) lets us change the implementation (another HTTP client, retry, batching) without another breaking change. Since the contract is a public type, any signature change also affects external implementers.",
 "We could have run a deprecation cycle (old and new API side by side during a minor version) or shipped a migration codemod. With few users, a direct major was an acceptable trade-off; with a large installed base I would choose deprecation."),
("Delivery guarantees: what happens if a client is offline or two instances publish at the same time?",
 "Do not assume exactly-once delivery. Mercure offers replay through `Last-Event-ID` from the history kept by the hub, but a client disconnected for too long can lose messages. So I treat push as an <i>invalidation signal</i> and the database as the <i>source of truth</i>.",
 "In practice: on (re)connection the client refetches the current state, then applies the events it receives; messages carry an `id` for deduplication, and consumers are idempotent (at-least-once). Ordering is only reasonably guaranteed per topic and per hub; do not build logic that depends on global ordering across topics. The details (history size, transport durability) depend on the hub configuration and edition: confirm them in its documentation.",
 "The package handles neither persistence nor delivery guarantees: that is the responsibility of the hub and of the application design. Improvement: document this consistency model and provide a resync-on-reconnect example."),
("If the company uses NestJS or Fastify instead of AdonisJS, what do you reuse from this work?",
 "Almost the whole core: `Mercure`, `Publisher`, `TokenGenerator`, `defineConfig`, the errors and `FakeMercure` import nothing from AdonisJS. Only the provider, `configure.ts`, `services/mercure.ts` and `types/extended.ts` are AdonisJS-specific.",
 "That is the payoff of separation of concerns: the core is a class with one injected dependency (the config) and a contract (`MercureContract`). In NestJS you expose it through a provider (`useFactory`); in Fastify with `decorate()`; in Express as a module singleton. The patterns (IoC, singleton, DIP, fail-fast, scaffolding) are the same; only the glue changes (see the mapping table, section 3).",
 "Today the package ships the AdonisJS provider in the same artifact. Improvement: extract a framework-agnostic core package (`mercure-core`) and thin per-framework adapters, which would widen the audience."),
]
CHECK_ROWS=[['Keyword','How to place it naturally'],
['trade-off','“The trade-off is operational complexity versus keeping the app stateless.”'],
['stateless / horizontal scaling','“Keeping the app stateless lets us scale horizontally behind the load balancer.”'],
['fail-fast vs graceful degradation','“Config errors fail fast at boot; a hub outage degrades gracefully.”'],
['blast radius','“Publishing out of the request path limits the blast radius of a hub outage.”'],
['timeout / retry budget / backoff / jitter','“I’d retry only transient errors, with exponential backoff and jitter, within a retry budget.”'],
['circuit breaker','“A circuit breaker avoids hammering a failing hub.”'],
['idempotency / at-least-once','“Delivery is at-least-once, so consumers must be idempotent.”'],
['dual write / outbox pattern','“To avoid the dual-write problem I’d use an outbox.”'],
['source of truth','“The database stays the source of truth; push is just an invalidation signal.”'],
['thundering herd','“After a deploy, clients reconnect at once, so we add jitter.”'],
['observability (metrics, logs, traces)','“Typed errors give clean metric labels for observability.”'],
['SLO / p99 latency','“A 5s default is too loose for a p99 SLO, so I’d lower it.”'],
['least privilege / defense in depth','“Subscriber tokens are scoped to specific topics: least privilege.”'],
['dependency inversion / test double','“I depend on the contract, not on fetch, so a test double is enough.”'],
['contract test','“I’d add a contract test run against both the real and the fake.”'],
['breaking change / deprecation cycle','“It was a deliberate breaking change; with more users I’d use a deprecation cycle.”'],
['peer dependency','“The framework is a peer dependency, so we don’t ship a duplicate.”'],
]

def cover(c,doc):
    c.saveState()
    c.setFillColor(colors.HexColor('#0b1b4d')); c.rect(0,0,A4[0],A4[1],fill=1,stroke=0)
    c.setFillColor(BLUE); c.rect(0,A4[1]-14*mm,A4[0],14*mm,fill=1,stroke=0)
    c.setStrokeColor(colors.HexColor('#3b82f6')); c.setLineWidth(1.2)
    for k in range(5):
        c.setStrokeAlpha(0.5-0.08*k)
        p=c.beginPath(); y0=60*mm+k*9*mm; p.moveTo(0,y0)
        for x in range(0,int(A4[0])+10,10): p.lineTo(x,y0+8*math.sin(x/28+k))
        c.drawPath(p,stroke=1,fill=0)
    c.restoreState()
def later(c,doc):
    c.saveState(); c.setFont('DV',7.5); c.setFillColor(MUTED)
    c.drawString(18*mm,10*mm,'adonis-mercure — Technical interview preparation (Canada)')
    c.drawRightString(A4[0]-18*mm,10*mm,'Page %d'%doc.page)
    c.setStrokeColor(colors.HexColor('#e5e7eb')); c.line(18*mm,14*mm,A4[0]-18*mm,14*mm); c.restoreState()

OUT='/home/user/adonis-mercure/docs/adonis-mercure-guide-ca-en.pdf'
doc=BaseDocTemplate(OUT,pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=16*mm,bottomMargin=20*mm,
    title='adonis-mercure — Technical interview preparation (Canada)',author='Guide for Michael DAŞ')
doc.addPageTemplates([PageTemplate('cover',[Frame(22*mm,30*mm,A4[0]-44*mm,A4[1]-80*mm,id='c')],onPage=cover),
                      PageTemplate('main',[Frame(18*mm,20*mm,W,A4[1]-36*mm,id='m')],onPage=later)])
st=[]
st+= [Spacer(1,55*mm),P('@mdsiha369/<br/>adonis-mercure','cover1'),Spacer(1,8),
 P('Technical interview preparation (Canada): system design, trade-offs and production pragmatism','cover2'),Spacer(1,62*mm),
 P('npm package for AdonisJS 6 / 7 · TypeScript · Mercure (SSE) · JWT<br/>Project author: Michael DAŞ · MIT license · version 3.0.0<br/>Intermediate / senior posture · professional English · French vocabulary help','cover2'),NextPageTemplate('main'),PageBreak()]

# 1
st+=[H1('1. The project in 30 seconds'),
P('<b>adonis-mercure</b> is an <b>npm package</b> written in TypeScript that bridges a web application built on the <b>AdonisJS</b> framework and a <b>Mercure Hub</b>. It allows the backend to <b>push real-time updates</b> (a notification, an order status, a chat message…) to its users’ browsers without those browsers having to ask for them. The hub, a dedicated server, takes care of fanning the messages out to every connected client.'),
*trade(TRADE[0]),
*vocab([('to push', 'envoyer de façon proactive'), ('to fan out', 'diffuser à de nombreux clients'), ('bridge', 'faire le lien'), ('seamless', 'fluide, sans couture'), ('robustness', 'robustesse'), ('happy path', 'scénario nominal')]),
H2('What the package gives you (5 things)'),
*table([['Feature','What it is for'],
['send()','Publish a message on one or more “topics” (channels), public or private.'],
['generateSubscribeToken() / generate()','Create JWTs (signed badges) so that browsers can listen to private channels.'],
['ping()','Check that the hub is alive (health check).'],
['FakeMercure','A fake Mercure to test your code without a real hub (assertSent, etc.).'],
['configure / defineConfig / Provider','Install in one command, check the configuration, plug everything into AdonisJS.']],[55*mm,W-55*mm]),
H2('Pitch to say out loud (30 seconds)'),
P('<i>“I designed and published an npm package that integrates the Mercure protocol into AdonisJS. It enables a backend to push real-time updates to browsers over Server-Sent Events, with access control based on JWTs. Beyond the happy path, I paid attention to robustness: fail-fast configuration validation, request timeouts, a typed error hierarchy and an in-memory fake for testing. The package is covered by Japa tests, verified in CI across Node 20 and 22 on Linux and Windows, and is compatible with both AdonisJS 6 and 7.”</i>'),
*tip('Memorise the structure of this pitch (what / how / quality), not every word. Interviewers care less about the feature list than about the <b>reasoning</b> behind each decision, so every section of this guide spells out the “why”.'),
PageBreak()]

# 2
st+=[H1('2. Core concepts (an engineer’s view)'),
H2('2.1 What is “real time” and why is it a problem?'),
P('HTTP is fundamentally a request–response protocol: the browser <b>asks</b>, the server <b>answers</b>, and the server cannot initiate a conversation. Yet a chat, a parcel-tracking page or a live dashboard needs the opposite: the server must <b>notify</b> the client the moment something changes. Three techniques address this problem:'),
*fig(d_proto(),'Figure 1 — Three ways to do “real time”'),
*B(['<b>Polling</b>: the client re-sends the same request every few seconds. It is trivial to implement, but it is wasteful (most responses are empty) and latency is bounded by the polling interval.',
'<b>SSE (Server-Sent Events)</b>: the client opens <i>a single</i> long-lived HTTP connection and the server streams events through it whenever it likes. It is unidirectional (server → browser), reconnects automatically and plays well with existing HTTP infrastructure. <b>This is what Mercure builds on.</b>',
'<b>WebSocket</b>: a full-duplex channel. More powerful, but it needs its own protocol upgrade, and it is harder to load-balance, authenticate and monitor.']),
*trade(TRADE[1]),
*vocab([('latency', 'latence'), ('long-lived', 'de longue durée'), ('full-duplex', 'bidirectionnel simultané'), ('wasteful', 'inefficace'), ('to initiate', 'déclencher'), ('to address (a problem)', 'traiter (un problème)')]),
H2('2.2 Mercure and its “Hub”'),
P('<b>Mercure</b> is an open protocol (mercure.rocks) layered on top of SSE. A <b>Mercure Hub</b> is a standalone server (written in Go, typically run with Docker or as a Caddy module) that does the heavy lifting: it maintains thousands of open connections, routes each message to the right subscribers and enforces authorization. Your application merely sends <b>one plain HTTP POST</b> to the hub. The key benefit is architectural: your Node process stays lightweight and stateless, because it never has to track who is connected.'),
P('There are two roles:'),
*B(['<b>Publisher</b>: the one who sends messages. Here it is the AdonisJS application, with an <b>admin JWT</b>.',
'<b>Subscriber</b>: the one who listens. Here it is the browser, with an <b>EventSource</b>. For private messages it must show a <b>subscriber JWT</b>.']),
H2('2.3 “Topics”'),
P('A <b>topic</b> is simply the <b>name of a channel</b>, usually modelled as a URL-like identifier: ' + M('/orders/42') + ', ' + M('/chat/room/7') + ' or ' + M('/notifications/user/1') + '. A publisher posts to a topic and every client subscribed to it receives the update. A single update can target several topics at once.'),
*trade(TRADE[2]),
*vocab([('stateless', 'sans état'), ('to enforce', 'faire respecter'), ('to route', 'acheminer'), ('lightweight', 'léger'), ('standalone', 'autonome'), ('heavy lifting', 'le gros du travail')]),
H2('2.4 JWT (JSON Web Token)'),
P('A <b>JWT</b> is a compact, self-contained credential made of three dot-separated parts (header . payload . signature). The payload carries <i>claims</i>, for instance “this bearer may subscribe to ' + M('/orders/42') + '”. The <b>signature</b> is computed with a <b>secret</b> shared only by the application and the hub, so a token cannot be forged or tampered with without that secret. Note that the payload is merely encoded, not encrypted: never put sensitive data in it.'),
*fig(d_jwt(),'Figure 2 — Anatomy of a Mercure JWT (the “mercure” key contains the rights)'),
*trade(TRADE[3]),
*vocab([('claim', 'revendication / information du jeton'), ('to forge', 'falsifier'), ('to tamper with', 'altérer'), ('self-contained', 'autonome'), ('bearer', 'porteur'), ('to mint (a token)', 'émettre un jeton')]),
H2('2.5 AdonisJS, package, provider, container'),
*B(['<b>AdonisJS</b>: a web framework for Node.js in TypeScript (like Laravel for PHP). Versions 6 and 7 are supported.',
'<b>npm package</b>: reusable code published on the npm registry and installed with ' + M('npm install') + '.',
'<b>IoC container / dependency injection</b>: a “central toolbox” in AdonisJS. You <i>register</i> objects in it (for example “mercure”) and you <i>ask for</i> them elsewhere without building them by hand.',
'<b>Provider</b>: a class with lifecycle methods (' + M('register') + ', ' + M('boot') + '…). It registers our objects in the container when the app starts.',
'<b>Singleton</b>: the object is created <b>only once</b> and reused everywhere.',
'<b>Ace</b>: the AdonisJS command line. ' + M('node ace configure') + ' runs the installation script of the package.']),
PageBreak()]

# 3
st+=[H1('3. The big picture: how everything fits together'),
*fig(d_big(),'Figure 3 — The three actors: browser, AdonisJS application (with the package) and Mercure Hub'),
P('My package covers only the “application → hub” leg (step ①) and the minting of subscriber tokens (step ③). The browser connects to the hub directly (step ②) using the standard ' + M('EventSource') + ' API, so I deliberately did <b>not</b> have to build or operate a real-time server. Delegating that responsibility to Mercure is the central design idea.'),
H2('Inside the package'),
*fig(d_arch(),'Figure 4 — The classes of the package and who calls whom'),
*B(['<b>Mercure</b> is the public <b>facade</b>. It contains almost no logic of its own and <i>delegates</i> to the collaborators below.',
'<b>Publisher</b> owns everything related to the outbound HTTP request to the hub.',
'<b>TokenGenerator</b> owns JWT creation and signing.',
'<b>MercureContract</b> is a TypeScript <b>interface</b> (a “contract”) exposing ' + M('send, generate, generateSubscribeToken, ping') + '. Both <b>Mercure</b> and <b>FakeMercure</b> implement it, which makes them interchangeable and keeps the fake honest: if the real API changes, the compiler flags the fake.']),
*tip('Design patterns to mention: <b>Facade</b> (Mercure), <b>Separation of concerns / Single Responsibility</b> (Publisher vs TokenGenerator), <b>Dependency injection + Singleton</b> (provider), <b>Test double / Fake</b> (FakeMercure), <b>Interface contract</b> (MercureContract), <b>Fail fast</b> (defineConfig checks at startup).'),
*vocab([('to delegate', 'déléguer'), ('collaborator', 'objet collaborateur'), ('interchangeable', 'interchangeable'), ('to flag', 'signaler'), ('deliberately', 'délibérément'), ('leg (of a journey)', 'tronçon')])]

# 4

FW=[[Paragraph(c.replace('<code>','<font face="DVM" size="7.3" color="#be123c">').replace('</code>','</font>'),S['cellh'] if i==0 else S['cell']) for c in r] for i,r in enumerate(FW_ROWS)]
_fwt=Table(FW,colWidths=[30*mm,34*mm,28*mm,38*mm,W-130*mm],repeatRows=1)
_fwst=[('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#d1d5db')),('BACKGROUND',(0,0),(-1,0),BLUE),
 ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4)]
for _i in range(2,len(FW_ROWS),2): _fwst.append(('BACKGROUND',(0,_i),(-1,_i),GREY))
_fwt.setStyle(TableStyle(_fwst))
st+=[PageBreak(),H2('Framework abstraction: these patterns are universal'),
P('In Canada, <b>NestJS, Express and Fastify</b> dominate the Node.js ecosystem. Nothing implemented here is specific to AdonisJS: only the “wiring” (provider, configure, service) is. The table below maps each building block to the other frameworks. In an interview, talk about the <b>pattern</b> first and the framework second.'),
_fwt,Spacer(1,8),
*callout('Framework-agnostic core vs framework-specific glue',bt('The files `src/mercure.ts`, `publisher.ts`, `token_generator.ts`, `define_config.ts`, `fake_mercure.ts` and `src/errors/*` <b>import nothing from AdonisJS</b> (only `src/types/extended.ts` touches the framework types). Only <b>the provider, `configure.ts`, `services/mercure.ts` and `extended.ts`</b> are specific. Consequence: porting the package to NestJS or Fastify only needs a thin adapter layer.'),LBLUE,BLUE),
*code(FW_CODE_NEST,'Illustrative: reusing the core elsewhere'),
*tip('Portability pitch: <i>“The core is framework-agnostic. The only AdonisJS-specific parts are the provider, the configure hook and the service import. Everything else is plain TypeScript, so porting it is mostly wiring.”</i>')]
st+=[PageBreak(),H1('4. Guided tour of the repository'),
*table([['File','Role'],
['index.ts','Entry point of the package: re-exports everything public (classes, errors, types).'],
['configure.ts','Runs with ' + M('node ace configure') + ': creates config/mercure.ts, adds .env variables and env validation, registers the provider.'],
['stubs/config/mercure.stub','Template of the config/mercure.ts file created in the user’s project.'],
['stubs/main.ts','Exports ' + M('stubsRoot') + ': the path of the stubs folder.'],
['providers/mercure_provider.ts','Registers the “mercure” singleton in the container at startup.'],
['services/mercure.ts','Import shortcut ' + M('import mercure from \'…/services/main\'') + ': gets the instance from the container.'],
['src/mercure.ts','The Mercure facade (send, generate, generateSubscribeToken, ping).'],
['src/publisher.ts','Builds and sends the POST request to the hub; handles timeout and errors.'],
['src/token_generator.ts','Signs JWTs with the jws library; handles expiresIn.'],
['src/define_config.ts','Validates the configuration (allowed algorithm, URL, token, secret length).'],
['src/fake_mercure.ts','Fake Mercure for tests: records what is sent and offers assertions.'],
['src/errors/*.ts','5 typed error classes (MercureError + 4 specific ones).'],
['src/types/main.ts','Public types: MercureConfig, SendOptions, TokenOptions, MercureContract…'],
['src/types/extended.ts','Tells TypeScript that the AdonisJS container contains “mercure” (auto-completion).'],
['tests/*.spec.ts','7 Japa test files (about 700 lines).'],
['.github/workflows','CI (test.yml) and npm publication (npm-publish.yml).'],
['tsconfig*.json, tsnode.esm.js, bin/test.ts','TypeScript compilation; running tests with ts-node + SWC.']],[52*mm,W-52*mm]),
H2('The “exports” of package.json'),
*code('''"exports": {
  ".": "./build/index.js",                  // import { defineConfig } from '@mdsiha369/adonis-mercure'
  "./types": "./build/src/types/main.js",   // types only
  "./services/main": "./build/services/mercure.js",   // import mercure from '…/services/main'
  "./mercure_provider": "./build/providers/mercure_provider.js"
}''','package.json'),
P('This table tells Node which files other people may import. Only the ' + M('build') + ' folder (TypeScript compiled to JavaScript) is published on npm (' + M('"files": ["build"]') + '). This keeps the package small (about 9 kB).'),
*vocab([('entry point', 'point d’entrée'), ('to re-export', 'réexporter'), ('consumer', 'utilisateur (du package)'), ('footprint', 'empreinte (taille)'), ('template', 'modèle'), ('to scaffold', 'générer une structure')]),
PageBreak()]

# 5
st+=[H1('5. Installation and startup, step by step'),
*fig(d_boot(),'Figure 5 — From “npm install” to the first use'),
H2('Step 1 — ' + M('node ace configure')),
P('The script ' + M('configure.ts') + ' uses <b>codemods</b> (“robots that edit the source code of the user”):'),
*code('''export async function configure(_command: ConfigureCommand) {
  const codemods = await _command.createCodemods()

  await codemods.makeUsingStub(stubsRoot, 'config/mercure.stub', {})   // creates config/mercure.ts
  await codemods.defineEnvVariables({ MERCURE_ENDPOINT: 'http://localhost:3000/.well-known/mercure',
                                      MERCURE_ADMIN_JWT: '', MERCURE_JWT_SECRET: '' })   // .env
  await codemods.defineEnvValidations({ ... })                         // start/env.ts
  await codemods.updateRcFile((rc) => rc.addProvider('@mdsiha369/adonis-mercure/mercure_provider'))
}''','configure.ts (shortened)'),
P('Note: ' + M('MERCURE_ADMIN_JWT') + ' and ' + M('MERCURE_JWT_SECRET') + ' are <b>empty on purpose</b>. In an old version, a default secret was written in the code. That was a security hole. It was fixed in 2.0.1: empty values force developers to set real secrets before the app starts.'),
H2('Step 2 — ' + M('defineConfig()') + ': the guard'),
P('The generated file calls ' + M('defineConfig({...})') + '. The function is essentially an identity function with validation: it <b>verifies</b> the configuration and returns it untouched. If anything is invalid, the application <b>refuses to boot</b>. This is the “fail fast” principle: a misconfiguration should blow up at startup, not surface weeks later in production.'),
*code('''export function defineConfig<T extends MercureConfig>(config: T): T {
  if (!ALLOWED_ALGORITHMS.includes(config.jwt.alg))   // allow-list: no "none"!
    throw new MercureConfigError(`Algorithm "${config.jwt.alg}" is not allowed...`)
  if (!isHttpUrl(config.endpoint))
    throw new MercureConfigError('endpoint must be a valid http(s) URL')
  if (!config.adminToken)
    throw new MercureConfigError('adminToken must not be empty')
  if (config.jwt.secret.length < 32)
    throw new MercureConfigError('jwt.secret must be at least 32 characters long')
  return config
}''','src/define_config.ts'),
*trade(TRADE[4]),
*warn('Why forbid the algorithm <b>none</b>? A famous JWT security hole was to write “alg: none” (“no signature”) to create fake tokens. The allow-list (HS256/384/512 and RS256/384/512) stops this.'),
H2('Step 3 — The provider'),
*code('''export default class MercureProvider {
  constructor(protected app: ApplicationService) {}

  async boot() {
    this.app.container.singleton('mercure', async () => {
      const config = this.app.config.get<MercureConfig | undefined>('mercure')
      if (!config?.endpoint || !config?.adminToken || !config?.jwt?.secret) {
        throw new MercureConfigError('Missing or incomplete Mercure config. Run "node ace configure"')
      }
      return new Mercure(config)
    })
  }
}''','providers/mercure_provider.ts'),
P('During startup, AdonisJS invokes ' + M('boot()') + '. Here we register a factory: “whenever <b>mercure</b> is requested, build a ' + M('new Mercure(config)') + ' <i>once</i> and cache it”. Instantiation is <b>lazy</b>, i.e. deferred until the first time the service is actually resolved, and the config check lives inside that factory.'),
H2('Step 4 — The service (the import shortcut)'),
*code('''let mercure: Mercure
await app.booted(async () => {            // top-level await: wait until the app has finished starting
  mercure = await app.container.make('mercure')
})
export { mercure as default }''','services/mercure.ts'),
P('Thanks to this file, consumers simply write ' + M("import mercure from '@mdsiha369/adonis-mercure/services/main'") + ' and receive a ready-to-use instance. It follows the conventional “service” pattern of the AdonisJS ecosystem.'),
P('One last detail: ' + M('src/types/extended.ts') + ' “augments” the AdonisJS type ' + M('ContainerBindings') + ' (module augmentation), so ' + M("container.make('mercure')") + ' has the right type.'),
*vocab([('misconfiguration', 'mauvaise configuration'), ('to blow up', 'exploser, planter'), ('lazy / deferred', 'différé'), ('to resolve (a service)', 'obtenir (un service)'), ('allow-list', 'liste blanche'), ('bouncer', 'videur')]),
PageBreak()]

# 6
st+=[H1('6. The core: publishing a message with send()'),
*fig(d_seq(),'Figure 6 — Full sequence of a send() call'),
H2('6.1 The facade: two ways to call it'),
*code('''send(topics, data = {}, isPrivateOrOptions: boolean | SendOptions = false) {
  const options: SendOptions =
    typeof isPrivateOrOptions === 'boolean' ? { private: isPrivateOrOptions } : isPrivateOrOptions
  return this.#publisher.publish(topics, data, options)
}''','src/mercure.ts'),
P('The third argument may be a plain boolean (the legacy API: ' + M("send('/x', data, true)") + ') or an options object. We normalise both into the object form, which preserves <b>backward compatibility</b> without cluttering the internals.'),
P('Note: the <b>#</b> in ' + M('#publisher') + ' is a <b>native private field</b> of JavaScript (ES2022). It is really impossible to reach from outside. It is stricter than the TypeScript keyword ' + M('private') + ', which disappears after compilation.'),
H2('6.2 The Publisher: build and send the request'),
*code('''const form = new URLSearchParams()
for (const topic of topicList) form.append('topic', topic)       // one "topic" field per channel
form.append('data', JSON.stringify(data))                         // the content, as JSON text
if (options.private) form.append('private', 'on')                 // private message
if (options.id)      form.append('id', options.id)                // SSE id
if (options.type)    form.append('type', options.type)            // event type
if (options.retry !== undefined) form.append('retry', String(options.retry))

const response = await fetch(this.#config.endpoint, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${this.#config.adminToken}`,
             'Content-Type': 'application/x-www-form-urlencoded' },
  body: form.toString(),
  signal: controller?.signal,        // allows us to cancel after N ms
})
if (!response.ok) throw new MercurePublishError(response.status, await response.text())
return (await response.text()).trim()    // the "urn:uuid:..." id sent back by the hub''','src/publisher.ts (shortened)'),
P('The Mercure specification expects <b>' + M('application/x-www-form-urlencoded') + '</b> (the encoding of ordinary HTML forms) rather than a JSON body, hence ' + M('URLSearchParams') + '. The actual payload (' + M('data') + ') is itself serialised to a JSON string.'),
H3('The timeout explained (AbortController)'),
*code('''const timeout = this.#config.http?.timeout ?? 5000          // 5 s by default, 0 = disabled
const controller = timeout > 0 ? new AbortController() : null
const timer = controller ? setTimeout(() => controller.abort(), timeout) : null
try { ... fetch(..., { signal: controller?.signal }) ... }
catch (err) {
  if (err instanceof MercureError) throw err                       // already one of our errors
  if (err?.name === 'AbortError') throw new MercureTimeoutError(timeout)
  throw new MercureConnectionError(err)                            // everything else = network
} finally { if (timer) clearTimeout(timer) }                       // always clean the timer''','src/publisher.ts'),
*trade(TRADE[5]),
H2('6.3 The SSE options'),
*table([['Option','Effect'],
['private: true','Only subscribers with a valid token for this topic receive the message.'],
['id','Event identifier. If the browser disconnects, it sends “Last-Event-ID” and the hub can replay what it missed.'],
['type','Event name; in the browser: addEventListener(\'order.shipped\', …).'],
['retry','Delay (ms) before the browser tries to reconnect.']],[35*mm,W-35*mm]),
*vocab([('legacy', 'hérité, ancien'), ('to normalise', 'normaliser'), ('to clutter', 'encombrer'), ('to serialise', 'sérialiser'), ('to abort', 'interrompre'), ('to cancel', 'annuler')]),
PageBreak()]

# 7
st+=[H1('7. Security and JWT tokens'),
H2('7.1 Two kinds of badges'),
*table([['Token','Who has it?','Right','Where it is used'],
['Admin JWT (adminToken)','The AdonisJS server only','publish: ["*"] — publish anywhere','Given in .env, sent in the Authorization header of send()'],
['Subscriber JWT','The user’s browser','subscribe: [allowed topics]','Created by generateSubscribeToken(), short life']],[32*mm,40*mm,45*mm,W-117*mm]),
H2('7.2 How a token is made'),
*code('''async generate(payload, options = {}) {
  const claims = { mercure: payload }              // Mercure wants the rights under the key "mercure"
  if (options.expiresIn !== undefined) {
    if (!Number.isInteger(options.expiresIn) || options.expiresIn <= 0)
      throw new MercureError('expiresIn must be a positive integer (seconds)')
    claims.exp = Math.floor(Date.now() / 1000) + options.expiresIn   // expiry date (UNIX seconds)
  }
  return new Promise((resolve, reject) => {
    jws.createSign({ payload: claims, secret: this.#config.jwt.secret,
                     header: { alg: this.#config.jwt.alg } })
       .on('error', reject).on('done', resolve)             // the jws library uses events
  })
}''','src/token_generator.ts'),
P('The <b>jws</b> library, the project’s only runtime dependency, signs the token. Its API is event-based (' + M('.on(\'done\')') + '), so we wrap it in a ' + M('Promise') + ' to make it ' + M('await') + '-able. ' + M('generateSubscribeToken(topics)') + ' is merely sugar for ' + M('generate({ subscribe: topics })') + '.'),
*warn('A token without ' + M('expiresIn') + ' <b>never</b> expires (documented choice, to stay compatible with Mercure). In production it is better to pass ' + M('{ expiresIn: 3600 }') + '. Another trap noted in the code: a wildcard topic ' + M('*') + ' gives access to all private events. Never put user input there without checking it.'),
H2('7.3 How the browser gives its token to the hub'),
P('A well-known limitation: the browser’s ' + M('EventSource') + ' <b>cannot</b> set custom headers such as ' + M('Authorization') + '. The README documents two workarounds:'),
*fig(d_cookie(),'Figure 7 — Option 1: the token travels in a cookie'),
*B(['<b>Cookie option</b>: the app puts the JWT in a cookie with ' + M('response.plainCookie') + ' (not ' + M('response.cookie') + ', which <i>signs</i> the value, so the hub would reject it). Conditions: same registrable domain (app.example.com + hub.example.com) and HTTPS for the ' + M('__Secure-') + ' prefix.',
'<b>Fetch option</b>: use ' + M('@microsoft/fetch-event-source') + '. It reads the stream with ' + M('fetch()') + ', so it accepts the ' + M('Authorization: Bearer …') + ' header.']),
H2('7.4 Other security choices in the project'),
*B(['<b>Truncation</b> of the error body to 200 characters in ' + M('MercurePublishError') + ': it avoids leaking big parts of a response (maybe sensitive) into logs.',
'<b>Secret of at least 32 characters</b> and <b>no “none” algorithm</b> (see section 5).',
'<b>No default secret</b> in configure.ts.',
'Secrets come from the environment (' + M('env.get(...)') + '), never from the code.']),
*vocab([('limitation', 'limite'), ('workaround', 'contournement'), ('to leak', 'fuiter'), ('to truncate', 'tronquer'), ('to expire', 'expirer'), ('trap / pitfall', 'piège')]),
PageBreak()]

# 8
st+=[H1('8. Errors, ping and testing without a hub'),
H2('8.1 A hierarchy of typed errors'),
*fig(d_err(),'Figure 8 — All errors inherit from MercureError'),
P('Why is it useful? Because the user of the package can <b>react differently</b> depending on the problem:'),
*code('''try {
  await mercure.send('/orders/42', { status: 'shipped' })
} catch (e) {
  if (e instanceof MercureTimeoutError)    { /* slow hub: try again later */ }
  else if (e instanceof MercurePublishError){ console.log(e.statusCode, e.responseBody) }
  else if (e instanceof MercureConnectionError) { console.log(e.cause) }   // e.g. ECONNREFUSED
}''','usage example'),
P('A subtle detail: on network failures ' + M('fetch()') + ' throws an unhelpful “TypeError: fetch failed” and buries the real reason (ECONNREFUSED, ENOTFOUND…) in ' + M('error.cause.code') + '. The ' + M('describe()') + ' helper in ' + M('MercureConnectionError') + ' digs it out to produce an actionable message, while preserving the original error in ' + M('cause') + '.'),
H2('8.2 ping()'),
P('It sends a ' + M('HEAD') + ' request (no response body) to the hub. Status <b>below 500</b> ⇒ true (even a 401/404 proves the hub answers). A 5xx, a network error or a timeout ⇒ false. It never throws an exception: it is a simple yes/no signal for a health check.'),
H2('8.3 FakeMercure: test without a server'),
P('Testing code that talks to an external server is slow, flaky and requires infrastructure. The remedy is a <b>fake</b>: an object that honours the same contract but simply <b>records</b> what it receives so that tests can assert on it.'),
*code('''export class FakeMercure implements MercureContract {
  #sent: SentMessage[] = []
  async send(topics, data = {}, opts = false) {
    this.#sent.push({ topics: asArray(topics), data, options: normalize(opts) })
    return options.id ?? `urn:uuid:${randomUUID()}`           // imitates the id of the real hub
  }
  assertSent(topic, data?) { /* throws an Error if no message matches */ }
  assertNotSent(topic)  { ... }   assertSentCount(n) { ... }   assertNothingSent() { ... }
  getSent() { return [...this.#sent] }    // a copy: the caller cannot change the internal state
  clear()   { this.#sent = []; this.#tokens = [] }
}''','src/fake_mercure.ts (shortened)'),
P('In the tests of the application: ' + M("app.container.swap('mercure', () => new FakeMercure())") + ' replaces the real one by the fake one. Then ' + M("fake.assertSent('/orders/42', { status: 'shipped' })") + ' checks the result. A quality detail: the data comparison uses ' + M('JSON.parse(JSON.stringify(...))') + ' to compare <i>what the hub would really receive</i> (key order does not matter; ' + M('undefined') + ' disappears).'),
*trade(TRADE[6]),
*vocab([('flaky', 'instable, peu fiable'), ('actionable', 'exploitable'), ('to dig out', 'déterrer'), ('to swallow (an error)', 'avaler (une erreur)'), ('to honour a contract', 'respecter un contrat'), ('to assert', 'vérifier / affirmer')]),
PageBreak()]

# 9
st+=[H1('9. Quality: tests, CI and publishing'),
H2('9.1 The tests (Japa)'),
P('Framework: <b>Japa</b> (the test framework of the AdonisJS ecosystem) with ' + M('@japa/assert') + '. Coverage is measured by <b>c8</b>. There are 7 files:'),
*table([['File','What it checks'],
['publisher.spec.ts','URL called, form body, Bearer header, options, returned id, 4xx/5xx errors, timeout, network error.'],
['mercure.spec.ts','Facade delegates to publisher/token, boolean vs options object, ping().'],
['token_generator.spec.ts','JWT structure, mercure claim, valid/invalid expiresIn.'],
['define_config.spec.ts','Forbidden algorithms, bad URLs, empty token, short secret are rejected.'],
['provider.spec.ts','Singleton registered, MercureConfigError if config is missing.'],
['configure.spec.ts','Codemods are called with the right arguments.'],
['fake_mercure.spec.ts','All assertions and their failure cases.']],[45*mm,W-45*mm]),
P('Key technique: each test <b>swaps</b> ' + M('globalThis.fetch') + ' for a stub and restores it in ' + M('teardown') + '. This lets us exercise Publisher <b>without any network</b>, which keeps the suite fast and deterministic (a form of <i>mocking</i>).'),
*code('''group.each.setup(() => { originalFetch = globalThis.fetch })
group.each.teardown(() => { globalThis.fetch = originalFetch })

test('returns the id sent back by the hub', async ({ assert }) => {
  globalThis.fetch = async () => new Response('urn:uuid:1234\\n', { status: 200 })
  const id = await new Publisher(config).publish('test-topic', {})
  assert.equal(id, 'urn:uuid:1234')
})''','tests/publisher.spec.ts'),
H2('9.2 Continuous integration (GitHub Actions)'),
*table([['Job','Goal'],
['lint','ESLint (AdonisJS config) + Prettier: consistent style.'],
['typecheck','tsc --noEmit: the TypeScript compiler checks all types.'],
['tests','Matrix: Ubuntu and Windows × Node 20.x and 22.x (4 combinations).'],
['adonis-v7','Installs AdonisJS 7 “without saving” and runs typecheck + tests again: proves compatibility with v6 AND v7.']],[28*mm,W-28*mm]),
H2('9.3 Publishing on npm'),
P('When we create a <b>Release</b> on GitHub, the workflow ' + M('npm-publish.yml') + ' (1) runs ' + M('npm test') + ' and (2) if it passes, runs ' + M('npm publish --access public') + ' with the permission ' + M('id-token: write') + ' (OIDC “trusted publishing”: no npm password stored as a secret). Before publishing, ' + M('prepublishOnly') + ' compiles the TypeScript, and ' + M('postbuild') + ' copies the stubs into ' + M('build/') + ' because tsc does not copy .stub files.'),
H2('9.4 The npm scripts'),
*table([['Command','Role'],
['npm run build','Lint → clean → tsc → copy stubs'],
['npm test','Lint, then tests with coverage (c8)'],
['npm run quick:test','Tests only, no lint, no coverage'],
['npm run typecheck','Type checking'],
['npm run release','Publish with the “np” tool (version bump, git tag, publish)']],[45*mm,W-45*mm]),
*vocab([('deterministic', 'déterministe'), ('to stub / to mock', 'simuler'), ('to exercise (code)', 'exécuter / tester'), ('coverage', 'couverture'), ('matrix', 'matrice de tests'), ('to restore', 'restaurer')]),
Spacer(1,6)]

# 10
st+=[H1('10. History of the project and decisions'),
*fig(d_time(),'Figure 9 — The main versions (from CHANGELOG.md)'),
*table([['Version','What changed and why'],
['1.0.12 (2024)','First stable version.'],
['2.0.0','Major rewrite: Publisher/TokenGenerator split; <b>the “got” dependency was replaced by the native fetch</b> of Node (fewer dependencies); errors are thrown instead of hidden; added ping, FakeMercure, MercureContract, SSE options, generateSubscribeToken.'],
['2.0.1','Security fixes: hard-coded secrets removed, algorithm allow-list, secret ≥ 32 characters, error body truncated.'],
['2.1.x','Package renamed (@das3mical → @mdsiha369), configurable timeout + MercureTimeoutError.'],
['2.2.0','expiresIn, MercureConnectionError, AdonisJS 7 support, public types without @types/jws, reliable ping() (5xx = false), lighter package (13.7 → 9 kB).'],
['3.0.0','<b>Breaking change</b>: send() returns the id (string) instead of a Response object. Major version because existing code can break (SemVer).']],[28*mm,W-28*mm]),
H2('Design decisions you must be able to justify'),
*table([['Decision','Why'],
['Native fetch instead of “got”','Fewer dependencies, smaller attack surface, available in Node 18+.'],
['Only one runtime dependency (jws)','Small and maintained; JWT needs cryptography that we should not rewrite ourselves.'],
['MercureContract interface','Makes FakeMercure interchangeable; the real and the fake evolve together (the compiler complains otherwise).'],
['Specific error classes','The caller can tell “slow hub”, “hub down”, “refused” without parsing text.'],
['defineConfig validates at startup','Fail fast: a bad config breaks at boot, not in the middle of a user request.'],
['Native private fields (#)','Real encapsulation at runtime.'],
['send() returns the id (v3)','More useful than Response: no need to read the body; the id helps tracking and replay. Price: a major version.'],
['peerDependency @adonisjs/core ^6.2 || ^7','We use the framework already installed by the user; no duplicate.'],
['ESM ("type": "module")','Modern standard; AdonisJS 6/7 is ESM (so imports end with “.js”).']],[55*mm,W-55*mm]),
*vocab([('breaking change', 'changement incompatible'), ('attack surface', 'surface d’attaque'), ('encapsulation', 'encapsulation'), ('trade-off', 'compromis'), ('to justify', 'justifier'), ('rationale', 'justification')]),
PageBreak()]

# 11
st+=[H1('11. Real usage examples'),
H2('Backend: publish'),
*code('''import mercure from '@mdsiha369/adonis-mercure/services/main'

// Public
const id = await mercure.send('/orders/42', { status: 'shipped' })

// Several topics + private + SSE options
await mercure.send(['/orders/42', '/notifications/user/1'], { status: 'shipped' },
  { private: true, id: 'msg-001', type: 'order.shipped', retry: 5000 })

// Health check
if (!(await mercure.ping())) logger.warn('Mercure hub unreachable')''','AdonisJS application'),
H2('Frontend: listen'),
*code('''const url = new URL('https://hub.example.com/.well-known/mercure')
url.searchParams.append('topic', '/orders/42')

const es = new EventSource(url, { withCredentials: true })   // the cookie is sent automatically
es.addEventListener('order.shipped', (e) => {
  const payload = JSON.parse(e.data)       // { status: 'shipped' }
  updateUI(payload.status)
})''','Browser'),
H2('Unit test of a controller'),
*code('''test('ship order notifies subscribers', async ({ assert }) => {
  app.container.swap('mercure', () => new FakeMercure())
  await controller.ship(42)
  const fake = (await app.container.make('mercure')) as FakeMercure
  fake.assertSent('/orders/42', { status: 'shipped' })
  app.container.restore('mercure')
})''','Test'),
H2('Roadmap (from the README)'),
*B([M('generatePublishToken(topics)') + ' — the twin of generateSubscribeToken',
M('sendBatch(messages[])') + ' — several publications in one call',
'<b>Retry with backoff</b> — automatic new attempt after a temporary error',
'<b>Typed event classes</b> — ' + M('new OrderShippedEvent(id)') + ' instead of loose objects']),
PageBreak()]

# 12 Q&A (Canada edition)
st+=[H1('12. Interview questions (system design, production, security, testing)'),
P('Every answer follows the format: <b>Direct answer (30 s)</b> → <b>Technical justification</b> → <b>Limit / Possible improvement</b>. Precise statements about the Mercure hub (history, transport, clustering) depend on the deployed version and edition: confirm them in its documentation before asserting them. The repo contains no benchmark and no production metrics: do not present numbers as measured.','small')]
for _n,(q,d,j,l) in enumerate(QA_CA,1):
    st+=qa(_n,q,d,j,l)
st+=[PageBreak()]

# 13
st+=[H1('13. Glossary (English = French)'),
*table([['Term','Simple definition','En français'],
['SSE','Server-Sent Events: a one-way HTTP stream from server to browser.','flux serveur → navigateur'],
['EventSource','Browser API that opens and keeps an SSE stream.','API navigateur pour SSE'],
['Hub','The Mercure server that receives and redistributes messages.','serveur Mercure'],
['Topic','Name of a broadcast channel (often a path or URL).','canal de diffusion'],
['Publisher / Subscriber','The one who sends / the one who listens.','éditeur / abonné'],
['JWT','JSON Web Token: a signed token containing rights.','jeton signé'],
['HS256 / RS256','Signature algorithms: HMAC with a shared secret / RSA with a key pair.','algorithmes de signature'],
['claim','A piece of information in the JWT payload (e.g. exp, mercure).','information du jeton'],
['exp','Expiry date of the token (UNIX seconds).','date d’expiration'],
['IoC / DI','Inversion of control / dependency injection: the framework gives you the objects.','injection de dépendances'],
['Container','Central registry of services in AdonisJS.','registre de services'],
['Provider','Class that registers services at startup.','fournisseur de services'],
['Codemod','Script that edits the source code of a project automatically.','script de modification de code'],
['Stub','Template file used to generate another file.','fichier modèle'],
['Facade','Simple object that hides a complex system.','façade'],
['Mock / Fake / Stub','A test double that replaces a real dependency.','doublure de test'],
['AbortController','Standard API to cancel a fetch (used for the timeout).','annulation de requête'],
['ESM','ECMAScript modules: native import/export.','modules JavaScript'],
['SemVer','Version numbering convention MAJOR.MINOR.PATCH.','versionnement sémantique'],
['CI','Continuous integration: automatic tests on every push.','intégration continue'],
['OIDC / trusted publishing','Publish to npm with a GitHub identity, no stored password.','publication sans mot de passe'],
['peerDependency','A dependency the user must already have (here AdonisJS).','dépendance « paire »'],
['Graceful degradation','The system keeps working (in a reduced mode) when a dependency fails.','dégradation maîtrisée'],
['Fail-fast','Fail immediately and loudly on an avoidable error (invalid config at boot).','échouer tôt'],
['Backoff / jitter','Growing delay between attempts / randomness added to avoid synchronized spikes.','temporisation / aléa'],
['Circuit breaker','Cuts calls to a failing service so that it can recover.','disjoncteur'],
['Idempotency','Replaying an operation gives the same result (essential with at-least-once).','idempotence'],
['Outbox pattern','Write the event to the database in the transaction, then publish it with a worker: avoids dual writes.','patron « outbox »'],
['Thundering herd','Many clients reconnecting at the same time after an outage or a deploy.','ruée simultanée'],
['SLO / p99','Service level objective / 99th percentile latency.','objectif de service / latence p99'],
['Observability','Ability to understand the system through metrics, logs and traces.','observabilité'],
['Test double','Generic term for fake, stub, mock, spy.','doublure de test'],
['Least privilege','Grant only the strictly necessary rights (e.g. precise topics in the JWT).','moindre privilège']],[38*mm,W-38*mm-36*mm,36*mm]),
H2('Useful sentences for the interview'),
*B(['<i>“I chose X because…”</i> — Je l’ai choisi parce que…',
'<i>“The main advantage is…”</i> — Le principal avantage est…',
'<i>“The trade-off is…”</i> — Le compromis est…',
'<i>“If I had more time, I would…”</i> — Si j’avais plus de temps, je…',
'<i>“I don’t remember the exact detail, but I would check…”</i> — Je ne me souviens pas du détail exact, mais je vérifierais…',
'<i>“Could you repeat the question, please?”</i> — Pouvez-vous répéter la question, s’il vous plaît ?']),
H2('Before the interview: defending your decisions in front of a Tech Lead / Engineering Manager'),
*B(['<b>Speak in trade-offs</b>: for each decision, name the rejected alternative, the gain, the cost, and the context in which you would change your mind (“it depends on the SLO”).',
'<b>Lead with the pattern, not the framework</b>: IoC / DIP / Facade / fail-fast. Show the NestJS / Fastify / Express equivalent (section 3).',
'<b>Be able to draw by hand</b>: Figure 3 (browser — app — hub), Figure 6 (send() sequence) and the cookie flow (Figure 7).',
'<b>Own the limits</b>: no retry, no metrics, optional `expiresIn`, `FakeMercure` cannot simulate failures, no benchmark. Then propose the concrete improvement (that is what a senior does).',
'<b>Prepare 3 numbers you can justify</b> (5 s timeout, secret ≥ 32 characters, ~6 HTTP/1.1 connections) and be clear about what is measured and what is not.',
'<b>Stay honest about scope</b>: this is a library, not a large-scale production service; talk about what you would do at scale without claiming you did it.',
'<b>North-American style</b>: structured answers (situation → decision → result), ownership (“I decided / I chose”), concrete examples, and clarifying questions before answering a system-design prompt.']),
H2('English keywords to place naturally'),
*table(CHECK_ROWS,[52*mm,W-52*mm])]
doc.build(st)
print('ok')
