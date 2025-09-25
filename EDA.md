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

## 3. Estadísticas de Color (Media y Desviación Estándar por Canal RGB)

### Análisis de Media y Desviación Estándar (Normalización)

#### Resultados de Estadísticas
| Canal | Media ($\mu$) | Desviación Estándar ($\sigma$) |
| :---: | :---: | :---: |
| **R (Rojo)** | 0.4625 | 0.2748 |
| **G (Verde)** | 0.4580 | 0.2690 |
| **B (Azul)** | 0.4298 | 0.2856 |


##### Interpretación de las Estadísticas
1.  **Media General:** Las medias de los tres canales son muy similares y están todas cerca de $0.45$. Esto sugiere que el *dataset* tiene una **iluminación general ligeramente oscura** (ya que $0.5$ sería el gris medio perfecto).

2.  **Dominancia de Color:** La media del canal **Azul (0.4298)** es notablemente la más baja, mientras que las de Rojo y Verde son las más altas. Esto, en contraste con los valores de color de Imagenette (que suelen tener una media azul más baja), sugiere que el *dataset* **no tiene una dominancia de color azul** o ambientes fríos tan fuerte como el promedio de Imagenette.

3.  **Variabilidad (Desviación Estándar):** La $\sigma$ es alta (alrededor de $0.27 - 0.28$), lo que indica una **alta varianza de contraste y brillo** entre las imágenes. El canal **Azul (0.2856)** tiene la mayor varianza, lo que implica que la saturación y la distribución de azules varían más que el rojo o el verde.

---

### Análisis del Histograma de Intensidad

El gráfico muestra la distribución de todos los valores de píxel para cada canal en el conjunto de entrenamiento.

#### Interpretación del Histograma
1.  **Forma General (Curva):** La distribución principal de la intensidad (la "joroba" ancha y baja en el centro) es bastante **plana y uniforme** en el rango de $0.2$ a $0.8$. Esto confirma la alta $\sigma$ e indica que hay una buena mezcla de píxeles oscuros, medios y brillantes.
2.  **Dominancia de Píxeles Oscuros (Valor 0.0):** Hay un pico masivo en el valor de píxel **$0.0$** (negro), especialmente en el canal **Azul**. Esto es un indicador de la presencia de:
    * **Mucho *background* negro/muy oscuro** en los bordes de las imágenes (común en imágenes de Imagenette recortadas).
    * **Sombras profundas** o **imágenes muy oscuras**.
3.  **Dominancia de Píxeles Brillantes (Valor 1.0):** Hay otro pico significativo en el valor de píxel **$1.0$** (blanco), también fuerte en el canal **Azul**, y presente en Rojo y Verde. Esto indica la presencia de:
    * **Sobresaturación / *Highlights*** (zonas muy iluminadas).
    * **Fondo blanco o *background* muy brillante**.
4.  **Implicación del Canal Azul:** La **dominancia del canal Azul** en ambos extremos ($0.0$ y $1.0$) es muy notable. Esto podría ser debido a cielos azules brillantes o a la inclusión de objetos con fuertes tonos azules. La alta varianza del canal Azul ya mencionada se refleja aquí en estos picos extremos.

### Justificación de Acciones de Preprocesamiento y Modelado
El análisis de color confirma la necesidad de normalización y sugiere algunas consideraciones para el *Data Augmentation*:

| Resultado del Análisis | Decisión y Justificación |
| :--- | :--- |
| **Medias y Desviaciones Estándar Específicas** | **Acción: Normalizar la entrada.** Debemos normalizar el tensor de imágenes usando los valores calculados: $\text{Imagen}_{\text{norm}} = (\text{Imagen} - \mu) / \sigma$. Esto centrará los datos y mejorará la convergencia del modelo. |
| **Picos Extremos (0.0 y 1.0)** | **Acción: Evaluar el recorte (*clipping*).** Los picos en $0.0$ y $1.0$ sugieren que las imágenes pueden tener áreas grandes de negro puro o blanco puro. Si estas áreas no son informativas (ej. bordes negros), el modelo podría enfocarse en ellas. Esto subraya la importancia de usar **Random Resized Crop** para eliminar estos bordes no informativos y centrarse en el objeto. |
| **Variabilidad de Brillo/Contraste** | **Acción: Implementar Augmentation de color.** El *Data Augmentation* debe incluir transformaciones de color (ajustes aleatorios de **Brillo, Contraste, y Saturación**) para hacer que el modelo sea robusto a la alta varianza de iluminación observada. |

---

## 4. Análisis Detallado de la Calidad de Imágenes

### Interpretación de los Resultados

El análisis de calidad revela que la calidad del *dataset* es **excepcionalmente alta** y que los problemas de baja calidad son **marginales**.

