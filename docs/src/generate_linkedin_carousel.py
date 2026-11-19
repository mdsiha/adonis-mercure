import sys
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
D='/usr/share/fonts/truetype/dejavu/'
for n,f in [('DV','DejaVuSans.ttf'),('DV-B','DejaVuSans-Bold.ttf'),('DVM','DejaVuSansMono.ttf')]: pdfmetrics.registerFont(TTFont(n,D+f))
W,H=1080,1350
NAVY=colors.HexColor('#0b1b4d'); BLUE=colors.HexColor('#2563eb'); LBLUE=colors.HexColor('#dbeafe')
GREEN=colors.HexColor('#16a34a'); LGREEN=colors.HexColor('#dcfce7'); ORANGE=colors.HexColor('#ea580c'); LORANGE=colors.HexColor('#ffedd5')
RED=colors.HexColor('#dc2626'); LRED=colors.HexColor('#fee2e2'); PURPLE=colors.HexColor('#7c3aed'); LPURPLE=colors.HexColor('#ede9fe')
INK=colors.HexColor('#1f2937'); MUTED=colors.HexColor('#6b7280'); DARK=colors.HexColor('#111827'); WHITE=colors.white
M=80  # margin
def text(c,x,y,t,font='DV',size=40,color=INK,width=None,lead=1.3,align='l'):
    c.setFont(font,size); c.setFillColor(color)
    lines=simpleSplit(t,font,size,width) if width else [t]
    for i,l in enumerate(lines):
        yy=y-i*size*lead
        if align=='c': c.drawCentredString(x,yy,l)
        else: c.drawString(x,yy,l)
    return y-len(lines)*size*lead
def box(c,x,y,w,h,lines,fill,stroke,size=30):
    c.setFillColor(fill); c.setStrokeColor(stroke); c.setLineWidth(3); c.roundRect(x,y,w,h,18,fill=1,stroke=1)
    n=len(lines); lh=size*1.35; top=y+h/2+(n-1)*lh/2-size*0.3
    for i,l in enumerate(lines):
        c.setFillColor(INK); c.setFont('DV-B' if i==0 else 'DV',size if i==0 else size-6)
        c.drawCentredString(x+w/2,top-i*lh,l)
def arrow(c,x1,y1,x2,y2,color,dash=None,lw=4):
    import math
    c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(lw)
    if dash: c.setDash(*dash)
    c.line(x1,y1,x2,y2); c.setDash()
    a=math.atan2(y2-y1,x2-x1); s=20
    p=c.beginPath(); p.moveTo(x2,y2); p.lineTo(x2-s*math.cos(a-0.4),y2-s*math.sin(a-0.4)); p.lineTo(x2-s*math.cos(a+0.4),y2-s*math.sin(a+0.4)); p.close(); c.drawPath(p,fill=1,stroke=0)
def code(c,x,y,w,lines,size=25):
    h=len(lines)*size*1.45+50
    c.setFillColor(DARK); c.roundRect(x,y-h,w,h,16,fill=1,stroke=0)
    for i,(l,col) in enumerate(lines):
        c.setFillColor(col); c.setFont('DVM',size); c.drawString(x+28,y-45-i*size*1.45,l)
    return y-h
CG=colors.HexColor('#9ca3af'); CW=colors.HexColor('#e5e7eb'); CY=colors.HexColor('#fcd34d'); CGr=colors.HexColor('#86efac'); CR=colors.HexColor('#fca5a5')

