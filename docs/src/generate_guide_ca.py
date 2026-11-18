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
def kid(t): return callout('Explication « comme à un enfant »',t,LORANGE,ORANGE)
def tip(t): return callout('À retenir pour l’entretien',t,LGREEN,GREEN)
def warn(t): return callout('Attention / piège',t,LRED,RED)
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
    box(d,10,110,120,60,['Navigateur','(React, Vue, JS…)','EventSource'],LGREEN,GREEN)
    box(d,W-130,110,120,60,['App AdonisJS','+ ce package','adonis-mercure'],LBLUE,BLUE)
    box(d,W/2-60,10,120,55,['Hub Mercure','(serveur externe)','« la boîte aux lettres »'],LORANGE,ORANGE)
    arrow(d,W-70,110,W/2+45,65,BLUE)
    txt(d,W-10,88,'① POST /.well-known/mercure',7,BLUE,anchor='end')
    txt(d,W-10,78,'(JWT admin + topic + data)',7,BLUE,anchor='end')
    arrow(d,W/2-45,65,70,110,ORANGE,'② pousse en direct (SSE)',lx=-62,ly=2,size=7)
    arrow(d,W-130,150,130,150,PURPLE,None,dash=[3,2])
    txt(d,W/2,155,'③ (privé) l’app donne un token JWT « subscriber »',7.5,PURPLE,anchor='middle')
    arrow(d,130,128,W-130,128,GREEN,None,dash=[2,2])
    txt(d,W/2,118,'(le navigateur s’abonne au hub : GET + topic)',7,GREEN,anchor='middle')
    return d
# D2 polling/sse/ws
def d_proto():
    d=Drawing(W,150)
    cols=[('Polling','« Y a-t-il du nouveau ? »',RED,LRED),('SSE (Mercure)','« Je t’écoute, parle quand tu veux »',GREEN,LGREEN),('WebSocket','Tuyau dans les 2 sens',PURPLE,LPURPLE)]
    cw=(W-20)/3
    for i,(t,sub,c,l) in enumerate(cols):
        x=i*(cw+10)
        d.add(Rect(x,5,cw,140,rx=6,ry=6,fillColor=l,strokeColor=c))
        txt(d,x+cw/2,128,t,10,c,True,'middle'); txt(d,x+cw/2,116,sub,6.8,INK,False,'middle')
        cx1,cx2=x+22,x+cw-22
        d.add(Line(cx1,25,cx1,105,strokeColor=INK,strokeDashArray=[2,2])); d.add(Line(cx2,25,cx2,105,strokeColor=INK,strokeDashArray=[2,2]))
        txt(d,cx1,10,'Client',7,INK,True,'middle'); txt(d,cx2,10,'Serveur',7,INK,True,'middle')
        if i==0:
            for k,yy in enumerate([95,75,55,35]):
                arrow(d,cx1,yy,cx2,yy,RED,'rien ?' if k<3 else 'ok !',size=6.5,ly=2)
        if i==1:
            arrow(d,cx1,95,cx2,95,GREEN,'je m’abonne',size=6.5,ly=2)
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
    box(d,W/2-70,135,140,40,['Mercure','(façade : send, ping…)'],LBLUE,BLUE,9)
    box(d,10,60,140,44,['Publisher','publish() → fetch POST'],LORANGE,ORANGE,8.5)
    box(d,W-150,60,140,44,['TokenGenerator','generate() → JWT (jws)'],LGREEN,GREEN,8.5)
    box(d,W/2-70,5,140,38,['MercureConfig','endpoint, adminToken, jwt…'],GREY,MUTED,8)
    box(d,W-135,195,125,50,['MercureContract','(interface TypeScript)'],YEL,colors.HexColor('#ca8a04'),8)
    box(d,10,195,125,50,['FakeMercure','(faux pour les tests)'],LRED,RED,8)
    arrow(d,W/2,205,W/2,175,PURPLE,'new Mercure(config)',lx=45,ly=-2)
    arrow(d,W/2-40,135,100,104,BLUE,'send()',lx=-20,ly=4)
    arrow(d,W/2+40,135,W-100,104,BLUE,'generate…()',lx=22,ly=4)
    arrow(d,80,60,W/2-30,43,MUTED,'lit config',lx=-10,ly=-10,size=6.5)
    arrow(d,W-80,60,W/2+30,43,MUTED,'lit config',lx=10,ly=-10,size=6.5)
    arrow(d,W-72,195,W/2+50,175,colors.HexColor('#ca8a04'),None,dash=[3,2])
    txt(d,W-50,182,'implements',6.5,colors.HexColor('#ca8a04'),anchor='middle')
    arrow(d,72,195,W/2-50,175,RED,None,dash=[3,2])
    txt(d,50,182,'implements',6.5,RED,anchor='middle')
    return d
# D4 sequence send
def d_seq():
    d=Drawing(W,240)
    names=['Ton code','Mercure','Publisher','Hub Mercure']
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
    txt(d,xs[2]+8,150,'URLSearchParams',6.5,ORANGE); txt(d,xs[2]+8,140,'+ timer anti-blocage',6.5,ORANGE)
    msg(2,3,120,'POST + Bearer adminToken',PURPLE)
    msg(3,2,92,'200 OK  « urn:uuid:… »',PURPLE,[3,2])
    msg(2,1,70,'return id',ORANGE,[3,2])
    msg(1,0,48,'return id',BLUE,[3,2])
    txt(d,xs[3]+6,50,'diffuse aux abonnés',6.5,PURPLE)
    d.add(Rect(W-318,14,312,12,fillColor=colors.white,strokeColor=None))
    txt(d,W-8,17,'Si ça rate : MercurePublishError / TimeoutError / ConnectionError',6.8,RED,anchor='end')
    return d
# D5 timeline
def d_time():
    d=Drawing(W,160)
    d.add(Line(15,75,W-15,75,strokeColor=MUTED,strokeWidth=2))
    ev=[('1.0.12','août 2024','Version initiale',1),('2.0.0','mai 2026','Refonte :\nFake, ping,\nerreurs, fetch',-1),('2.0.1','mai 2026','Sécurité',1),('2.1.x','mai 2026','Renommage\nnpm, timeout',-1),('2.2.0','nov 2026','expiresIn,\nConnectionError,\nv7',1),('3.0.0','nov 2026','send()\nretourne l’id',-1)]
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
    names=['Navigateur','App AdonisJS','Hub Mercure']
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
    txt(d,xs[2]-4,80,'vérifie la signature du JWT',6.5,ORANGE,anchor='end')
    msg(2,0,60,'flux SSE ouvert…',ORANGE,[3,2])
    msg(2,0,35,'data: {"status":"shipped"}',ORANGE)
    return d
# D7 errors
def d_err():
    d=Drawing(W,150)
    box(d,W/2-60,112,120,30,['Error','(JavaScript natif)'],GREY,MUTED,8.5)
    box(d,W/2-60,66,120,30,['MercureError','classe mère'],LBLUE,BLUE,8.5)
    arrow(d,W/2,112,W/2,96,MUTED); 
    items=[('ConfigError','config invalide',PURPLE,LPURPLE),('PublishError','hub répond non-2xx',RED,LRED),('TimeoutError','trop lent (5 s)',ORANGE,LORANGE),('ConnectionError','hub injoignable',GREEN,LGREEN)]
    bw=(W-30)/4
    for i,(t,s,c,l) in enumerate(items):
        x=5+i*(bw+7); box(d,x,6,bw,34,['Mercure'+t,s],l,c,7.5)
        arrow(d,x+bw/2,40,W/2+(i-1.5)*18,66,c)
    return d
# D8 boot flow
def d_boot():
    d=Drawing(W,130)
    steps=[('node ace\nconfigure','Tu installes',GREEN,LGREEN),('configure.ts','crée config,\n.env, rcfile',BLUE,LBLUE),('Démarrage\nAdonis','lit adonisrc',PURPLE,LPURPLE),('Provider.boot()','déclare\nsingleton',ORANGE,LORANGE),('import service\n(1re fois)','container.make\n→ new Mercure',RED,LRED)]
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
    txt(d,W/2,8,'Le hub recalcule la signature avec le même secret : si ça colle, le token est authentique.',7.2,MUTED,anchor='middle')
    return d

