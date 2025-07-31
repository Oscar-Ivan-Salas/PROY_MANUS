#!/bin/bash

# Dashboard Tesis Pro - Script de inicio del Explorador de Archivos
# Basado en FileBrowser

echo "🚀 Iniciando Dashboard Tesis Pro - Explorador de Archivos..."

# Directorio del módulo
MODULE_DIR="/home/ubuntu/project_manus/dashboard_tesis_pro/modules/file_explorer"
cd "$MODULE_DIR"

# Verificar si FileBrowser está instalado
if ! command -v filebrowser &> /dev/null; then
    echo "❌ FileBrowser no está instalado. Instalando..."
    curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash
fi

# Crear base de datos si no existe
if [ ! -f "filebrowser.db" ]; then
    echo "🔧 Configurando base de datos inicial..."
    filebrowser config init --config config.json
    filebrowser users add admin admin123 --perm.admin --config config.json
fi

# Configurar usuario administrador
echo "👤 Configurando usuario administrador..."
filebrowser users update admin --perm.admin --config config.json

# Mostrar información de conexión
echo ""
echo "✅ Explorador de Archivos configurado correctamente"
echo "📂 Directorio raíz: /home/ubuntu/project_manus/dashboard_tesis_pro/shared/data"
echo "🌐 URL de acceso: http://localhost:8058"
echo "👤 Usuario: admin"
echo "🔑 Contraseña: admin123"
echo ""
echo "🎨 Personalización:"
echo "   - Tema inspirado en VSCode"
echo "   - Iconos personalizados por tipo de archivo"
echo "   - Estructura de carpetas optimizada para tesis"
echo ""

# Iniciar FileBrowser
echo "🚀 Iniciando servidor en puerto 8058..."
filebrowser --config config.json

# Mensaje de cierre
echo ""
echo "⏹️  Explorador de Archivos detenido"

