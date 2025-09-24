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



### Decision: Exploración de datos completa (EDA) (fecha: 2025-09-24)

**Qué:** Realizar un análisis exploratorio exhaustivo del dataset Imagenette antes de definir transforms, arquitectura y estrategias de regularización.

**Por qué (justificación):**

* Detecta posibles **desbalances de clases**, problemas de **calidad de imagen** o **variaciones fuertes entre clases** que impactan el diseño del modelo y los augmentations.
* Permite definir **normalización correcta** (media / std por canal), resoluciones y transforms que preserven información relevante.
* Proporciona métricas sobre **textura, frecuencia y ruido**, que ayudan a decidir sobre regularización y posibles técnicas de denoising o data augmentation.
* Fortalece la justificación de decisiones posteriores, valorando la comprensión del dataset más allá de la performance.

**Pasos realizados (Resumen del EDA):**

1. **Conteo por clase (train / val)**

   * Conteo de imágenes por clase y porcentaje de cada clase.
   * Visualización en gráfico de barras.

2. **Visualización de ejemplos por clase**

   * 3–5 imágenes al azar por clase en un grid.

3. **Estadísticas de tamaño / relación de aspecto**

   * Análisis de ancho, alto y aspect ratio antes del resize.
   * Histogramas de cada medida para detectar outliers.

4. **Media y desviación estándar por canal RGB**

   * Cálculo de media y std por canal para normalización.
   * Histogramas de intensidad para inspeccionar dominancia de color.

5. **Verificación de calidad de imágenes**

   * Identificación de imágenes borrosas, oscuras, ruidosas o mal etiquetadas.

6. **Distribución del brillo / contraste / saturación**

   * Análisis de variaciones de iluminación y color para decidir augmentations.

7. **Análisis del espectro de frecuencia (FFT)**

   * Cálculo del espectro de magnitud promedio de Fourier sobre una muestra de imágenes.
   * Permite identificar patrones globales de textura y frecuencia, útil para comprender estructura de la información visual.

8. **Estimación de ruido local (desviación estándar de parches)**

   * Cálculo de desviación estándar en parches 10×10 de las imágenes para estimar granularidad/ruido.
   * Generación de histograma de la distribución de ruido y cálculo de media/std de la muestra.

**Evidencia:**

* Código: notebook `imagenette.ipynb`, celdas de análisis de imagen, FFT y estimación de ruido.
* Figuras:

  * Todas las figuras se encuentran en la notebook `imagenette.ipynb`.

* Números:
  * Porcentaje de clases, media y std por canal, relaciones de aspecto.
  * Media y std de desviación estándar local (estimación de ruido).

**Estado:** Finalizado

---


