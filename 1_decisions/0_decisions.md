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


### Decision: Geometría y Distribución de Imágenes (fecha: 2025-09-26)

**Qué:** Adaptar preprocesamiento para imágenes uniformes y balanceadas en tamaño y clases.
**Por qué (justificación del EDA):**

* Todas las imágenes son $160 \times 160$ y cuadradas (aspect ratio 1.0), por lo que no hay necesidad de correcciones de forma, solo adaptación a la arquitectura.
* Dataset perfectamente balanceado (~950 imágenes por clase), eliminando la necesidad de weighted loss.
* Random Resized Crop obligatorio para introducir variabilidad de escala y romper posibles bordes uniformes.
  **Decisiones de preprocesamiento:**
* No se aplica weighted loss.
* Aplicar *resize* si se requiere por arquitectura pre-entrenada (ej. $224 \times 224$).
* Aplicar Random Resized Crop.

**Evidencia:** Estadísticas de tamaño, aspect ratio y conteo por clase del EDA.
**Estado:** Finalizado en el baseline y posteriormente en la decisión del 2025-09-26.

---

### Decision: Color, Brillo y Saturación (fecha: 2025-09-26)

**Qué:** Normalización y augmentations específicas para brillo, contraste y saturación.
**Por qué (justificación del EDA):**

* Media RGB $\mu \approx [0.4625, 0.4580, 0.4298]$, desviación $\sigma \approx [0.2748, 0.2690, 0.2856]$ → se requiere normalización.
* Baja saturación promedio (~50) → aplicar augmentations de saturación agresivas (rango 0.5–1.5).
* Presencia de picos extremos de brillo/contraste en ~1.7% de imágenes → augmentations de brillo/contraste moderadas (rango 0.7–1.3).
  **Decisiones de preprocesamiento:**
* Normalización RGB con los valores calculados.
* Augmentation de saturación alta prioridad.
* Augmentation de brillo/contraste prioridad media.

**Evidencia:** Histogramas de intensidad, saturación y brillo del EDA.
**Estado:** Finalizado en el baseline y posteriormente en la decisión del 2025-09-26.

---

### Decision: Textura y Frecuencia (fecha: 2025-09-26)

**Qué:** Incorporar augmentations y arquitectura que capturen información textural y patrones de baja frecuencia.
**Por qué (justificación del EDA):**

* FFT muestra predominio de bajas frecuencias (formas grandes, fondos uniformes) y líneas axiales (artefactos de resizing).
* Alta granularidad local: desviación estándar de parches ~23.4, con 280 imágenes outliers >42.4.
  **Decisiones de modelado y augmentation:**
* Aplicar Ruido Gaussiano aleatorio con baja probabilidad para robustez frente a outliers de alta textura.
* Augmentations geométricos: rotaciones leves y shear para forzar invariancia a orientación y romper uniformidad axial.
* Usar arquitectura convolucional (ej. ResNet, VGG) para capturar texturas locales y patrones de baja frecuencia.

**Evidencia:** FFT global, desviación estándar de parches y histogramas del EDA.

**Estado:** Finalizado en el baseline y posteriormente en la decisión del 2025-09-26.


---

### Decision: Modelo Baseline CNN (fecha: 2025-09-26)

**Qué:** Definir un **modelo baseline CNN sencillo** para clasificación de Imagenette, incorporando insights de EDA.
**Por qué (justificación del EDA):**

* La alta granularidad local y predominio de bajas frecuencias sugieren que las **convoluciones pequeñas (3×3)** son adecuadas para capturar texturas y formas.
* Las augmentations de saturación, brillo/contraste y ruido requieren que el modelo sea **robusto a variaciones de color y texturas**.
* Random Resized Crop y augmentations geométricas implican que el modelo debe aprender invariancia a **rotaciones leves y cambios de escala**.
  **Arquitectura propuesta (ejemplo sencillo):**
* 3 bloques convolucionales: Conv2D → BatchNorm → ReLU → MaxPool2D
* Dropout entre bloques para regularización
* Fully connected final con softmax para las 10 clases
* Entrada: $160 \times 160 \times 3$ (o *resize* a 224×224 si se usa pre-trained backbone en un futuro)
  
  **Evidencia:**
* Basada en análisis de FFT, desviación estándar de parches y distribución de color del EDA.
* Figuras: se registrarán curvas de entrenamiento/validación en W&B.
  
**Estado:** Pendiente

---

### Decision: División interna Train/Validation/Test (fecha: 2025-09-26)

**Qué:** Crear un split interno del `train_dataset` para validación, y mantener el `val_dataset` de Imagenette como test final.
**Por qué (justificación del EDA / best practice):**

* El `val` de Imagenette es en realidad el conjunto de test final.
* Para monitorear **loss y accuracy** durante entrenamiento necesitamos un val interno separado.
* Garantiza que el test final permanezca **independiente** y pueda usarse para evaluación objetiva.
  **Decisiones de implementación:**
