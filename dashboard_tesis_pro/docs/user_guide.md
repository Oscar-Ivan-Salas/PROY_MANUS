# Guía de Usuario - Dashboard Tesis Pro 2.0

## Introducción

Dashboard Tesis Pro es una plataforma integral diseñada para facilitar la gestión, análisis y documentación de proyectos de investigación académica. Esta guía te ayudará a aprovechar al máximo todas las funcionalidades del sistema, desde la gestión básica de archivos hasta la generación de informes profesionales.

## Primeros Pasos

### Acceso al Sistema

Una vez que el sistema esté instalado y configurado, puedes acceder a través de tu navegador web:

**Dashboard Principal**: http://localhost:3000

El dashboard principal es tu punto de entrada al sistema. Desde aquí puedes:
- Monitorear el estado de todos los módulos
- Acceder directamente a cada funcionalidad
- Visualizar métricas del sistema en tiempo real
- Gestionar configuraciones globales

### Navegación Principal

La interfaz está organizada en cuatro secciones principales:

1. **Dashboard**: Vista general con métricas y accesos rápidos
2. **Módulos**: Gestión y acceso a los tres módulos principales
3. **Sistema**: Configuración y monitoreo del sistema
4. **Ayuda**: Documentación y soporte

## Módulo 1: Explorador de Archivos Profesional

### Características Principales

El Explorador de Archivos está basado en FileBrowser y proporciona una interfaz moderna para la gestión de archivos de investigación.

#### Acceso al Módulo
- Desde el dashboard principal: Clic en "Explorador de Archivos"
- URL directa: http://localhost:8058
- A través del menú lateral: Módulos > Explorador de Archivos

### Gestión de Archivos

#### Subida de Archivos

1. **Navegación**: Utiliza el panel izquierdo para navegar entre carpetas
2. **Subida Simple**: 
   - Clic en el botón "Upload" en la barra superior
   - Selecciona archivos desde tu computadora
   - Los archivos se subirán a la carpeta actual

3. **Subida por Arrastrar y Soltar**:
   - Arrastra archivos directamente desde tu explorador de archivos
   - Suéltalos en el área principal de FileBrowser

#### Organización Recomendada

El sistema incluye una estructura de carpetas predefinida optimizada para proyectos de tesis:

```
📁 01_datos_originales/
   ├── encuestas/
   ├── entrevistas/
   ├── documentos/
   └── multimedia/

📁 02_datos_procesados/
   ├── limpios/
   ├── transformados/
   └── validados/

📁 03_resultados_analisis/
   ├── descriptivos/
   ├── inferenciales/
   └── modelos/

📁 04_visualizaciones/
   ├── graficos/
   ├── tablas/
   └── dashboards/

📁 05_informes/
   ├── borradores/
   ├── finales/
   └── presentaciones/
```

#### Gestión de Permisos

El sistema incluye tres roles predefinidos:

1. **Administrador**: Control total del sistema
   - Crear, editar, eliminar archivos y carpetas
   - Gestionar usuarios y permisos
   - Acceso a configuración del sistema

2. **Investigador**: Acceso completo a datos
   - Subir y descargar archivos
   - Crear y editar contenido
   - Ejecutar análisis

3. **Lector**: Solo lectura
   - Visualizar archivos
   - Descargar contenido autorizado
   - Acceso a reportes finales

### Funciones Avanzadas

#### Búsqueda de Archivos

1. Utiliza la barra de búsqueda en la parte superior
2. Busca por nombre de archivo, extensión o contenido
3. Aplica filtros por fecha, tamaño o tipo de archivo

#### Vista Previa

- **Documentos**: PDF, Word, Excel se muestran directamente
- **Imágenes**: Vista previa automática con zoom
- **Código**: Resaltado de sintaxis para múltiples lenguajes
- **Datos**: Vista tabular para CSV y Excel

#### Compartir Archivos

1. Selecciona el archivo que deseas compartir
2. Clic derecho > "Share" o usa el botón de compartir
3. Configura permisos y tiempo de expiración
4. Copia el enlace generado

## Módulo 2: Análisis Estadístico Interactivo

### Acceso y Configuración Inicial

**URL de acceso**: http://localhost:8050

El módulo de análisis utiliza Streamlit para proporcionar una interfaz interactiva y fácil de usar.