1.  **Imágenes Problemáticas Totales (1.73%):** Solo 164 de las 9,469 imágenes cumplen con al menos uno de los umbrales. Esto es un porcentaje muy bajo, lo que significa que el **$98.27\%$** del conjunto de entrenamiento es de buena calidad.
2.  **Borrosidad (0.02%):** La borrosidad no es un problema. Solo 2 imágenes fueron detectadas con el estricto umbral de $<10.0$. Esto confirma que el *dataset* tiene **gran nitidez** en general.
3.  **Brillo y Contraste (Los Defectos Dominantes):** La mayoría de los problemas se concentran en los extremos de iluminación y contraste, pero siguen siendo porcentajes muy bajos:
    * **Muy Brillantes (0.63%):** El defecto más común.
    * **Bajo Contraste (0.62%):** El segundo defecto más común.
    * **Muy Oscuras (0.48%):** Es el tercer defecto más común.
4.  **Problemas Múltiples (0.02%):** Es prácticamente nulo (solo 2 imágenes). Esto sugiere que la mayoría de las imágenes que fallan, lo hacen por **un solo defecto extremo** (o son imágenes tan malas que entran en la categoría de múltiples defectos, pero son muy pocas).

### Justificación de Acciones de Preprocesamiento y Limpieza

| Hallazgo | Conclusión | Acción Recomendada |
| :--- | :--- | :--- |
| **Bajo Porcentaje Total (1.73%)** | La limpieza manual o eliminación de datos **no es necesaria ni eficiente**. Eliminar solo el $1.73\%$ de los datos apenas tendría impacto. | **No hay acción de limpieza requerida.** Los recursos se deben enfocar en el modelado. |
| **Problemas concentrados en Brillo/Contraste** | Estos defectos son casos extremos de la varianza ya observada en el análisis del histograma (Punto 3). El modelo debe ser robusto ante la iluminación. | **Data Augmentation de Color Vigoroso:** Es la solución ideal. Ajustes aleatorios de brillo, contraste y saturación deben ser pasos obligatorios en el *pipeline* de aumento de datos. |
| **Borrosidad Nula** | Las imágenes son nítidas. | **Data Augmentation de Nitidez:** Se puede incluir un ligero *Random Blur* como parte del *augmentation* para simular imágenes del mundo real tomadas en movimiento. |

---

## 5. Análisis de la Distribución de Brillo, Contraste y Saturación

### Interpretación de los Histogramas

Los tres histogramas muestran distribuciones que, en general, son **similares a una campana de Gauss**, pero con variaciones que indican tendencias claras en el *dataset*.

#### 1. Distribución de Brillo (Amarillo)
* **Forma y Pico:** La distribución está bien centrada alrededor de un valor medio de píxel de **aproximadamente $120-130$** (en una escala de $0-255$). Esto confirma la media global de $0.45-0.5$ (punto 3), indicando que las imágenes están, en promedio, **bien iluminadas** (cerca del gris medio).
* **Asimetría:** Hay una ligera **cola hacia la derecha** (valores altos), lo que sugiere que hay más imágenes con brillo medio-alto que imágenes muy oscuras.
* **Implicación:** La mayoría de las imágenes no están demasiado oscuras ni demasiado brillantes, pero el modelo necesita aprender a manejar la variabilidad a lo largo de todo el rango.

#### 2. Distribución de Contraste (Azul Claro)
* **Forma y Pico:** La distribución es casi simétrica y se centra alrededor de una desviación estándar de **aproximadamente $55-65$**. Este valor indica una varianza de píxeles **moderada a alta**, confirmando el análisis del punto 3.
* **Rango:** El contraste se distribuye en un rango amplio (de casi $0$ hasta más de $100$), lo que significa que el *dataset* ya contiene una **alta variabilidad natural de contraste**.
* **Implicación:** El modelo no debería tener problemas con el contraste general, pero introducir variaciones aleatorias ayudará a generalizar en los extremos.

#### 3. Distribución de Saturación (Verde Claro)
* **Forma y Pico:** Esta distribución es la más **asimétrica** de las tres. El pico se encuentra en un valor medio de saturación **relativamente bajo** (aproximadamente $50$). La cola se extiende mucho hacia la derecha (valores altos).
* **Implicación:** La mayoría de las imágenes en Imagenette tienen **tonos de color apagados o moderados**. Las imágenes con colores muy vivos (alta saturación) son la minoría.
* **Riesgo:** El modelo podría aprender a depender de la baja saturación. La *Data Augmentation* es importante para enseñar al modelo a reconocer objetos **incluso si los colores son mucho más saturados** de lo que son en el *dataset* original.

---

### Justificación de Acciones de Data Augmentation

