#!/bin/bash

# Dashboard Tesis Pro - Script de inicio del Módulo de Análisis Estadístico
# Panel central en Streamlit

echo "📊 Iniciando Dashboard Tesis Pro - Módulo de Análisis Estadístico..."

# Directorio del módulo
MODULE_DIR="/home/ubuntu/project_manus/dashboard_tesis_pro/modules/data_analysis"
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
REQUIRED_PACKAGES=("streamlit" "pandas" "numpy" "plotly" "scipy" "scikit-learn" "statsmodels" "requests")

for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! python3 -c "import $package" &> /dev/null; then
        echo "⚠️  Instalando $package..."
        pip3 install $package
    else
        echo "✅ $package está disponible"
    fi
done

# Verificar conexión con el explorador de archivos
echo "🔌 Verificando conexión con explorador de archivos..."
if curl -f http://localhost:8060/api/status &> /dev/null; then
    echo "✅ Explorador de archivos conectado (puerto 8060)"
else
    echo "⚠️  Explorador de archivos no responde en puerto 8060"
    echo "💡 Inicia el explorador de archivos primero:"
    echo "   cd ../file_explorer && ./start_filebrowser.sh"
fi

# Verificar datos de ejemplo
echo "📊 Verificando datos de ejemplo..."
DATA_DIR="../../shared/data/01_datos_originales"
if [ -d "$DATA_DIR" ] && [ "$(ls -A $DATA_DIR)" ]; then
    echo "✅ Datos de ejemplo disponibles"
    echo "📁 Archivos encontrados:"
    ls -la "$DATA_DIR"/*.csv "$DATA_DIR"/*.xlsx "$DATA_DIR"/*.json 2>/dev/null | awk '{print "   " $9 " (" $5 " bytes)"}'
else
    echo "⚠️  No se encontraron datos de ejemplo"
    echo "🔄 Generando datos de ejemplo..."
    python3 generate_sample_data.py
fi

# Mostrar información del sistema
echo ""
echo "📋 Información del Sistema:"
echo "   🐍 Python: $(python3 --version)"
echo "   📊 Streamlit: $(python3 -c 'import streamlit; print(streamlit.__version__)')"
echo "   📈 Pandas: $(python3 -c 'import pandas; print(pandas.__version__)')"
echo "   🎨 Plotly: $(python3 -c 'import plotly; print(plotly.__version__)')"
echo ""

# Mostrar información de acceso
echo "✅ Módulo de Análisis Estadístico configurado correctamente"
echo ""
echo "🌐 Información de Acceso:"
echo "   📊 Dashboard Principal: http://localhost:8050"
echo "   📁 Explorador de Archivos: http://localhost:8058"
echo "   🔌 API de Archivos: http://localhost:8060"
echo ""
echo "🎯 Características Disponibles:"
echo "   ✓ Carga de archivos desde explorador"
echo "   ✓ Análisis estadístico descriptivo"
echo "   ✓ Visualizaciones interactivas con Plotly"
echo "   ✓ Validación automática de datos"
echo "   ✓ Exportación a Excel y CSV"
echo "   ✓ Interfaz responsive y profesional"
echo ""
echo "📊 Datasets de Ejemplo Disponibles:"
echo "   • encuesta_estudiantes.csv (500 registros)"
echo "   • ventas_empresa.csv (1,000 registros)"
echo "   • experimento_tratamiento.csv (200 registros)"
echo "   • datos_problematicos.csv (300 registros)"
echo "   • datos_ejemplo.json (50 registros)"
echo ""

# Función para manejar Ctrl+C
cleanup() {
    echo ""
    echo "⏹️  Deteniendo Dashboard de Análisis Estadístico..."
    exit 0
}

trap cleanup SIGINT

# Iniciar Streamlit
echo "🚀 Iniciando dashboard en puerto 8050..."
echo "💡 Presiona Ctrl+C para detener el servidor"
echo ""

# Configurar Streamlit para producción
export STREAMLIT_SERVER_PORT=8050
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Iniciar aplicación
streamlit run main_dashboard.py \
    --server.port=8050 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false \
    --theme.primaryColor="#2196F3" \
    --theme.backgroundColor="#FFFFFF" \
    --theme.secondaryBackgroundColor="#F0F2F6" \
    --theme.textColor="#262730"

# Mensaje de cierre
echo ""
echo "⏹️  Dashboard de Análisis Estadístico detenido"

