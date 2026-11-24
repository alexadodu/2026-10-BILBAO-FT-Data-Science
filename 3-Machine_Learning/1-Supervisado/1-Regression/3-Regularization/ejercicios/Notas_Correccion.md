# Informe de Revisión del Jupyter Notebook de Alexa Dodu

**Nombre de archivo:** Ejercicio_Ridge_Lasso_ElasticNet.ipynb

---

## Calificación Global: **Regular**

### Resumen de Desempeño en Factores Principales

1. **Comprensión de las Tareas:** Alexa comprende la necesidad de preprocesar los datos, escalar las variables para regularización y probar distintas familias de modelos (Regresión Lineal, Ridge, Lasso, ElasticNet e interacciones polinómicas). Sin embargo, la comprensión es incompleta en la fase final del ejercicio: la **Tarea 3** pedía interpretar el modelo, extraer la fórmula explícita y responder a preguntas de negocio específicas sobre el impacto en ventas ante variaciones en la inversión publicitaria, aspectos que no fueron abordados.
2. **Corrección de las Respuestas:**
   - La limpieza de datos y el análisis exploratorio (EDA) son correctos y destacan positivamente por corregir manualmente la errata `"6s9.2"` en la columna `newpaper`.
   - El escalado y la separación de conjuntos de entrenamiento y prueba evitan adecuadamente el *data leakage*.
   - Se detecta un error conceptual importante en la parametrización de Lasso: se configuró `fit_intercept=False` tanto en el modelo lineal como en el polinómico. Al estar $X$ escalado pero la variable objetivo $y$ sin centrar, forzar el intercepto a cero desvirtúa por completo el ajuste y las curvas de error.
3. **Ejercicios No Resueltos:**
   - La **Tarea 3** se encuentra prácticamente sin resolver: no se extrajeron los coeficientes para formular la ecuación matemática del modelo final, ni se calculó ni respondió cuánto varían las ventas si aumenta la inversión en radio, televisión o periódicos. La última celda de código quedó vacía.

### Resumen de Desempeño en Factores Secundarios

1. **Legibilidad del Código:**
   - El código sigue una secuencia lógica y el uso de gráficos para visualizar la evolución del error frente a los hiperparámetros ($\lambda$ / `alpha`) aporta claridad.
   - Debe evitarse dejar expresiones coloquiales o comentarios de frustración en las celdas Markdown (`"Esto es una ... :((((("`), manteniendo un tono profesional en la entrega.
2. **Comentarios en el Código:**
   - Hay muy pocos comentarios explicativos en el código; la mayoría son anotaciones puntuales en los bucles (`# guarda el error`).
   - Faltó justificar mediante texto o conclusiones la elección final del modelo y la explicación de los resultados obtenidos.

---

## Lista de Ejercicios con Problemas

| Nº         | Ejercicio / Tarea                                              | Problema Detectado                                                                                                                                                                                                                                                                                      | Recomendación                                                                                                                                                                                                                   |
| :---------- | :------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1** | **Modelado con Lasso (`fit_intercept=False`)**         | En las líneas donde se instancia Lasso (tanto simple como polinómico) se utiliza `fit_intercept=False`. Dado que la variable objetivo `sales` no está centrada (su media es ~14), obligar a la recta a pasar por el origen distorsiona la penalización y produce errores artificialmente altos. | Mantener `fit_intercept=True` (el valor por defecto) en `Lasso` cuando la variable dependiente $y$ no esté estandarizada o centrada previamente.                                                                          |
| **2** | **Tarea 3: Formulación matemática del modelo**         | No se tradujo el mejor modelo a una fórmula matemática. No se imprimieron los coeficientes (`.coef_`) ni el intercepto (`.intercept_`) del modelo final para componer la ecuación predictiva.                                                                                                    | Extraer los parámetros del modelo final (`lassoR.intercept_`, `lassoR.coef_`) y documentar la fórmula resultante: $\text{Ventas} = \beta_0 + \sum \beta_i \cdot X_i$.                                                    |
| **3** | **Tarea 3: Preguntas de negocio e impacto marginal**     | Se omitió por completo responder a las preguntas: *¿Cuánto cambian las ventas si aumentamos la inversión en radio un punto más? ¿Y si aumentamos la inversión en TV o periódicos?*.                                                                                                           | Analizar las derivadas parciales o coeficientes asociados a cada medio publicitario (teniendo en cuenta la transformación polinómica o el escalador inverso) para estimar el impacto en ventas por unidad monetaria invertida. |
| **4** | **Reutilización y consistencia de variables en bucles** | En los bucles de evaluación de alphas, la lista `baseline` se reutiliza y se agregan 100 elementos idénticos en cada iteración sin reinicializarla en algunos bloques, lo cual puede generar desfases al graficar si cambia el tamaño de `alphas`.                                              | Definir `baseline` como un valor escalar o crear un arreglo constante directamente con `np.full_like(alphas, baseline_error)` para graficar la línea de referencia.                                                         |

---

## Comentarios Finales

Alexa demuestra buenas destrezas prácticas en la etapa inicial del flujo de trabajo: supo identificar y corregir un error de formato en los datos fuente, aplicó correctamente el escalado sobre el conjunto de entrenamiento para evitar fuga de información y estructuró con éxito barridos sistemáticos de hiperparámetros con curvas de validación.