# ======== CANADA / SENIOR EDITION BLOCK ========
import re as _re
def bt(t): return _re.sub(r'`([^`]+)`',lambda m: M(m.group(1)),t)
def trade(t): return callout('Compromis techniques & Impact Production (Trade-offs)',bt(t),LPURPLE,PURPLE)
TRADE=[
"""<b>Build vs Buy : déléguer le temps réel à un hub externe.</b><br/>
• <b>Gain</b> : l’application reste <i>stateless</i> ; aucune connexion longue durée dans le process Node ; le hub scale indépendamment de l’app.<br/>
• <b>Coût</b> : un composant d’infrastructure de plus à opérer (déploiement, monitoring, HA, upgrades), un hop réseau supplémentaire et un nouveau point de défaillance (SPOF si une seule instance).<br/>
• <b>Impact prod</b> : le temps réel doit être conçu comme <i>dégradable</i> (graceful degradation) : si le hub tombe, l’app continue de servir les requêtes, et l’UI retombe sur un refresh manuel ou du polling.""",
"""<b>SSE vs WebSocket : coûts serveur, mémoire, load balancing.</b><br/>
• <b>SSE</b> = HTTP standard : traverse proxies, CDN et WAF existants ; reconnexion et <i>Last-Event-ID</i> natifs ; authentification par cookie / headers classiques ; HTTP/2 multiplexe plusieurs streams sur une seule connexion TCP. Aucun protocole de heartbeat ou de framing applicatif à écrire, donc moins de code et moins de mémoire par connexion côté serveur.<br/>
• <b>Limites SSE</b> : unidirectionnel (le sens client → serveur reste des requêtes HTTP normales) ; texte UTF-8 seulement ; en HTTP/1.1, ~6 connexions par domaine et par navigateur (→ HTTP/2, ou un seul EventSource avec plusieurs topics) ; derrière nginx il faut désactiver <code>proxy_buffering</code> et augmenter <code>proxy_read_timeout</code>.<br/>
• <b>Load balancing</b> : une connexion longue rend la répartition inégale après un <i>rolling deploy</i> et provoque un <i>thundering herd</i> à la reconnexion (prévoir du jitter côté client). WebSocket exige souvent des sticky sessions et son propre heartbeat.<br/>
• <i>Les ordres de grandeur (mémoire/connexion, limites de file descriptors) sont à valider par un load test (k6, Artillery) : le repo ne contient aucun benchmark.</i>""".replace('<code>','`').replace('</code>','`'),
"""<b>Granularité des topics : par ressource ou par utilisateur ?</b><br/>
• <b>Un topic par ressource</b> (`/orders/42`) : ciblage précis et ACL fine via le JWT, mais forte cardinalité ; la liste `subscribe` du JWT grossit, or le token voyage dans un cookie (limite ~4 KB) ou un header.<br/>
• <b>Un topic par utilisateur</b> (`/users/1`) : peu de topics et un token minuscule, mais le fan-out (qui doit recevoir quoi) migre dans le code applicatif.<br/>
• Le protocole Mercure permet des <i>topic selectors</i> (URI templates, joker) pour réduire la taille du token, au prix d’une surface d’autorisation plus large : à valider avec le principe de <i>least privilege</i>.""",
"""<b>JWT stateless vs sessions côté serveur.</b><br/>
• <b>Gain</b> : le hub vérifie la signature localement, sans appel à la base ni à l’app : pas de couplage, scale horizontal trivial.<br/>
• <b>Coût</b> : pas de révocation avant `exp`. Un token volé reste valide jusqu’à expiration. Mitigation : TTL court (quelques minutes) + endpoint qui ré-émet un token, et rotation du secret en cas d’incident.<br/>
• <b>Dans ce package</b> : `expiresIn` est optionnel et, par défaut, le token n’expire jamais. C’est un compromis DX contre sécurité ; en production, je rendrais un TTL obligatoire ou je fixerais un défaut raisonnable.""",
"""<b>Fail-fast au boot vs tolérance aux pannes.</b><br/>
• `defineConfig()` plante au démarrage si la config est invalide : l’erreur est détectée au déploiement (readiness probe en échec, rolling update interrompu, rollback automatique) et non à la première requête utilisateur.<br/>
• <b>Choix volontaire</b> : le provider ne fait <i>pas</i> de `ping()` du hub au boot. Sinon une panne du hub bloquerait tous les déploiements de l’app, alors que le temps réel n’est pas critique. Config invalide = bug du développeur (fail-fast) ; hub indisponible = incident d’exploitation (graceful degradation).""",
"""<b>Timeout par défaut de 5 s : pourquoi et à quel prix.</b><br/>
• `send()` est souvent appelé dans le chemin critique d’une requête HTTP utilisateur. Sans timeout, un hub lent accumule des requêtes en attente, fait exploser la latence p99 et peut déclencher un <i>cascading failure</i>.<br/>
• 5 s est un défaut large : pour une API avec un SLO p99 &lt; 500 ms, il faut baisser `http.timeout` (ex. 1000 ms). `timeout: 0` désactive la protection : à éviter en production.<br/>
• Mieux encore : sortir la publication du chemin critique (job en file d’attente, <i>outbox pattern</i>) pour que la latence du hub n’impacte jamais l’utilisateur.""",
"""<b>Test double (FakeMercure) vs mock de `fetch`.</b><br/>
• Le <i>fake</i> est un code de plus à maintenir et il peut <i>diverger</i> du vrai comportement ; en échange, les tests de l’app expriment l’intention (« topic X a reçu Y ») et ne dépendent pas de la forme HTTP (URL, encodage form, headers).<br/>
• Mocker `fetch` ne coûte aucun code, mais couple chaque test à l’implémentation du transport : un changement interne du package casserait les tests de tous ses utilisateurs.<br/>
• Le package garde les deux niveaux : mock de `fetch` pour tester <i>Publisher</i> (c’est la frontière), `FakeMercure` pour les consommateurs. Un <i>contract test</i> contre un vrai hub (Docker) limiterait le risque de dérive.""",
]

FW_ROWS=[['Concept dans ce package','Pattern universel','AdonisJS (ici)','NestJS','Express / Fastify'],
['MercureProvider + container.singleton','IoC container, DI, scope <b>Singleton</b>, <i>composition root</i>','Provider.boot() enregistre un singleton lazy','Provider d’un Module (<code>useFactory</code>), scope singleton par défaut','Express : instance exportée d’un module. Fastify : <code>fastify.decorate()</code> dans un plugin'],
['MercureContract + FakeMercure','<b>Dependency Inversion</b> (DIP), <b>Strategy</b> pattern, <b>test double</b>','interface + <code>container.swap()</code>','<code>overrideProvider()</code> dans <code>Test.createTestingModule</code>','Injection manuelle (paramètre / factory) ou override de la décoration en test'],
['configure.ts + stubs + codemods','<b>CLI scaffolding</b>, modification d’<b>AST</b> (codemods)','<code>node ace configure</code> (codemods)','Schematics (<code>nest g</code>)','<code>create-*</code>, jscodeshift / ts-morph, ou étapes manuelles'],
['defineConfig() (validation au boot)','<b>Fail-fast</b> typed configuration','<code>defineConfig</code> + <code>start/env.ts</code>','<code>ConfigModule.forRoot({ validate })</code> (Joi / zod)','zod, envalid ; <code>@fastify/env</code> (JSON Schema)'],
['services/mercure.ts','<b>Facade</b> / service locator (lazy singleton)','import du service','Injection par constructeur (pas de facade)','Import d’un module singleton ou <code>fastify.mercure</code>'],
['Hiérarchie MercureError','Erreurs typées du domaine, <b>error boundary</b>','<code>instanceof</code> + handler global','Exception filters (<code>@Catch</code>)','Error middleware / <code>setErrorHandler</code>'],
['Publisher : fetch + AbortController','Appel sortant avec <b>timeout</b> (deadline propagation)','<code>fetch</code> natif','<code>HttpModule</code> (axios) ou <code>timeout()</code> RxJS','<code>undici</code> / <code>fetch</code> + signal'],
['peerDependency @adonisjs/core','<b>Peer dependency</b> : le framework est fourni par l’hôte','<code>^6.2 || ^7</code>','<code>@nestjs/common</code> en peer','<code>express</code> / <code>fastify</code> en peer'],
]
FW_CODE_NEST='''// ILLUSTRATIF (non présent dans le repo) : réutiliser le noyau dans NestJS
@Module({
  providers: [{ provide: 'MERCURE', useFactory: () => new Mercure(defineConfig(config)) }],
  exports: ['MERCURE'],
})
export class MercureModule {}

// Fastify
fastify.decorate('mercure', new Mercure(defineConfig(config)))

// Express
export const mercure = new Mercure(defineConfig(config))   // module = singleton'''

def qa(n,q,d,j,l):
    return [KeepTogether([P('Q%d. %s'%(n,q),'q'),P('<b><font color="#16a34a">Réponse directe (30 s)</font></b> — '+bt(d))]),
            P('<b><font color="#2563eb">Justification technique</font></b> — '+bt(j)),
            P('<b><font color="#ea580c">Limite / Amélioration possible</font></b> — '+bt(l))]

