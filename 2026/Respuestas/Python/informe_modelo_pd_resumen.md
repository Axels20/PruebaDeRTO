
# Informe resumido del modelo de PD y grupos T1–T8

Este documento resume el desarrollo del modelo de probabilidad de incumplimiento (PD) y la construcción de la tabla de rating T1–T8.

## Fase 1: Datos y preprocesamiento
- Se usó 2018 como periodo de entrenamiento (base_train-2), 201901 como validación y 201902 como prueba.
- Se identificaron códigos negativos como marcadores de falta de información y se generaron flags *_neg_flag por variable.
- Se aplicó imputación por mediana calculada en 2018 a todas las bases.

## Fase 2: Modelado
- Modelo principal: GradientBoostingClassifier sobre todas las variables numéricas y engineered.
- El tuning se hizo sobre clientes `tipo_cliente = objetivo` usando validación cruzada, luego se reentrenó con todo 2018 (objetivo + adicion).
- Métricas estándar en 201901 objetivo: AUC, Gini y KS superiores al baseline de regresión logística.

## Fase 3: Calibración y grupos T1–T8
- Se calibró el GBM con CalibratedClassifierCV (método isotónico) sobre 2018 objetivo.
- Se definieron umbrales iniciales según los rangos de PD objetivo y se ajustaron mediante búsqueda aleatoria local.
- La función objetivo fue maximizar el porcentaje de población cuya tasa de default observada por grupo cae dentro del rango T1–T8.

## Fase 4: Aplicación a 201902
- Se aplicó el pipeline completo a base_prueba (201902).
- Se generó el archivo `salida_grupo_riesgo_201902.csv` con columnas `num_doc`, `tipo_cliente` y `grupo_riesgo` (t1–t8).
- No hay nulos ni valores de grupo fuera de {t1, ..., t8}.

## Fase 5: Uso y consideraciones
- El modelo puede usarse para originación, pricing y seguimiento de portafolio, sujeto a backtesting periódico.
- Se recomienda complementar con variables de buró y/o macroeconómicas y revisar la estabilidad de la calibración al menos una vez al año.