* Split interno: 90% train / 10% val usando `random_split` de PyTorch.
* `train_loader` → train subset, `val_loader_internal` → val subset, `test_loader` → val_dataset original.
  **Evidencia:**
* Tamaños de los subsets y clases verificadas en código.
* Dataloaders listos para usar en entrenamiento y evaluación.
  **Estado:** Finalizado

---


### Decision: Pipeline de transformaciones Train / Val / Test (fecha: 2025-09-27)

**Qué:** Definir y separar claramente las transformaciones aplicadas a cada partición (train, val y test) para asegurar consistencia y medición justa del rendimiento.

**Por qué (justificación):**
- Evita sesgos al evaluar, aplicando *solo transformaciones determinísticas* (Resize + Normalize) en validación y test.
- Permite que el modelo vea más variaciones en entrenamiento (augmentations), pero se evalúe sobre imágenes representativas sin aleatoriedad.
- Mantiene coherencia con los valores de normalización calculados en el EDA.

**Detalles de las transformaciones:**

| Tipo de transformación          | Train | Val/Test |
|----------------------------------|-------|----------|
| Resize / CenterCrop             | ✅    | ✅        |
| ToTensor + Normalize            | ✅    | ✅        |
| Random crop / rotation / flip   | ✅    | ❌        |
| ColorJitter                     | ✅    | ❌        |

**Evidencia:**
- Código en notebook `imagenette.ipynb` (celdas de definiciones de `train_transform`, `val_transform` y uso en DataLoaders).
- Resultados en test después de aplicar la separación correcta: `test_acc ≈ 60%` (coherente con `val_acc`).

**Estado:** Finalizado

---

###  Decision: Refactorizar función de entrenamiento (fecha: 2025-09-27)

**Qué:** Se decidió encapsular el loop de entrenamiento y validación en una función `train_model` genérica, en lugar de usar un bloque de código suelto. Además, se incorporó early stopping configurable.
**Justificación:**

* Permite reutilizar la misma lógica de entrenamiento para distintas arquitecturas (CNN Baseline, LeNet, etc.) y configuraciones sin duplicar código.
* Facilita la integración con sweeps de hiperparámetros (W&B) al tener una interfaz estándar.
* Early stopping mejora la eficiencia del entrenamiento, evitando correr épocas innecesarias cuando la validación deja de mejorar.
* Mantiene un registro consistente en W&B de métricas de train y validación para análisis posterior.

**Evidencia:**

* Entrenamientos previos requerían correr 100 épocas completas; con early stopping, se detiene automáticamente cuando no hay mejoras, reduciendo el tiempo de cómputo.
* Se verificó que la nueva función entrena correctamente el modelo baseline y devuelve el mejor checkpoint según la pérdida de validación.
* Los logs en W&B se mantienen consistentes y permiten monitorear el proceso.

**Estado:** Finalizado

---

### Decision: Registro histórico de losses para graficar (fecha: 2025-09-27)

**Qué:** Guardar los valores de train_loss y val_loss por época dentro de listas o diccionarios retornados por train_model.  

**Por qué (justificación):**  
- Permite generar curvas de aprendizaje y detectar overfitting o underfitting.  
- Facilita comparaciones entre distintas configuraciones de hiperparámetros y modelos.  

**Detalles de implementación:**  
- train_model ahora retorna: best_model y history, donde history contiene listas de train_loss, train_acc, val_loss y val_acc por época.  
- Se pueden usar estas listas para graficar curvas usando matplotlib o seaborn.

**Evidencia:**  
- Curvas de entrenamiento/validación generadas en W&B y localmente.  

**Estado:** Finalizado

---

### Decision: Early stopping configurable (fecha: 2025-09-27)

**Qué:** Incorporar early stopping en la función train_model.  

**Por qué (justificación):**  
- Evita entrenamientos innecesariamente largos cuando la validación deja de mejorar.  
- Mejora eficiencia computacional y reduce tiempo de experimentación.  

**Detalles de implementación:**  
- Parámetro patience define cuántas épocas consecutivas sin mejora en la val_loss se permiten antes de detener el entrenamiento.  
- Se guarda el best_model basado en la mejor val_loss.  

**Evidencia:**  
- Reducción de tiempo de entrenamiento de 100 épocas a ~30–40 para el CNNBaseline sin perder accuracy.  
- Comportamiento verificado con distintos valores de patience.  

**Estado:** Finalizado

---

### Decision: Función train_model genérica y reutilizable (fecha: 2025-09-27)

**Qué:** Refactorizar loop de entrenamiento en función que recibe cualquier modelo y configuración de hiperparámetros.  