QA_CA=[
("System Design : comment gérer 50 000 connexions simultanées avec ce setup ?",
 "Le package n’est pas le goulot d’étranglement : l’application n’émet qu’un POST court par événement. Les 50 000 connexions longue durée sont portées par le hub Mercure, qu’on scale horizontalement derrière un load balancer, pas par les workers Node.",
 "Points de vigilance : (1) limites de file descriptors (`ulimit -n`) et mémoire par connexion sur le hub ; (2) un seul EventSource par onglet avec plusieurs topics, en HTTP/2, pour contourner la limite de ~6 connexions HTTP/1.1 par domaine ; (3) proxy : `proxy_buffering off`, `proxy_read_timeout` élevé, heartbeats ; (4) pour plusieurs instances de hub, il faut un <i>transport</i> partagé (selon l’édition du hub : Bolt en local, ou une édition HA avec transport externe) : à vérifier dans la doc de la version déployée ; (5) après un deploy ou une panne, une reconnexion massive (<i>thundering herd</i>) : jitter côté client et rolling deploy lent.",
 "Le repo ne contient ni load test ni benchmark : je ne promettrais pas un chiffre sans test (k6/Artillery avec 50k clients simulés, métriques mémoire et CPU du hub). Côté package, `sendBatch` (roadmap) réduirait le nombre de POST en cas de forte émission."),
("SSE ou WebSocket : lequel choisir en production, et pourquoi ?",
 "SSE quand le flux est surtout serveur → client (notifications, statuts, dashboards) : c’est du HTTP standard, plus simple à opérer et à sécuriser. WebSocket quand il y a un trafic bidirectionnel à faible latence (jeux, édition collaborative).",
 "Coûts : SSE réutilise l’infra HTTP existante (proxies, WAF, auth par cookie), la reconnexion et `Last-Event-ID` sont natifs, et il n’y a pas de protocole applicatif à maintenir. WebSocket demande souvent des sticky sessions, un heartbeat applicatif, et une gestion explicite de la reconnexion et du backpressure. Les deux consomment une connexion longue par client ; la différence se joue sur la complexité d’exploitation.",
 "Limites de SSE : unidirectionnel, UTF-8 uniquement, limite de connexions par domaine en HTTP/1.1. Si le besoin devient bidirectionnel, on garde SSE pour le push et des requêtes HTTP pour l’upstream, ou on migre vers WebSocket."),
("`send()` est appelé dans une requête utilisateur et le hub est lent ou en panne : que se passe-t-il ?",
 "L’appel est borné par un timeout (5 s par défaut, `http.timeout`) et échoue avec une erreur typée : `MercureTimeoutError`, `MercureConnectionError` ou `MercurePublishError`. L’appelant décide quoi faire : ignorer, logger, ou réessayer.",
 "Sans timeout, les requêtes s’empilent, le p99 explose et on risque un cascading failure. Le vrai sujet est le <i>dual write</i> : si la transaction base de données est commitée mais la publication échoue, l’état et les notifications divergent. Solutions : publier après le commit et traiter l’échec comme une dégradation acceptable, ou utiliser un <i>outbox pattern</i> (écrire l’événement dans la base dans la même transaction, puis un worker le publie avec retry).",
 "Le timeout de 5 s est trop long pour un SLO p99 agressif : le configurer (par ex. 1 s) ou sortir la publication du chemin critique via une file (BullMQ, etc.). Le package ne fournit ni retry ni circuit breaker (voir question suivante)."),
("Le package n’a pas de retry. Comment l’implémenter proprement ?",
 "Un wrapper autour de `send()` avec <i>exponential backoff + jitter</i>, limité à quelques tentatives, qui ne réessaie que les erreurs transitoires : `MercureTimeoutError`, `MercureConnectionError`, et `MercurePublishError` avec un status 5xx (éventuellement 429). Pas de retry sur 4xx comme 401/403/400 : c’est un bug de config ou de payload.",
 "Les erreurs typées rendent la politique de retry triviale à écrire sans parser de texte. Il faut un <i>retry budget</i> (durée totale &lt; SLO de la requête) ; sinon, on retry de façon asynchrone via une queue. Sémantique de livraison : un retry peut dupliquer un message (at-least-once) ; passer un `id` stable permet aux clients de dédupliquer. Pour éviter de marteler un hub malade, ajouter un <i>circuit breaker</i> (ex. opossum) : au bout de N échecs, on court-circuite et on dégrade.",
 "À implémenter dans le package (roadmap « Retry with backoff ») avec une option `retry: { attempts, baseDelay, retryOn }` et un test double qui sait simuler des pannes (`failNext(error)`), ce que `FakeMercure` ne permet pas aujourd’hui. Attention aussi : le hub ne garantit pas la déduplication ; c’est au consommateur d’être idempotent."),
("Observabilité : que mesureriez-vous et comment ?",
 "Un histogramme de latence autour de `send()`, un compteur d’erreurs par classe (`MercureTimeoutError`, `MercureConnectionError`, `MercurePublishError` + status), le nombre de messages publiés, et un span OpenTelemetry par appel. Alertes sur le taux d’erreur et la latence p99.",
 "Les erreurs typées donnent des labels de métriques propres (cardinalité maîtrisée). `ping()` sert de sonde de santé, mais attention : l’utiliser en <i>liveness</i> ferait redémarrer toute l’app quand le hub tombe. Il faut l’exposer en <i>readiness</i> « dégradée » ou dans un health endpoint informatif, cohérent avec la graceful degradation. Côté logs : `MercurePublishError.responseBody` est tronqué à 200 caractères pour ne pas fuiter de données sensibles.",
 "Le package n’émet aujourd’hui ni logs ni métriques : on instrumente au niveau d’un wrapper applicatif. Amélioration : accepter un logger et des hooks (`onPublish`, `onError`) ou exposer des événements pour brancher Prometheus / OpenTelemetry sans dépendance dure."),
("Sécurité : quelles failles JWT connaissez-vous et comment le package s’en protège-t-il ?",
 "Principales failles : <b>`alg: none`</b>, <b>confusion d’algorithme</b> (HS256 vs RS256), <b>secret faible</b> (brute force hors-ligne sur HS256), <b>tokens sans expiration</b>, <b>claims trop larges</b> (joker), et <b>token dans l’URL</b> (fuite dans les logs). Le package impose une allow-list d’algorithmes (HS/RS 256-384-512, jamais `none`) et un secret d’au moins 32 caractères, tous deux vérifiés au boot.",
 "La vérification des tokens est faite par le hub, pas par le package : on ne fait que <i>signer</i>. Le token admin (`publish: [\"*\"]`) ne doit jamais quitter le serveur (principe de <i>least privilege</i>) ; les tokens subscriber doivent lister des topics précis, avec un TTL court (`expiresIn`). Le secret vient de l’environnement, jamais du code ; `configure.ts` laisse les valeurs vides exprès.",
 "Faiblesses restantes : `expiresIn` est optionnel (aucun défaut), il n’y a pas de révocation avant `exp`, et le secret n’a pas de rotation. Améliorations : TTL obligatoire, support de `kid` pour la rotation de clés, et test de non-régression qui prouve qu’un token signé avec un autre algorithme est refusé."),
("Un token subscriber est visible côté client : quels sont les risques et comment les réduire ?",
 "Le principal risque est le vol du token (XSS, extension malveillante, logs). On limite l’impact : token à portée minimale (topics précis), TTL court, et transport par cookie `HttpOnly` plutôt que stocké en JavaScript.",
 "`EventSource` ne peut pas envoyer de header `Authorization`, donc deux options : cookie posé par l’app (avec `response.plainCookie`, car `response.cookie` signe la valeur et le hub la rejetterait) ou une lib basée sur `fetch` avec header Bearer. Le cookie `HttpOnly` n’est pas lisible par JavaScript : un XSS ne peut pas l’exfiltrer, même s’il peut encore lancer des requêtes authentifiées depuis la page. Ne jamais passer le token en query string (il finit dans les logs et les referrers).",
 "Un token volé reste valide jusqu’à son expiration (pas de révocation) : d’où le TTL court et un endpoint qui le renouvelle. Défense en profondeur : CSP stricte, sanitisation des entrées, et surveillance des accès anormaux côté hub."),
("CORS et cookies `__Secure-` : qu’est-ce qui peut mal tourner avec `EventSource` ?",
 "Si le hub est sur un autre origin, il faut `withCredentials: true` côté client, et côté hub une config CORS qui liste l’origin exact et autorise les credentials : un joker `*` est refusé avec des credentials. Le cookie `__Secure-` exige HTTPS et l’attribut `Secure`.",
 "Le cookie doit atteindre le hub : même <i>site</i> (ex. `app.example.com` et `hub.example.com`, avec `domain: '.example.com'`) ; `SameSite=Lax` suffit entre sous-domaines du même site, tandis qu’un hub sur un autre site demande `SameSite=None; Secure`. Le préfixe `__Host-` est impossible pour un cookie partagé entre sous-domaines (il interdit l’attribut `Domain`). En développement local HTTP, il faut un nom de cookie sans préfixe et `secure: false`.",
 "Point souvent oublié : la route qui émet le token doit vérifier que l’utilisateur a le droit de s’abonner à ce topic (contrôle d’accès / IDOR). L’exemple du README construit le topic depuis `params.id` sans cette vérification : en prod, il faut contrôler l’autorisation avant d’appeler `generateSubscribeToken`."),
("Pourquoi avoir créé un `FakeMercure` plutôt que mocker `fetch` dans l’application cliente ?",
 "Parce que `fetch` est un détail d’implémentation du package. Un test double au niveau du <i>contrat</i> (`MercureContract`) teste l’intention métier (« le topic `/orders/42` a reçu `{status:'shipped'}` ») et reste stable si le transport change.",
 "Avec un mock de `fetch`, chaque test connaîtrait l’URL, l’encodage `x-www-form-urlencoded`, les headers et la forme de la réponse : un refactor interne casserait tous les consommateurs. `FakeMercure` implémente la même interface (vérifiée par le compilateur) et se branche par `container.swap()`, donc sans toucher au code applicatif (Dependency Inversion). Il compare les données via `JSON.parse(JSON.stringify())` pour refléter ce que le hub recevrait vraiment.",
 "Risque de dérive entre le fake et le vrai : `FakeMercure` renvoie toujours `'fake-token'`, `ping()` est toujours `true`, et il ne simule aucune panne. Améliorations : un test de contrat exécuté sur les deux implémentations, un test d’intégration avec un vrai hub en Docker (Testcontainers), et `failNext(error)` pour tester les chemins d’erreur."),
("Vous avez changé `send()` pour retourner un id au lieu d’un `Response` (v3.0.0). Comment avez-vous géré ce breaking change ?",
 "C’était un breaking change assumé : version majeure (SemVer 3.0.0), entrée explicite dans le CHANGELOG avec les instructions de migration, et rappel que les classes implémentant `MercureContract` doivent changer le type de retour.",
 "Retourner un `Response` fuitait un détail de transport dans l’API publique et obligeait chaque appelant à lire le corps. Retourner une valeur de domaine (l’id) permet de changer l’implémentation (autre client HTTP, retry, batch) sans nouveau breaking change. Le contrat étant un type public, tout changement de signature touche aussi les implémenteurs externes.",
 "On aurait pu faire un cycle de dépréciation (ancienne et nouvelle API en parallèle pendant une version mineure) ou fournir un codemod de migration. Avec peu d’utilisateurs, la majeure directe était un compromis acceptable ; avec une grande base installée, je choisirais la dépréciation."),
("Garanties de livraison : que se passe-t-il si un client est hors-ligne ou si deux instances publient en même temps ?",
 "Il ne faut pas supposer de livraison exactement-une-fois. Mercure fournit un replay via `Last-Event-ID` depuis l’historique conservé par le hub, mais un client déconnecté trop longtemps peut perdre des messages. Je traite donc le push comme un <i>signal d’invalidation</i> et la base de données comme <i>source of truth</i>.",
 "Concrètement : à la (re)connexion, le client refait un fetch de l’état courant, puis applique les événements reçus ; les messages portent un `id` pour la déduplication, et les consommateurs sont idempotents (at-least-once). L’ordre n’est raisonnablement garanti que par topic et par hub ; ne pas bâtir de logique qui dépend de l’ordre global entre topics. Les détails (taille de l’historique, durabilité du transport) dépendent de la config et de l’édition du hub : à confirmer dans sa documentation.",
 "Le package ne gère ni la persistance ni la garantie de livraison : c’est la responsabilité du hub et du design applicatif. Amélioration : documenter ce modèle de cohérence et fournir un exemple de resynchronisation au reconnect."),
("Si l’entreprise utilise NestJS ou Fastify au lieu d’AdonisJS, que réutilisez-vous de ce travail ?",
 "Presque tout le noyau : `Mercure`, `Publisher`, `TokenGenerator`, `defineConfig`, les erreurs et `FakeMercure` n’importent rien d’AdonisJS. Seuls le provider, `configure.ts`, `services/mercure.ts` et `types/extended.ts` sont spécifiques à AdonisJS.",
 "C’est le bénéfice de la séparation des responsabilités : le cœur est une classe avec une dépendance injectée (la config) et un contrat (`MercureContract`). Dans NestJS on l’expose via un provider (`useFactory`) ; dans Fastify via `decorate()` ; dans Express comme un singleton de module. Les patterns (IoC, singleton, DIP, fail-fast, scaffolding) sont les mêmes, seule la colle change (voir tableau de correspondance, section 3).",
 "Aujourd’hui le package est publié avec le provider AdonisJS dans le même artefact. Amélioration : extraire un paquet noyau framework-agnostic (`mercure-core`) et de fines couches d’adaptation par framework, ce qui élargirait l’audience."),
]

