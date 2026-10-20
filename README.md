# NEON SLICE

Un juego 2D de **cortar fruta** al estilo Fruit Ninja: desliza el ratón o el dedo para
trazar tu cuchilla neón, encadena cortes para multiplicar la puntuación y esquiva las bombas.

Todo el juego vive en un único archivo (`index.html`): sin dependencias, sin build step,
sin frameworks. Solo HTML + CSS + Canvas 2D + WebAudio.

## Jugar

```sh
python -m http.server 8123 --directory .
# abre http://localhost:8123
```

O simplemente abre `index.html` en el navegador (funciona también con `file://`).

## Qué hay dentro

| Mecánica | Detalle |
|---|---|
| **Cuchilla neón** | Estela con degradado, brillo y desvanecido en 420 ms. |
| **Racha ×5** | Cortes seguidos en menos de 1,15 s multiplican los puntos (10 × racha). |
| **Combo** | Varias frutas en un solo trazo: bonus de 25 puntos por cada una de más. |
| **Frenesí** | La fruta dorada activa 8 s de **puntos x2** y la pantalla se vuelve arcoíris. |
| **Bombas** | 3 vidas. Cortar una bomba quita vida, rompe la racha, congela la partida 90 ms y sacude la cámara. |
| **6 frutas + dorada** | Sandía, naranja, lima, ciruela, melocotón y fresa, cada una dibujada con degradados, pepitas y hoja. |
| **Dificultad progresiva** | Las oleadas se aceleran y aparecen más bombas según avanza la ronda (hasta el 30 %). |
| **75 segundos** | Medallas por puntuación: bronce 1.200, plata 4.000, oro 10.000. Récord guardado en `localStorage`. |
| **Sonido** | Sintetizado con WebAudio: corte, explosión, nota ascendente por racha y música chiptune de fondo. Tecla `M` para silenciar. |

## Detalles técnicos

- Las frutas **se lanzan desde abajo** (950–1320 px/s) y luego caen por gravedad (1500 px/s²),
  describiendo un arco. Cada oleada sale en abanico desde el borde inferior.
- Resolución virtual fija de **960×600** con escalado y letterbox: se adapta a cualquier
  pantalla sin deformar la partida.
- Bucle de **paso fijo a 120 Hz** con acumulador, y `requestAnimationFrame` para dibujar.
- Sacudida de cámara, destello a pantalla completa, `hitstop` al cortar una bomba y
  salpicaduras de jugo que se desvanecen en el fondo.
- Partículas, estelas y efectos dibujados con composición aditiva (`lighter`).
- En móvil se pide orientación horizontal (con aviso si se juega en vertical).

## Atajos

| Tecla | Acción |
|---|---|
| `ESPACIO` / `ENTER` | Jugar o continuar |
| `P` / `ESC` | Pausa |
| `R` | Reiniciar |
| `M` | Silenciar |

Para depurar desde la consola del navegador: `NeonSlice.state` (puntuación, racha, vidas),
`NeonSlice.tick(dt)` (avanza la simulación), `NeonSlice.spawn('bomb', x, y)` y `NeonSlice.end()`.

## Despliegue

Es un sitio estático. En Vercel basta con importar el repo (o desplegar a mano):

```sh
deno run -A npm:vercel@latest deploy --prod --yes
```
