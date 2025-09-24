# Decisiones durante el proceso

### Decision: Dataset inicial (fecha: 2025-09-19)
**Qué:** Empezar con la variante pequeña (`size="160px"`) de Imagenette para prototipado rápido.  
**Por qué (justificación):**
- Permite entrenamientos más rápidos y pruebas ágiles en la etapa inicial.
- Escalar a `320px` más adelante puede mejorar performance, pero implica mayor costo computacional.  
**Evidencia:**
- Están las celdas en la notebook `imagenette.ipynb`.


**Estado:** Finalizado

---

### Decision: Modelo baseline (fecha: 2025-09-19)
**Qué:** Definir un baseline con una CNN sencilla (capas convolucionales + fully connected).  
**Por qué (justificación):**
- Establece un punto de comparación mínimo requerido para evaluar mejoras.
- Cumple con la restricción de no usar modelos pre-entrenados.  
**Evidencia:**
- Link a W&B: pendiente
- Figuras: outputs/figures/baseline_training.png
- Números: pendiente (val_acc, val_f1)  
**Estado:** pendiente

---

### Decision: Regularización inicial (fecha: 2025-09-19)
**Qué:** Incluir al menos Batch Normalization, Dropout y Data Augmentation.  
**Por qué (justificación):**
- BatchNorm estabiliza y acelera el entrenamiento.
- Dropout reduce sobreajuste en fully connected.
- Data Augmentation aumenta la variabilidad de datos y previene overfitting.  
**Evidencia:**
- Link a W&B: pendiente
- Figuras: outputs/figures/augmentation_examples.png
- Números: pendiente (comparación con/ sin aug)  
**Estado:** pendiente

---

### Decision: Logging y experimentos (fecha: 2025-09-19)
**Qué:** Usar **Weights & Biases (wandb)** desde el inicio.  
**Por qué (justificación):**
- Registra métricas de entrenamiento y validación de forma centralizada.
- Facilita la comparación de runs y reproducibilidad de resultados.
- Es un requisito explícito de la consigna.  
**Evidencia:**
- Link a W&B: pendiente
- Figuras: pendiente (curvas de loss/accuracy)
- Números: pendiente  
**Estado:** pendiente


---

### Decision: Logging y experimentos (fecha: 2025-09-24)
**Qué:** Usar **Weights & Biases (wandb)** desde el inicio en un solo proyecto (`imagenette`).  
**Por qué (justificación):**
- Registra métricas de entrenamiento y validación de forma centralizada.
- Facilita la comparación de runs gracias a nombres descriptivos y uso de `tags`.
- Permite organizar configuraciones de modelos y regularización de forma clara (ej. `baseline`, `resnet_scratch`, `dropout`).
- Es un requisito explícito de la consigna.  
- Primero se hará una versión dummy. 

**Evidencia:**
- Link a W&B: https://wandb.ai/kidnixt-ort/imagenette/runs/1omx7ii5?nw=nwuserkidnixt  

**Estado:** Finalizado

---

### Decision: Exploración de datos (EDA) inicial (fecha: 2025-09-24)
**Qué:** Realizar un análisis exploratorio del dataset Imagenette antes de definir transforms y arquitectura.  
**Por qué (justificación):**
- Permite detectar posibles desbalances de clases, problemas de calidad de imagen o variaciones fuertes entre clases que impactan diseño del modelo y augmentations.  
- Ayuda a definir normalización correcta (media / std por canal), resoluciones, y transforms que preserven información relevante.  
- Fortalece la justificación de decisiones posteriores, lo cual es valorado en la entrega (más allá de performance).  

**Evidencia:**
- Link a W&B: pendiente  
- Figuras: ejemplos por clase, conteos por clase, histogramas de canal, medias/std  
- Números: porcentaje de clases, media y std por canal, relaciones de aspecto (aspect ratios)  

**Estado:** pendiente