CHECK_ROWS=[['Mot-clé (EN)','Comment le placer naturellement'],
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

# ---------- Document ----------
def cover(c,doc):
    c.saveState()
    c.setFillColor(colors.HexColor('#0b1b4d')); c.rect(0,0,A4[0],A4[1],fill=1,stroke=0)
    c.setFillColor(BLUE); c.rect(0,A4[1]-14*mm,A4[0],14*mm,fill=1,stroke=0)
    # decorative waves
    c.setStrokeColor(colors.HexColor('#3b82f6')); c.setLineWidth(1.2)
    for k in range(5):
        c.setStrokeAlpha(0.5-0.08*k)
        p=c.beginPath(); y0=60*mm+k*9*mm; p.moveTo(0,y0)
        for x in range(0,int(A4[0])+10,10): p.lineTo(x,y0+8*math.sin(x/28+k))
        c.drawPath(p,stroke=1,fill=0)
    c.restoreState()
def later(c,doc):
    c.saveState(); c.setFont('DV',7.5); c.setFillColor(MUTED)
    c.drawString(18*mm,10*mm,'adonis-mercure — Préparation entretien technique (Canada)')
    c.drawRightString(A4[0]-18*mm,10*mm,'Page %d'%doc.page)
    c.setStrokeColor(colors.HexColor('#e5e7eb')); c.line(18*mm,14*mm,A4[0]-18*mm,14*mm); c.restoreState()

OUT='/home/user/adonis-mercure/docs/adonis-mercure-guide-ca.pdf'
doc=BaseDocTemplate(OUT,pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=16*mm,bottomMargin=20*mm,
    title='adonis-mercure — Préparation entretien technique (Canada)',author='Guide généré pour Michael DAŞ')
doc.addPageTemplates([PageTemplate('cover',[Frame(22*mm,30*mm,A4[0]-44*mm,A4[1]-80*mm,id='c')],onPage=cover),
                      PageTemplate('main',[Frame(18*mm,20*mm,W,A4[1]-36*mm,id='m')],onPage=later)])
st=[]
# cover
st+= [Spacer(1,55*mm),P('@mdsiha369/<br/>adonis-mercure','cover1'),Spacer(1,8),
 P('Préparation à un entretien technique (Canada) : System Design, trade-offs, pragmatisme de production','cover2'),Spacer(1,90*mm),
 P('Package npm pour AdonisJS 6 / 7 · TypeScript · Mercure (SSE) · JWT<br/>Posture intermédiaire / senior · terminologie bilingue FR/EN<br/>Auteur du projet : Michael DAŞ · Licence MIT · version 3.0.0','cover2'),NextPageTemplate('main'),PageBreak()]

# 1
st+=[H1('1. Le projet en 30 secondes'),
P('<b>adonis-mercure</b> est une <b>bibliothèque (package npm)</b> écrite en TypeScript. Elle permet à une application web construite avec le framework <b>AdonisJS</b> d’<b>envoyer des messages en temps réel</b> aux navigateurs de ses utilisateurs (notification, statut de commande, message de chat…), en passant par un serveur spécialisé appelé <b>Mercure Hub</b>.'),
*trade(TRADE[0]),
H2('Ce que le package fournit (5 choses)'),
*table([['Fonction','À quoi ça sert'],
['send()','Publier un message sur un ou plusieurs « topics » (canaux), public ou privé.'],
['generateSubscribeToken() / generate()','Fabriquer des JWT (badges signés) pour que les navigateurs puissent écouter les canaux privés.'],
['ping()','Vérifier que le hub est vivant (health check).'],
['FakeMercure','Un faux Mercure pour tester son code sans hub réel (assertSent, etc.).'],
['configure / defineConfig / Provider','Installation en 1 commande, validation de la config, branchement dans AdonisJS.']],[55*mm,W-55*mm]),
H2('Pitch à dire à voix haute (FR)'),
P('« J’ai développé et publié sur npm un package AdonisJS qui intègre le protocole Mercure. Concrètement, une application AdonisJS peut pousser des mises à jour en temps réel vers les navigateurs via Server-Sent Events, avec authentification par JWT. Le package gère la configuration, la génération de tokens, la publication avec timeout et erreurs typées, et fournit un faux hub pour les tests. Il est testé avec Japa, vérifié en CI sur Node 20 et 22, Linux et Windows, et compatible AdonisJS 6 et 7. »'),
H2('Pitch to say out loud (EN) — au cas où l’entretien est en anglais'),
P('<i>“I built and published an npm package that integrates the Mercure protocol into AdonisJS. It lets a backend push real-time updates to browsers through Server-Sent Events, secured with JWTs. It handles configuration validation, token generation, publishing with timeouts and typed errors, and ships a fake hub for testing. It is tested with Japa, runs in CI on Node 20 and 22 on Linux and Windows, and supports AdonisJS 6 and 7.”</i>'),
PageBreak()]

# 2 concepts
st+=[H1('2. Les concepts fondamentaux (vue ingénieur)'),
H2('2.1 Le « temps réel » et pourquoi c’est un problème'),
P('Le web fonctionne normalement ainsi : le navigateur <b>demande</b>, le serveur <b>répond</b>. Le serveur ne peut pas parler le premier. Or pour un chat, un suivi de livraison ou un tableau de bord, on veut que le serveur puisse <b>prévenir</b> le navigateur dès qu’il y a du nouveau. Trois techniques existent :'),
*fig(d_proto(),'Figure 1 — Trois façons de faire du « temps réel »'),
*B(['<b>Polling</b> : le navigateur redemande toutes les X secondes. Simple mais gaspilleur (et jamais vraiment instantané).',
'<b>SSE (Server-Sent Events)</b> : le navigateur ouvre <i>une</i> connexion et le serveur y écrit des messages quand il veut. Un seul sens (serveur → navigateur), reconnexion automatique, fonctionne en HTTP normal. <b>C’est ce que Mercure utilise.</b>',
'<b>WebSocket</b> : tuyau bidirectionnel. Plus puissant, mais plus complexe à déployer et à sécuriser.']),
*trade(TRADE[1]),
H2('2.2 Mercure et son « Hub »'),
P('<b>Mercure</b> est un protocole ouvert (mercure.rocks) bâti sur SSE. Un <b>Hub Mercure</b> est un petit serveur (écrit en Go, souvent lancé via Docker ou le serveur Caddy) qui s’occupe de tout le travail pénible : garder des milliers de connexions ouvertes, router les messages, gérer l’autorisation. Ton application n’a qu’à lui envoyer <b>une simple requête HTTP POST</b>. C’est un énorme avantage : ton serveur Node reste léger et « sans état ».'),
P('Deux rôles :'),
*B(['<b>Publisher</b> (éditeur) : celui qui envoie des messages. Ici : l’application AdonisJS, authentifiée avec un <b>JWT admin</b>.',
'<b>Subscriber</b> (abonné) : celui qui écoute. Ici : le navigateur, avec un <b>EventSource</b>. Pour les messages privés, il doit présenter un <b>JWT subscriber</b>.']),
H2('2.3 Les « topics »'),
P('Un <b>topic</b> est simplement le <b>nom d’un canal</b>, souvent écrit comme une URL : ' + M('/orders/42') + ', ' + M('/chat/room/7') + ', ' + M('/notifications/user/1') + '. On publie sur un topic ; tous ceux abonnés à ce topic reçoivent. Un message peut cibler plusieurs topics à la fois.'),
*trade(TRADE[2]),
H2('2.4 JWT (JSON Web Token)'),
P('Un <b>JWT</b> est un « badge numérique » : une chaîne de texte en 3 parties (header . payload . signature). Le payload contient des informations (« cette personne a le droit d’écouter ' + M('/orders/42') + ' »). La <b>signature</b> est calculée avec un <b>secret</b> que seuls l’application et le hub connaissent : impossible de falsifier le badge sans le secret.'),
*fig(d_jwt(),'Figure 2 — Anatomie d’un JWT Mercure (la clé « mercure » contient les droits)'),
*trade(TRADE[3]),
H2('2.5 AdonisJS, package, provider, container'),
*B(['<b>AdonisJS</b> : framework web Node.js en TypeScript (comparable à Laravel en PHP). Versions 6 et 7 supportées.',
'<b>Package npm</b> : du code réutilisable publié sur le registre npm, installé par ' + M('npm install') + '.',
'<b>Container IoC / injection de dépendances</b> : une « boîte à outils centrale » d’AdonisJS. On y <i>enregistre</i> des objets (ex. « mercure ») et on les <i>demande</i> ailleurs sans les construire à la main.',
'<b>Provider</b> : une classe avec des méthodes de cycle de vie (' + M('register') + ', ' + M('boot') + '…) qui enregistre nos objets dans le container au démarrage de l’app.',
'<b>Singleton</b> : l’objet n’est créé qu’<b>une seule fois</b> et réutilisé partout.',
'<b>Ace</b> : la ligne de commande d’AdonisJS ; ' + M('node ace configure') + ' lance le script d’installation du package.']),
PageBreak()]

# 3 architecture
st+=[H1('3. Vue d’ensemble : comment tout s’emboîte'),
*fig(d_big(),'Figure 3 — Les trois acteurs : navigateur, application AdonisJS (avec le package) et Hub Mercure'),
P('Mon package ne touche <b>que</b> la partie « application → hub » (étape ①) et la fabrication des badges (étape ③). Le navigateur parle au hub directement (étape ②) avec le standard du web ' + M('EventSource') + '. Je n’ai donc <b>pas</b> besoin d’écrire de serveur temps réel : c’est la force de Mercure.'),
H2('Architecture interne du package'),
*fig(d_arch(),'Figure 4 — Les classes du package et qui appelle qui'),
*B(['<b>Mercure</b> = la <b>façade</b> : ce que l’utilisateur voit. Elle ne fait presque rien elle-même, elle <i>délègue</i>.',
'<b>Publisher</b> = responsable de l’envoi HTTP au hub.',
'<b>TokenGenerator</b> = responsable de la fabrication des JWT.',
'<b>MercureContract</b> = une <b>interface</b> TypeScript (le « contrat ») : toute classe qui la respecte offre ' + M('send, generate, generateSubscribeToken, ping') + '. <b>Mercure</b> et <b>FakeMercure</b> la respectent, donc on peut remplacer l’un par l’autre dans les tests.']),
*tip('Patrons de conception à citer : <b>Façade</b> (Mercure), <b>Séparation des responsabilités / Single Responsibility</b> (Publisher vs TokenGenerator), <b>Injection de dépendances + Singleton</b> (provider), <b>Test double / Fake</b> (FakeMercure), <b>Contrat d’interface</b> (MercureContract), <b>Fail fast</b> (defineConfig valide au démarrage).')]

FW=[[Paragraph(c.replace('<code>','<font face="DVM" size="7.3" color="#be123c">').replace('</code>','</font>'),S['cellh'] if i==0 else S['cell']) for c in r] for i,r in enumerate(FW_ROWS)]
_fwt=Table(FW,colWidths=[30*mm,34*mm,28*mm,38*mm,W-130*mm],repeatRows=1)
_fwst=[('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#d1d5db')),('BACKGROUND',(0,0),(-1,0),BLUE),
 ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4)]
