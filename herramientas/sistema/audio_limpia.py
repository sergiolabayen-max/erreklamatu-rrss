# Limpieza de audio captado por micrófono (grabación de pantalla): perfil de ruido tomado de las pausas del propio archivo
import soundfile as sf, numpy as np, sys, subprocess, noisereduce as nr
from scipy.signal import stft, butter, sosfiltfilt
def limpiar(ent, sal, fuerza=0.85):
    a, sr = sf.read(ent, dtype='float32')
    if a.ndim > 1: a = a.mean(1)
    a = sosfiltfilt(butter(4, 105, 'hp', fs=sr, output='sos'), a).astype('float32')     # retumbe por debajo de la voz
    hop = int(sr * 0.02); n = len(a) // hop
    lv = np.array([10 * np.log10((a[i * hop:(i + 1) * hop] ** 2).mean() + 1e-16) for i in range(n)])
    um = np.percentile(lv, 8)
    ruido = np.concatenate([a[i * hop:(i + 1) * hop] for i in range(n) if lv[i] <= um])   # tramas más silenciosas = pausas
    b = nr.reduce_noise(y=a, sr=sr, y_noise=ruido, stationary=True, prop_decrease=fuerza, n_fft=2048, n_std_thresh_stationary=1.2)
    sf.write(sal + '.tmp.wav', b, sr)
    # ganancia fija hasta nivel de emisión + expansor suave en pausas + limitador (sin normalizador dinámico: no "bombea" el fondo)
    lb = np.array([10 * np.log10((b[i * hop:(i + 1) * hop] ** 2).mean() + 1e-16) for i in range(n)])
    g = -19.0 - np.percentile(lb, 95)                    # la voz fuerte queda siempre al mismo nivel, haya o no golpes sueltos
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', sal + '.tmp.wav', '-af',
        f'volume={g:.1f}dB,agate=threshold=0.02:ratio=2:attack=5:release=200:range=0.25:knee=4,alimiter=limit=0.89', '-ar', '48000', sal], check=True)
    print(ent, '->', sal, f'ganancia {g:.1f} dB')
if __name__ == '__main__':
    limpiar(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.85)
