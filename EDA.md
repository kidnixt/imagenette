# Resultados del EDA

## 1. Conteo por clase (train / val)

1.  **Balance de Clases (General):** El conjunto de datos está **bastante bien balanceado**. Todas las clases tienen un número de imágenes muy similar. El conteo total de imágenes por clase oscila aproximadamente entre 850 (para 'chain saw') y 1000 (para 'cassette player'). Presentando una suerte de uniformidad.

2.  **División Train/Val:** La división entre los conjuntos de *Train* (azul) y *Val* (rosa) es **consistente** y también bien balanceada en todas las clases.

### Justificación de Acciones de Preprocesamiento y Modelado
Dado que el *dataset* es tan balanceado, la mayoría de las técnicas de mitigación de desbalance no son necesarias:

| Problema Detectado | Decisión y Justificación |
| :--- | :--- |
| **Buen Balance** | **No se requieren** técnicas de balanceo como *oversampling* (SMOTE, etc.), *undersampling*, o pérdida ponderada (*weighted loss*). |
| **Métricas de Evaluación** | Podemos confiar en métricas simples como la **precisión (*accuracy*)** global. Métricas específicas por clase (Precisión, *Recall*, $F1$-Score) seguirán siendo informativas, pero la precisión general es un buen indicador de rendimiento, ya que no hay una clase minoritaria que pueda ser ignorada. |


--- 

## 2. Tamaño y Aspect Ratio


1.  **Uniformidad Perfecta:** Los histogramas muestran picos únicos y estrechos, y las desviaciones estándar son $0.0$.
2.  **Dimensiones Fijas:** **Todas las imágenes** en el dataset Imagenette tienen un **ancho de $160$ píxeles** y un **alto de $160$ píxeles**.
3.  **Relación de Aspecto Fija:** Como consecuencia, la relación de aspecto ($\text{Ancho} / \text{Alto}$) es **$1.0$ (cuadrada)** para absolutamente todas las imágenes.

Este resultado es muy común en *datasets* que ya han sido **preprocesados** o extraídos con reglas de recorte y *resize* muy estrictas (como es el caso de Imagenette, que es un subconjunto de ImageNet, pero con un *resize* inicial a 160x160).



### Justificación de Acciones de Preprocesamiento y Modelado

La uniformidad elimina la necesidad de tomar decisiones complejas sobre el *resize* y el manejo de relaciones de aspecto variables:

| Problema Detectado | Decisión y Justificación |
| :--- | :--- |
| **Tamaño Fijo 160x160** | **Decisión: El *resize* inicial no es necesario.** El paso de *resize* se convierte en un simple *casting* o transformación a tensor, ya que el tamaño de entrada ya es uniforme. |
| **Relación de Aspecto Cuadrada** | **Decisión: No se requiere *padding* ni *cropping* agresivo.** Como todas son cuadradas, no hay riesgo de distorsión geométrica (aplanamiento o estiramiento) al usar un tamaño de entrada típico para modelos. |
| **Data Augmentation** | Dado que la variación de tamaño es $0$, la data augmentation debe incluir **escalado aleatorio (*Random Resized Crop*)** para simular variaciones de tamaño y enfoque que no existen en el *dataset* original. |

-----