for _i in range(2,len(FW_ROWS),2): _fwst.append(('BACKGROUND',(0,_i),(-1,_i),GREY))
_fwt.setStyle(TableStyle(_fwst))
st+=[PageBreak(),H2('Abstraction du framework : ces patterns sont universels'),
P('Au Canada, <b>NestJS, Express et Fastify</b> dominent l’écosystème Node.js. Rien de ce qui est implémenté ici n’est propre à AdonisJS : seul le « câblage » (provider, configure, service) l’est. Le tableau ci-dessous traduit chaque brique vers les autres frameworks. En entretien, parlez du <b>pattern</b> d’abord, du framework ensuite.'),
_fwt,Spacer(1,8),
*callout('Noyau framework-agnostic vs colle spécifique',bt('Les fichiers `src/mercure.ts`, `publisher.ts`, `token_generator.ts`, `define_config.ts`, `fake_mercure.ts` et `src/errors/*` <b>n’importent rien d’AdonisJS</b> (seul `src/types/extended.ts` touche aux types du framework). Seuls <b>le provider, `configure.ts`, `services/mercure.ts` et `extended.ts`</b> sont spécifiques. Conséquence : porter le package vers NestJS ou Fastify ne demande qu’une fine couche d’adaptation.'),LBLUE,BLUE),
*code(FW_CODE_NEST,'Illustratif : réutiliser le noyau ailleurs'),
*tip('Pitch de portabilité : <i>“The core is framework-agnostic. The only AdonisJS-specific parts are the provider, the configure hook and the service import. Everything else is plain TypeScript, so porting it is mostly wiring.”</i>')]


# 4 structure
st+=[Spacer(1,10),H1('4. Visite guidée du dépôt, fichier par fichier'),
*table([['Fichier','Rôle'],
['index.ts','Point d’entrée du package : réexporte tout ce qui est public (classes, erreurs, types).'],
['configure.ts','Exécuté par ' + M('node ace configure') + ' : crée config/mercure.ts, ajoute les variables .env, la validation d’env et enregistre le provider.'],
['stubs/config/mercure.stub','Modèle (template) du fichier config/mercure.ts généré chez l’utilisateur.'],
['stubs/main.ts','Exporte ' + M('stubsRoot') + ' : le chemin du dossier des stubs.'],
['providers/mercure_provider.ts','Enregistre le singleton « mercure » dans le container au démarrage.'],
['services/mercure.ts','Raccourci d’import ' + M('import mercure from \'…/services/main\'') + ' : récupère l’instance depuis le container.'],
['src/mercure.ts','Façade Mercure (send, generate, generateSubscribeToken, ping).'],
['src/publisher.ts','Construit et envoie la requête POST au hub ; gère timeout et erreurs.'],
['src/token_generator.ts','Signe les JWT avec la librairie jws ; gère expiresIn.'],
['src/define_config.ts','Valide la configuration (algo autorisé, URL, token, longueur du secret).'],
['src/fake_mercure.ts','Faux Mercure pour tests : enregistre les envois, fournit des assertions.'],
['src/errors/*.ts','5 classes d’erreurs typées (MercureError + 4 spécialisées).'],
['src/types/main.ts','Types publics : MercureConfig, SendOptions, TokenOptions, MercureContract…'],
['src/types/extended.ts','Déclare au compilateur que le container AdonisJS contient « mercure » (autocomplétion).'],
['tests/*.spec.ts','7 fichiers de tests Japa (~700 lignes).'],
['.github/workflows','CI (test.yml) et publication npm (npm-publish.yml).'],
['tsconfig*.json, tsnode.esm.js, bin/test.ts','Compilation TypeScript, exécution des tests avec ts-node + SWC.']],[52*mm,W-52*mm]),
H2('Les « exports » du package.json'),
*code('''"exports": {
  ".": "./build/index.js",                  // import { defineConfig } from '@mdsiha369/adonis-mercure'
  "./types": "./build/src/types/main.js",   // types seuls
  "./services/main": "./build/services/mercure.js",   // import mercure from '…/services/main'
  "./mercure_provider": "./build/providers/mercure_provider.js"
}''','package.json'),
P('Cette table dit à Node quels fichiers on a le droit d’importer. Seul le dossier ' + M('build') + ' (le TypeScript compilé en JavaScript) est publié sur npm (' + M('"files": ["build"]') + '), ce qui garde le paquet petit (~9 kB).'),
PageBreak()]

