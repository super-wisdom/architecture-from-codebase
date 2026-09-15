#!/usr/bin/env python3
import html, os, textwrap
INK="#111C29"; SOFT="#42556A"; TEAL="#0F7788"; TEALD="#0b5460"
LINE="#C4CFDA"; PANEL="#16273B"
NOTE_BG="#E4F3F5"; NOTE_BD="#bfe2e7"; NOTE_TX="#0b5460"
SAFE_BG="#fdf6f1"; SAFE_BD="#e3c3ad"; SAFE_TX="#8a3d13"
FRAG_BD="#9cc9d1"; FRAG_TAB="#E4F3F5"
FONT="'Inter','Segoe UI',system-ui,sans-serif"; MONO="'IBM Plex Mono',monospace"
def esc(s): return html.escape(str(s))
def wrap(t,w):
    o=[]
    for ln in t.split("\n"): o+=textwrap.wrap(ln,w) or [""]
    return o

class Seq:
    def __init__(self, parts, actors=None, safety=False, annotations=None):
        self.parts=parts; self.keys=[p[0] for p in parts]
        self.actors=set(actors or []); self.safety=safety
        self.events=[]; self.ann=annotations or []; self.mc=0
        self.pad_l=24; self.box_h=36; self.box_gap=34; self.row_h=48
        self.top=16; self.line_top=self.top+self.box_h
        self.px={}; self.box_w={}; x=self.pad_l
        for k,lab in parts:
            w=max(96,12+len(lab)*8.2); self.box_w[k]=w; self.px[k]=x+w/2; x+=w+self.box_gap
        self.diagram_w=x-self.box_gap+self.pad_l
        self.has_ann=bool(self.ann); self.ann_w=250 if self.has_ann else 0
        self.width=self.diagram_w+(self.ann_w+16 if self.has_ann else 8)
    def msg(self,a,b,label,ret=False): self.events.append(["msg",a,b,label,ret,self.mc]); self.mc+=1
    def selfmsg(self,a,label): self.events.append(["self",a,label,self.mc]); self.mc+=1
    def note(self,keys,label): self.events.append(["note",keys,label])
    def frag(self,label): self.events.append(["frag_s",label])
    def alt(self,label): self.events.append(["frag_div",label])
    def endfrag(self): self.events.append(["frag_e"])

    def render(self):
        y=self.line_top+30; fstack=[]; frags=[]; ymap={}
        for ev in self.events:
            t=ev[0]
            if t=="msg": ev.append(y); ymap[ev[5]]=y; y+=self.row_h
            elif t=="self": ev.append(y); ymap[ev[3]]=y; y+=self.row_h+6
            elif t=="note":
                y+=14; ev.append(y); y+=len(wrap(ev[2],44))*15+24
            elif t=="frag_s": y+=10; fstack.append([len(frags),y,ev[1],[]]); frags.append([y,None,ev[1],[]]); y+=36
            elif t=="frag_div": fstack[-1][3].append((y,ev[1])); y+=34
            elif t=="frag_e":
                top=fstack.pop(); frags[top[0]][1]=y+6; frags[top[0]][3]=top[3]; y+=16
        H=y+26; W=int(self.width)
        S=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {int(H)}" width="{W}" height="{int(H)}" '
           f'font-family="{FONT}" style="max-width:100%;height:auto;display:block">']
        S.append(f'<rect width="{W}" height="{int(H)}" fill="#ffffff"/>')
        fx1=self.px[self.keys[0]]-self.box_w[self.keys[0]]/2-14
        fx2=self.px[self.keys[-1]]+self.box_w[self.keys[-1]]/2+14
        for ty,by,label,divs in frags:
            by=by or ty+40
            S.append(f'<rect x="{fx1:.0f}" y="{ty:.0f}" width="{fx2-fx1:.0f}" height="{by-ty:.0f}" rx="6" '
                     f'fill="none" stroke="{FRAG_BD}" stroke-width="1.3"/>')
            kind=label.split()[0]; rest=label[len(kind):].strip(); tabw=26+len(kind)*7
            S.append(f'<path d="M{fx1:.0f},{ty:.0f} h{tabw:.0f} v14 l-8,8 h-{tabw-8:.0f} z" fill="{FRAG_TAB}" stroke="{FRAG_BD}"/>')
            S.append(f'<text x="{fx1+7:.0f}" y="{ty+15:.0f}" font-size="11" font-weight="700" fill="{TEALD}" font-family="{MONO}">{esc(kind)}</text>')
            if rest: S.append(f'<text x="{fx1+tabw+8:.0f}" y="{ty+15:.0f}" font-size="11" fill="{SOFT}">{esc(rest)}</text>')
            for dy,dl in divs:
                S.append(f'<line x1="{fx1:.0f}" y1="{dy:.0f}" x2="{fx2:.0f}" y2="{dy:.0f}" stroke="{FRAG_BD}" stroke-dasharray="5 4"/>')
                dk=dl.split()[0]; dr=dl[len(dk):].strip()
                S.append(f'<text x="{fx1+8:.0f}" y="{dy+15:.0f}" font-size="11" font-weight="700" fill="{TEALD}" font-family="{MONO}">{esc(dk)}</text>')
                if dr: S.append(f'<text x="{fx1+8+len(dk)*7+6:.0f}" y="{dy+15:.0f}" font-size="11" fill="{SOFT}">{esc(dr)}</text>')
        for k,lab in self.parts:
            x=self.px[k]; w=self.box_w[k]
            S.append(f'<line x1="{x:.0f}" y1="{self.line_top:.0f}" x2="{x:.0f}" y2="{H-16:.0f}" stroke="{LINE}" stroke-width="1.3" stroke-dasharray="2 4"/>')
            fill=PANEL if k in self.actors else TEAL
            S.append(f'<rect x="{x-w/2:.0f}" y="{self.top}" width="{w:.0f}" height="{self.box_h}" rx="7" fill="{fill}"/>')
            S.append(f'<text x="{x:.0f}" y="{self.top+self.box_h/2+4:.0f}" text-anchor="middle" font-size="12.5" font-weight="600" fill="#fff">{esc(lab)}</text>')
        ncol=SAFE_BG if self.safety else NOTE_BG; nbd=SAFE_BD if self.safety else NOTE_BD; ntx=SAFE_TX if self.safety else NOTE_TX
        for ev in self.events:
            t=ev[0]
            if t=="msg":
                _,a,b,label,ret,idx,y=ev; x1=self.px[a]; x2=self.px[b]
                dash=' stroke-dasharray="6 4"' if ret else ''
                S.append(f'<line x1="{x1:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y:.0f}" stroke="{SOFT}" stroke-width="1.5"{dash}/>')
                if x2>=x1: S.append(f'<path d="M{x2:.0f},{y:.0f} l-9,-4.5 l0,9 z" fill="{SOFT}"/>')
                else: S.append(f'<path d="M{x2:.0f},{y:.0f} l9,-4.5 l0,9 z" fill="{SOFT}"/>')
                S.append(f'<text x="{(x1+x2)/2:.0f}" y="{y-7:.0f}" text-anchor="middle" font-size="11.5" fill="{INK}">{esc(label)}</text>')
            elif t=="self":
                _,a,label,idx,y=ev; x=self.px[a]
                S.append(f'<path d="M{x:.0f},{y:.0f} h34 v20 h-34" fill="none" stroke="{SOFT}" stroke-width="1.5"/>')
                S.append(f'<path d="M{x:.0f},{y+20:.0f} l9,-4.5 l0,9 z" fill="{SOFT}"/>')
                S.append(f'<text x="{x+42:.0f}" y="{y+3:.0f}" font-size="11.5" fill="{INK}">{esc(label)}</text>')
            elif t=="note":
                _,keys,label,y=ev; xs=[self.px[k] for k in keys]; c1=min(xs); c2=max(xs)
                lines=wrap(label,44); bw=max(c2-c1+120, max(len(l) for l in lines)*6.6+24); bx=(c1+c2)/2-bw/2
                bh=len(lines)*15+12
                S.append(f'<rect x="{bx:.0f}" y="{y:.0f}" width="{bw:.0f}" height="{bh}" rx="5" fill="{ncol}" stroke="{nbd}" stroke-width="1.2"/>')
                for j,l in enumerate(lines):
                    S.append(f'<text x="{(c1+c2)/2:.0f}" y="{y+16+j*15:.0f}" text-anchor="middle" font-size="11" fill="{ntx}">{esc(l)}</text>')
        if self.has_ann:
            ax=self.diagram_w+14; last=self.line_top+6
            for n,(mi,text) in enumerate(self.ann,1):
                ty=ymap.get(mi,self.line_top+40); lines=wrap(text,30); ch=len(lines)*14+16
                cy=max(ty-ch/2,last+10); last=cy+ch; mx=self.px[self.keys[-1]]
                S.append(f'<line x1="{mx:.0f}" y1="{ty:.0f}" x2="{ax:.0f}" y2="{cy+ch/2:.0f}" stroke="{TEAL}" stroke-dasharray="3 3" opacity="0.65"/>')
                S.append(f'<rect x="{ax:.0f}" y="{cy:.0f}" width="{self.ann_w-8:.0f}" height="{ch:.0f}" rx="7" fill="#f6fbfc" stroke="{TEAL}" stroke-width="1.2"/>')
                S.append(f'<rect x="{ax:.0f}" y="{cy:.0f}" width="4" height="{ch:.0f}" rx="2" fill="{TEAL}"/>')
                S.append(f'<circle cx="{ax+18:.0f}" cy="{cy+15:.0f}" r="9" fill="{TEAL}"/>')
                S.append(f'<text x="{ax+18:.0f}" y="{cy+19:.0f}" text-anchor="middle" font-size="11" font-weight="700" fill="#fff" font-family="{MONO}">{n}</text>')
                for j,l in enumerate(lines):
                    S.append(f'<text x="{ax+32:.0f}" y="{cy+13+j*14:.0f}" font-size="11" fill="{INK}">{esc(l)}</text>')
        S.append('</svg>'); return "\n".join(S)

