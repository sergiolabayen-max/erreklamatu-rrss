# Filtro de corrección antes de «Revisar»

Pedido por Sergio el 16/11/2026, después de devolver dos piezas con errores de imagen básicos. En PUB-0617, la cara de la chica salía cortada en el gancho. En PUB-0619, de Jon Ortiz solo se veía la frente mientras hablaba. Ninguna pieza (vídeo, imagen o carrusel) pasa a «Pendiente de revisión» sin superar este filtro.

## Cómo se hace
1. **Hojas de revisión.** Ejecuta `python3 sistema/hoja_revision.py <vídeo o imágenes> --salida <carpeta>`. En los vídeos saca un fotograma por segundo, de principio a fin. En las imágenes, cada lámina a buen tamaño. Mirar uno o dos fotogramas sueltos no vale.
2. **Revisor independiente.** Un subagente nuevo, que no ha hecho la pieza, mira TODAS las hojas con la lista de abajo. Usa el modelo superior. Se le pasan las hojas, los textos de la pieza y los subtítulos esperados. Devuelve «OK» o una lista de fallos con el segundo o la lámina.
3. **Si hay fallos:** se corrigen, se vuelven a sacar las hojas y se repite la revisión. Solo con un «OK» la pieza pasa a «Pendiente de revisión».
4. **Constancia.** La pieza guarda `control_calidad` = {fecha, revisor: "subagente", hojas: n, resultado: "OK", fallos_corregidos: [...]}. Las tareas programadas sin subagente hacen ellas mismas la revisión con las hojas completas y lo dicen en `control_calidad.revisor`.

## Lista de comprobación (todas las hojas, fotograma a fotograma)
- **Caras.** Ninguna cara cortada por el borde del recuadro, por el titular, por los subtítulos, por las barras o por la cortinilla. Cuando habla o sale una persona, se le ven ojos, nariz y boca. Nada de «solo la frente» ni «solo la barbilla».
- **Personas.** Ninguna sale cortada por la mitad de forma rara, deformada ni con aspecto de IA evidente. Las personas tienen la edad y el aspecto del caso.
- **Textos legibles.** Ningún texto sobre un fondo que no contraste (verde o blanco sobre fondo claro). Nada desborda ni queda cortado ni se solapa con otro texto.
- **Correspondencia.** Lo que se ve encaja con lo que dice la locución en ese momento.
- **Erratas** en titulares, rótulos y subtítulos. Cifras, nombres de bancos y aerolíneas, y ciudades en euskera (Bilbo, Donostia, Gasteiz, Iruñea).
- **Planos.** Sin fotogramas negros ni en blanco, sin saltos bruscos y sin planos repetidos dentro de la misma pieza. Ningún plano se alarga tanto que el vídeo quede estático.
- **Portada y miniatura.** Titular que se entiende solo, cara completa y sin huecos vacíos.
- **Cierre.** Logotipo, teléfono 944 027 596 y web correctos.