# 5 install & config
st+=[H1('5. Installation et démarrage, étape par étape'),
*fig(d_boot(),'Figure 5 — Du « npm install » à la première utilisation'),
H2('Étape 1 — ' + M('node ace configure') ),
P('Le script ' + M('configure.ts') + ' utilise des <b>codemods</b> (des « robots qui modifient le code source de l’utilisateur ») :'),
*code('''export async function configure(_command: ConfigureCommand) {
  const codemods = await _command.createCodemods()

  await codemods.makeUsingStub(stubsRoot, 'config/mercure.stub', {})      // crée config/mercure.ts
  await codemods.defineEnvVariables({ MERCURE_ENDPOINT: 'http://localhost:3000/.well-known/mercure',
                                      MERCURE_ADMIN_JWT: '', MERCURE_JWT_SECRET: '' }) // .env
  await codemods.defineEnvValidations({ ... })                            // start/env.ts
  await codemods.updateRcFile((rc) => rc.addProvider('@mdsiha369/adonis-mercure/mercure_provider'))
}''','configure.ts (abrégé)'),
P('Remarque : les valeurs ' + M('MERCURE_ADMIN_JWT') + ' et ' + M('MERCURE_JWT_SECRET') + ' sont volontairement <b>vides</b>. Dans une ancienne version, un secret par défaut était codé en dur ; c’était une faille, corrigée en 2.0.1 (« force les développeurs à mettre de vrais secrets »).'),
H2('Étape 2 — ' + M('defineConfig()') + ' : la sentinelle'),
P('Le fichier généré appelle ' + M('defineConfig({...})') + '. Cette fonction ne transforme rien : elle <b>vérifie</b> et renvoie la config. Si quelque chose cloche, l’application <b>refuse de démarrer</b> (principe « fail fast » : mieux vaut planter tout de suite que découvrir le problème en production).'),
*code('''export function defineConfig<T extends MercureConfig>(config: T): T {
  if (!ALLOWED_ALGORITHMS.includes(config.jwt.alg))   // liste blanche : pas de "none" !
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
*warn('Pourquoi interdire l’algorithme <b>none</b> ? Historiquement, une faille JWT célèbre consistait à déclarer « alg: none » (« pas de signature ») pour fabriquer de faux tokens. La liste blanche HS256/384/512 et RS256/384/512 l’empêche.'),
H2('Étape 3 — Le provider'),
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
P('Au démarrage, AdonisJS appelle ' + M('boot()') + '. On y déclare : « quand on me demande <b>mercure</b>, fabrique un ' + M('new Mercure(config)') + ' <i>une seule fois</i> et garde-le ». La fabrication est <b>paresseuse</b> (lazy) : elle n’a lieu que lors de la première demande.'),
H2('Étape 4 — Le service (le raccourci d’import)'),
*code('''let mercure: Mercure
await app.booted(async () => {            // top-level await : attend la fin du démarrage de l'app
  mercure = await app.container.make('mercure')
})
export { mercure as default }''','services/mercure.ts'),
P('Grâce à ce fichier, l’utilisateur écrit simplement ' + M("import mercure from '@mdsiha369/adonis-mercure/services/main'") + ' et obtient l’instance prête à l’emploi. C’est la convention officielle des packages AdonisJS (comme ' + M('@adonisjs/core/services/app') + ').'),
P('Dernier détail : ' + M('src/types/extended.ts') + ' « augmente » (module augmentation) le type ' + M('ContainerBindings') + ' d’AdonisJS pour que ' + M("container.make('mercure')") + ' soit correctement typé.'),
PageBreak()]

# 6 send flow
st+=[H1('6. Le cœur : publier un message avec send()'),
*fig(d_seq(),'Figure 6 — Séquence complète d’un ' + 'send()'),
H2('6.1 La façade : accepter deux écritures'),
*code('''send(topics, data = {}, isPrivateOrOptions: boolean | SendOptions = false) {
  const options: SendOptions =
    typeof isPrivateOrOptions === 'boolean' ? { private: isPrivateOrOptions } : isPrivateOrOptions
  return this.#publisher.publish(topics, data, options)
}''','src/mercure.ts'),
P('Le troisième argument peut être un simple booléen (ancienne API : ' + M("send('/x', data, true)") + ') ou un objet d’options. On normalise vers l’objet : c’est de la <b>rétrocompatibilité</b>.'),
P('Note : le <b>#</b> dans ' + M('#publisher') + ' est un champ <b>privé natif JavaScript</b> (ES2022), vraiment inaccessible de l’extérieur — plus strict que le mot-clé ' + M('private') + ' de TypeScript qui disparaît à la compilation.'),
H2('6.2 Le Publisher : fabriquer et envoyer la requête'),
*code('''const form = new URLSearchParams()
for (const topic of topicList) form.append('topic', topic)       // un champ "topic" par canal
form.append('data', JSON.stringify(data))                         // le contenu, en JSON
if (options.private) form.append('private', 'on')                 // message privé
if (options.id)      form.append('id', options.id)                // id SSE
if (options.type)    form.append('type', options.type)            // type d'évènement
if (options.retry !== undefined) form.append('retry', String(options.retry))

const response = await fetch(this.#config.endpoint, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${this.#config.adminToken}`,
             'Content-Type': 'application/x-www-form-urlencoded' },
  body: form.toString(),
  signal: controller?.signal,        // permet d'annuler au bout de N ms
})
if (!response.ok) throw new MercurePublishError(response.status, await response.text())
return (await response.text()).trim()    // l'id "urn:uuid:..." renvoyé par le hub''','src/publisher.ts (abrégé)'),
P('Le protocole Mercure demande du <b>' + M('application/x-www-form-urlencoded') + '</b> (le format des formulaires HTML classiques), pas du JSON. C’est pourquoi on utilise ' + M('URLSearchParams') + '. Le contenu utile (' + M('data') + ') est lui-même du JSON converti en texte.'),
H3('Le timeout expliqué (AbortController)'),
*code('''const timeout = this.#config.http?.timeout ?? 5000          // 5 s par défaut, 0 = désactivé
const controller = timeout > 0 ? new AbortController() : null
const timer = controller ? setTimeout(() => controller.abort(), timeout) : null
try { ... fetch(..., { signal: controller?.signal }) ... }
catch (err) {
  if (err instanceof MercureError) throw err                       // déjà une erreur à nous
  if (err?.name === 'AbortError') throw new MercureTimeoutError(timeout)
  throw new MercureConnectionError(err)                            // le reste = réseau
} finally { if (timer) clearTimeout(timer) }                       // toujours nettoyer le minuteur''','src/publisher.ts'),
*trade(TRADE[5]),
H2('6.3 Les options SSE'),
*table([['Option','Effet'],
['private: true','Seuls les abonnés munis d’un token valide pour ce topic reçoivent le message.'],
['id','Identifiant de l’évènement. Si le navigateur se déconnecte, il renvoie « Last-Event-ID » et le hub peut lui rejouer ce qu’il a manqué.'],
['type','Nom de l’évènement ; côté navigateur : addEventListener(\'order.shipped\', …).'],
['retry','Délai (ms) avant que le navigateur retente de se reconnecter.']],[35*mm,W-35*mm]),
PageBreak()]

