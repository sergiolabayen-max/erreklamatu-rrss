#!/usr/bin/env python3
"""Sintonía de Erreklamatu: música original, generada por código, para los vídeos que no tienen voz.

Uso:  python3 sintonia.py salida.wav segundos [arreglo] [segundos_de_cierre]
  arreglo: "viva" (por defecto: 104 pulsos por minuto, con base rítmica suave) o "tranquila" (92, sin percusión).
  segundos_de_cierre: lo que dura la última pantalla del vídeo (la del teléfono); ahí suena el motivo completo y la música se apaga.

Qué es: un motivo de cinco notas, una por sílaba de «E-rre-kla-ma-tu» (corta, corta, larga, corta, larga), en re mayor,
sobre cuatro acordes (re, si menor, sol, la). Al principio el motivo queda abierto (termina en la); al final se cierra (termina en re).
Todo se sintetiza aquí con ondas y ruido: no usa grabaciones, muestras ni bibliotecas de sonidos de terceros.
Necesita numpy y scipy. Nadie ha escuchado el resultado al generarlo: lo juzga Sergio.
"""
import sys
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
from scipy.io import wavfile

SR = 44100
A4 = 440.0
def hz(m): return A4 * 2 ** ((m - 69) / 12)
def t_(n): return np.arange(int(n)) / SR

def env_adsr(n, a, d, s, r):
    """Envolvente: ataque, caída, nivel sostenido y salida (en segundos), para n muestras."""
    a_, d_, r_ = int(a * SR), int(d * SR), int(r * SR)
    e = np.full(n, s, dtype=np.float64)
    a_ = min(a_, n); e[:a_] = np.linspace(0, 1, a_, endpoint=False)
    d2 = min(d_, max(n - a_, 0)); e[a_:a_ + d2] = np.linspace(1, s, d2, endpoint=False)
    r_ = min(r_, n); e[n - r_:] *= np.linspace(1, 0, r_)
    return e

