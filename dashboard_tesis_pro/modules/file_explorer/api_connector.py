#!/usr/bin/env python3
"""
Dashboard Tesis Pro - Conector API
Módulo de Explorador de Archivos

Este módulo proporciona la API para comunicación entre el explorador
de archivos y el módulo de análisis de datos.
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import json
import mimetypes
from datetime import datetime
import sqlite3
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Permitir CORS para integración con otros módulos

# Configuración
DATA_ROOT = "/home/ubuntu/project_manus/dashboard_tesis_pro/shared/data"
DB_PATH = "/home/ubuntu/project_manus/dashboard_tesis_pro/modules/file_explorer/filebrowser.db"

class FileExplorerAPI:
    def __init__(self, data_root=DATA_ROOT):
        self.data_root = data_root
        self.supported_formats = {
            'csv': 'text/csv',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'xls': 'application/vnd.ms-excel',
            'json': 'application/json',
            'txt': 'text/plain',
            'parquet': 'application/octet-stream'
        }
    
    def get_file_list(self, path="", file_types=None):
        """Obtener lista de archivos en un directorio"""
        try:
            full_path = os.path.join(self.data_root, path.lstrip('/'))
            
            if not os.path.exists(full_path):
                return {"error": "Directorio no encontrado"}, 404
            
            files = []
            directories = []
            
            for item in os.listdir(full_path):
                item_path = os.path.join(full_path, item)
                relative_path = os.path.join(path, item).replace('\\', '/')
                
                if os.path.isdir(item_path):
                    directories.append({
                        "name": item,
                        "type": "directory",
                        "path": relative_path,
                        "size": self.get_directory_size(item_path),
                        "modified": datetime.fromtimestamp(os.path.getmtime(item_path)).isoformat(),
                        "files_count": len([f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))])
                    })
                else:
                    file_ext = os.path.splitext(item)[1].lower().lstrip('.')
                    file_info = {
                        "name": item,
                        "type": "file",
                        "extension": file_ext,
                        "path": relative_path,
                        "size": os.path.getsize(item_path),
                        "size_human": self.human_readable_size(os.path.getsize(item_path)),
                        "modified": datetime.fromtimestamp(os.path.getmtime(item_path)).isoformat(),
                        "mime_type": mimetypes.guess_type(item_path)[0],
                        "analyzable": file_ext in self.supported_formats
                    }
                    
                    # Filtrar por tipos de archivo si se especifica
                    if file_types is None or file_ext in file_types:
                        files.append(file_info)
            
            return {
                "current_path": path,
                "directories": sorted(directories, key=lambda x: x['name']),
                "files": sorted(files, key=lambda x: x['name']),
                "total_files": len(files),
                "total_directories": len(directories)
            }
            
        except Exception as e:
            return {"error": str(e)}, 500
    
    def get_analyzable_files(self):
        """Obtener solo archivos que pueden ser analizados"""
        analyzable_files = []
        
        def scan_directory(directory, relative_path=""):
            try:
                for item in os.listdir(directory):
                    item_path = os.path.join(directory, item)
                    item_relative = os.path.join(relative_path, item).replace('\\', '/')
                    
                    if os.path.isdir(item_path):
                        scan_directory(item_path, item_relative)
                    else:
                        file_ext = os.path.splitext(item)[1].lower().lstrip('.')
                        if file_ext in self.supported_formats:
                            analyzable_files.append({
                                "name": item,
                                "path": item_relative,
                                "extension": file_ext,
                                "size": os.path.getsize(item_path),
                                "size_human": self.human_readable_size(os.path.getsize(item_path)),
                                "modified": datetime.fromtimestamp(os.path.getmtime(item_path)).isoformat(),
                                "directory": os.path.dirname(item_relative) or "/"
                            })
            except PermissionError:
                pass
        
        scan_directory(self.data_root)
        return sorted(analyzable_files, key=lambda x: x['modified'], reverse=True)
    
    def get_file_info(self, file_path):
        """Obtener información detallada de un archivo"""
        try:
            full_path = os.path.join(self.data_root, file_path.lstrip('/'))
            
            if not os.path.exists(full_path) or not os.path.isfile(full_path):
                return {"error": "Archivo no encontrado"}, 404
            
            stat = os.stat(full_path)
            file_ext = os.path.splitext(file_path)[1].lower().lstrip('.')
            
            info = {
                "name": os.path.basename(file_path),
                "path": file_path,
                "extension": file_ext,
                "size": stat.st_size,
                "size_human": self.human_readable_size(stat.st_size),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
                "mime_type": mimetypes.guess_type(full_path)[0],
                "analyzable": file_ext in self.supported_formats,
                "full_path": full_path
            }
            
            # Información adicional para archivos analizables
            if file_ext in self.supported_formats:
                info["analysis_info"] = self.get_analysis_preview(full_path, file_ext)
            
            return info
            
        except Exception as e:
            return {"error": str(e)}, 500
    
    def get_analysis_preview(self, file_path, file_ext):
        """Obtener preview básico para análisis"""
        try:
            if file_ext == 'csv':
                import pandas as pd
                df = pd.read_csv(file_path, nrows=5)
                return {
                    "rows_sample": len(df),
                    "columns": list(df.columns),
                    "column_count": len(df.columns),
                    "data_types": df.dtypes.to_dict(),
                    "preview": df.head().to_dict('records')
                }
            elif file_ext in ['xlsx', 'xls']:
                import pandas as pd
                df = pd.read_excel(file_path, nrows=5)
                return {
                    "rows_sample": len(df),
                    "columns": list(df.columns),
                    "column_count": len(df.columns),
                    "data_types": df.dtypes.to_dict(),
                    "preview": df.head().to_dict('records')
                }
            elif file_ext == 'json':
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return {
                            "type": "array",
                            "length": len(data),
                            "sample": data[:3] if data else []
                        }
                    elif isinstance(data, dict):
                        return {
                            "type": "object",
                            "keys": list(data.keys())[:10],
                            "sample": {k: v for k, v in list(data.items())[:3]}
                        }
            
            return {"preview_available": False}
            
        except Exception as e:
            return {"preview_error": str(e)}
    
    def human_readable_size(self, size_bytes):
        """Convertir bytes a formato legible"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
    
    def get_directory_size(self, directory):
        """Calcular tamaño de directorio"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
        except (OSError, PermissionError):
            pass
        return total_size

# Instancia de la API
file_api = FileExplorerAPI()

# Rutas de la API
@app.route('/api/files', methods=['GET'])
def list_files():
    """Listar archivos en un directorio"""
    path = request.args.get('path', '')
    file_types = request.args.get('types', '').split(',') if request.args.get('types') else None
    
    result = file_api.get_file_list(path, file_types)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)

@app.route('/api/files/analyzable', methods=['GET'])
def list_analyzable_files():
    """Listar solo archivos analizables"""
    files = file_api.get_analyzable_files()
    return jsonify({
        "files": files,
        "count": len(files),
        "supported_formats": list(file_api.supported_formats.keys())
    })

@app.route('/api/files/info', methods=['GET'])
def file_info():
    """Obtener información de un archivo específico"""
    file_path = request.args.get('path')
    if not file_path:
        return jsonify({"error": "Parámetro 'path' requerido"}), 400
    
    result = file_api.get_file_info(file_path)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)

@app.route('/api/files/download', methods=['GET'])
def download_file():
    """Descargar un archivo"""
    file_path = request.args.get('path')
    if not file_path:
        return jsonify({"error": "Parámetro 'path' requerido"}), 400
    
    full_path = os.path.join(DATA_ROOT, file_path.lstrip('/'))
    
    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        return jsonify({"error": "Archivo no encontrado"}), 404
    
    return send_file(full_path, as_attachment=True)

@app.route('/api/status', methods=['GET'])
def api_status():
    """Estado de la API"""
    return jsonify({
        "status": "active",
        "version": "1.0.0",
        "data_root": DATA_ROOT,
        "supported_formats": list(file_api.supported_formats.keys()),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Estadísticas del explorador"""
    try:
        total_files = 0
        total_size = 0
        file_types = {}
        
        for root, dirs, files in os.walk(DATA_ROOT):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.exists(file_path):
                    total_files += 1
                    size = os.path.getsize(file_path)
                    total_size += size
                    
                    ext = os.path.splitext(file)[1].lower().lstrip('.')
                    if ext:
                        file_types[ext] = file_types.get(ext, 0) + 1
        
        return jsonify({
            "total_files": total_files,
            "total_size": total_size,
            "total_size_human": file_api.human_readable_size(total_size),
            "file_types": file_types,
            "analyzable_count": sum(file_types.get(fmt, 0) for fmt in file_api.supported_formats.keys())
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Iniciando API del Explorador de Archivos...")
    print(f"📂 Directorio raíz: {DATA_ROOT}")
    print("🌐 API disponible en: http://localhost:8060")
    print("\n📋 Endpoints disponibles:")
    print("   GET /api/files - Listar archivos")
    print("   GET /api/files/analyzable - Archivos analizables")
    print("   GET /api/files/info - Información de archivo")
    print("   GET /api/files/download - Descargar archivo")
    print("   GET /api/status - Estado de la API")
    print("   GET /api/stats - Estadísticas")
    
    app.run(host='0.0.0.0', port=8060, debug=True)

