# Dashboard Tesis Pro 2.0

![Dashboard Tesis Pro](https://img.shields.io/badge/Dashboard-Tesis%20Pro-blue?style=for-the-badge&logo=react)
![Version](https://img.shields.io/badge/version-2.0.0-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-orange?style=for-the-badge)

**Dashboard Tesis Pro** es un sistema integrado de gestión, análisis y generación de informes diseñado específicamente para proyectos de investigación académica y tesis profesionales. Combina un explorador de archivos profesional, análisis estadístico interactivo y generación automática de informes en una plataforma unificada y moderna.

## 🚀 Características Principales

### 📁 **Módulo 1: Explorador de Archivos Profesional**
- **FileBrowser integrado** con interfaz moderna inspirada en VSCode
- **Gestión de permisos** por roles (admin, investigador, lector)
- **API REST completa** para integración con otros módulos
- **Estructura organizada** específica para proyectos de tesis
- **Subida y descarga** de archivos con validación automática

### 📊 **Módulo 2: Análisis Estadístico Interactivo**
- **Análisis inferenciales completos**: pruebas t, ANOVA, chi-cuadrado
- **Clustering automático** con visualizaciones 2D y 3D
- **Validación de datos** con mensajes de error amigables
- **Visualizaciones interactivas** con Plotly y Streamlit
- **Exportación de resultados** en múltiples formatos

### 📄 **Módulo 3: Generador de Informes Profesionales**
- **Reportes automáticos** en HTML, PDF, Word y Markdown
- **Plantillas personalizables** con sistema Jinja2
- **Integración de gráficos** automática en base64
- **Análisis inteligente** con conclusiones y recomendaciones
- **Historial completo** de reportes generados

### 🏠 **Dashboard Principal Unificado**
- **Interfaz React moderna** con Tailwind CSS y shadcn/ui
- **Backend Flask robusto** con API REST completa
- **Monitoreo en tiempo real** del sistema y módulos
- **Navegación fluida** entre módulos con estado sincronizado
- **Notificaciones inteligentes** y gestión centralizada

## 🏗️ Arquitectura del Sistema

```
Dashboard Tesis Pro/
├── main_dashboard/          # Dashboard principal (Flask + React)
│   ├── src/                # Backend Flask
│   │   ├── routes/         # Blueprints de API
│   │   └── config/         # Configuración del sistema
│   └── static/             # Frontend React compilado
├── dashboard_frontend/      # Frontend React (desarrollo)
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── contexts/       # Estado global
│   │   └── assets/         # Recursos estáticos
├── modules/                # Módulos independientes
│   ├── file_explorer/      # FileBrowser + API
│   ├── data_analysis/      # Streamlit + análisis
│   └── report_generator/   # Generador de informes
└── shared/                 # Recursos compartidos
    └── data/               # Estructura de datos organizada
```

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask 3.0+** - Framework web principal
- **FileBrowser** - Explorador de archivos profesional
- **Streamlit** - Interfaz de análisis interactivo
- **Python 3.11+** - Lenguaje principal

### Frontend
- **React 18+** - Framework de interfaz de usuario
- **Tailwind CSS** - Framework de estilos
- **shadcn/ui** - Componentes de interfaz
- **Framer Motion** - Animaciones fluidas
- **React Router** - Navegación SPA

### Análisis y Datos
- **pandas** - Manipulación de datos
- **plotly** - Visualizaciones interactivas
- **scipy** - Análisis estadísticos
- **scikit-learn** - Machine learning

### Generación de Documentos
- **Jinja2** - Sistema de plantillas
- **WeasyPrint** - Generación de PDF
- **python-docx** - Documentos Word
- **ReportLab** - PDF avanzados

## 📦 Instalación y Configuración

### Requisitos Previos
- Python 3.11 o superior
- Node.js 18+ y pnpm
- Sistema operativo: Linux/macOS/Windows

### Instalación Rápida

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/dashboard-tesis-pro.git
cd dashboard-tesis-pro
```

2. **Configurar el entorno Python**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Instalar dependencias del frontend**
```bash
cd dashboard_frontend
pnpm install
pnpm run build
cd ..
```

4. **Configurar módulos**
```bash
# Configurar FileBrowser
cd modules/file_explorer
chmod +x start_filebrowser.sh
python3 security_config.py

# Configurar análisis
cd ../data_analysis
chmod +x start_analysis_dashboard.sh

# Configurar generador de informes
cd ../report_generator
chmod +x start_report_generator.sh
cd ../..
```

### Configuración Avanzada

#### Variables de Entorno
Crear un archivo `.env` en la raíz del proyecto:

```env
# Configuración del dashboard principal
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui

# Puertos de los módulos
FILE_EXPLORER_PORT=8058
FILE_EXPLORER_API_PORT=8060
DATA_ANALYSIS_PORT=8050
REPORT_GENERATOR_PORT=8070
MAIN_DASHBOARD_PORT=3000

# Configuración de seguridad
ENABLE_AUTH=False
SESSION_TIMEOUT=3600
MAX_FILE_SIZE=100MB

# Configuración de base de datos (opcional)
DATABASE_URL=sqlite:///dashboard.db
```

#### Configuración de Módulos

**FileBrowser** (`modules/file_explorer/config.json`):
```json
{
  "port": 8058,
  "address": "0.0.0.0",
  "database": "./filebrowser.db",
  "root": "../../shared/data",
  "baseURL": "",
  "log": "stdout",
  "commands": {
    "after_upload": ["python3", "api_connector.py", "file_uploaded"]
  }
}
```

**Análisis de Datos** (`modules/data_analysis/.streamlit/config.toml`):
```toml
[server]
port = 8050
address = "0.0.0.0"
enableCORS = true
enableXsrfProtection = false

[theme]
primaryColor = "#2196F3"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#262730"
```

## 🚀 Uso del Sistema

### Inicio Rápido

1. **Iniciar el dashboard principal**
```bash
cd main_dashboard
source venv/bin/activate
python src/main.py
```

2. **Acceder al sistema**
- Dashboard Principal: http://localhost:3000
- Explorador de Archivos: http://localhost:8058
- Análisis Estadístico: http://localhost:8050
- Generador de Informes: http://localhost:8070

### Flujo de Trabajo Típico

#### 1. Gestión de Archivos
1. Acceder al **Explorador de Archivos** desde el dashboard principal
2. Subir archivos de datos (CSV, Excel, JSON) a la carpeta `01_datos_originales`
3. Organizar archivos según la estructura recomendada
4. Configurar permisos de acceso según el equipo de investigación

#### 2. Análisis de Datos
1. Navegar al **Módulo de Análisis Estadístico**
2. Seleccionar archivos de datos desde el explorador integrado
3. Ejecutar análisis descriptivos e inferenciales
4. Generar visualizaciones interactivas
5. Exportar resultados a la carpeta `03_resultados_analisis`

#### 3. Generación de Informes
1. Acceder al **Generador de Informes**
2. Seleccionar tipo de reporte (ejecutivo, técnico, dashboard)
3. Configurar parámetros y plantillas
4. Generar informes en múltiples formatos
5. Descargar o compartir reportes finales

### Estructura de Carpetas Recomendada

```
shared/data/
├── 01_datos_originales/     # Datos sin procesar
├── 02_datos_procesados/     # Datos limpios y transformados
├── 03_resultados_analisis/  # Outputs de análisis estadísticos
├── 04_visualizaciones/      # Gráficos y plots generados
├── 05_informes/            # Reportes finales
├── 06_codigo/              # Scripts y notebooks
├── 07_documentacion/       # Documentación del proyecto
├── 08_referencias/         # Bibliografía y fuentes
├── 09_anexos/              # Material complementario
└── 10_presentaciones/      # Slides y presentaciones
```

## 🔧 Configuración Avanzada

### Personalización de Temas

El sistema permite personalización completa de temas y colores:

```javascript
// dashboard_frontend/src/contexts/DashboardContext.jsx
const themeConfig = {
  primary_color: '#2196F3',
  secondary_color: '#1976D2',
  accent_color: '#FF9800',
  background_color: '#FFFFFF',
  text_color: '#262730'
}
```

### Integración con APIs Externas

El sistema incluye un conector para APIs externas:

```python
# modules/file_explorer/api_connector.py
class APIConnector:
    def __init__(self):
        self.base_url = "http://localhost:3000/api"
    
    def notify_file_upload(self, filename, path):
        # Notificar al dashboard principal
        pass
    
    def get_analysis_results(self, file_id):
        # Obtener resultados de análisis
        pass
```

### Configuración de Seguridad

Para entornos de producción, habilitar autenticación:

```python
# main_dashboard/src/config/security.py
SECURITY_CONFIG = {
    'enable_auth': True,
    'auth_method': 'local',  # 'local', 'ldap', 'oauth'
    'session_timeout': 3600,
    'max_login_attempts': 5,
    'require_https': True,
    'allowed_origins': ['https://tu-dominio.com']
}
```

## 📊 Monitoreo y Métricas

### Dashboard de Sistema

El dashboard principal incluye métricas en tiempo real:

- **Estado de módulos**: Online/Offline con tiempos de respuesta
- **Uso de recursos**: CPU, memoria, disco y red
- **Estadísticas de uso**: Archivos gestionados, análisis realizados, reportes generados
- **Logs del sistema**: Eventos y errores en tiempo real

### API de Métricas

```bash
# Obtener estado general
curl http://localhost:3000/api/system/health

# Métricas detalladas
curl http://localhost:3000/api/system/metrics

# Estado de módulos
curl http://localhost:3000/api/modules
```

## 🔌 Extensibilidad

### Agregar Nuevos Módulos

1. **Crear estructura del módulo**
```bash
mkdir modules/nuevo_modulo
cd modules/nuevo_modulo
```

2. **Implementar interfaz estándar**
```python
# nuevo_modulo/main.py
class NuevoModulo:
    def __init__(self):
        self.port = 8080
        self.name = "Nuevo Módulo"
    
    def start(self):
        # Lógica de inicio
        pass
    
    def stop(self):
        # Lógica de parada
        pass
    
    def get_status(self):
        # Estado del módulo
        return {"status": "online"}
```

3. **Registrar en el dashboard principal**
```python
# main_dashboard/src/routes/modules.py
MODULES_CONFIG['nuevo_modulo'] = {
    'name': 'Nuevo Módulo',
    'port': 8080,
    'start_script': '../modules/nuevo_modulo/start.sh'
}
```

### Personalizar Análisis

Agregar nuevos tipos de análisis estadísticos:

```python
# modules/data_analysis/custom_analysis.py
def nuevo_analisis(data):
    """
    Implementar nuevo tipo de análisis
    """
    results = {
        'summary': 'Resumen del análisis',
        'plots': [],
        'conclusions': []
    }
    return results
```

## 🐛 Solución de Problemas

### Problemas Comunes

#### Módulo no inicia
```bash
# Verificar logs
tail -f modules/[modulo]/logs/error.log

# Verificar puertos
netstat -tulpn | grep [puerto]

# Reiniciar módulo
curl -X POST http://localhost:3000/api/modules/[modulo]/restart
```

#### Error de permisos
```bash
# Ajustar permisos de archivos
chmod +x modules/*/start_*.sh
chown -R $USER:$USER shared/data/
```

#### Problemas de memoria
```bash
# Verificar uso de memoria
curl http://localhost:3000/api/system/metrics

# Limpiar cache
curl -X POST http://localhost:3000/api/system/clear-cache
```

### Logs del Sistema

Los logs se almacenan en:
- Dashboard principal: `main_dashboard/logs/`
- FileBrowser: `modules/file_explorer/logs/`
- Análisis: `modules/data_analysis/logs/`
- Reportes: `modules/report_generator/logs/`

## 📚 Documentación Adicional

- [Guía de Usuario](docs/user_guide.md) - Manual completo para usuarios finales
- [Guía de Desarrollo](docs/development_guide.md) - Documentación para desarrolladores
- [API Reference](docs/api_reference.md) - Documentación completa de APIs
- [Guía de Despliegue](docs/deployment_guide.md) - Instrucciones para producción

## 🤝 Contribución

### Cómo Contribuir

1. Fork del repositorio
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Estándares de Código

- **Python**: Seguir PEP 8 con black y flake8
- **JavaScript**: Usar ESLint y Prettier
- **Documentación**: Docstrings en español para funciones públicas
- **Tests**: Cobertura mínima del 80%

### Reportar Bugs

Usar el [sistema de issues](https://github.com/tu-usuario/dashboard-tesis-pro/issues) con:
- Descripción detallada del problema
- Pasos para reproducir
- Logs relevantes
- Información del entorno

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Equipo de Desarrollo

- **Manus AI** - Desarrollo principal y arquitectura
- **Equipo Dashboard Tesis Pro** - Diseño y testing

## 🙏 Agradecimientos

- **FileBrowser** - Explorador de archivos base
- **Streamlit** - Framework de análisis interactivo
- **React** y **Tailwind CSS** - Tecnologías de frontend
- **shadcn/ui** - Componentes de interfaz
- **Comunidad Open Source** - Librerías y herramientas utilizadas

## 📞 Soporte

- **Documentación**: [docs.dashboard-tesis-pro.com](https://docs.dashboard-tesis-pro.com)
- **Issues**: [GitHub Issues](https://github.com/tu-usuario/dashboard-tesis-pro/issues)
- **Email**: soporte@dashboard-tesis-pro.com
- **Discord**: [Servidor de la comunidad](https://discord.gg/dashboard-tesis-pro)

---

**Dashboard Tesis Pro 2.0** - Desarrollado con ❤️ para la comunidad académica e investigativa.

![Footer](https://img.shields.io/badge/Made%20with-Python%20%7C%20React%20%7C%20Love-red?style=for-the-badge)

