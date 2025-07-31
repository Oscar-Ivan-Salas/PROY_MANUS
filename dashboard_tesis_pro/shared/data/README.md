# Estructura de Carpetas - Dashboard Tesis Pro

Esta estructura está diseñada para organizar eficientemente los proyectos de tesis y análisis de datos, siguiendo las mejores prácticas de ciencia de datos y gestión de proyectos académicos.

## 📁 Estructura de Directorios

### 01_datos_originales
**Propósito**: Almacenar los datos en su formato original, sin modificaciones.
- **Contenido**: Archivos CSV, Excel, JSON, bases de datos, encuestas, etc.
- **Regla**: NUNCA modificar estos archivos directamente
- **Ejemplos**: `encuesta_estudiantes.xlsx`, `datos_censo.csv`, `registros_experimento.json`

### 02_datos_procesados
**Propósito**: Datos limpiados, transformados y preparados para análisis.
- **Contenido**: Datasets procesados, variables creadas, datos normalizados
- **Ejemplos**: `datos_limpios.csv`, `variables_transformadas.pkl`, `dataset_final.parquet`

### 03_analisis_exploratorio
**Propósito**: Resultados del análisis exploratorio de datos (EDA).
- **Contenido**: Gráficos descriptivos, estadísticas básicas, visualizaciones iniciales
- **Ejemplos**: `distribucion_variables.png`, `correlaciones.html`, `resumen_descriptivo.xlsx`

### 04_analisis_estadistico
**Propósito**: Análisis estadísticos formales y pruebas de hipótesis.
- **Contenido**: Resultados de t-tests, ANOVA, regresiones, chi-cuadrado
- **Ejemplos**: `test_hipotesis.xlsx`, `regresion_lineal.html`, `anova_resultados.csv`

### 05_modelos_predictivos
**Propósito**: Modelos de machine learning y análisis predictivo.
- **Contenido**: Modelos entrenados, métricas de evaluación, predicciones
- **Ejemplos**: `modelo_clasificacion.pkl`, `metricas_evaluacion.json`, `predicciones.csv`

### 06_resultados_finales
**Propósito**: Resultados consolidados y hallazgos principales.
- **Contenido**: Tablas finales, gráficos para publicación, conclusiones
- **Ejemplos**: `tabla_resultados_principales.xlsx`, `graficos_publicacion/`, `conclusiones.md`

### 07_informes_generados
**Propósito**: Informes automáticos generados por el dashboard.
- **Contenido**: PDFs, Word, presentaciones generadas automáticamente
- **Ejemplos**: `informe_analisis_2024.pdf`, `presentacion_resultados.pptx`

### 08_documentos_referencia
**Propósito**: Literatura, manuales, documentación de referencia.
- **Contenido**: Papers, libros, documentación técnica, metodologías
- **Ejemplos**: `bibliografia.pdf`, `metodologia_analisis.docx`, `papers_referencia/`

### 09_scripts_codigo
**Propósito**: Código fuente, scripts y notebooks del proyecto.
- **Contenido**: Scripts Python/R, notebooks Jupyter, código de análisis
- **Ejemplos**: `limpieza_datos.py`, `analisis_principal.ipynb`, `funciones_utils.R`

### 10_recursos_multimedia
**Propósito**: Imágenes, videos, audio y otros recursos multimedia.
- **Contenido**: Fotos, diagramas, videos explicativos, presentaciones
- **Ejemplos**: `diagrama_metodologia.png`, `video_explicativo.mp4`, `logos/`

## 🏷️ Convenciones de Nomenclatura

### Archivos
- **Formato**: `descripcion_clara_fecha.extension`
- **Ejemplos**: 
  - `datos_encuesta_2024-01-15.csv`
  - `analisis_regresion_v2.xlsx`
  - `informe_final_2024-03-20.pdf`

### Carpetas
- **Usar números para orden**: `01_`, `02_`, etc.
- **Nombres descriptivos**: Sin espacios, usar guiones bajos
- **Subcarpetas**: Organizar por fecha o tema cuando sea necesario

## 🔧 Integración con el Dashboard

Esta estructura está optimizada para trabajar con los módulos del Dashboard Tesis Pro:

1. **Explorador de Archivos**: Navega fácilmente entre las carpetas organizadas
2. **Módulo de Análisis**: Carga automáticamente datos desde `01_datos_originales` y `02_datos_procesados`
3. **Generador de Informes**: Guarda automáticamente en `07_informes_generados`

## 📋 Checklist de Organización

- [ ] Datos originales guardados en `01_datos_originales` (sin modificar)
- [ ] Datos procesados documentados en `02_datos_procesados`
- [ ] EDA completado y guardado en `03_analisis_exploratorio`
- [ ] Análisis estadísticos en `04_analisis_estadistico`
- [ ] Modelos (si aplica) en `05_modelos_predictivos`
- [ ] Resultados principales en `06_resultados_finales`
- [ ] Código documentado en `09_scripts_codigo`
- [ ] Referencias organizadas en `08_documentos_referencia`

## 🚀 Migración a la Nube

Para migrar esta estructura a la nube:

1. **Google Drive/OneDrive**: Mantener la misma estructura de carpetas
2. **AWS S3/Azure Blob**: Usar prefijos para simular carpetas
3. **GitHub**: Usar `.gitignore` para datos sensibles, mantener estructura
4. **Dropbox**: Sincronización automática manteniendo organización

## 🔒 Consideraciones de Seguridad

- **Datos sensibles**: Usar carpeta `_privado/` con permisos restringidos
- **Respaldos**: Configurar backup automático de carpetas críticas
- **Versionado**: Usar Git para código en `09_scripts_codigo`
- **Acceso**: Configurar permisos diferenciados por tipo de usuario