def build(lang):
    T={
    'fr':dict(out='carrousel-linkedin-fr.pdf',
      s1=['Un service tiers lent','peut faire tomber','votre application'],s1b='3 décisions de design tirées de mon package AdonisJS + Mercure (temps réel)',s1c='Swipe →',
      s2t='Le contexte',s2a='Mon package envoie 1 POST au hub.',s2b='Le hub garde les connexions ouvertes et diffuse en SSE.',
      boxes=(['Navigateur','EventSource'],['App AdonisJS','+ adonis-mercure'],['Hub Mercure','(serveur externe)']),
      s2c='Question : que se passe-t-il quand le hub est lent ou injoignable ?',
      s3t='Décisions 1 & 2',s3a='1. Un timeout explicite',s3a2='5 s par défaut. Sans lui, un hub lent accumule des requêtes en attente et fait exploser la latence p99.',
      s3b='2. Des erreurs typées',s3b2='L’appelant décide quoi faire, sans parser de texte. Brancher un retry devient simple.',s3c='simplifié',
      s4t='Décision 3',s4a='Fail-fast au démarrage…',s4b='…mais sans ping du hub',
      s4l=['Config invalide','→ l’app refuse de démarrer','Bug développeur : détecté au déploiement'],
      s4r=['Hub en panne','→ l’app démarre quand même','Incident d’exploitation : le temps réel se dégrade, le reste fonctionne'],
      s4c='Sinon une panne du hub bloquerait tous mes déploiements.',
      s5t='Limites assumées',s5l=['Pas de retry pour l’instant','Pas de logs ni de métriques intégrés','Timeout de 5 s trop long pour un SLO p99 strict'],
      s5n='Prochaine étape',s5nl=['Retry avec backoff + jitter, seulement sur erreurs transitoires','Circuit breaker','Hooks pour métriques (OpenTelemetry)'],
      s5q='Et vous : un timeout par défaut dans vos clients HTTP ?',s5p='npm : @mdsiha369/adonis-mercure'),
    'en':dict(out='carousel-linkedin-en.pdf',
      s1=['A slow third-party','service can take down','your application'],s1b='3 design decisions from my AdonisJS + Mercure (real-time) package',s1c='Swipe →',
      s2t='The context',s2a='My package sends 1 POST to the hub.',s2b='The hub keeps connections open and fans out over SSE.',
      boxes=(['Browser','EventSource'],['AdonisJS app','+ adonis-mercure'],['Mercure Hub','(external server)']),
      s2c='Question: what happens when the hub is slow or unreachable?',
      s3t='Decisions 1 & 2',s3a='1. An explicit timeout',s3a2='5 s by default. Without it, a slow hub piles up pending requests and blows up p99 latency.',
      s3b='2. Typed errors',s3b2='The caller decides what to do, without parsing text. Plugging in a retry becomes easy.',s3c='simplified',
      s4t='Decision 3',s4a='Fail-fast at startup…',s4b='…but no hub ping',
      s4l=['Invalid config','→ the app refuses to start','Developer bug: caught at deploy time'],
      s4r=['Hub down','→ the app starts anyway','Operational incident: real time degrades, everything else works'],
      s4c='Otherwise a hub outage would block all my deployments.',
      s5t='Known limits',s5l=['No retry yet','No built-in logs or metrics','5 s timeout is too long for a strict p99 SLO'],
      s5n='Next step',s5nl=['Retry with backoff + jitter, transient errors only','Circuit breaker','Metrics hooks (OpenTelemetry)'],
      s5q='What about you: a default timeout in your HTTP clients?',s5p='npm: @mdsiha369/adonis-mercure'),
    }[lang]
    c=canvas.Canvas('/home/user/adonis-mercure/docs/linkedin/'+T['out'],pagesize=(W,H))
    c.setTitle('adonis-mercure — 3 design decisions'); 
    def frame(n,bg=WHITE,fg=MUTED):
        c.setFillColor(bg); c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColor(BLUE); c.rect(0,H-18,W,18,fill=1,stroke=0)
        c.setFont('DV',24); c.setFillColor(fg); c.drawString(M,50,'@mdsiha369/adonis-mercure'); c.drawRightString(W-M,50,'%d / 5'%n)
    # 1
    frame(1,NAVY,colors.HexColor('#93c5fd'))
    y=H-380
    for l in T['s1']: c.setFont('DV-B',68); c.setFillColor(WHITE); c.drawString(M,y,l); y-=90
    text(c,M,y-40,T['s1b'],'DV',38,colors.HexColor('#bfdbfe'),W-2*M,1.4)
    c.setFillColor(BLUE); c.roundRect(M,150,260,80,40,fill=1,stroke=0); c.setFillColor(WHITE); c.setFont('DV-B',34); c.drawCentredString(M+130,178,T['s1c'])
    c.showPage()
    # 2
    frame(2); text(c,M,H-130,T['s2t'],'DV-B',64,BLUE)
    y=text(c,M,H-230,T['s2a'],'DV',38,INK,W-2*M); y=text(c,M,y-6,T['s2b'],'DV',38,INK,W-2*M)
    bw,bh=230,140; xs=[M,W/2-bw/2,W-M-bw]; yy=820
    box(c,xs[0],yy,bw,bh,T['boxes'][0],LGREEN,GREEN,26); box(c,xs[1],yy,bw,bh,T['boxes'][1],LBLUE,BLUE,26); box(c,xs[2],yy,bw,bh,T['boxes'][2],LORANGE,ORANGE,26)
    arrow(c,xs[1]+bw+6,yy+bh/2,xs[2]-6,yy+bh/2,BLUE); text(c,(xs[1]+bw+xs[2])/2,yy+bh/2+22,'POST','DV-B',28,BLUE,align='c')
    # SSE push path: hub bottom -> down -> left -> up to browser
    c.setStrokeColor(ORANGE); c.setLineWidth(4)
    c.line(xs[2]+bw/2,yy,xs[2]+bw/2,yy-110); c.line(xs[2]+bw/2,yy-110,xs[0]+bw/2,yy-110)
    arrow(c,xs[0]+bw/2,yy-110,xs[0]+bw/2,yy-6,ORANGE)
    text(c,W/2,yy-80,'SSE (push)','DV-B',30,ORANGE,align='c')
    text(c,M,520,T['s2c'],'DV-B',46,RED,W-2*M,1.35)
    c.showPage()
    # 3
    frame(3); text(c,M,H-130,T['s3t'],'DV-B',64,BLUE)
    y=text(c,M,H-230,T['s3a'],'DV-B',44,INK,W-2*M); y=text(c,M,y,T['s3a2'],'DV',36,INK,W-2*M,1.35)
    y=code(c,M,y-10,W-2*M,[('const ctrl = new AbortController()',CW),('setTimeout(() => ctrl.abort(), 5000)',CY),('await fetch(endpoint, { signal: ctrl.signal })',CW)],25)
    y=text(c,M,y-90,T['s3b'],'DV-B',44,INK,W-2*M); y=text(c,M,y,T['s3b2'],'DV',36,INK,W-2*M,1.35)
    y=code(c,M,y-10,W-2*M,[('if (err.name === \'AbortError\')',CW),('  throw new MercureTimeoutError(ms)',CGr),('throw new MercureConnectionError(err)',CR),('// + MercurePublishError (non-2xx)',CG)],27)
    text(c,W-M,y-34,T['s3c'],'DV',22,MUTED,align='l') if False else c.drawRightString(W-M,y-34,T['s3c'])
    c.showPage()
    # 4
    frame(4); text(c,M,H-130,T['s4t'],'DV-B',64,BLUE)
    y=text(c,M,H-230,T['s4a'],'DV-B',46,INK,W-2*M); y=text(c,M,y,T['s4b'],'DV-B',46,ORANGE,W-2*M)
    cw=(W-2*M-30)/2; top=y-50; ch=600
    for i,(L,col,fill) in enumerate([(T['s4l'],GREEN,LGREEN),(T['s4r'],ORANGE,LORANGE)]):
        x=M+i*(cw+30); c.setFillColor(fill); c.setStrokeColor(col); c.setLineWidth(3); c.roundRect(x,top-ch,cw,ch,20,fill=1,stroke=1)
        text(c,x+28,top-80,L[0],'DV-B',42,col,cw-56); text(c,x+28,top-170,L[1],'DV-B',35,INK,cw-56,1.3); text(c,x+28,top-330,L[2],'DV',32,INK,cw-56,1.4)
    text(c,M,top-ch-70,T['s4c'],'DV-B',40,INK,W-2*M,1.35)
    c.showPage()
    # 5
    frame(5); text(c,M,H-130,T['s5t'],'DV-B',64,RED)
    y=H-230
    for l in T['s5l']: y=text(c,M,y,'• '+l,'DV',34,INK,W-2*M,1.35)-14
    y=text(c,M,y-30,T['s5n'],'DV-B',56,GREEN,W-2*M)
    for l in T['s5nl']: y=text(c,M,y,'• '+l,'DV',34,INK,W-2*M,1.35)-14
    c.setFillColor(LBLUE); c.roundRect(M,120,W-2*M,200,20,fill=1,stroke=0)
    text(c,M+30,260,T['s5q'],'DV-B',36,BLUE,W-2*M-60,1.3); text(c,M+30,160,T['s5p'],'DVM',28,INK)
    c.showPage(); c.save()
build('fr'); build('en'); print('ok')