# 7 JWT & subscribe
st+=[H1('7. Sécurité et tokens JWT'),
H2('7.1 Deux types de badges'),
*table([['Token','Qui le possède ?','Droit','Où ça se passe'],
['Admin JWT (adminToken)','Le serveur AdonisJS uniquement','publish: ["*"] — publier partout','Fourni en .env, envoyé dans l’en-tête Authorization de send()'],
['Subscriber JWT','Le navigateur de l’utilisateur','subscribe: [topics autorisés]','Généré par generateSubscribeToken(), à courte durée de vie']],[32*mm,40*mm,45*mm,W-117*mm]),
H2('7.2 La fabrication d’un token'),
*code('''async generate(payload, options = {}) {
  const claims = { mercure: payload }              // Mercure veut les droits sous la clé "mercure"
  if (options.expiresIn !== undefined) {
    if (!Number.isInteger(options.expiresIn) || options.expiresIn <= 0)
      throw new MercureError('expiresIn must be a positive integer (seconds)')
    claims.exp = Math.floor(Date.now() / 1000) + options.expiresIn   // expiration (secondes UNIX)
  }
  return new Promise((resolve, reject) => {
    jws.createSign({ payload: claims, secret: this.#config.jwt.secret,
                     header: { alg: this.#config.jwt.alg } })
       .on('error', reject).on('done', resolve)             // la lib jws est basée sur des évènements
  })
}''','src/token_generator.ts'),
P('La librairie <b>jws</b> (seule dépendance runtime du projet) signe le token. Comme elle fonctionne par <i>évènements</i> (' + M('.on(\'done\')') + '), on l’enveloppe dans une ' + M('Promise') + ' pour pouvoir écrire ' + M('await') + '. ' + M('generateSubscribeToken(topics)') + ' est juste un raccourci qui appelle ' + M('generate({ subscribe: topics })') + '.'),
*warn('Un token sans ' + M('expiresIn') + ' ne expire <b>jamais</b> (choix documenté pour rester compatible Mercure). En production, il vaut mieux passer ' + M('{ expiresIn: 3600 }') + '. Autre piège noté dans le code : un topic joker ' + M('*') + ' donne accès à tous les évènements privés ; ne jamais y mettre de texte venant de l’utilisateur sans validation.'),
H2('7.3 Comment le navigateur donne son token au hub'),
P('Problème classique : l’objet ' + M('EventSource') + ' du navigateur <b>ne permet pas</b> d’ajouter l’en-tête ' + M('Authorization') + '. Le README documente donc deux solutions :'),
*fig(d_cookie(),'Figure 7 — Option 1 : le token voyage dans un cookie'),
*B(['<b>Option cookie</b> : l’app dépose le JWT dans un cookie via ' + M('response.plainCookie') + ' (et non ' + M('response.cookie') + ', qui <i>signe</i> la valeur : le hub la rejetterait). Condition : même domaine « enregistrable » (app.example.com + hub.example.com) et HTTPS pour le préfixe ' + M('__Secure-') + '.',
'<b>Option fetch</b> : utiliser ' + M('@microsoft/fetch-event-source') + ' qui lit le flux avec ' + M('fetch()') + ' et accepte donc l’en-tête ' + M('Authorization: Bearer …') + '.']),
H2('7.4 Autres choix de sécurité du projet'),
*B(['<b>Troncature</b> du corps d’erreur à 200 caractères dans ' + M('MercurePublishError') + ' : évite de fuiter de gros morceaux de réponse (potentiellement sensibles) dans les logs.',
'<b>Secret ≥ 32 caractères</b> et <b>pas d’algorithme « none »</b> (voir §5).',
'<b>Aucun secret par défaut</b> dans configure.ts.',
'Les secrets viennent de l’environnement (' + M('env.get(...)') + '), jamais du code.']),
PageBreak()]

# 8 errors, ping, fake
st+=[H1('8. Erreurs, ping et tests sans hub'),
H2('8.1 Une hiérarchie d’erreurs typées'),
*fig(d_err(),'Figure 8 — Toutes les erreurs héritent de MercureError'),
P('Pourquoi c’est utile ? Pour que l’utilisateur du package puisse <b>réagir différemment</b> selon le problème :'),
*code('''try {
  await mercure.send('/orders/42', { status: 'shipped' })
} catch (e) {
  if (e instanceof MercureTimeoutError)    { /* hub lent : réessayer plus tard */ }
  else if (e instanceof MercurePublishError){ console.log(e.statusCode, e.responseBody) }
  else if (e instanceof MercureConnectionError) { console.log(e.cause) }   // ex: ECONNREFUSED
}''','exemple d\'usage'),
P('Détail malin : ' + M('fetch()') + ' lève juste « TypeError: fetch failed » et cache la vraie cause (ECONNREFUSED, ENOTFOUND…) dans ' + M('error.cause.code') + '. La fonction ' + M('describe()') + ' de ' + M('MercureConnectionError') + ' va la chercher pour donner un message lisible, et garde l’erreur d’origine dans ' + M('cause') + '.'),
H2('8.2 ping()'),
P('Envoie une requête ' + M('HEAD') + ' (sans corps de réponse) au hub. Réponse <b>&lt; 500</b> ⇒ vrai (même un 401/404 prouve que le hub répond) ; 5xx, erreur réseau ou timeout ⇒ faux. Ne lance jamais d’exception : c’est un indicateur « oui/non » pour un health check.'),
H2('8.3 FakeMercure : tester sans serveur'),
P('Tester du code qui appelle un serveur externe est pénible (lent, instable, nécessite un hub). La solution : un <b>faux</b> objet qui respecte le même contrat mais <b>enregistre</b> simplement ce qu’on lui demande.'),
*code('''export class FakeMercure implements MercureContract {
  #sent: SentMessage[] = []
  async send(topics, data = {}, opts = false) {
    this.#sent.push({ topics: asArray(topics), data, options: normalize(opts) })
    return options.id ?? `urn:uuid:${randomUUID()}`           // imite l'id du vrai hub
  }
  assertSent(topic, data?) { /* lance une Error si aucun message ne correspond */ }
  assertNotSent(topic)  { ... }   assertSentCount(n) { ... }   assertNothingSent() { ... }
  getSent() { return [...this.#sent] }    // copie : l'appelant ne peut pas modifier l'état interne
  clear()   { this.#sent = []; this.#tokens = [] }
}''','src/fake_mercure.ts (abrégé)'),
P('Dans les tests de l’application : ' + M("app.container.swap('mercure', () => new FakeMercure())") + ' remplace le vrai par le faux, puis ' + M("fake.assertSent('/orders/42', { status: 'shipped' })") + ' vérifie. Détail de qualité : la comparaison des données passe par ' + M('JSON.parse(JSON.stringify(...))') + ' pour comparer <i>ce que le hub recevrait vraiment</i> (l’ordre des clés ne compte pas ; ' + M('undefined') + ' disparaît).'),
*trade(TRADE[6]),
PageBreak()]

# 9 tests CI release
st+=[H1('9. Qualité : tests, CI et publication'),
H2('9.1 Les tests (Japa)'),
P('Framework : <b>Japa</b> (le framework de test de l’écosystème AdonisJS) avec ' + M('@japa/assert') + '. Couverture mesurée par <b>c8</b>. 7 fichiers :'),
*table([['Fichier','Ce qu’il vérifie'],
['publisher.spec.ts','URL appelée, corps du formulaire, en-tête Bearer, options, id renvoyé, erreurs 4xx/5xx, timeout, erreur réseau.'],
['mercure.spec.ts','Délégation façade → publisher/token, booléen vs objet d’options, ping().'],
['token_generator.spec.ts','Structure du JWT, claim mercure, expiresIn valide/invalide.'],
['define_config.spec.ts','Rejet des algos interdits, URL invalides, token vide, secret trop court.'],
['provider.spec.ts','Singleton enregistré, MercureConfigError si config manquante.'],
['configure.spec.ts','Les codemods sont appelés avec les bons arguments.'],
['fake_mercure.spec.ts','Toutes les assertions et les cas d’échec.']],[45*mm,W-45*mm]),
P('Technique clé : on <b>remplace</b> ' + M('globalThis.fetch') + ' par une fausse fonction dans chaque test, puis on la restaure dans ' + M('teardown') + '. Ainsi on teste Publisher <b>sans réseau</b>, de façon rapide et déterministe (c’est du <i>mocking</i> / <i>stubbing</i>).'),
*code('''group.each.setup(() => { originalFetch = globalThis.fetch })
group.each.teardown(() => { globalThis.fetch = originalFetch })

test('returns the id sent back by the hub', async ({ assert }) => {
  globalThis.fetch = async () => new Response('urn:uuid:1234\\n', { status: 200 })
  const id = await new Publisher(config).publish('test-topic', {})
  assert.equal(id, 'urn:uuid:1234')
})''','tests/publisher.spec.ts'),
H2('9.2 Intégration continue (GitHub Actions)'),
*table([['Job','But'],
['lint','ESLint (config AdonisJS) + Prettier : style cohérent.'],
['typecheck','tsc --noEmit : le compilateur TypeScript valide tous les types.'],
['tests','Matrice : Ubuntu et Windows × Node 20.x et 22.x (4 combinaisons).'],
['adonis-v7','Installe AdonisJS 7 « sans sauvegarder » et relance typecheck + tests : prouve la compatibilité v6 ET v7.']],[28*mm,W-28*mm]),
H2('9.3 Publication sur npm'),
P('Quand on crée une <b>Release</b> sur GitHub, le workflow ' + M('npm-publish.yml') + ' : (1) lance ' + M('npm test') + ', (2) si OK, ' + M('npm publish --access public') + ' avec la permission ' + M('id-token: write') + ' (authentification par OIDC « trusted publishing », sans stocker de mot de passe npm en secret). Avant publication, ' + M('prepublishOnly') + ' compile le TypeScript ; ' + M('postbuild') + ' copie les stubs dans ' + M('build/') + ' car tsc ne copie pas les fichiers .stub.'),
PageBreak(),H2('9.4 Les scripts npm'),
*table([['Commande','Rôle'],
['npm run build','Lint → nettoyage → tsc → copie des stubs'],
['npm test','Lint puis tests avec couverture (c8)'],
['npm run quick:test','Tests seuls, sans lint ni couverture'],
['npm run typecheck','Vérification des types'],
['npm run release','Publie via l’outil « np » (bump de version, tag git, publish)']],[45*mm,W-45*mm]),
Spacer(1,6)]

