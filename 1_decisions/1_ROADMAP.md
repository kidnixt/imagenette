# ROADMAP


## 0) Principios obligatorios (leer antes de empezar)

* **No usar modelos pre-entrenados** (restricción del enunciado).
* **Registrar TODO** en `decisions.md`: cada decisión debe tener *qué*, *por qué* (justificación) y *evidencia* (gráfica, run de W\&B o resultado numérico).
* **Control experimental estricto**: en cada experimento cambia **UNA** variable a la vez (p. ej. sólo augmentation; o sólo optimizador).
* **Reproducibilidad**: siempre guardar seed, entorno (`requirements.txt`), commit hash y hardware usado.
* **Trazabilidad**: cada run en W\&B debe incluir el config completo (hyperparámetros + nombre del experimento + decisión clave).

---

## 1) Phase 1 — Exploración de datos (EDA) — obligatorio y reportable

Tareas (checboxable, ejecutar y pegar en notebook):

* [ ] Descargar Imagenette variant: `size="160px"` para prototipo. (Documentar en `decisions.md` por qué.)
* [ ] Listar las 10 clases (`dataset.classes`).
* [ ] Contar imágenes por clase (train / val) → gráfico de barras.
* [ ] Mostrar 5–10 ejemplos por clase (grid).
* [ ] Calcular mean/std por canal RGB (usar para normalización) y guardar números en `decisions.md`.
* [ ] Revisar tamaños y aspect ratio si trabajas con “full” (si no, documentar que usas `160px` o `320px`).
* [ ] Verificar split train/val (balance) y documentar si existe desbalance. Si hay desbalance, decidir y documentar la estrategia (weighted loss / oversample / stratified loader).

**Deliverable**: Sección “EDA” en el notebook con todas las gráficas y observaciones (copiar resumen a `decisions.md`).

---

## 2) Phase 2 — Decisiones de preprocesamiento (firmes y justificadas)

Para cada transform que elijas debes escribir en `decisions.md`: *qué*, *por qué*, *evidencia*.

Mínimo obligatorio:

* Resize / `RandomResizedCrop` (resolución: 160 o 320) — justificar por EDA.
* Normalización: usar mean/std calculada en EDA (preferido) o ImageNet si justificás.
* Al menos **una** técnica de augmentation en training: flip, rotation, color jitter.

Recomendadas (documentar si las usas):

* RandAugment / AutoAugment (si compute lo permite).
* MixUp o CutMix (requiere ajustes en loss/labels).

**Deliverable**: Tabla en `decisions.md` con transforms elegidos y evidencia (imágenes before/after).

---

## 3) Phase 3 — Baseline (implementar y ejecutar)

Objetivo: tener una referencia funcional lo antes posible.

* Implementar **SimpleCNN** (baseline):

  * 3–4 bloques Conv2d -> BatchNorm -> ReLU -> MaxPool
  * 1–2 FC layers con Dropout (0.5 en FC final)
  * Output: 10 clases (softmax/cross-entropy)
* Entrenar 1 run corto (p. ej. 10–20 epochs) con `size="160px"` y batch 64.
* Loguear en W\&B: train/val loss, train/val accuracy, lr, epoch.
* Guardar checkpoint `models/baseline_seed42.pt`.

**Deliverable**: baseline run en W\&B + comentario en `decisions.md` con interpretación de curvas y problemas detectados.

---

## 4) Phase 4 — Suite de modelos y regularización (mínimo obligatorio)

Implementar al menos estos modelos (desde cero):

1. **SimpleCNN** (ya hecho) — baseline
2. **ResNet-18 desde cero** (no usar pesos) — preferible por estabilidad de entrenamiento.
3. **Versión regularizada** del modelo ganador con: BatchNorm, Dropout y Data Augmentation + (MixUp o CutMix).

**Reglas**:

* **Al menos 2 técnicas de regularización** usadas en los experimentos finales (p. ej. BatchNorm + MixUp).
* Documentar por qué cada técnica fue elegida con evidencia.

---

## 5) Phase 5 — Plan experimental (estricto)

Sigue la regla: **una variable por experimento**. Haz correr cada experimento con la misma semilla salvo cuando evalúes robustez (see below).

### Experimentos mínimos (ejecutar todos)

* Run A — Baseline SimpleCNN + transforms básicos.
* Run B — ResNet-18 (sin augment fuerte).
* Run C — ResNet-18 + RandAugment.
* Run D — ResNet-18 + RandAugment + MixUp (o CutMix).
* Run E — ResNet-34 + la mejor combinación encontrada.
* Run F — Best model (E) re-entrenado 3 veces con seeds distintos (42, 123, 999) para estimar varianza.

(Esto son 6 corridas mínimas; si tiempo/compute lo permiten, expande con optimizadores distintos.)

### Hyperparámetros recomendados (punto de partida)

* Optimizer: **SGD** (momentum=0.9), lr inicial: 0.05 (usar LR-finder).
* Weight decay: 1e-4.
* Batch size: 64 (o lo máximo que tu GPU aguante).
* Epochs: 30–80 (depende de recursos).
* LR schedule: **1-cycle** o **cosine annealing**.
  Registra todo en W\&B `config`.

**Deliverable**: Tabla de experimentos en `decisions.md` con hyperparámetros y objetivo de cada run.

---

## 6) Phase 6 — Métricas y evaluación (obligatorio)

Por run, guardar y reportar:

* Por-epoch: train\_loss, val\_loss, train\_acc, val\_acc (obligatorio).
* Al final: **accuracy, precision, recall, F1** (macro y por clase).
* Matriz de confusión (guardar imagen).
* Mostrar ejemplos de falsos positivos y falsos negativos (al menos 6).
* Para el mejor modelo: curva de loss/acc y curva de lr.

**Deliverable**: sección “Evaluation” en notebook + `outputs/metrics/<run>.json` con números finales.

---

## 7) Phase 7 — Ablation y conclusiones (obligatorio)

* Realizar al menos **2 estudios de ablación** (ejemplos):

  * Ablation 1: quitar MixUp/CutMix → comparar métricas.
  * Ablation 2: quitar BatchNorm o Dropout → efecto en val performance.
* Presentar una tabla comparativa con métricas clave de cada experimento.
* Concluir con **qué decisiones tomaste para el modelo final** y por qué (evidencia: W\&B + gráficas + números).

**Deliverable**: sección “Ablation” en notebook + actualización en `decisions.md`.

---

## 8) Phase 8 — Entrega y checklist final (hacer justo antes de entregar)

* [ ] Notebook `.ipynb` **con todas las celdas ejecutadas** (outputs visibles).
* [ ] `decisions.md` completo: cada decisión tiene *qué*, *por qué*, *evidencia (link a W\&B o figura)*.
* [ ] `requirements.txt` actualizado.
* [ ] Al menos 3 runs en W\&B con comparativa (links en notebook).
* [ ] Guardar checkpoint del mejor modelo en `models/` y/o artifacts en W\&B.
* [ ] README con instrucciones para reproducir el mejor run (comando exacto para entrenar y evaluar).
* [ ] ZIP final (si lo piden): `notebook.ipynb`, `decisions.md`, `requirements.txt`, `README.md`, `models/*.pt` (opcional).

---

## Formatos y convenciones (obligatorio seguir)

* **Nombres de run en W\&B**: `<Model>__<Augmentation>__<Regularization>__seed<NN>`
  Ej: `ResNet18__RandAug__MixUp__seed42`
* **Keys en config (W\&B)**: `model`, `arch`, `dataset_size`, `batch_size`, `lr`, `optimizer`, `weight_decay`, `augmentations`, `regularizations`, `seed`, `epochs`
* **Naming de archivos**:

  * Notebook: `imagenette_experiments.ipynb` o `notebook.ipynb`
  * Checkpoint: `models/<run-name>__best.pt`
  * Metrics: `outputs/metrics/<run-name>.json`
* **Cambio experimental**: escribir una línea en `decisions.md` antes de ejecutar cada run: `RUN <run-name> — cambio: <qué variable alteraste> — seed: <N> — objetivo: <qué pruebas quieres confirmar>`.

---

## Reglas estrictas de análisis e interpretación

* No interpretar mejoras sin evidencia: cualquier afirmación del tipo “X mejoró Y porque Z” debe acompañarse de:

  * gráfico de comparación (train/val), y
  * valores numéricos (p.ej. +3.2% en F1 macro entre runs A y B).
* Para la conclusión final, **presentar la decisión final** (modelo y transforms) y justificar con: EDA → experimentación → ablacion.

---

## Plantilla rápida para una entrada de `decisions.md`

Usa exactamente este formato (copiar y pegar por cada decisión):

```markdown
### Decision: [TÍTULO CORTO]  (fecha: YYYY-MM-DD)
**Qué:** <descripción corta de la decisión>
**Por qué (justificación):**
- Punto 1 (basado en EDA / paper / regla práctica)
- Punto 2 (riesgos / trade-offs)

**Evidencia:**
- Link a W&B: <url>
- Figuras: outputs/figures/<file>.png
- Números: val_acc=XX.XX, val_f1_macro=YY.YY

**Estado:** [pendiente / aplicada / revertida]
```

---

## Ejemplo de matriz de experimentos (para pegar)

```markdown
| Run name                        | Model      | Augmentations        | Regularization         | Optimizer | LR    | Batch | Epochs |
|---------------------------------|------------|----------------------|-------------------------|-----------|-------|-------|--------|
| Baseline_SimpleCNN_seed42       | SimpleCNN  | basic (flip, crop)   | BatchNorm, Dropout      | SGD       | 0.05  | 64    | 30     |
| ResNet18_noAug_seed42           | ResNet18   | none                 | BatchNorm               | SGD       | 0.05  | 64    | 50     |
| ResNet18_RandAug_seed42         | ResNet18   | RandAugment          | BatchNorm               | SGD       | 0.05  | 64    | 50     |
| ResNet18_RandAug_Mixup_seed42   | ResNet18   | RandAug + MixUp      | BatchNorm               | SGD       | 0.05  | 64    | 50     |
| ResNet34_bestcombo_seed42       | ResNet34   | Best found           | Best found              | SGD       | 0.03  | 32    | 80     |
| Best_3seeds                     | BestModel  | Best found           | Best found              | SGD       | best  | best  | best   |
```

---

## Consejos finales

* **Documenta cada paso**: los profesores valoran la justificación tanto como las métricas.
* **Control de versiones**: guarda un commit por cada bloque grande de cambios (EDA, baseline, suite de modelos, ablation). Pegar el commit hash en `decisions.md`.
* **Prioriza claridad** en el notebook: títulos claros, celdas pequeñas, figuras con leyendas y captions.
* **Si algo falla**, deja la entrada en `decisions.md` con el diagnóstico (qué probaste y por qué falló). Eso suma.

---

