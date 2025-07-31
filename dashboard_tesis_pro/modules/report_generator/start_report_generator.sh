#!/bin/bash

# Dashboard Tesis Pro - Script de inicio del Módulo Generador de Informes
# Interfaz Streamlit para generación de reportes profesionales

echo "📄 Iniciando Dashboard Tesis Pro - Módulo Generador de Informes..."

# Directorio del módulo
MODULE_DIR="/home/ubuntu/project_manus/dashboard_tesis_pro/modules/report_generator"
cd "$MODULE_DIR"

# Verificar dependencias
echo "🔧 Verificando dependencias..."

# Verificar Python y pip
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado"
    exit 1
fi

# Verificar e instalar dependencias de Python
echo "📦 Verificando paquetes de Python..."
REQUIRED_PACKAGES=("streamlit" "pandas" "numpy" "plotly" "jinja2" "requests")

for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! python3 -c "import $package" &> /dev/null; then
        echo "⚠️  Instalando $package..."
        pip3 install $package
    else
        echo "✅ $package está disponible"
    fi
done

# Verificar dependencias opcionales para diferentes formatos
echo "📋 Verificando dependencias opcionales..."

# WeasyPrint para PDF
if ! python3 -c "import weasyprint" &> /dev/null; then
    echo "⚠️  WeasyPrint no disponible - Generación de PDF limitada"
    echo "💡 Para habilitar PDF: pip3 install weasyprint"
else
    echo "✅ WeasyPrint disponible - Generación de PDF habilitada"
fi

# ReportLab para PDF alternativo
if ! python3 -c "import reportlab" &> /dev/null; then
    echo "⚠️  ReportLab no disponible - PDF alternativo no disponible"
    echo "💡 Para habilitar: pip3 install reportlab"
else
    echo "✅ ReportLab disponible - PDF alternativo habilitado"
fi

# python-docx para Word
if ! python3 -c "import docx" &> /dev/null; then
    echo "⚠️  python-docx no disponible - Generación de Word deshabilitada"
    echo "💡 Para habilitar Word: pip3 install python-docx"
else
    echo "✅ python-docx disponible - Generación de Word habilitada"
fi

# Verificar conexión con otros módulos
echo "🔌 Verificando conexiones con otros módulos..."

# Verificar explorador de archivos
if curl -f http://localhost:8060/api/status &> /dev/null; then
    echo "✅ Explorador de archivos conectado (puerto 8060)"
else
    echo "⚠️  Explorador de archivos no responde en puerto 8060"
    echo "💡 Inicia el explorador de archivos:"
    echo "   cd ../file_explorer && ./start_filebrowser.sh"
fi

# Verificar módulo de análisis
if curl -f http://localhost:8050 &> /dev/null; then
    echo "✅ Módulo de análisis disponible (puerto 8050)"
else
    echo "⚠️  Módulo de análisis no responde en puerto 8050"
    echo "💡 Inicia el módulo de análisis:"
    echo "   cd ../data_analysis && ./start_analysis_dashboard.sh"
fi

# Crear directorios necesarios
echo "📁 Verificando estructura de directorios..."
mkdir -p templates assets exports

# Verificar plantillas
echo "📄 Verificando plantillas..."
if [ ! -f "templates/comprehensive_analysis.html" ]; then
    echo "⚠️  Plantillas no encontradas - Se crearán automáticamente al generar reportes"
else
    echo "✅ Plantillas disponibles"
fi

# Mostrar información del sistema
echo ""
echo "📋 Información del Sistema:"
echo "   🐍 Python: $(python3 --version)"
echo "   📄 Streamlit: $(python3 -c 'import streamlit; print(streamlit.__version__)')"
echo "   📊 Pandas: $(python3 -c 'import pandas; print(pandas.__version__)')"
echo "   🎨 Plotly: $(python3 -c 'import plotly; print(plotly.__version__)')"
echo "   📝 Jinja2: $(python3 -c 'import jinja2; print(jinja2.__version__)')"
echo ""

# Mostrar información de acceso
echo "✅ Módulo Generador de Informes configurado correctamente"
echo ""
echo "🌐 Información de Acceso:"
echo "   📄 Generador de Informes: http://localhost:8070"
echo "   📊 Módulo de Análisis: http://localhost:8050"
echo "   📁 Explorador de Archivos: http://localhost:8058"
echo "   🔌 API de Archivos: http://localhost:8060"
echo ""
echo "🎯 Características Disponibles:"
echo "   ✓ Reportes ejecutivos automáticos"
echo "   ✓ Reportes técnicos detallados"
echo "   ✓ Dashboards interactivos"
echo "   ✓ Múltiples formatos de exportación"
echo "   ✓ Plantillas personalizables"
echo "   ✓ Configuración avanzada de diseño"
echo "   ✓ Integración con módulos de análisis"
echo ""
echo "📊 Formatos de Exportación:"
echo "   • HTML (interactivo y responsive)"
echo "   • PDF (con WeasyPrint o ReportLab)"
echo "   • Word/DOCX (con python-docx)"
echo "   • Markdown (para documentación)"
echo ""
echo "🎨 Tipos de Reporte:"
echo "   • 📊 Ejecutivo: Resumen de alto nivel"
echo "   • 🔬 Técnico: Análisis detallado"
echo "   • 📈 Dashboard: Visualizaciones interactivas"
echo "   • 🎨 Personalizado: Configuración avanzada"
echo ""

# Función para manejar Ctrl+C
cleanup() {
    echo ""
    echo "⏹️  Deteniendo Generador de Informes..."
    exit 0
}

trap cleanup SIGINT

# Iniciar Streamlit
echo "🚀 Iniciando generador de informes en puerto 8070..."
echo "💡 Presiona Ctrl+C para detener el servidor"
echo ""

# Configurar Streamlit para producción
export STREAMLIT_SERVER_PORT=8070
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Iniciar aplicación
streamlit run streamlit_report_interface.py \
    --server.port=8070 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false \
    --theme.primaryColor="#FF9800" \
    --theme.backgroundColor="#FFFFFF" \
    --theme.secondaryBackgroundColor="#FFF3E0" \
    --theme.textColor="#262730"

# Mensaje de cierre
echo ""
echo "⏹️  Generador de Informes detenido"

