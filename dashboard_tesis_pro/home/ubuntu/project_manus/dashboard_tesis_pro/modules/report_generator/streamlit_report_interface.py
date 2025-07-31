#!/usr/bin/env python3
"""
Dashboard Tesis Pro - Interfaz Streamlit para Generador de Informes

Interfaz web completa para:
- Configuración de reportes personalizados
- Vista previa en tiempo real
- Generación en múltiples formatos
- Gestión de plantillas
- Historial de reportes generados
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
import requests
import io
import zipfile
from typing import Dict, List, Any

# Importar el generador de reportes
from report_generator import ProfessionalReportGenerator

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Tesis Pro - Generador de Informes",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #FF9800, #F57C00);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .report-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #FF9800;
        margin-bottom: 1rem;
    }
    
    .template-preview {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .config-section {
        background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
        border: 1px solid #FF9800;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .success-message {
        background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
        border: 1px solid #4CAF50;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .stSelectbox > div > div > select {
        background-color: #fff3e0;
        border-radius: 6px;
    }
    
    .report-metric {
        background: #fff3e0;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

class StreamlitReportInterface:
    def __init__(self):
        self.file_api_url = "http://localhost:8060/api"
        self.report_generator = ProfessionalReportGenerator()
        
        # Inicializar estado de sesión
        if 'report_history' not in st.session_state:
            st.session_state.report_history = []
        
        if 'current_data' not in st.session_state:
            st.session_state.current_data = None
        
        if 'report_config' not in st.session_state:
            st.session_state.report_config = self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Obtener configuración por defecto"""
        return {
            'company_name': 'Dashboard Tesis Pro',
            'author': 'Sistema de Análisis Automático',
            'language': 'es',
            'theme': 'professional',
            'include_visualizations': True,
            'include_statistics': True,
            'include_conclusions': True,
            'include_recommendations': True,
            'color_scheme': {
                'primary': '#2196F3',
                'secondary': '#1976D2',
                'accent': '#FF9800',
                'success': '#4CAF50',
                'warning': '#FF9800',
                'error': '#F44336'
            }
        }
    
    def get_available_files(self):
        """Obtener archivos disponibles desde el explorador"""
        try:
            response = requests.get(f"{self.file_api_url}/files/analyzable", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {"files": [], "count": 0}
        except requests.exceptions.RequestException:
            return {"files": [], "count": 0}
    
    def load_file(self, file_path):
        """Cargar archivo para generar reporte"""
        try:
            # Obtener información del archivo
            file_info_response = requests.get(
                f"{self.file_api_url}/files/info", 
                params={"path": file_path},
                timeout=10
            )
            
            if file_info_response.status_code != 200:
                st.error("❌ No se pudo obtener información del archivo")
                return None
            
            file_info = file_info_response.json()
            full_path = file_info["full_path"]
            extension = file_info["extension"]
            
            # Cargar datos según el tipo de archivo
            if extension == "csv":
                df = pd.read_csv(full_path)
            elif extension in ["xlsx", "xls"]:
                df = pd.read_excel(full_path)
            elif extension == "json":
                with open(full_path, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        df = pd.DataFrame(data)
                    elif isinstance(data, dict):
                        if 'records' in data:
                            df = pd.DataFrame(data['records'])
                        else:
                            df = pd.json_normalize(data)
                    else:
                        st.error("❌ Formato JSON no soportado")
                        return None
            else:
                st.error(f"❌ Formato de archivo no soportado: {extension}")
                return None
            
            return df, file_info["name"]
            
        except Exception as e:
            st.error(f"❌ Error al cargar el archivo: {str(e)}")
            return None
    
    def render_main_interface(self):
        """Renderizar interfaz principal"""
        
        # Header principal
        st.markdown("""
        <div class="main-header">
            <h1>📄 Dashboard Tesis Pro - Generador de Informes Profesionales</h1>
            <p>Crea reportes ejecutivos, técnicos y dashboards interactivos con análisis automático</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar para configuración
        self.render_sidebar()
        
        # Contenido principal con tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Selección de Datos",
            "⚙️ Configuración",
            "📄 Generación de Reportes",
            "👁️ Vista Previa",
            "📚 Historial"
        ])
        
        with tab1:
            self.render_data_selection_tab()
        
        with tab2:
            self.render_configuration_tab()
        
        with tab3:
            self.render_report_generation_tab()
        
        with tab4:
            self.render_preview_tab()
        
        with tab5:
            self.render_history_tab()
    
    def render_sidebar(self):
        """Renderizar sidebar con controles principales"""
        
        st.sidebar.title("🔧 Panel de Control")
        st.sidebar.markdown("---")
        
        # Estado actual
        st.sidebar.subheader("📊 Estado Actual")
        
        if st.session_state.current_data is not None:
            data = st.session_state.current_data
            st.sidebar.success(f"✅ Datos cargados: {st.session_state.get('current_filename', 'archivo')}")
            st.sidebar.info(f"📊 {len(data):,} filas × {len(data.columns)} columnas")
        else:
            st.sidebar.warning("⚠️ No hay datos cargados")
        
        # Acciones rápidas
        st.sidebar.markdown("---")
        st.sidebar.subheader("🚀 Acciones Rápidas")
        
        if st.sidebar.button("📊 Reporte Ejecutivo Rápido", type="primary"):
            if st.session_state.current_data is not None:
                self.generate_quick_executive_report()
            else:
                st.sidebar.error("❌ Carga datos primero")
        
        if st.sidebar.button("🔬 Reporte Técnico Completo"):
            if st.session_state.current_data is not None:
                self.generate_quick_technical_report()
            else:
                st.sidebar.error("❌ Carga datos primero")
        
        if st.sidebar.button("📈 Dashboard Interactivo"):
            if st.session_state.current_data is not None:
                self.generate_quick_dashboard_report()
            else:
                st.sidebar.error("❌ Carga datos primero")
        
        # Configuración rápida
        st.sidebar.markdown("---")
        st.sidebar.subheader("⚙️ Configuración Rápida")
        
        # Tema
        theme = st.sidebar.selectbox(
            "Tema del reporte:",
            ["professional", "modern", "academic", "corporate"],
            format_func=lambda x: {
                "professional": "🏢 Profesional",
                "modern": "✨ Moderno",
                "academic": "🎓 Académico",
                "corporate": "🏛️ Corporativo"
            }[x]
        )
        st.session_state.report_config['theme'] = theme
        
        # Idioma
        language = st.sidebar.selectbox(
            "Idioma:",
            ["es", "en"],
            format_func=lambda x: "🇪🇸 Español" if x == "es" else "🇺🇸 English"
        )
        st.session_state.report_config['language'] = language
        
        # Información del sistema
        st.sidebar.markdown("---")
        st.sidebar.subheader("ℹ️ Información")
        st.sidebar.info(f"📄 Reportes generados: {len(st.session_state.report_history)}")
        
        # Verificar conexión con otros módulos
        try:
            response = requests.get(f"{self.file_api_url}/status", timeout=3)
            if response.status_code == 200:
                st.sidebar.success("✅ Explorador conectado")
            else:
                st.sidebar.error("❌ Explorador desconectado")
        except:
            st.sidebar.error("❌ Sin conexión al explorador")
    
    def render_data_selection_tab(self):
        """Renderizar tab de selección de datos"""
        
        st.subheader("📊 Selección y Carga de Datos")
        
        # Opciones de carga
        data_source = st.radio(
            "Fuente de datos:",
            ["file_explorer", "upload", "analysis_module"],
            format_func=lambda x: {
                "file_explorer": "📁 Explorador de Archivos",
                "upload": "📤 Subir Archivo",
                "analysis_module": "📊 Módulo de Análisis"
            }[x]
        )
        
        if data_source == "file_explorer":
            self.render_file_explorer_selection()
        elif data_source == "upload":
            self.render_file_upload_selection()
        elif data_source == "analysis_module":
            self.render_analysis_module_selection()
        
        # Vista previa de datos cargados
        if st.session_state.current_data is not None:
            st.markdown("---")
            st.subheader("🔍 Vista Previa de Datos")
            
            data = st.session_state.current_data
            
            # Métricas básicas
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Filas", f"{len(data):,}")
            with col2:
                st.metric("📋 Columnas", len(data.columns))
            with col3:
                st.metric("💾 Memoria", f"{data.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
            with col4:
                missing_pct = (data.isnull().sum().sum() / (len(data) * len(data.columns)) * 100)
                st.metric("❓ Faltantes", f"{missing_pct:.1f}%")
            
            # Tabla de vista previa
            st.dataframe(data.head(10), use_container_width=True)
            
            # Información de columnas
            with st.expander("📋 Información Detallada de Columnas"):
                info_data = []
                for col in data.columns:
                    col_data = data[col]
                    info_data.append({
                        'Columna': col,
                        'Tipo': str(col_data.dtype),
                        'No Nulos': col_data.count(),
                        'Únicos': col_data.nunique(),
                        'Ejemplo': str(col_data.dropna().iloc[0]) if len(col_data.dropna()) > 0 else 'N/A'
                    })
                
                info_df = pd.DataFrame(info_data)
                st.dataframe(info_df, use_container_width=True)
    
    def render_file_explorer_selection(self):
        """Renderizar selección desde explorador de archivos"""
        
        available_files = self.get_available_files()
        
        if available_files["count"] > 0:
            file_options = [f"{file['name']} ({file['directory']})" for file in available_files["files"]]
            selected_file_display = st.selectbox(
                "Seleccionar archivo:",
                options=file_options,
                help="Archivos disponibles desde el explorador"
            )
            
            if selected_file_display:
                selected_file_index = file_options.index(selected_file_display)
                selected_file_path = available_files["files"][selected_file_index]["path"]
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button("🔄 Cargar Archivo", type="primary"):
                        with st.spinner("Cargando archivo..."):
                            result = self.load_file(selected_file_path)
                            if result:
                                data, filename = result
                                st.session_state.current_data = data
                                st.session_state.current_filename = filename
                                st.success(f"✅ Archivo cargado: {filename}")
                                st.rerun()
                
                with col2:
                    # Información del archivo seleccionado
                    file_info = available_files["files"][selected_file_index]
                    st.info(f"📁 **Directorio:** {file_info['directory']}")
                    st.info(f"📄 **Extensión:** {file_info['extension']}")
                    st.info(f"💾 **Tamaño:** {file_info.get('size_human', 'N/A')}")
        else:
            st.warning("⚠️ No hay archivos disponibles en el explorador")
            st.info("💡 Sube archivos al explorador de archivos primero")
    
    def render_file_upload_selection(self):
        """Renderizar carga manual de archivos"""
        
        uploaded_file = st.file_uploader(
            "Subir archivo para generar reporte",
            type=['csv', 'xlsx', 'xls', 'json'],
            help="Formatos soportados: CSV, Excel, JSON"
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    data = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                    data = pd.read_excel(uploaded_file)
                elif uploaded_file.name.endswith('.json'):
                    data = pd.read_json(uploaded_file)
                
                st.session_state.current_data = data
                st.session_state.current_filename = uploaded_file.name
                st.success(f"✅ Archivo cargado: {uploaded_file.name}")
                
            except Exception as e:
                st.error(f"❌ Error al cargar archivo: {str(e)}")
    
    def render_analysis_module_selection(self):
        """Renderizar selección desde módulo de análisis"""
        
        st.info("🔗 Integración con el Módulo de Análisis")
        
        # Verificar si hay datos en el módulo de análisis
        if 'analysis_data' in st.session_state:
            st.success("✅ Datos disponibles desde el módulo de análisis")
            
            if st.button("📊 Usar Datos del Análisis", type="primary"):
                st.session_state.current_data = st.session_state.analysis_data
                st.session_state.current_filename = st.session_state.get('analysis_filename', 'datos_analisis')
                st.success("✅ Datos importados desde el módulo de análisis")
                st.rerun()
        else:
            st.warning("⚠️ No hay datos disponibles en el módulo de análisis")
            st.info("💡 Ejecuta análisis en el módulo de análisis estadístico primero")
    
    def render_configuration_tab(self):
        """Renderizar tab de configuración"""
        
        st.subheader("⚙️ Configuración Avanzada de Reportes")
        
        # Configuración general
        with st.expander("🏢 Configuración General", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                company_name = st.text_input(
                    "Nombre de la organización:",
                    value=st.session_state.report_config['company_name']
                )
                st.session_state.report_config['company_name'] = company_name
                
                author = st.text_input(
                    "Autor del reporte:",
                    value=st.session_state.report_config['author']
                )
                st.session_state.report_config['author'] = author
            
            with col2:
                theme = st.selectbox(
                    "Tema visual:",
                    ["professional", "modern", "academic", "corporate"],
                    index=["professional", "modern", "academic", "corporate"].index(
                        st.session_state.report_config['theme']
                    ),
                    format_func=lambda x: {
                        "professional": "🏢 Profesional",
                        "modern": "✨ Moderno", 
                        "academic": "🎓 Académico",
                        "corporate": "🏛️ Corporativo"
                    }[x]
                )
                st.session_state.report_config['theme'] = theme
                
                language = st.selectbox(
                    "Idioma:",
                    ["es", "en"],
                    index=["es", "en"].index(st.session_state.report_config['language']),
                    format_func=lambda x: "🇪🇸 Español" if x == "es" else "🇺🇸 English"
                )
                st.session_state.report_config['language'] = language
        
        # Configuración de contenido
        with st.expander("📋 Contenido del Reporte", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.session_state.report_config['include_statistics'] = st.checkbox(
                    "📊 Incluir estadísticas descriptivas",
                    value=st.session_state.report_config['include_statistics']
                )
                
                st.session_state.report_config['include_visualizations'] = st.checkbox(
                    "📈 Incluir visualizaciones",
                    value=st.session_state.report_config['include_visualizations']
                )
            
            with col2:
                st.session_state.report_config['include_conclusions'] = st.checkbox(
                    "💡 Incluir conclusiones automáticas",
                    value=st.session_state.report_config['include_conclusions']
                )
                
                st.session_state.report_config['include_recommendations'] = st.checkbox(
                    "🎯 Incluir recomendaciones",
                    value=st.session_state.report_config['include_recommendations']
                )
        
        # Configuración de colores
        with st.expander("🎨 Esquema de Colores"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                primary_color = st.color_picker(
                    "Color primario:",
                    value=st.session_state.report_config['color_scheme']['primary']
                )
                st.session_state.report_config['color_scheme']['primary'] = primary_color
                
                secondary_color = st.color_picker(
                    "Color secundario:",
                    value=st.session_state.report_config['color_scheme']['secondary']
                )
                st.session_state.report_config['color_scheme']['secondary'] = secondary_color
            
            with col2:
                accent_color = st.color_picker(
                    "Color de acento:",
                    value=st.session_state.report_config['color_scheme']['accent']
                )
                st.session_state.report_config['color_scheme']['accent'] = accent_color
                
                success_color = st.color_picker(
                    "Color de éxito:",
                    value=st.session_state.report_config['color_scheme']['success']
                )
                st.session_state.report_config['color_scheme']['success'] = success_color
            
            with col3:
                warning_color = st.color_picker(
                    "Color de advertencia:",
                    value=st.session_state.report_config['color_scheme']['warning']
                )
                st.session_state.report_config['color_scheme']['warning'] = warning_color
                
                error_color = st.color_picker(
                    "Color de error:",
                    value=st.session_state.report_config['color_scheme']['error']
                )
                st.session_state.report_config['color_scheme']['error'] = error_color
        
        # Guardar configuración
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("💾 Guardar Configuración", type="primary"):
                # Guardar en archivo JSON
                config_path = os.path.join(self.report_generator.exports_dir, 'report_config.json')
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(st.session_state.report_config, f, indent=2, ensure_ascii=False)
                st.success("✅ Configuración guardada")
        
        with col2:
            if st.button("🔄 Restaurar Defecto"):
                st.session_state.report_config = self.get_default_config()
                st.success("✅ Configuración restaurada")
                st.rerun()
        
        with col3:
            # Cargar configuración desde archivo
            uploaded_config = st.file_uploader(
                "📤 Cargar configuración",
                type=['json'],
                key="config_upload"
            )
            
            if uploaded_config is not None:
                try:
                    config_data = json.load(uploaded_config)
                    st.session_state.report_config = {**self.get_default_config(), **config_data}
                    st.success("✅ Configuración cargada")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error al cargar configuración: {str(e)}")
    
    def render_report_generation_tab(self):
        """Renderizar tab de generación de reportes"""
        
        st.subheader("📄 Generación de Reportes Profesionales")
        
        if st.session_state.current_data is None:
            st.warning("⚠️ Carga datos primero en la pestaña 'Selección de Datos'")
            return
        
        # Tipos de reporte disponibles
        st.markdown("### 📋 Tipos de Reporte Disponibles")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="report-card">
                <h4>📊 Reporte Ejecutivo</h4>
                <p>Resumen de alto nivel con métricas clave, hallazgos principales y recomendaciones estratégicas.</p>
                <ul>
                    <li>Resumen de datos</li>
                    <li>Métricas clave</li>
                    <li>Hallazgos principales</li>
                    <li>Recomendaciones</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📊 Generar Ejecutivo", type="primary", key="exec_btn"):
                self.generate_executive_report()
        
        with col2:
            st.markdown("""
            <div class="report-card">
                <h4>🔬 Reporte Técnico</h4>
                <p>Análisis detallado con estadísticas completas, metodología y resultados técnicos.</p>
                <ul>
                    <li>Metodología detallada</li>
                    <li>Estadísticas completas</li>
                    <li>Pruebas estadísticas</li>
                    <li>Detalles técnicos</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔬 Generar Técnico", type="primary", key="tech_btn"):
                self.generate_technical_report()
        
        with col3:
            st.markdown("""
            <div class="report-card">
                <h4>📈 Dashboard Interactivo</h4>
                <p>Reporte visual con gráficos interactivos, métricas en tiempo real y navegación intuitiva.</p>
                <ul>
                    <li>Visualizaciones interactivas</li>
                    <li>Métricas dinámicas</li>
                    <li>Navegación intuitiva</li>
                    <li>Responsive design</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📈 Generar Dashboard", type="primary", key="dash_btn"):
                self.generate_dashboard_report()
        
        # Configuración de formato de salida
        st.markdown("---")
        st.markdown("### 📤 Configuración de Exportación")
        
        col1, col2 = st.columns(2)
        
        with col1:
            output_formats = st.multiselect(
                "Formatos de salida:",
                ["html", "pdf", "docx", "markdown"],
                default=["html"],
                format_func=lambda x: {
                    "html": "🌐 HTML",
                    "pdf": "📄 PDF",
                    "docx": "📝 Word",
                    "markdown": "📋 Markdown"
                }[x]
            )
        
        with col2:
            # Opciones adicionales
            include_raw_data = st.checkbox("📊 Incluir datos originales", value=False)
            compress_output = st.checkbox("🗜️ Comprimir en ZIP", value=False)
        
        # Generación personalizada
        st.markdown("---")
        st.markdown("### 🎨 Generación Personalizada")
        
        with st.expander("⚙️ Configuración Avanzada"):
            custom_title = st.text_input("Título personalizado:", value="")
            custom_subtitle = st.text_input("Subtítulo:", value="")
            
            # Secciones personalizadas
            st.markdown("**Secciones a incluir:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                include_summary = st.checkbox("📋 Resumen ejecutivo", value=True)
                include_data_overview = st.checkbox("📊 Vista general de datos", value=True)
                include_statistics = st.checkbox("📈 Estadísticas descriptivas", value=True)
            
            with col2:
                include_visualizations = st.checkbox("📊 Visualizaciones", value=True)
                include_correlations = st.checkbox("🔗 Análisis de correlación", value=True)
                include_outliers = st.checkbox("⚠️ Detección de outliers", value=True)
            
            with col3:
                include_conclusions = st.checkbox("💡 Conclusiones", value=True)
                include_recommendations = st.checkbox("🎯 Recomendaciones", value=True)
                include_methodology = st.checkbox("🔬 Metodología", value=False)
        
        # Botón de generación personalizada
        if st.button("🎨 Generar Reporte Personalizado", type="primary"):
            self.generate_custom_report(
                output_formats=output_formats,
                custom_title=custom_title,
                custom_subtitle=custom_subtitle,
                sections={
                    'summary': include_summary,
                    'data_overview': include_data_overview,
                    'statistics': include_statistics,
                    'visualizations': include_visualizations,
                    'correlations': include_correlations,
                    'outliers': include_outliers,
                    'conclusions': include_conclusions,
                    'recommendations': include_recommendations,
                    'methodology': include_methodology
                },
                include_raw_data=include_raw_data,
                compress_output=compress_output
            )
    
    def render_preview_tab(self):
        """Renderizar tab de vista previa"""
        
        st.subheader("👁️ Vista Previa de Reportes")
        
        if st.session_state.current_data is None:
            st.warning("⚠️ Carga datos primero para generar vista previa")
            return
        
        # Selector de tipo de vista previa
        preview_type = st.selectbox(
            "Tipo de vista previa:",
            ["executive", "technical", "dashboard"],
            format_func=lambda x: {
                "executive": "📊 Reporte Ejecutivo",
                "technical": "🔬 Reporte Técnico",
                "dashboard": "📈 Dashboard Interactivo"
            }[x]
        )
        
        if st.button("👁️ Generar Vista Previa", type="primary"):
            with st.spinner("Generando vista previa..."):
                preview_content = self.generate_preview(preview_type)
                
                if preview_content:
                    st.markdown("### 📄 Vista Previa del Reporte")
                    
                    # Mostrar vista previa en HTML
                    st.components.v1.html(preview_content, height=600, scrolling=True)
                    
                    # Opciones de descarga
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.download_button(
                            label="⬇️ Descargar HTML",
                            data=preview_content,
                            file_name=f"vista_previa_{preview_type}_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                            mime="text/html"
                        )
                    
                    with col2:
                        if st.button("📄 Generar PDF"):
                            st.info("🚧 Generación de PDF desde vista previa en desarrollo")
                    
                    with col3:
                        if st.button("📝 Generar Word"):
                            st.info("🚧 Generación de Word desde vista previa en desarrollo")
    
    def render_history_tab(self):
        """Renderizar tab de historial"""
        
        st.subheader("📚 Historial de Reportes Generados")
        
        if not st.session_state.report_history:
            st.info("📝 No hay reportes en el historial")
            return
        
        # Estadísticas del historial
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📄 Total Reportes", len(st.session_state.report_history))
        
        with col2:
            formats = [report.get('format', 'unknown') for report in st.session_state.report_history]
            most_common_format = max(set(formats), key=formats.count) if formats else 'N/A'
            st.metric("📊 Formato Más Usado", most_common_format.upper())
        
        with col3:
            types = [report.get('type', 'unknown') for report in st.session_state.report_history]
            most_common_type = max(set(types), key=types.count) if types else 'N/A'
            st.metric("📋 Tipo Más Usado", most_common_type.title())
        
        with col4:
            if st.button("🗑️ Limpiar Historial"):
                st.session_state.report_history = []
                st.success("✅ Historial limpiado")
                st.rerun()
        
        # Lista de reportes
        st.markdown("### 📋 Reportes Generados")
        
        for i, report in enumerate(reversed(st.session_state.report_history)):
            with st.expander(f"📄 {report.get('title', f'Reporte #{len(st.session_state.report_history)-i}')}"):
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Tipo:** {report.get('type', 'N/A').title()}")
                    st.markdown(f"**Formato:** {report.get('format', 'N/A').upper()}")
                    st.markdown(f"**Archivo:** {report.get('filename', 'N/A')}")
                
                with col2:
                    st.markdown(f"**Generado:** {report.get('timestamp', 'N/A')}")
                    st.markdown(f"**Tamaño:** {report.get('size_human', 'N/A')}")
                    st.markdown(f"**Estado:** {'✅ Exitoso' if report.get('success', False) else '❌ Error'}")
                
                # Botones de acción
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if report.get('filepath') and os.path.exists(report['filepath']):
                        with open(report['filepath'], 'rb') as f:
                            st.download_button(
                                label="⬇️ Descargar",
                                data=f.read(),
                                file_name=report.get('filename', 'reporte'),
                                mime=self.get_mime_type(report.get('format', 'html')),
                                key=f"download_{i}"
                            )
                    else:
                        st.button("❌ No disponible", disabled=True, key=f"unavailable_{i}")
                
                with col2:
                    if st.button("🔄 Regenerar", key=f"regenerate_{i}"):
                        st.info("🚧 Funcionalidad de regeneración en desarrollo")
                
                with col3:
                    if st.button("🗑️ Eliminar", key=f"delete_{i}"):
                        # Eliminar del historial
                        actual_index = len(st.session_state.report_history) - 1 - i
                        del st.session_state.report_history[actual_index]
                        
                        # Eliminar archivo si existe
                        if report.get('filepath') and os.path.exists(report['filepath']):
                            try:
                                os.remove(report['filepath'])
                            except:
                                pass
                        
                        st.success("✅ Reporte eliminado")
                        st.rerun()
    
    # Métodos de generación de reportes
    def generate_quick_executive_report(self):
        """Generar reporte ejecutivo rápido"""
        if st.session_state.current_data is None:
            return
        
        with st.spinner("Generando reporte ejecutivo..."):
            data = st.session_state.current_data
            
            # Generar hallazgos y recomendaciones básicos
            key_findings = self.generate_basic_findings(data)
            recommendations = self.generate_basic_recommendations(data)
            
            result = self.report_generator.generate_executive_summary(
                data=data,
                key_findings=key_findings,
                recommendations=recommendations,
                config=st.session_state.report_config
            )
            
            if result['success']:
                self.add_to_history(result, 'executive', 'Reporte Ejecutivo Rápido')
                st.success(f"✅ Reporte ejecutivo generado: {result['filename']}")
                
                # Botón de descarga
                with open(result['filepath'], 'rb') as f:
                    st.download_button(
                        label="⬇️ Descargar Reporte Ejecutivo",
                        data=f.read(),
                        file_name=result['filename'],
                        mime="text/html"
                    )
            else:
                st.error(f"❌ Error al generar reporte: {result['error']}")
    
    def generate_quick_technical_report(self):
        """Generar reporte técnico rápido"""
        if st.session_state.current_data is None:
            return
        
        with st.spinner("Generando reporte técnico..."):
            data = st.session_state.current_data
            
            # Preparar datos para reporte técnico
            statistical_tests = self.prepare_statistical_tests(data)
            visualizations = self.prepare_visualizations_data(data)
            methodology = self.generate_methodology_description(data)
            
            result = self.report_generator.generate_technical_report(
                data=data,
                statistical_tests=statistical_tests,
                visualizations=visualizations,
                methodology=methodology,
                config=st.session_state.report_config
            )
            
            if result['success']:
                self.add_to_history(result, 'technical', 'Reporte Técnico Completo')
                st.success(f"✅ Reporte técnico generado: {result['filename']}")
                
                # Botón de descarga
                with open(result['filepath'], 'rb') as f:
                    st.download_button(
                        label="⬇️ Descargar Reporte Técnico",
                        data=f.read(),
                        file_name=result['filename'],
                        mime="text/html"
                    )
            else:
                st.error(f"❌ Error al generar reporte: {result['error']}")
    
    def generate_quick_dashboard_report(self):
        """Generar dashboard interactivo rápido"""
        if st.session_state.current_data is None:
            return
        
        with st.spinner("Generando dashboard interactivo..."):
            data = st.session_state.current_data
            
            # Preparar datos para dashboard
            charts = self.prepare_dashboard_charts(data)
            metrics = self.prepare_dashboard_metrics(data)
            
            result = self.report_generator.generate_dashboard_report(
                data=data,
                charts=charts,
                metrics=metrics,
                config=st.session_state.report_config
            )
            
            if result['success']:
                self.add_to_history(result, 'dashboard', 'Dashboard Interactivo')
                st.success(f"✅ Dashboard generado: {result['filename']}")
                
                # Botón de descarga
                with open(result['filepath'], 'rb') as f:
                    st.download_button(
                        label="⬇️ Descargar Dashboard",
                        data=f.read(),
                        file_name=result['filename'],
                        mime="text/html"
                    )
            else:
                st.error(f"❌ Error al generar dashboard: {result['error']}")
    
    # Métodos auxiliares
    def generate_basic_findings(self, data: pd.DataFrame) -> List[str]:
        """Generar hallazgos básicos automáticamente"""
        findings = []
        
        # Hallazgo sobre tamaño del dataset
        findings.append(f"El dataset contiene {len(data):,} registros y {len(data.columns)} variables, proporcionando una base sólida para el análisis.")
        
        # Hallazgo sobre calidad de datos
        missing_pct = (data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100
        if missing_pct < 5:
            findings.append("La calidad de los datos es excelente con menos del 5% de valores faltantes.")
        else:
            findings.append(f"Se identificaron {missing_pct:.1f}% de valores faltantes que requieren atención.")
        
        # Hallazgo sobre tipos de variables
        numeric_cols = len(data.select_dtypes(include=[np.number]).columns)
        categorical_cols = len(data.select_dtypes(include=['object', 'category']).columns)
        
        if numeric_cols > categorical_cols:
            findings.append("El dataset es predominantemente numérico, ideal para análisis estadísticos avanzados.")
        else:
            findings.append("El dataset contiene principalmente variables categóricas, apropiado para análisis de frecuencias.")
        
        return findings
    
    def generate_basic_recommendations(self, data: pd.DataFrame) -> List[str]:
        """Generar recomendaciones básicas automáticamente"""
        recommendations = []
        
        # Recomendación sobre valores faltantes
        missing_cols = data.columns[data.isnull().any()].tolist()
        if missing_cols:
            recommendations.append(f"Implementar estrategias de imputación para las columnas con valores faltantes: {', '.join(missing_cols[:3])}")
        
        # Recomendación sobre análisis adicionales
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            recommendations.append("Realizar análisis de correlación entre variables numéricas para identificar relaciones significativas.")
        
        # Recomendación sobre visualizaciones
        recommendations.append("Crear visualizaciones interactivas para facilitar la exploración de patrones en los datos.")
        
        return recommendations
    
    def add_to_history(self, result: Dict[str, Any], report_type: str, title: str):
        """Agregar reporte al historial"""
        history_entry = {
            'title': title,
            'type': report_type,
            'format': result['format'],
            'filename': result['filename'],
            'filepath': result['filepath'],
            'success': result['success'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'size_bytes': result.get('size_bytes', 0),
            'size_human': self.format_file_size(result.get('size_bytes', 0))
        }
        
        st.session_state.report_history.append(history_entry)
    
    def format_file_size(self, size_bytes: int) -> str:
        """Formatear tamaño de archivo"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"
    
    def get_mime_type(self, format_type: str) -> str:
        """Obtener tipo MIME según el formato"""
        mime_types = {
            'html': 'text/html',
            'pdf': 'application/pdf',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'markdown': 'text/markdown',
            'json': 'application/json'
        }
        return mime_types.get(format_type, 'application/octet-stream')
    
    # Métodos de preparación de datos (stubs para implementación completa)
    def prepare_statistical_tests(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Preparar datos de pruebas estadísticas"""
        return {
            'descriptive_stats': 'Estadísticas descriptivas calculadas',
            'normality_tests': 'Pruebas de normalidad realizadas',
            'correlation_analysis': 'Análisis de correlación completado'
        }
    
    def prepare_visualizations_data(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Preparar datos de visualizaciones"""
        return [
            {'title': 'Distribución de Variables', 'type': 'histogram'},
            {'title': 'Matriz de Correlación', 'type': 'heatmap'},
            {'title': 'Análisis de Outliers', 'type': 'boxplot'}
        ]
    
    def generate_methodology_description(self, data: pd.DataFrame) -> str:
        """Generar descripción de metodología"""
        return """
        Metodología de Análisis:
        1. Carga y validación de datos
        2. Análisis exploratorio de datos (EDA)
        3. Estadísticas descriptivas
        4. Detección de valores atípicos
        5. Análisis de correlaciones
        6. Generación de conclusiones
        """
    
    def prepare_dashboard_charts(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Preparar gráficos para dashboard"""
        return [
            {'title': 'Métricas Principales', 'type': 'metrics'},
            {'title': 'Distribuciones', 'type': 'histograms'},
            {'title': 'Correlaciones', 'type': 'heatmap'}
        ]
    
    def prepare_dashboard_metrics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Preparar métricas para dashboard"""
        return {
            'total_records': len(data),
            'total_columns': len(data.columns),
            'missing_percentage': (data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100,
            'numeric_columns': len(data.select_dtypes(include=[np.number]).columns)
        }
    
    def generate_preview(self, preview_type: str) -> str:
        """Generar vista previa del reporte"""
        data = st.session_state.current_data
        
        if preview_type == "executive":
            key_findings = self.generate_basic_findings(data)
            recommendations = self.generate_basic_recommendations(data)
            
            result = self.report_generator.generate_executive_summary(
                data=data,
                key_findings=key_findings,
                recommendations=recommendations,
                config=st.session_state.report_config
            )
            
            return result.get('content', '') if result['success'] else None
        
        # Implementar otros tipos de vista previa
        return "<p>Vista previa no disponible para este tipo de reporte</p>"
    
    def generate_executive_report(self):
        """Generar reporte ejecutivo completo"""
        self.generate_quick_executive_report()
    
    def generate_technical_report(self):
        """Generar reporte técnico completo"""
        self.generate_quick_technical_report()
    
    def generate_dashboard_report(self):
        """Generar dashboard completo"""
        self.generate_quick_dashboard_report()
    
    def generate_custom_report(self, **kwargs):
        """Generar reporte personalizado"""
        st.info("🚧 Generación de reportes personalizados en desarrollo")

# Función principal
def main():
    """Función principal de la aplicación"""
    interface = StreamlitReportInterface()
    interface.render_main_interface()

if __name__ == "__main__":
    main()