**Por qué (justificación):**  
- Permite entrenar múltiples arquitecturas (CNNBaseline, LeNet, etc.) sin duplicar código.  
- Facilita sweeps de hiperparámetros y logging consistente en W&B.  
- Integra early stopping y registro histórico de métricas de manera estándar.  

**Detalles de implementación:**  
- Entradas: model, train_loader, val_loader, config, device, patience.  
- Salidas: best_model y history con listas de métricas.  
- Se maneja el optimizador según config["optimizer"] y learning rate.  
- Log de métricas por época en W&B.  

**Evidencia:**  
- Función probada con CNNBaseline y LeNet.  
- Sweeps de W&B funcionan usando la misma interfaz.  

**Estado:** Finalizado

---

### Decision: Sweeps de hiperparámetros con W&B (fecha: 2025-09-27)

**Qué:** Configurar sweeps de hiperparámetros para probar distintas combinaciones de learning rate, batch size, optimizador y dropout.  

**Por qué (justificación):**  
- Permite explorar automáticamente múltiples configuraciones de manera aleatoria o bayesiana sin ejecutar runs manuales individuales.  
- Optimiza la performance del modelo baseline y de futuras arquitecturas.  
- Mantiene consistencia en logging y comparación de métricas.  

**Detalles de implementación:**  
- Se define un diccionario de parámetros con rangos o listas de valores posibles.  
- La función train_model recibe la configuración de cada sweep y entrena el modelo correspondiente.  
- Se guarda el mejor modelo de cada sweep según val_loss y se registran métricas en W&B.  

**Evidencia:**  
- Sweeps configurados y ejecutados para CNNBaseline con distintas combinaciones de dropout, lr, batch_size y optimizador.  
- Se observan mejoras en val_acc y val_loss según la selección de hiperparámetros.  

**Estado:** Finalizado

---

### Decision: Flexibilidad de modelos en sweeps (fecha: 2025-09-27)

**Qué:** Permitir que cualquier modelo definido (CNNBaseline, LeNet, etc.) pueda ser entrenado usando la misma función train_model dentro de un sweep.  

**Por qué (justificación):**  
- No hardcodear un modelo dentro de la función facilita comparaciones entre arquitecturas.  
- Posibilita escalar el pipeline a futuros modelos sin modificar la lógica de entrenamiento o sweeps.  

**Detalles de implementación:**  
- train_model recibe como parámetro el objeto model previamente instanciado.  
- Sweeps pasan la configuración de hiperparámetros y crean instancias del modelo según sea necesario.  
- Se mantiene logging y early stopping independiente de la arquitectura.  

**Evidencia:**  
- Comparación entre CNNBaseline y LeNet usando el mismo pipeline de entrenamiento y sweeps.  
- Métricas consistentes registradas en W&B.  

**Estado:** Finalizado

---

### Decision: Flujo de entrenamiento post-sweep y evaluación (fecha: 2025-09-27)

**Qué:**  
Tras ejecutar los sweeps de hiperparámetros, se selecciona la run con la mejor validación (val_acc) y se entrenan de nuevo esos hiperparámetros para obtener un modelo base. Luego se evalúa la performance en el set de test antes de decidir próximos pasos.

**Por qué (justificación):**  
- Permite usar los mejores hiperparámetros encontrados automáticamente sin depender de runs anteriores ya completadas.  
- Facilita comparar la performance del modelo base en test antes de extender entrenamiento o explorar hiperparámetros adicionales.  
- Mantener el modelo en memoria (sin artifact) permite iterar rápidamente, pero se identifica la necesidad de guardar el modelo final para reproducibilidad y análisis posterior.

**Detalles de implementación:**  
- Se ejecuta un sweep de hiperparámetros sobre learning rate, batch size, optimizador y dropout.  
- No se guarda el mejor modelo directamente como artifact durante el sweep; se registra solo la configuración y métricas.  
- Se identifica la run con mayor val_acc y se extraen sus hiperparámetros.  
- Se reentrena un modelo desde cero con esos hiperparámetros usando los mismos datos de entrenamiento/validación y número de epochs, con early stopping opcional.  
- Una vez entrenado, se evalúa el modelo en el set de test para medir performance real.  
- Próximos pasos incluyen: entrenar el modelo con más epochs, ajustar paciencia para early stopping, o explorar hiperparámetros cercanos a los mejores encontrados.  

**Evidencia:**  
- Sweeps ejecutados correctamente y validación usada para seleccionar la mejor run.  
- Modelo entrenado desde cero con hiperparámetros óptimos y evaluado en test.  
- Discusión de opciones futuras: entrenar más tiempo o refinar hiperparámetros.  

**Mejora futura:**  
- Guardar el modelo con mejores métricas (peso + configuración) como artifact de W&B para reproducibilidad y evitar reentrenamientos innecesarios.

**Estado:** En progreso