### Carga de Datos

#### Métodos de Carga

1. **Desde el Explorador de Archivos**:
   - Los archivos subidos al explorador están automáticamente disponibles
   - Navega a la carpeta correspondiente
   - Selecciona el archivo desde el dropdown

2. **Subida Directa**:
   - Utiliza el widget de subida en la barra lateral
   - Formatos soportados: CSV, Excel (.xlsx, .xls), JSON
   - Tamaño máximo: 200MB por archivo

#### Validación de Datos

El sistema incluye validación automática que verifica:
- **Integridad**: Archivos no corruptos
- **Formato**: Estructura de datos válida
- **Tipos de datos**: Identificación automática de variables numéricas y categóricas
- **Valores faltantes**: Detección y reporte de datos incompletos

### Análisis Descriptivos

#### Estadísticas Básicas

Una vez cargados los datos, el sistema genera automáticamente:

1. **Resumen General**:
   - Número de observaciones y variables
   - Tipos de datos identificados
   - Porcentaje de valores faltantes

2. **Estadísticas Descriptivas**:
   - Media, mediana, moda
   - Desviación estándar y varianza
   - Percentiles y cuartiles
   - Valores mínimos y máximos

3. **Distribuciones**:
   - Histogramas automáticos
   - Gráficos de densidad
   - Diagramas de caja (boxplots)

#### Visualizaciones Interactivas

El módulo genera automáticamente:

1. **Gráficos Univariados**:
   - Histogramas con bins ajustables
   - Gráficos de barras para variables categóricas
   - Gráficos de densidad con curvas suavizadas

2. **Gráficos Bivariados**:
   - Diagramas de dispersión con líneas de tendencia
   - Mapas de calor de correlación
   - Gráficos de cajas agrupados

3. **Gráficos Multivariados**:
   - Matrices de dispersión
   - Gráficos de coordenadas paralelas
   - Análisis de componentes principales (PCA)

### Análisis Inferenciales

#### Pruebas de Hipótesis

El sistema incluye una amplia gama de pruebas estadísticas:

1. **Pruebas t**:
   - t de una muestra
   - t de muestras independientes
   - t de muestras pareadas
   - Interpretación automática de resultados

2. **ANOVA**:
   - ANOVA de una vía
   - ANOVA de dos vías
   - Pruebas post-hoc (Tukey, Bonferroni)
   - Verificación de supuestos

3. **Pruebas No Paramétricas**:
   - Mann-Whitney U
   - Wilcoxon
   - Kruskal-Wallis
   - Chi-cuadrado

#### Análisis de Correlación

1. **Correlación de Pearson**: Para variables numéricas
2. **Correlación de Spearman**: Para datos ordinales
3. **Correlación de Kendall**: Para muestras pequeñas
4. **Visualización**: Matrices de correlación interactivas

### Análisis Avanzados

#### Clustering Automático

El sistema incluye algoritmos de clustering no supervisado:

1. **K-means**:
   - Determinación automática del número óptimo de clusters
   - Visualización en 2D y 3D
   - Interpretación de centroides

2. **Clustering Jerárquico**:
   - Dendrogramas interactivos
   - Diferentes métodos de enlace
   - Corte automático del árbol

#### Análisis de Regresión

1. **Regresión Lineal Simple y Múltiple**:
   - Selección automática de variables
   - Diagnósticos de residuos
   - Métricas de bondad de ajuste

2. **Regresión Logística**:
   - Para variables dependientes categóricas
   - Curvas ROC automáticas
   - Interpretación de odds ratios

### Exportación de Resultados

#### Formatos Disponibles

1. **Gráficos**:
   - PNG de alta resolución
   - SVG vectorial
   - PDF para publicaciones

2. **Datos**:
   - CSV procesados
   - Excel con múltiples hojas
   - JSON estructurado

3. **Reportes**:
   - HTML interactivo
   - PDF con gráficos embebidos
   - Markdown para documentación

## Módulo 3: Generador de Informes Profesionales

### Acceso y Configuración

**URL de acceso**: http://localhost:8070

Este módulo permite crear informes profesionales automáticos basados en los análisis realizados.

### Tipos de Informes

#### 1. Reporte Ejecutivo

