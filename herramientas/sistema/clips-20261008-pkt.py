# Palabras con su segundo (modelo Parakeet): python3 pkt.py v3 276 282 [v2 158 164 ...]
import sys, glob, sherpa_onnx, soundfile as sf
d = glob.glob("/tmp/claude-0/-home-claude-erreklamatu-rrss/e7eefa61-a30f-57c7-bc2e-7996fd2458cc/scratchpad/pk/sherpa-onnx-nemo-parakeet*/")[0]
rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=d+'encoder.int8.onnx', decoder=d+'decoder.int8.onnx', joiner=d+'joiner.int8.onnx', tokens=d+'tokens.txt', model_type='nemo_transducer', num_threads=2)
A = sys.argv[1:]
for k in range(0, len(A), 3):
    v, p, q = A[k], float(A[k+1]), float(A[k+2]); a, sr = sf.read(v + ".wav", dtype="float32")
    st = rec.create_stream(); st.accept_waveform(sr, a[int(p*sr):int(q*sr)]); rec.decode_stream(st); r = st.result
    ws = []; 
    for tok, t in zip(r.tokens, r.timestamps):
        if tok.startswith(" ") or not ws: ws.append([tok.strip(), p + t])
        else: ws[-1][0] += tok
    print(v, p, q, "|", " ".join(f"{w}@{t:.2f}" for w, t in ws))
