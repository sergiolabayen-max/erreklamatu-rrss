# En Jake: encuadres fijos. Con pantalla partida (36 s a 237 s) Jon está siempre en la misma ventana; antes, primer plano de perfil que el detector no ve.
import defs
SPLIT=[4,114,556]
def fijo(t):
    a,b=t[0],t[1]
    if len(t)>4 and "enc" in t[4]: return t
    if a>=35.92 and b<=237.3: e=SPLIT
    elif a>=11.5 and b<=27.0: e=[[a,200,60,520],[13.2,316,45,690]]
    elif a>=27.0 and b<=42.2: e=[[a,316,45,690],[35.92]+SPLIT]
    else: raise SystemExit(f"sin regla {t[:3]}")
    return tuple(t[:4])+({"enc":e},)
for i,c in enumerate(defs.C):
    if c[0]=="ej": defs.C[i]=(c[0],c[1],c[2],c[3],[fijo(t) for t in c[4]],c[5])