Diseñado para audiencias no técnicas:
- **Resumen ejecutivo** con hallazgos principales
- **Visualizaciones simplificadas** y fáciles de interpretar
- **Recomendaciones** basadas en los datos
- **Conclusiones** en lenguaje accesible

#### 2. Reporte Técnico

Para audiencias especializadas:
- **Metodología detallada** de análisis
- **Resultados estadísticos** completos
- **Tablas de datos** con todos los valores
- **Interpretación técnica** de resultados

#### 3. Dashboard Interactivo

Reporte web interactivo:
- **Gráficos dinámicos** con filtros
- **Tablas ordenables** y filtrables
- **Navegación** entre secciones
- **Exportación** de elementos individuales

### Configuración de Reportes

#### Selección de Contenido

1. **Datos de Origen**:
   - Selecciona archivos analizados
   - Elige análisis específicos a incluir
   - Configura período de datos

2. **Secciones del Reporte**:
   - Resumen ejecutivo
   - Metodología
   - Resultados descriptivos
   - Análisis inferenciales
   - Conclusiones y recomendaciones

#### Personalización Visual

1. **Tema y Colores**:
   - Paleta de colores corporativa
   - Fuentes y tipografía
   - Logos y branding

2. **Formato de Gráficos**:
   - Tamaño y resolución
   - Estilo de visualización
   - Colores y leyendas

### Plantillas Disponibles

#### Plantilla Académica

Optimizada para tesis y publicaciones:
- **Formato APA** estándar
- **Numeración** automática de figuras y tablas
- **Referencias** bibliográficas integradas
- **Índices** automáticos

#### Plantilla Corporativa

Para reportes empresariales:
- **Diseño profesional** moderno
- **Secciones ejecutivas** destacadas
- **Gráficos** optimizados para presentaciones
- **Branding** corporativo integrado

#### Plantilla Científica

Para publicaciones de investigación:
- **Formato de revista** científica
- **Metodología** detallada
- **Resultados** con significancia estadística
- **Discusión** estructurada

### Generación y Exportación

#### Proceso de Generación

1. **Configuración**:
   - Selecciona tipo de reporte
   - Configura parámetros
   - Elige plantilla

2. **Generación**:
   - El sistema procesa automáticamente
   - Integra datos y análisis
   - Aplica formato seleccionado

3. **Revisión**:
   - Vista previa del reporte
   - Edición de secciones
   - Ajustes finales

#### Formatos de Exportación

1. **HTML**:
   - Interactivo y responsive
   - Ideal para web
   - Gráficos dinámicos

2. **PDF**:
   - Formato profesional
   - Listo para imprimir
   - Gráficos de alta calidad

3. **Word (DOCX)**:
   - Editable
   - Compatible con Microsoft Word
   - Formato académico estándar

4. **Markdown**:
   - Para documentación técnica
   - Compatible con GitHub
   - Fácil de versionar

## Flujos de Trabajo Recomendados

### Proyecto de Tesis Completo

#### Fase 1: Preparación de Datos

1. **Organización Inicial**:
   - Crear estructura de carpetas en el Explorador de Archivos
   - Subir datos originales a `01_datos_originales/`
   - Documentar fuentes y metodología de recolección

2. **Limpieza de Datos**:
   - Utilizar el módulo de análisis para identificar problemas
   - Procesar y limpiar datos
   - Guardar versiones procesadas en `02_datos_procesados/`

#### Fase 2: Análisis Exploratorio

1. **Análisis Descriptivo**:
   - Generar estadísticas básicas
   - Crear visualizaciones exploratorias
   - Identificar patrones y anomalías

2. **Validación de Supuestos**:
   - Verificar normalidad de distribuciones
   - Evaluar homogeneidad de varianzas
   - Detectar valores atípicos

#### Fase 3: Análisis Confirmatorio

1. **Pruebas de Hipótesis**:
   - Ejecutar análisis inferenciales
   - Interpretar resultados estadísticos
   - Documentar hallazgos significativos

2. **Análisis Avanzados**:
   - Aplicar técnicas de clustering si es relevante
   - Realizar análisis de regresión
   - Validar modelos predictivos

#### Fase 4: Documentación y Reportes

1. **Generación de Informes**:
   - Crear reporte técnico completo
   - Generar resumen ejecutivo
   - Preparar presentaciones

