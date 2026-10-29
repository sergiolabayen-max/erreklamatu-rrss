# Cómics v2

`comic.py` hace todo el montaje: recorte de viñetas, láminas del carrusel (1080 × 1350), voz, vídeo (1080 × 1920) y portada. La ayuda está en la cabecera del script.

- Fuentes: Bangers y Comic Neue (Google Fonts, licencia OFL), en `fuentes/`; Poppins, la del sistema.
- Logo y sintonía: los toma de `../sistema/`.
- Ejemplo: `ejemplo/spec-ejemplo.json` (con viñetas de prueba sacadas de PUB-0486) y su hoja de comprobación.
- Cada cómic producido guarda su spec en `specs/<PUB-XXXX>.json` y las viñetas originales de Magnific en `../../recursos/viñetas/<PUB-XXXX>/`, con el *prompt* en `FUENTES.md`.
- **Para que quepa el gancho en la portada del carrusel**, la primera viñeta se pide con el tercio superior despejado (cielo, pared o techo).