El análisis de las distribuciones confirma que el *Data Augmentation* de color no solo es útil, sino **necesario**, especialmente para la saturación:

| Propiedad | Rango Natural del Dataset | Decisión de Augmentation | Parámetros Sugeridos (Ej. para PyTorch) |
| :--- | :--- | :--- | :--- |
| **Brillo** | Centrado en el medio ($\approx 120$); bien distribuido. | **Moderado.** Modificar aleatoriamente para cubrir la ligera asimetría y los casos extremos. | `brightness=(0.7, 1.3)` (Rango de variación de $\pm 30\%$). |
| **Contraste** | Alto y bien distribuido ($\approx 60$); amplio rango. | **Moderado.** El modelo ya ve mucha variación, pero el *augmentation* lo hará más robusto. | `contrast=(0.7, 1.3)` (Rango de variación de $\pm 30\%$). |
| **Saturación** | **Bajo** (pico en $\approx 50$); fuerte asimetría. | **Agresivo.** Es vital aumentar la saturación para evitar que el modelo se sobreajuste a los colores apagados. | `saturation=(0.5, 1.5)` (Rango de variación más amplio; de $50\%$ menos a $50\%$ más). |


---


## 6. Análisis del Espectro de Magnitud Promedio (FFT)

El gráfico muestra la intensidad promedio de las frecuencias de la imagen. El **centro** corresponde a las **bajas frecuencias** (patrones grandes, colores uniformes, formas generales), y las **esquinas/bordes** corresponden a las **altas frecuencias** (detalles finos, texturas, ruido, bordes agudos).

### Interpretación del Espectro

1.  **Concentración Central Fuerte (Bajas Frecuencias):**
    * Hay un **punto central blanco muy brillante** y una caída de intensidad muy rápida a medida que nos alejamos del centro. Esto indica que la **mayor parte de la energía** del *dataset* está concentrada en las **bajas frecuencias**.
    * **Significado:** Las imágenes están dominadas por **formas grandes, fondos uniformes y objetos con gradientes de color suaves**. Esto es típico de imágenes de objetos grandes en el centro o paisajes amplios, donde la información visual dominante es la forma y el color, no la textura fina.

2.  **Líneas Horizontales y Verticales (Patrones Axiales):**
    * Se observan **líneas de energía más brillante** que se extienden horizontal y verticalmente desde el centro (ejes $X$ y $Y$).
    * **Significado:** Esto suele indicar la presencia de **patrones estructurales consistentes** como:
        * **Bordes fuertes** horizontales y verticales (ej. estructuras arquitectónicas, edificios, líneas de horizonte).
        * **Efectos de *resizing*** o **compresión JPEG** (los algoritmos a menudo introducen artefactos en estas orientaciones).
        * Dada la naturaleza de Imagenette (subconjunto de ImageNet con clases como 'church' y 'garbage truck'), los bordes estructurales fuertes son muy probables.

3.  **Bordes/Esquinas Oscuras (Altas Frecuencias):**
    * La región de alta frecuencia (bordes y esquinas) es **muy oscura**.
    * **Significado:** Las imágenes tienen **poca energía** en las frecuencias muy altas. Esto implica que, en promedio:
        * Hay **poco ruido aleatorio** (ruido es típicamente muy alta frecuencia).
        * Hay **pocos detalles muy finos o texturas extremadamente granulares**.

### Justificación de Acciones de Preprocesamiento y Modelado

| Hallazgo | Conclusión | Acción Recomendada |
| :--- | :--- | :--- |
| **Dominancia de Bajas Frecuencias** | El modelo tenderá a aprender **formas y colores generales** (información de baja frecuencia). | **Data Augmentation de Perspectiva/Geometría:** Incluir rotaciones y cambios de perspectiva (shear) ayuda a enseñar al modelo que la forma del objeto es relevante independientemente de su orientación o ligera distorsión. |
| **Poca Energía en Altas Frecuencias** | El modelo podría ser **poco robusto** a texturas finas o ruido en el mundo real. | **Data Augmentation de Ruido/Nitidez:** Aplicar **ruido Gaussiano aleatorio** o un *blur* ligero aleatorio (ya sugerido en el punto 5) es esencial para simular la variabilidad textural del mundo real y evitar sobreajuste a la limpieza de Imagenette. |
| **Líneas Axiales (Efectos de Resizing/Estructuras)** | La información estructural es importante. | **Asegurar *Data Augmentation* Simétrica:** Usar *Random Horizontal Flip* es seguro (a menos que haya objetos que cambien de significado al voltearse), y ayuda a balancear los patrones estructurales. El *Random Resized Crop* (ya recomendado) también ayudará a mitigar el efecto de los bordes. |

---