# ---------------------------------------------------------------------------
# DEMO — run `python seqgen.py` to emit svgs/demo.svg. Import `Seq` elsewhere.
# API:  s=Seq(participants=[("key","Label"),...], actors={"key"}, safety=False,
#             annotations=[(msg_index, "note text"), ...])
#   s.msg(a,b,"label", ret=False)  solid call (ret=True → dashed return)
#   s.selfmsg(a,"label")           self-call loop
#   s.note([keys],"text")          note box spanning participants
#   s.frag("alt <cond>") / s.alt("else <cond>") / s.endfrag()   fragments
#   svg = s.render()               → responsive inline <svg> string
# annotation msg_index counts msg + selfmsg calls in order, starting at 0.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import os
    os.makedirs("svgs", exist_ok=True)
    s = Seq([("U","User"),("FE","front-end"),("Core","core"),("API","model API")],
            actors={"U"},
            annotations=[(1,"One decoupled queue buys streaming + cancellation."),
                         (3,"Deltas stream back as events.")])
    s.msg("U","FE","prompt")
    s.msg("FE","Core","submit (queue)")
    s.msg("Core","API","request (stream)")
    s.frag("loop streaming")
    s.msg("API","Core","delta", ret=True)
    s.msg("Core","FE","event", ret=True)
    s.endfrag()
    s.msg("API","Core","done", ret=True)
    open("svgs/demo.svg","w").write(s.render())
    print("wrote svgs/demo.svg")