def campana(f, dur, vel=1.0):
    """Nota de timbre de marimba o campanilla suave: el motivo y los arpegios."""
    n = int(dur * SR); t = t_(n)
    x = (np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2)
         + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 5.5)
         + 0.18 * np.sin(2 * np.pi * 4.02 * f * t) * np.exp(-t * 11)
         + 0.06 * np.sin(2 * np.pi * 6.1 * f * t) * np.exp(-t * 18))
    x[:int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
    x[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
    return vel * x

def colchon(f, dur, desafina=0.0):
    """Nota larga y cálida para los acordes."""
    n = int(dur * SR); t = t_(n); x = np.zeros(n)
    for k, amp in ((1, 1.0), (2, 0.42), (3, 0.2), (4, 0.09), (5, 0.04)):
        x += amp * np.sin(2 * np.pi * k * f * (1 + desafina) * t + 0.6 * np.sin(2 * np.pi * 0.23 * t + k))
    return x * env_adsr(n, 0.5, 0.4, 0.8, 0.9)

def bajo(f, dur):
    n = int(dur * SR); t = t_(n)
    # con armónicos, para que se oiga también en el altavoz de un móvil, que apenas da graves
    x = np.sin(2 * np.pi * f * t) + 0.6 * np.sin(2 * np.pi * 2 * f * t) + 0.3 * np.sin(2 * np.pi * 3 * f * t)
    return x * env_adsr(n, 0.012, 0.25, 0.65, 0.12)

def bombo():
    n = int(0.28 * SR); t = t_(n)
    fase = 2 * np.pi * (48 * t + (120 - 48) * (1 - np.exp(-t * 28)) / 28)
    return np.sin(fase) * np.exp(-t * 13)

def maraca(rng, dur=0.07):
    n = int(dur * SR); x = rng.standard_normal(n) * np.exp(-t_(n) * 60)
    return sosfilt(butter(2, [5000, 11000], btype="band", fs=SR, output="sos"), x)

def pon(mezcla, x, cuando, pan=0.0, gan=1.0):
    """Suma x en la mezcla estéreo a partir del segundo «cuando». pan: -1 izquierda, 1 derecha."""
    i = int(cuando * SR)
    if i >= mezcla.shape[0]: return
    x = x[:mezcla.shape[0] - i]
    mezcla[i:i + len(x), 0] += gan * x * np.cos((pan + 1) * np.pi / 4)
    mezcla[i:i + len(x), 1] += gan * x * np.sin((pan + 1) * np.pi / 4)

# re mayor: re, si menor, sol, la (bajo y tres notas del acorde, en números MIDI)
ACORDES = [(38, (62, 66, 69)), (35, (62, 66, 71)), (43, (62, 67, 71)), (45, (61, 64, 69))]
# el motivo: una nota por sílaba, E-rre-KLA-ma-TU; (nota, comienzo en pulsos, duración en pulsos)
MOTIVO_ABIERTO = [(69, 0.0, 0.5), (74, 0.5, 0.5), (78, 1.0, 1.0), (76, 2.0, 0.5), (81, 2.5, 1.5)]
MOTIVO_CERRADO = [(69, 0.0, 0.5), (74, 0.5, 0.5), (78, 1.0, 1.0), (76, 2.0, 0.5), (74, 2.5, 2.5)]

def sintonia(segundos, arreglo="viva", cierre=5.0):
    viva = arreglo != "tranquila"
    ppm = 104 if viva else 92
    pulso = 60 / ppm; compas = 4 * pulso
    n = int(segundos * SR); m = np.zeros((n, 2)); rng = np.random.default_rng(7)
    t_cierre = max(segundos - cierre, 2 * compas)          # ahí entra el motivo cerrado
    n_comp = int(np.ceil(segundos / compas))
    for c in range(n_comp):
        t0 = c * compas
        if t0 >= t_cierre: break
        raiz, notas = ACORDES[c % 4]
        dur = min(compas, t_cierre - t0)
        for k, nota in enumerate(notas):                    # acordes
            pon(m, colchon(hz(nota), dur + 0.6, 0.0015 * (k - 1)), t0, pan=(-0.5, 0.0, 0.5)[k], gan=0.055)
        if c >= 2:                                          # la base entra tras la presentación del motivo
            for b, d in (((0, 1.5), (1.5, 0.5), (2, 1.5), (3.5, 0.5)) if viva else ((0, 2), (2, 2))):
                if t0 + b * pulso < t_cierre: pon(m, bajo(hz(raiz), d * pulso), t0 + b * pulso, gan=0.085)
            arpegio = [notas[0], notas[1], notas[2], notas[1] + 12, notas[2], notas[1], notas[0] + 12, notas[2]]
            for i, nota in enumerate(arpegio if viva else arpegio[::2]):
                tt = t0 + i * (pulso / 2 if viva else pulso)
                if tt < t_cierre: pon(m, campana(hz(nota + 12), 0.9, 0.55 + 0.25 * (i % 4 == 0)), tt, pan=0.45 * np.sin(i * 1.7), gan=0.14)
            if viva:
                for b in (0, 2):
                    if t0 + b * pulso < t_cierre: pon(m, bombo(), t0 + b * pulso, gan=0.17)
                for b in (0.5, 1.5, 2.5, 3.5):
                    if t0 + b * pulso < t_cierre: pon(m, maraca(rng), t0 + b * pulso, pan=0.3, gan=0.05)
        if c == 0 or (c % 8 == 4 and t0 + compas < t_cierre):   # el motivo abierto: al empezar y cada ocho compases
            for nota, b, d in MOTIVO_ABIERTO:
                pon(m, campana(hz(nota + 12), d * pulso + 1.2, 1.0), t0 + b * pulso, gan=0.26)
                pon(m, campana(hz(nota), d * pulso + 1.2, 0.6), t0 + b * pulso, gan=0.10)
    # cierre: acorde de re sostenido y el motivo que se resuelve en re
    for k, nota in enumerate((50, 62, 66, 69, 74)):
        pon(m, colchon(hz(nota), segundos - t_cierre + 0.5, 0.001 * (k - 2)), t_cierre, pan=(-0.6, -0.3, 0, 0.3, 0.6)[k], gan=0.05)
    pon(m, bajo(hz(38), min(2.5, segundos - t_cierre)), t_cierre, gan=0.085)
    for nota, b, d in MOTIVO_CERRADO:
        pon(m, campana(hz(nota + 12), d * pulso + 2.0, 1.0), t_cierre + 0.15 + b * pulso, gan=0.28)
        pon(m, campana(hz(nota), d * pulso + 2.0, 0.6), t_cierre + 0.15 + b * pulso, gan=0.11)
    # sala: un poco de reverberación
    k = int(1.6 * SR); ri = np.random.default_rng(3).standard_normal((k, 2)) * np.exp(-t_(k) * 4.2)[:, None]
    ri = sosfilt(butter(2, 6000, btype="low", fs=SR, output="sos"), ri, axis=0)
    hum = np.stack([fftconvolve(m[:, ch], ri[:, ch])[:n] for ch in (0, 1)], axis=1)
    m = m + 0.02 * hum
    m = sosfilt(butter(2, 30, btype="high", fs=SR, output="sos"), m, axis=0)
    # entrada y salida suaves, y nivel
    ent = int(0.03 * SR); m[:ent] *= np.linspace(0, 1, ent)[:, None]
    sal = int(min(1.8, cierre * 0.5) * SR); m[-sal:] *= (np.linspace(1, 0, sal) ** 1.5)[:, None]
    rms = np.sqrt(np.mean(m ** 2)); m *= (10 ** (-19 / 20)) / max(rms, 1e-9)     # unos -19 dB de media: música de fondo
    m = np.tanh(m * 1.1) / 1.1                                                    # tope suave, sin recortes
    return np.clip(m, -0.97, 0.97)

if __name__ == "__main__":
    salida, seg = sys.argv[1], float(sys.argv[2])
    arreglo = sys.argv[3] if len(sys.argv) > 3 else "viva"
    cierre = float(sys.argv[4]) if len(sys.argv) > 4 else 5.0
    x = sintonia(seg, arreglo, cierre)
    wavfile.write(salida, SR, (x * 32767).astype(np.int16))
    print(f"{salida}: {seg} s, arreglo {arreglo}, pico {np.abs(x).max():.2f}, media {20*np.log10(np.sqrt(np.mean(x**2))):.1f} dB")