2. **Revisión y Finalización**:
   - Revisar todos los análisis
   - Validar conclusiones
   - Preparar documentación final

### Proyecto de Investigación Colaborativa

#### Gestión de Equipo

1. **Configuración de Permisos**:
   - Asignar roles según responsabilidades
   - Configurar acceso a carpetas específicas
   - Establecer flujos de aprobación

2. **Colaboración en Análisis**:
   - Compartir datasets procesados
   - Documentar metodologías utilizadas
   - Mantener historial de cambios

#### Comunicación de Resultados

1. **Reportes Intermedios**:
   - Generar reportes de progreso regulares
   - Compartir hallazgos preliminares
   - Solicitar retroalimentación del equipo

2. **Presentaciones**:
   - Crear dashboards interactivos para reuniones
   - Generar reportes ejecutivos para stakeholders
   - Preparar documentación técnica para revisión

## Consejos y Mejores Prácticas

### Gestión de Archivos

1. **Nomenclatura Consistente**:
   - Utiliza fechas en formato YYYY-MM-DD
   - Incluye versiones en nombres de archivo
   - Evita espacios y caracteres especiales

2. **Backup Regular**:
   - Utiliza la función de backup del sistema
   - Mantén copias en ubicaciones externas
   - Documenta cambios importantes

### Análisis de Datos

1. **Documentación**:
   - Registra todas las transformaciones realizadas
   - Mantén un log de decisiones analíticas
   - Documenta supuestos y limitaciones

2. **Validación**:
   - Verifica resultados con métodos alternativos
   - Utiliza subconjuntos de datos para validación
   - Solicita revisión de colegas

### Generación de Reportes

1. **Audiencia**:
   - Adapta el nivel técnico al público objetivo
   - Incluye contexto suficiente para la comprensión
   - Utiliza visualizaciones apropiadas

2. **Calidad**:
   - Revisa ortografía y gramática
   - Verifica exactitud de números y gráficos
   - Mantén consistencia en formato y estilo

## Solución de Problemas Comunes

### Problemas de Carga de Datos

**Error: "Archivo no reconocido"**
- Verifica que el formato sea compatible (CSV, Excel, JSON)
- Asegúrate de que el archivo no esté corrupto
- Revisa la codificación de caracteres (UTF-8 recomendado)

**Error: "Datos faltantes"**
- Utiliza las herramientas de limpieza integradas
- Considera métodos de imputación apropiados
- Documenta el tratamiento de valores faltantes

### Problemas de Análisis

**Error: "Supuestos no cumplidos"**
- Verifica normalidad de distribuciones
- Considera transformaciones de datos
- Utiliza pruebas no paramétricas como alternativa

**Error: "Muestra insuficiente"**
- Verifica el tamaño mínimo requerido para el análisis
- Considera métodos de bootstrap
- Ajusta el nivel de significancia si es apropiado

### Problemas de Reportes

**Error: "Generación fallida"**
- Verifica que todos los análisis estén completos
- Asegúrate de que las plantillas estén disponibles
- Revisa los logs del sistema para detalles específicos

**Error: "Formato incorrecto"**
- Verifica la configuración de exportación
- Asegúrate de tener permisos de escritura
- Intenta con un formato alternativo

## Soporte y Recursos Adicionales

### Documentación Técnica

- **API Reference**: Documentación completa de todas las APIs
- **Development Guide**: Guía para desarrolladores y personalización
- **Deployment Guide**: Instrucciones para instalación en producción

### Comunidad y Soporte

- **GitHub Issues**: Para reportar bugs y solicitar funcionalidades
- **Discord**: Comunidad de usuarios para preguntas y discusión
- **Email**: Soporte técnico directo para problemas críticos

### Recursos de Aprendizaje

- **Tutoriales en Video**: Guías paso a paso para funcionalidades específicas
- **Casos de Estudio**: Ejemplos reales de uso del sistema
- **Webinars**: Sesiones en vivo sobre mejores prácticas

---

Esta guía de usuario te proporciona una base sólida para aprovechar al máximo Dashboard Tesis Pro. Para preguntas específicas o problemas técnicos, no dudes en consultar la documentación adicional o contactar al equipo de soporte.

