# Decisiones durante el proceso

### Decision: Dataset inicial (fecha: 2025-09-19)
**Qué:** Empezar con la variante pequeña (`size="160px"`) de Imagenette para prototipado rápido.  
**Por qué (justificación):**
- Permite entrenamientos más rápidos y pruebas ágiles en la etapa inicial.
- Escalar a `320px` más adelante puede mejorar performance, pero implica mayor costo computacional.  
**Evidencia:**
- Link a W&B: pendiente
- Figuras: pendiente (conteo por clase, ejemplos visuales)
- Números: pendiente (estadísticas básicas)  
**Estado:** pendiente

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

