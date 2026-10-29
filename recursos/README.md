# Recursos de producción

Originales que hacen falta para rehacer cualquier pieza. Origen y fecha de cada uno, en el `FUENTES.md` o el `.json` de su carpeta.

- `viñetas/<cómic>/NN.png`: viñetas elegidas, recortadas y a 1080 × 1350 (las de 2K están en el Mac de Sergio: `Documentos/LANA/Erreklamatu/Marketing/Magnific/viñetas/`).
- `viñetas/prompts-comics-v2.json`: prompts, referencias, variantes elegidas e identificadores de Magnific de cada viñeta y locución.
- `voces/comics-v2/`: locuciones (Magnific · ElevenLabs v3 · «Ana Beltrán»).
- `musica/musica-lofi-100bpm.mp3`: pista que eligió Sergio el 16/10/2026 para los cómics (Magnific · ElevenLabs Music). No subirla a plataformas de streaming musical.

## Carpeta del Mac (conectada el 29/10/2026)

`Documentos/LANA/Erreklamatu/Marketing/Magnific/`: el Chrome del perfil Erreklamatu descarga ahí. Tiene las subcarpetas `viñetas/`, `personajes/`, `voces/`, `musica/`, `stock/` y `sentencias/`. **Las sentencias no se suben nunca a este repositorio, que es público.**

## Cómo bajar de Magnific (probado el 29/10/2026)

Desde la pestaña de Magnific, con JavaScript, `fetch` de `creation.url` (o de `download_url` en imágenes) → blob → `<a download>`. En los audios, `download_url` devuelve a veces la forma de onda en JSON: usar siempre `creation.url`. Para listar las creaciones y sus prompts: `/app/api/projects/folders/<carpeta>/files?page=N&per_page=50…` (el campo `name` es el prompt).