# 10 history
st+=[H1('10. Histoire du projet et décisions'),
*fig(d_time(),'Figure 9 — Les grandes versions (d’après CHANGELOG.md)'),
*table([['Version','Ce qui a changé et pourquoi'],
['1.0.12 (2024)','Première version stable.'],
['2.0.0','Refonte majeure : séparation Publisher/TokenGenerator ; <b>remplacement de la dépendance « got » par le fetch natif</b> de Node (moins de dépendances) ; erreurs levées au lieu d’être avalées ; ajout de ping, FakeMercure, MercureContract, options SSE, generateSubscribeToken.'],
['2.0.1','Correctifs sécurité : suppression des secrets codés en dur, liste blanche d’algorithmes, secret ≥ 32 caractères, troncature des erreurs.'],
['2.1.x','Renommage du package (@das3mical → @mdsiha369), timeout configurable + MercureTimeoutError.'],
['2.2.0','expiresIn, MercureConnectionError, support AdonisJS 7, types publics sans dépendance à @types/jws, ping() fiable (5xx = faux), package allégé (13,7 → 9 kB).'],
['3.0.0','<b>Changement cassant (breaking)</b> : send() renvoie l’id (string) au lieu d’un objet Response. Version majeure car du code existant peut casser (SemVer).']],[28*mm,W-28*mm]),
H2('Les décisions de conception qu’il faut savoir justifier'),
*table([['Décision','Pourquoi'],
['Utiliser le fetch natif plutôt que « got »','Moins de dépendances, moins de surface d’attaque, disponible dans Node ≥ 18.'],
['Une seule dépendance runtime (jws)','Petit, maintenu ; les JWT demandent de la crypto qu’on ne réécrit pas soi-même.'],
['Interface MercureContract','Permet FakeMercure interchangeable ; garantit que le faux et le vrai évoluent ensemble (le compilateur râle sinon).'],
['Erreurs spécialisées','L’appelant distingue « hub lent », « hub en panne », « refus » sans parser du texte.'],
['defineConfig qui valide au démarrage','Fail fast : une mauvaise config casse au boot, pas au milieu d’une requête utilisateur.'],
['Champs privés natifs (#)','Vraie encapsulation à l’exécution.'],
['send() renvoie l’id (v3)','Plus utile que Response : l’appelant n’a plus à lire le corps ; l’id sert au suivi/rejeu. Prix : version majeure.'],
['peerDependency @adonisjs/core ^6.2 || ^7','On utilise le framework déjà installé par l’utilisateur ; pas de doublon.'],
['ESM ("type": "module")','Standard moderne ; AdonisJS 6/7 est en ESM (d’où les imports en « .js »).']],[55*mm,W-55*mm]),
PageBreak()]

# 11 usage cookbook
st+=[H1('11. Exemples d’utilisation concrets'),
H2('Backend : publier'),
*code('''import mercure from '@mdsiha369/adonis-mercure/services/main'

// Public
const id = await mercure.send('/orders/42', { status: 'shipped' })

// Plusieurs topics + privé + options SSE
await mercure.send(['/orders/42', '/notifications/user/1'], { status: 'shipped' },
  { private: true, id: 'msg-001', type: 'order.shipped', retry: 5000 })

// Health check
if (!(await mercure.ping())) logger.warn('Mercure hub unreachable')''','Application AdonisJS'),
H2('Frontend : écouter'),
*code('''const url = new URL('https://hub.example.com/.well-known/mercure')
url.searchParams.append('topic', '/orders/42')

const es = new EventSource(url, { withCredentials: true })   // cookie envoyé automatiquement
es.addEventListener('order.shipped', (e) => {
  const payload = JSON.parse(e.data)       // { status: 'shipped' }
  updateUI(payload.status)
})''','Navigateur'),
H2('Test unitaire d’un contrôleur'),
*code('''test('ship order notifies subscribers', async ({ assert }) => {
  app.container.swap('mercure', () => new FakeMercure())
  await controller.ship(42)
  const fake = (await app.container.make('mercure')) as FakeMercure
  fake.assertSent('/orders/42', { status: 'shipped' })
  app.container.restore('mercure')
})''','Test'),
H2('Feuille de route (README)'),
*B([M('generatePublishToken(topics)') + ' — symétrique de generateSubscribeToken',
M('sendBatch(messages[])') + ' — plusieurs publications en un appel',
'<b>Retry avec backoff</b> — nouvelle tentative automatique sur erreur transitoire',
'<b>Classes d’évènements typées</b> — ' + M('new OrderShippedEvent(id)') + ' au lieu d’objets en vrac']),
PageBreak()]

# 12 Q&A (Canada edition)
st+=[H1('12. Questions d’entretien (System Design, production, sécurité, tests)'),
P('Chaque réponse suit le format : <b>Réponse directe (30 s)</b> → <b>Justification technique</b> → <b>Limite / Amélioration possible</b>. Les éléments précis sur le hub Mercure (historique, transport, clustering) dépendent de la version et de l’édition déployées : à confirmer dans sa documentation avant de les affirmer. Le repo ne contient aucun benchmark ni métrique de production : ne présentez pas de chiffres comme mesurés.','small')]
for _n,(q,d,j,l) in enumerate(QA_CA,1):
    st+=qa(_n,q,d,j,l)
st+=PB_RETRY if False else []
st+=[PageBreak()]

# 13 glossary
st+=[H1('13. Glossaire express'),
*table([['Terme','Définition simple'],
['SSE','Server-Sent Events : flux HTTP à sens unique serveur → navigateur.'],
['EventSource','API navigateur qui ouvre et maintient un flux SSE.'],
['Hub','Serveur Mercure qui reçoit les publications et les redistribue.'],
['Topic','Nom d’un canal de diffusion (souvent une URL/chemin).'],
['Publisher / Subscriber','Celui qui envoie / celui qui écoute.'],
['JWT','JSON Web Token : jeton signé contenant des droits.'],
['HS256 / RS256','Algorithmes de signature : HMAC avec secret partagé / RSA avec clé privée-publique.'],
['claim','Une information dans le payload du JWT (ex. exp, mercure).'],
['exp','Date d’expiration du token (secondes UNIX).'],
['IoC / DI','Inversion de contrôle / injection de dépendances : le framework fournit les objets.'],
['Container','Registre central des services d’AdonisJS.'],
['Provider','Classe qui enregistre des services au démarrage.'],
['Codemod','Script qui modifie automatiquement le code source d’un projet.'],
['Stub','Fichier modèle servant à en générer un autre.'],
['Façade','Objet simple qui cache la complexité de sous-systèmes.'],
['Mock / Fake / Stub','Doublure de test qui remplace une vraie dépendance.'],
['AbortController','API standard pour annuler un fetch (utilisée pour le timeout).'],
['ESM','Modules ECMAScript : import/export natifs.'],
['SemVer','Convention de numérotation de versions MAJEUR.MINEUR.CORRECTIF.'],
['CI','Intégration continue : tests automatiques à chaque push.'],
['OIDC / trusted publishing','Publier sur npm via identité GitHub, sans mot de passe stocké.'],
['peerDependency','Dépendance que l’utilisateur doit déjà avoir (ici AdonisJS).'],
['Graceful degradation','Le système continue de fonctionner (en mode réduit) quand une dépendance tombe.'],
['Fail-fast','Échouer immédiatement et bruyamment sur une erreur évitable (config invalide au boot).'],
['Backoff / jitter','Délai croissant entre deux tentatives / aléa ajouté pour éviter les pics synchronisés.'],
['Circuit breaker','Coupe les appels vers un service défaillant pour lui laisser le temps de récupérer.'],
['Idempotency','Rejouer une opération donne le même résultat (essentiel avec at-least-once).'],
['Outbox pattern','Écrire l’événement dans la base dans la transaction, puis le publier par un worker : évite le dual write.'],
['Thundering herd','Reconnexion massive simultanée de clients après une panne ou un deploy.'],
['SLO / p99','Objectif de niveau de service / latence du 99e percentile.'],
['Observability','Capacité de comprendre le système via métriques, logs et traces.'],
['Test double','Terme générique pour fake, stub, mock, spy.'],
['Least privilege','Ne donner que les droits strictement nécessaires (ex. topics précis dans le JWT).']],[42*mm,W-42*mm]),
H2('Avant l’entretien : défendre vos décisions devant un Tech Lead / Engineering Manager'),
*B(['<b>Parlez en trade-offs</b> : pour chaque décision, nommez l’alternative écartée, le gain, le coût, et dans quel contexte vous changeriez d’avis (« it depends on the SLO »).',
'<b>Ouvrez par le pattern, pas le framework</b> : IoC / DIP / Facade / fail-fast. Montrez l’équivalent NestJS / Fastify / Express (section 3).',
'<b>Sachez dessiner</b> à la main : Figure 3 (browser — app — hub), Figure 6 (séquence send()) et le flux cookie (Figure 7).',
'<b>Assumez les limites</b> : pas de retry, pas de métriques, `expiresIn` optionnel, `FakeMercure` sans simulation de panne, aucun benchmark. Puis proposez l’amélioration concrète (c’est ce qu’un senior fait).',
'<b>Préparez 3 chiffres à justifier</b> (timeout 5 s, secret ≥ 32 caractères, limite ~6 connexions HTTP/1.1) et soyez clair sur ce qui est mesuré ou non.',
'<b>Restez honnête sur le périmètre</b> : c’est une bibliothèque, pas un service en production à grande échelle ; parlez de ce que vous feriez à l’échelle, sans prétendre l’avoir fait.',
'<b>Style nord-américain</b> : réponses structurées (situation → décision → résultat), ownership (« I decided / I chose »), exemples concrets, et questions de clarification avant de répondre à un System Design.']),
H2('Mots-clés anglais à placer naturellement'),
*table(CHECK_ROWS,[52*mm,W-52*mm])]
doc.build(st)
print('ok')
