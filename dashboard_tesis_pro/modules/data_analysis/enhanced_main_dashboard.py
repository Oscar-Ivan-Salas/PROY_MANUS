#!/usr/bin/env python3
"""
Dashboard Tesis Pro - Módulo de Análisis Estadístico Interactivo (Versión Completa)
Panel Central en Streamlit con Análisis Avanzados

Este módulo proporciona la interfaz completa para el análisis de datos:
- Carga de archivos desde el explorador
- Análisis estadístico descriptivo e inferencial
- Visualizaciones interactivas avanzadas
- Clustering automático
- Historial de análisis
- Exportación de resultados
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_advanced_visualization(df, viz_type, columns, color_palette, plot_theme):
    """Crear visualizaciones avanzadas"""
    try:
        fig = None
        
        if viz_type == "histogram" and len(columns) >= 1:
            fig = px.histogram(df, x=columns[0], title=f"Histograma de {columns[0]}")
            
        elif viz_type == "scatter" and len(columns) >= 2:
            color_col = columns[2] if len(columns) > 2 else None
            fig = px.scatter(df, x=columns[0], y=columns[1], color=color_col,
                           title=f"Gráfico de Dispersión: {columns[0]} vs {columns[1]}")
            
        elif viz_type == "3d_scatter" and len(columns) >= 3:
            color_col = columns[3] if len(columns) > 3 else None
            fig = px.scatter_3d(df, x=columns[0], y=columns[1], z=columns[2], color=color_col,
                              title=f"Dispersión 3D: {columns[0]}, {columns[1]}, {columns[2]}")
            
        elif viz_type == "parallel_coordinates":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) >= 3:
                fig = px.parallel_coordinates(df, dimensions=numeric_cols[:5],
                                            title="Coordenadas Paralelas")
        
        # Aplicar configuraciones de estilo
        if fig:
            fig.update_layout(
                template=plot_theme,
                font=dict(size=12),
                title_font_size=16,
                showlegend=True
            )
            
            # Aplicar paleta de colores si es aplicable
            if color_palette != "plotly":
                fig.update_traces(marker_colorscale=color_palette)
        
        return fig
        
    except Exception as e:
        st.error(f"❌ Error al crear visualización: {str(e)}")
        return None
import requests
import json
import os
from datetime import datetime
import io
import base64
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

# Importar módulos locales
from data_validation import DataValidator
from advanced_analysis_tab import render_advanced_analysis_tab

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Tesis Pro - Análisis Estadístico",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado mejorado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2196F3, #1976D2);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #2196F3;
        margin-bottom: 1rem;
    }
    
    .success-box {
        background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
        border: 1px solid #4CAF50;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
        border: 1px solid #FF9800;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .error-box {
        background: linear-gradient(135deg, #FFEBEE, #FFCDD2);
        border: 1px solid #F44336;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
        border: 1px solid #2196F3;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .stSelectbox > div > div > select {
        background-color: #f8f9fa;
        border-radius: 6px;
    }
    
    .stButton > button {
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa, #ffffff);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
    }
    
    .validation-summary {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #2196F3;
    }
</style>
""", unsafe_allow_html=True)

class EnhancedDataAnalysisModule:
    def __init__(self):
        self.file_api_url = "http://localhost:8060/api"
        self.data = None
        self.analysis_history = []
        self.validator = DataValidator()
        
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
        """Cargar archivo para análisis con validación"""
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
            elif extension == "parquet":
                df = pd.read_parquet(full_path)
            else:
                st.error(f"❌ Formato de archivo no soportado: {extension}")
                return None
            
            return df
            
        except Exception as e:
            st.error(f"❌ Error al cargar el archivo: {str(e)}")
            return None
    
    def create_interactive_table(self, df, max_rows=1000):
        """Crear tabla interactiva con AgGrid"""
        try:
            # Limitar filas para rendimiento
            display_df = df.head(max_rows) if len(df) > max_rows else df
            
            # Configurar AgGrid
            gb = GridOptionsBuilder.from_dataframe(display_df)
            gb.configure_pagination(paginationAutoPageSize=True)
            gb.configure_side_bar()
            gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children")
            gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
            
            # Configurar columnas numéricas
            numeric_cols = display_df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                gb.configure_column(col, type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2)
            
            gridOptions = gb.build()
            
            # Mostrar tabla
            grid_response = AgGrid(
                display_df,
                gridOptions=gridOptions,
                data_return_mode=DataReturnMode.AS_INPUT,
                update_mode=GridUpdateMode.MODEL_CHANGED,
                fit_columns_on_grid_load=False,
                theme='streamlit',
                enable_enterprise_modules=True,
                height=400,
                width='100%',
                reload_data=False
            )
            
            return grid_response
            
        except Exception as e:
            st.error(f"❌ Error al crear tabla interactiva: {str(e)}")
            return None

# Inicializar módulo
@st.cache_resource
def init_enhanced_analysis_module():
    return EnhancedDataAnalysisModule()

analysis_module = init_enhanced_analysis_module()

# Header principal
st.markdown("""
<div class="main-header">
    <h1>📊 Dashboard Tesis Pro - Análisis Estadístico Interactivo</h1>
    <p>Panel central completo para análisis de datos, visualización avanzada y estadísticas inferenciales</p>
</div>
""", unsafe_allow_html=True)

# Sidebar para navegación
st.sidebar.title("🔧 Panel de Control")
st.sidebar.markdown("---")

# Sección 1: Carga de Archivos
st.sidebar.subheader("📁 Carga de Datos")

# Obtener archivos disponibles
available_files = analysis_module.get_available_files()

if available_files["count"] > 0:
    file_options = [f"{file['name']} ({file['directory']})" for file in available_files["files"]]
    selected_file_display = st.sidebar.selectbox(
        "Seleccionar archivo:",
        options=file_options,
        help="Archivos disponibles desde el explorador"
    )
    
    if selected_file_display:
        # Obtener el path real del archivo seleccionado
        selected_file_index = file_options.index(selected_file_display)
        selected_file_path = available_files["files"][selected_file_index]["path"]
        
        if st.sidebar.button("🔄 Cargar Archivo", type="primary"):
            with st.spinner("Cargando y validando archivo..."):
                data = analysis_module.load_file(selected_file_path)
                if data is not None:
                    # Validar datos
                    validation_report = analysis_module.validator.create_validation_report(
                        data, available_files["files"][selected_file_index]["name"]
                    )
                    
                    st.session_state['data'] = data
                    st.session_state['file_name'] = available_files["files"][selected_file_index]["name"]
                    st.session_state['validation_report'] = validation_report
                    
                    # Mostrar resultado de validación en sidebar
                    if validation_report['summary']['is_ready_for_analysis']:
                        st.sidebar.success(f"✅ Archivo cargado y validado: {st.session_state['file_name']}")
                    else:
                        st.sidebar.warning(f"⚠️ Archivo cargado con advertencias: {st.session_state['file_name']}")
else:
    st.sidebar.warning("⚠️ No hay archivos analizables disponibles")
    st.sidebar.info("💡 Sube archivos CSV, Excel o JSON al explorador de archivos")

# Upload manual como alternativa
st.sidebar.markdown("---")
st.sidebar.subheader("📤 Upload Manual")
uploaded_file = st.sidebar.file_uploader(
    "Subir archivo",
    type=['csv', 'xlsx', 'xls', 'json'],
    help="Alternativamente, sube un archivo directamente"
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            data = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.json'):
            data = pd.read_json(uploaded_file)
        
        # Validar datos
        validation_report = analysis_module.validator.create_validation_report(data, uploaded_file.name)
        
        st.session_state['data'] = data
        st.session_state['file_name'] = uploaded_file.name
        st.session_state['validation_report'] = validation_report
        
        if validation_report['summary']['is_ready_for_analysis']:
            st.sidebar.success(f"✅ Archivo cargado y validado: {uploaded_file.name}")
        else:
            st.sidebar.warning(f"⚠️ Archivo cargado con advertencias: {uploaded_file.name}")
            
    except Exception as e:
        st.sidebar.error(f"❌ Error al cargar archivo: {str(e)}")

# Mostrar estado de validación en sidebar
if 'validation_report' in st.session_state:
    report = st.session_state['validation_report']
    summary = report['summary']
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Estado de Validación")
    
    # Puntuación de calidad
    score = summary['validation_score']
    if score >= 80:
        st.sidebar.success(f"📊 Calidad de datos: {score}/100")
    elif score >= 60:
        st.sidebar.warning(f"📊 Calidad de datos: {score}/100")
    else:
        st.sidebar.error(f"📊 Calidad de datos: {score}/100")
    
    # Resumen de problemas
    if summary['total_errors'] > 0:
        st.sidebar.error(f"❌ {summary['total_errors']} errores")
    if summary['total_warnings'] > 0:
        st.sidebar.warning(f"⚠️ {summary['total_warnings']} advertencias")
    if summary['total_suggestions'] > 0:
        st.sidebar.info(f"💡 {summary['total_suggestions']} sugerencias")

# Contenido principal
if 'data' in st.session_state and st.session_state['data'] is not None:
    df = st.session_state['data']
    file_name = st.session_state.get('file_name', 'archivo_cargado')
    validation_report = st.session_state.get('validation_report', {})
    
    # Tabs principales mejorados
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Vista General", 
        "🔍 Validación de Datos",
        "📊 Estadísticas Descriptivas", 
        "📈 Visualizaciones", 
        "🔬 Análisis Avanzados",
        "📤 Exportar Resultados"
    ])
    
    with tab1:
        st.subheader(f"📋 Vista General - {file_name}")
        
        # Métricas principales
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("📊 Filas", f"{len(df):,}")
        with col2:
            st.metric("📋 Columnas", len(df.columns))
        with col3:
            st.metric("💾 Memoria", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        with col4:
            missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
            st.metric("❓ Datos Faltantes", f"{missing_pct:.1f}%")
        with col5:
            numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
            st.metric("🔢 Cols. Numéricas", numeric_cols)
        
        # Vista previa con tabla interactiva
        st.markdown("### 🔍 Vista Previa Interactiva")
        
        # Opciones de visualización
        col1, col2, col3 = st.columns(3)
        with col1:
            show_rows = st.selectbox("Filas a mostrar:", [100, 500, 1000, "Todas"], index=0)
        with col2:
            table_type = st.selectbox("Tipo de tabla:", ["Interactiva (AgGrid)", "Estándar"], index=0)
        with col3:
            if st.button("🔄 Actualizar Vista"):
                st.rerun()
        
        # Mostrar tabla según configuración
        if table_type == "Interactiva (AgGrid)":
            max_rows = len(df) if show_rows == "Todas" else show_rows
            grid_response = analysis_module.create_interactive_table(df, max_rows)
        else:
            display_rows = len(df) if show_rows == "Todas" else show_rows
            st.dataframe(df.head(display_rows), use_container_width=True)
        
        # Información de columnas mejorada
        st.markdown("### 📋 Información Detallada de Columnas")
        
        info_data = []
        for col in df.columns:
            col_data = df[col]
            info_data.append({
                'Columna': col,
                'Tipo': str(col_data.dtype),
                'No Nulos': col_data.count(),
                'Nulos': col_data.isnull().sum(),
                '% Nulos': round((col_data.isnull().sum() / len(df)) * 100, 2),
                'Únicos': col_data.nunique(),
                'Memoria (KB)': round(col_data.memory_usage(deep=True) / 1024, 2)
            })
        
        info_df = pd.DataFrame(info_data)
        st.dataframe(info_df, use_container_width=True)
    
    with tab2:
        st.subheader("🔍 Validación y Calidad de Datos")
        
        if validation_report:
            # Resumen de validación
            summary = validation_report['summary']
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Puntuación de Calidad", f"{summary['validation_score']}/100")
            with col2:
                st.metric("❌ Errores", summary['total_errors'])
            with col3:
                st.metric("⚠️ Advertencias", summary['total_warnings'])
            with col4:
                st.metric("💡 Sugerencias", summary['total_suggestions'])
            
            # Estado general
            if summary['is_ready_for_analysis']:
                st.success("✅ Los datos están listos para análisis")
            else:
                st.warning("⚠️ Se recomienda revisar los problemas detectados antes del análisis")
            
            # Mostrar problemas detallados
            validation_result = validation_report['validation_result']
            
            if validation_result['errors']:
                st.markdown("### ❌ Errores Detectados")
                for error in validation_result['errors']:
                    st.error(f"**{error['message']}**\n\n💡 {error['suggestion']}")
            
            if validation_result['warnings']:
                st.markdown("### ⚠️ Advertencias")
                for warning in validation_result['warnings']:
                    st.warning(f"**{warning['message']}**\n\n💡 {warning['suggestion']}")
            
            if validation_result['suggestions']:
                st.markdown("### 💡 Sugerencias de Mejora")
                for suggestion in validation_result['suggestions']:
                    st.info(f"**{suggestion['message']}**\n\n💡 {suggestion['suggestion']}")
            
            # Sugerencias de limpieza
            cleaning_suggestions = validation_report.get('cleaning_suggestions', [])
            if cleaning_suggestions:
                st.markdown("### 🧹 Sugerencias de Limpieza")
                
                for idx, suggestion in enumerate(cleaning_suggestions):
                    with st.expander(f"🔧 {suggestion['description']}"):
                        st.code(suggestion['code'], language='python')
                        if st.button(f"Aplicar: {suggestion['action']}", key=f"btn_clean_{idx}_{suggestion['action']}"):
                            st.info("🚧 Funcionalidad de limpieza automática en desarrollo")
        else:
            st.info("📊 Carga un archivo para ver el reporte de validación")
    
    with tab3:
        st.subheader("📊 Estadísticas Descriptivas Avanzadas")
        
        # Selector de tipo de análisis descriptivo
        analysis_type = st.selectbox(
            "Tipo de análisis:",
            ["general", "numeric", "categorical", "temporal"],
            format_func=lambda x: {
                "general": "📊 Análisis General",
                "numeric": "🔢 Variables Numéricas",
                "categorical": "📝 Variables Categóricas",
                "temporal": "📅 Análisis Temporal"
            }[x]
        )
        
        if analysis_type == "general":
            # Estadísticas generales
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🔢 Variables Numéricas")
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    numeric_stats = df[numeric_cols].describe()
                    st.dataframe(numeric_stats.round(4), use_container_width=True)
                else:
                    st.info("No hay variables numéricas")
            
            with col2:
                st.markdown("#### 📝 Variables Categóricas")
                categorical_cols = df.select_dtypes(include=['object', 'category']).columns
                if len(categorical_cols) > 0:
                    cat_info = []
                    for col in categorical_cols:
                        cat_info.append({
                            'Columna': col,
                            'Únicos': df[col].nunique(),
                            'Más Frecuente': df[col].mode().iloc[0] if not df[col].mode().empty else 'N/A',
                            'Frecuencia': df[col].value_counts().iloc[0] if len(df[col].value_counts()) > 0 else 0
                        })
                    cat_df = pd.DataFrame(cat_info)
                    st.dataframe(cat_df, use_container_width=True)
                else:
                    st.info("No hay variables categóricas")
        
        elif analysis_type == "numeric":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if not numeric_cols:
                st.warning("⚠️ No hay columnas numéricas disponibles")
            else:
                selected_numeric = st.multiselect(
                    "Seleccionar variables numéricas:",
                    numeric_cols,
                    default=numeric_cols[:5]  # Máximo 5 por defecto
                )
                
                if selected_numeric:
                    # Estadísticas detalladas
                    stats_df = df[selected_numeric].describe()
                    
                    # Agregar estadísticas adicionales
                    additional_stats = pd.DataFrame({
                        col: {
                            'skewness': df[col].skew(),
                            'kurtosis': df[col].kurtosis(),
                            'cv': df[col].std() / df[col].mean() if df[col].mean() != 0 else np.nan
                        } for col in selected_numeric
                    }).T
                    
                    combined_stats = pd.concat([stats_df, additional_stats.T])
                    st.dataframe(combined_stats.round(4), use_container_width=True)
                    
                    # Matriz de correlación
                    if len(selected_numeric) > 1:
                        st.markdown("#### 🔗 Matriz de Correlación")
                        corr_matrix = df[selected_numeric].corr()
                        
                        fig = px.imshow(
                            corr_matrix,
                            title="Matriz de Correlación",
                            color_continuous_scale="RdBu_r",
                            aspect="auto"
                        )
                        fig.update_layout(template="plotly_white")
                        st.plotly_chart(fig, use_container_width=True)
        
        elif analysis_type == "categorical":
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            if not categorical_cols:
                st.warning("⚠️ No hay columnas categóricas disponibles")
            else:
                selected_categorical = st.selectbox("Seleccionar variable categórica:", categorical_cols)
                
                if selected_categorical:
                    col_data = df[selected_categorical]
                    
                    # Estadísticas básicas
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Valores únicos", col_data.nunique())
                    with col2:
                        st.metric("Más frecuente", col_data.mode().iloc[0] if not col_data.mode().empty else 'N/A')
                    with col3:
                        st.metric("Frecuencia máxima", col_data.value_counts().iloc[0] if len(col_data.value_counts()) > 0 else 0)
                    
                    # Tabla de frecuencias
                    st.markdown("#### 📊 Tabla de Frecuencias")
                    freq_table = col_data.value_counts().reset_index()
                    freq_table.columns = ['Valor', 'Frecuencia']
                    freq_table['Porcentaje'] = (freq_table['Frecuencia'] / len(col_data) * 100).round(2)
                    st.dataframe(freq_table, use_container_width=True)
                    
                    # Gráfico de barras
                    fig = px.bar(
                        freq_table.head(20),  # Top 20 valores
                        x='Valor',
                        y='Frecuencia',
                        title=f"Distribución de {selected_categorical}"
                    )
                    fig.update_layout(template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)
        
        elif analysis_type == "temporal":
            # Detectar columnas de fecha
            date_cols = []
            for col in df.columns:
                if df[col].dtype == 'datetime64[ns]' or 'date' in col.lower() or 'time' in col.lower():
                    date_cols.append(col)
            
            if not date_cols:
                st.warning("⚠️ No se detectaron columnas de fecha/tiempo")
                st.info("💡 Intenta convertir columnas de texto a formato fecha primero")
            else:
                selected_date = st.selectbox("Seleccionar columna de fecha:", date_cols)
                
                if selected_date:
                    # Intentar convertir a datetime si no lo es
                    try:
                        if df[selected_date].dtype != 'datetime64[ns]':
                            df[selected_date] = pd.to_datetime(df[selected_date])
                        
                        # Estadísticas temporales
                        date_data = df[selected_date].dropna()
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Fecha mínima", date_data.min().strftime('%Y-%m-%d'))
                        with col2:
                            st.metric("Fecha máxima", date_data.max().strftime('%Y-%m-%d'))
                        with col3:
                            st.metric("Rango (días)", (date_data.max() - date_data.min()).days)
                        
                        # Distribución temporal
                        st.markdown("#### 📅 Distribución Temporal")
                        
                        # Agrupar por mes
                        monthly_counts = date_data.dt.to_period('M').value_counts().sort_index()
                        
                        fig = px.line(
                            x=monthly_counts.index.astype(str),
                            y=monthly_counts.values,
                            title="Distribución de Registros por Mes"
                        )
                        fig.update_layout(template="plotly_white")
                        st.plotly_chart(fig, use_container_width=True)
                        
                    except Exception as e:
                        st.error(f"❌ Error al procesar fechas: {str(e)}")
    
    with tab4:
        st.subheader("📈 Visualizaciones Interactivas Avanzadas")
        
        # Panel de configuración de visualizaciones mejorado
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("#### ⚙️ Configuración Avanzada")
            
            viz_category = st.selectbox(
                "Categoría de gráfico:",
                ["basic", "statistical", "advanced", "custom"],
                format_func=lambda x: {
                    "basic": "📊 Básicos",
                    "statistical": "📈 Estadísticos",
                    "advanced": "🎯 Avanzados",
                    "custom": "🎨 Personalizados"
                }[x]
            )
            
            if viz_category == "basic":
                viz_type = st.selectbox(
                    "Tipo de gráfico:",
                    ["histogram", "scatter", "bar", "line", "pie"],
                    format_func=lambda x: {
                        "histogram": "📊 Histograma",
                        "scatter": "🔵 Dispersión",
                        "bar": "📊 Barras",
                        "line": "📈 Líneas",
                        "pie": "🥧 Circular"
                    }[x]
                )
            elif viz_category == "statistical":
                viz_type = st.selectbox(
                    "Tipo de gráfico:",
                    ["box", "violin", "correlation_heatmap", "distribution"],
                    format_func=lambda x: {
                        "box": "📦 Caja",
                        "violin": "🎻 Violín",
                        "correlation_heatmap": "🔥 Mapa de Calor",
                        "distribution": "📊 Distribución"
                    }[x]
                )
            elif viz_category == "advanced":
                viz_type = st.selectbox(
                    "Tipo de gráfico:",
                    ["parallel_coordinates", "radar", "treemap", "sunburst"],
                    format_func=lambda x: {
                        "parallel_coordinates": "🔗 Coordenadas Paralelas",
                        "radar": "🎯 Radar",
                        "treemap": "🌳 Mapa de Árbol",
                        "sunburst": "☀️ Sunburst"
                    }[x]
                )
            else:  # custom
                viz_type = st.selectbox(
                    "Tipo de gráfico:",
                    ["3d_scatter", "animated", "subplots", "dashboard"],
                    format_func=lambda x: {
                        "3d_scatter": "🌐 Dispersión 3D",
                        "animated": "🎬 Animado",
                        "subplots": "📊 Subgráficos",
                        "dashboard": "📋 Dashboard"
                    }[x]
                )
            
            # Configuración de columnas según el tipo de gráfico
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            columns = []
            if viz_type in ["histogram", "box", "violin", "distribution"]:
                if numeric_cols:
                    columns = [st.selectbox("Variable numérica:", numeric_cols)]
            elif viz_type in ["scatter", "line"]:
                if len(numeric_cols) >= 2:
                    x_col = st.selectbox("Eje X:", numeric_cols)
                    y_col = st.selectbox("Eje Y:", [col for col in numeric_cols if col != x_col])
                    columns = [x_col, y_col]
                    
                    # Opción de color
                    if categorical_cols:
                        color_col = st.selectbox("Color por:", ["Ninguno"] + categorical_cols)
                        if color_col != "Ninguno":
                            columns.append(color_col)
            elif viz_type == "bar":
                if categorical_cols and numeric_cols:
                    x_col = st.selectbox("Categorías:", categorical_cols)
                    y_col = st.selectbox("Valores:", numeric_cols)
                    columns = [x_col, y_col]
            elif viz_type == "pie":
                if categorical_cols:
                    columns = [st.selectbox("Variable categórica:", categorical_cols)]
            
            # Configuraciones adicionales
            st.markdown("##### 🎨 Estilo")
            color_palette = st.selectbox(
                "Paleta de colores:",
                ["plotly", "viridis", "plasma", "inferno", "magma", "Set1", "Set2", "Set3"],
                index=0
            )
            
            plot_theme = st.selectbox(
                "Tema:",
                ["plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white"],
                index=0
            )
            
            # Botón para generar gráfico
            if st.button("🎨 Generar Visualización", type="primary"):
                if not columns:
                    st.error("❌ Selecciona las columnas necesarias")
                else:
                    with st.spinner("Generando visualización..."):
                        fig = create_advanced_visualization(df, viz_type, columns, color_palette, plot_theme)
                        if fig:
                            st.session_state['current_viz'] = fig
                            st.session_state['viz_config'] = {
                                'type': viz_type,
                                'columns': columns,
                                'palette': color_palette,
                                'theme': plot_theme
                            }
        
        with col2:
            st.markdown("#### 📊 Visualización")
            
            if 'current_viz' in st.session_state:
                fig = st.session_state['current_viz']
                st.plotly_chart(fig, use_container_width=True)
                
                # Información de la visualización
                if 'viz_config' in st.session_state:
                    config = st.session_state['viz_config']
                    st.info(f"📊 **Tipo:** {config['type']} | **Columnas:** {', '.join(config['columns'])} | **Tema:** {config['theme']}")
                
                # Opciones de exportación
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📷 Exportar PNG"):
                        img_bytes = fig.to_image(format="png", width=1200, height=800)
                        st.download_button(
                            label="⬇️ Descargar PNG",
                            data=img_bytes,
                            file_name=f"grafico_{datetime.now().strftime('%Y%m%d_%H%M')}.png",
                            mime="image/png"
                        )
                
                with col2:
                    if st.button("📄 Exportar HTML"):
                        html_str = fig.to_html(include_plotlyjs='cdn')
                        st.download_button(
                            label="⬇️ Descargar HTML",
                            data=html_str,
                            file_name=f"grafico_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                            mime="text/html"
                        )
                
                with col3:
                    if st.button("📊 Exportar JSON"):
                        json_str = fig.to_json()
                        st.download_button(
                            label="⬇️ Descargar JSON",
                            data=json_str,
                            file_name=f"grafico_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                            mime="application/json"
                        )
            else:
                st.info("👈 Configura y genera una visualización para mostrar aquí")
                
                # Mostrar galería de ejemplos
                st.markdown("##### 🖼️ Galería de Ejemplos")
                
                example_images = [
                    "https://plotly.com/~plotly2_demo/542.png",
                    "https://plotly.com/~plotly2_demo/543.png",
                    "https://plotly.com/~plotly2_demo/544.png"
                ]
                
                cols = st.columns(3)
                for i, img_url in enumerate(example_images):
                    with cols[i]:
                        try:
                            st.image(img_url, caption=f"Ejemplo {i+1}", use_column_width=True)
                        except:
                            st.info(f"Ejemplo {i+1}")
    
    with tab5:
        # Tab de análisis avanzados (importado del módulo separado)
        render_advanced_analysis_tab(df, file_name)
    
    with tab6:
        st.subheader("📤 Exportar Resultados y Reportes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💾 Exportar Datos")
            
            # Opciones de exportación de datos
            export_format = st.selectbox(
                "Formato de exportación:",
                ["excel", "csv", "json", "parquet"],
                format_func=lambda x: {
                    "excel": "📊 Excel (.xlsx)",
                    "csv": "📄 CSV (.csv)",
                    "json": "📋 JSON (.json)",
                    "parquet": "🗃️ Parquet (.parquet)"
                }[x]
            )
            
            include_stats = st.checkbox("Incluir estadísticas descriptivas", value=True)
            include_validation = st.checkbox("Incluir reporte de validación", value=True)
            
            if st.button("📊 Generar Exportación Completa", type="primary"):
                with st.spinner("Generando archivo de exportación..."):
                    export_data = create_comprehensive_export(
                        df, file_name, export_format, include_stats, include_validation, validation_report
                    )
                    
                    if export_data:
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
                        filename = f"analisis_completo_{file_name}_{timestamp}.{export_format}"
                        
                        if export_format == "excel":
                            st.download_button(
                                label="⬇️ Descargar Excel Completo",
                                data=export_data,
                                file_name=filename,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        elif export_format == "csv":
                            st.download_button(
                                label="⬇️ Descargar CSV",
                                data=export_data,
                                file_name=filename,
                                mime="text/csv"
                            )
                        elif export_format == "json":
                            st.download_button(
                                label="⬇️ Descargar JSON",
                                data=export_data,
                                file_name=filename,
                                mime="application/json"
                            )
        
        with col2:
            st.markdown("#### 📊 Generar Reporte")
            
            # Opciones de reporte
            report_sections = st.multiselect(
                "Secciones del reporte:",
                [
                    "resumen_ejecutivo",
                    "validacion_datos", 
                    "estadisticas_descriptivas",
                    "visualizaciones",
                    "analisis_avanzados",
                    "conclusiones"
                ],
                default=[
                    "resumen_ejecutivo",
                    "validacion_datos",
                    "estadisticas_descriptivas"
                ],
                format_func=lambda x: {
                    "resumen_ejecutivo": "📋 Resumen Ejecutivo",
                    "validacion_datos": "🔍 Validación de Datos",
                    "estadisticas_descriptivas": "📊 Estadísticas Descriptivas",
                    "visualizaciones": "📈 Visualizaciones",
                    "analisis_avanzados": "🔬 Análisis Avanzados",
                    "conclusiones": "💡 Conclusiones"
                }[x]
            )
            
            report_format = st.selectbox(
                "Formato del reporte:",
                ["html", "markdown", "pdf"],
                format_func=lambda x: {
                    "html": "🌐 HTML",
                    "markdown": "📝 Markdown",
                    "pdf": "📄 PDF"
                }[x]
            )
            
            if st.button("📋 Generar Reporte Completo", type="primary"):
                with st.spinner("Generando reporte..."):
                    report_content = generate_comprehensive_report(
                        df, file_name, validation_report, report_sections, report_format
                    )
                    
                    if report_content:
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
                        filename = f"reporte_analisis_{file_name}_{timestamp}.{report_format}"
                        
                        if report_format == "html":
                            st.download_button(
                                label="⬇️ Descargar Reporte HTML",
                                data=report_content,
                                file_name=filename,
                                mime="text/html"
                            )
                        elif report_format == "markdown":
                            st.download_button(
                                label="⬇️ Descargar Reporte Markdown",
                                data=report_content,
                                file_name=filename,
                                mime="text/markdown"
                            )
                        elif report_format == "pdf":
                            st.info("🚧 Exportación a PDF en desarrollo")
        
        # Historial de exportaciones
        st.markdown("---")
        st.markdown("#### 📚 Historial de Exportaciones")
        
        if 'export_history' not in st.session_state:
            st.session_state.export_history = []
        
        if st.session_state.export_history:
            for i, export in enumerate(st.session_state.export_history):
                st.text(f"📄 {export['filename']} - {export['timestamp']} - {export['format']}")
        else:
            st.info("📝 No hay exportaciones en el historial")

else:
    # Pantalla de bienvenida mejorada
    st.markdown("""
    ## 👋 ¡Bienvenido al Módulo de Análisis Estadístico Avanzado!
    
    ### 🚀 Características Principales:
    
    #### 📊 **Análisis Descriptivo**
    - Estadísticas automáticas completas
    - Detección de outliers y valores faltantes
    - Análisis temporal avanzado
    
    #### 🔬 **Análisis Inferencial**
    - Pruebas t (una y dos muestras)
    - ANOVA de uno y múltiples factores
    - Pruebas de chi-cuadrado
    - Análisis de correlación (Pearson, Spearman, Kendall)
    - Regresión lineal y múltiple
    
    #### 🎯 **Machine Learning**
    - Clustering K-means y jerárquico
    - Análisis de componentes principales
    - Detección automática de patrones
    
    #### 📈 **Visualizaciones Avanzadas**
    - Gráficos interactivos con Plotly
    - Mapas de calor y correlaciones
    - Visualizaciones 3D y animadas
    - Dashboards personalizados
    
    #### 🔍 **Validación de Datos**
    - Detección automática de problemas
    - Sugerencias de limpieza
    - Puntuación de calidad de datos
    - Mensajes de error amigables
    
    ### 📋 **Formatos Soportados:**
    - **CSV** (.csv) - Archivos de valores separados por comas
    - **Excel** (.xlsx, .xls) - Hojas de cálculo de Microsoft Excel
    - **JSON** (.json) - Archivos de notación de objetos JavaScript
    - **Parquet** (.parquet) - Formato columnar optimizado
    
    ### 🔧 **Para Comenzar:**
    1. **📁 Carga un archivo** desde el explorador o súbelo manualmente
    2. **🔍 Revisa la validación** automática de datos
    3. **📊 Explora estadísticas** descriptivas detalladas
    4. **📈 Crea visualizaciones** interactivas personalizadas
    5. **🔬 Realiza análisis** estadísticos avanzados
    6. **📤 Exporta resultados** en múltiples formatos
    """)
    
    # Panel de estado del sistema
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔌 Estado de Conexiones")
        try:
            response = requests.get(f"{analysis_module.file_api_url}/status", timeout=3)
            if response.status_code == 200:
                st.success("✅ Explorador de archivos conectado")
                
                # Obtener estadísticas del explorador
                stats_response = requests.get(f"{analysis_module.file_api_url}/stats", timeout=3)
                if stats_response.status_code == 200:
                    stats = stats_response.json()
                    st.info(f"📁 {stats['total_files']} archivos disponibles")
                    st.info(f"💾 {stats['total_size_human']} de datos")
            else:
                st.error("❌ Explorador de archivos no responde")
        except:
            st.error("❌ No se puede conectar al explorador de archivos")
            st.info("💡 Inicia el explorador primero:\n`cd ../file_explorer && ./start_filebrowser.sh`")
    
    with col2:
        st.markdown("### 📊 Archivos Disponibles")
        if available_files["count"] > 0:
            st.success(f"📁 {available_files['count']} archivos analizables")
            
            # Mostrar tipos de archivo
            extensions = {}
            for file in available_files["files"]:
                ext = file["extension"].upper()
                extensions[ext] = extensions.get(ext, 0) + 1
            
            for ext, count in extensions.items():
                st.text(f"📄 {ext}: {count} archivos")
        else:
            st.warning("⚠️ No hay archivos disponibles")
            st.info("💡 Sube archivos al explorador o usa el upload manual")
    
    with col3:
        st.markdown("### 🎯 Ejemplos Disponibles")
        
        # Verificar si existen datos de ejemplo
        example_files = [
            "encuesta_estudiantes.csv",
            "ventas_empresa.csv", 
            "experimento_tratamiento.csv",
            "datos_problematicos.csv"
        ]
        
        examples_found = 0
        for example in example_files:
            if any(example in file['name'] for file in available_files.get('files', [])):
                examples_found += 1
                st.text(f"✅ {example}")
        
        if examples_found == 0:
            st.info("💡 Genera datos de ejemplo:")
            st.code("cd modules/data_analysis && python3 generate_sample_data.py")

# Footer mejorado
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em; padding: 1rem;">
    <strong>Dashboard Tesis Pro - Módulo de Análisis Estadístico v2.0.0</strong><br>
    🔧 Panel ejecutándose en puerto 8050 | 📁 Explorador en puerto 8058 | 🔌 API en puerto 8060<br>
    📊 Análisis Avanzados | 🔍 Validación Automática | 📈 Visualizaciones Interactivas | 📤 Exportación Completa
</div>
""", unsafe_allow_html=True)

# Funciones auxiliares

def create_comprehensive_export(df, file_name, export_format, include_stats, include_validation, validation_report):
    """Crear exportación completa de datos y análisis"""
    try:
        if export_format == "excel":
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                # Hoja principal con datos
                df.to_excel(writer, sheet_name='Datos', index=False)
                
                if include_stats:
                    # Hoja con estadísticas descriptivas
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        stats_df = df[numeric_cols].describe()
                        stats_df.to_excel(writer, sheet_name='Estadísticas')
                
                if include_validation and validation_report:
                    # Hoja con reporte de validación
                    validation_summary = pd.DataFrame([validation_report['summary']])
                    validation_summary.to_excel(writer, sheet_name='Validación', index=False)
            
            return output.getvalue()
            
        elif export_format == "csv":
            return df.to_csv(index=False)
            
        elif export_format == "json":
            export_data = {
                'metadata': {
                    'file_name': file_name,
                    'export_timestamp': datetime.now().isoformat(),
                    'rows': len(df),
                    'columns': len(df.columns)
                },
                'data': df.to_dict('records')
            }
            
            if include_stats:
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    export_data['statistics'] = df[numeric_cols].describe().to_dict()
            
            if include_validation and validation_report:
                export_data['validation'] = validation_report
            
            return json.dumps(export_data, indent=2, default=str, ensure_ascii=False)
        
        return None
        
    except Exception as e:
        st.error(f"❌ Error al crear exportación: {str(e)}")
        return None

def generate_comprehensive_report(df, file_name, validation_report, sections, report_format):
    """Generar reporte completo de análisis"""
    try:
        if report_format == "markdown":
            report_lines = []
            
            # Encabezado
            report_lines.append(f"# Reporte de Análisis - {file_name}")
            report_lines.append(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_lines.append("")
            
            if "resumen_ejecutivo" in sections:
                report_lines.append("## 📋 Resumen Ejecutivo")
                report_lines.append(f"- **Archivo analizado:** {file_name}")
                report_lines.append(f"- **Número de filas:** {len(df):,}")
                report_lines.append(f"- **Número de columnas:** {len(df.columns)}")
                report_lines.append(f"- **Tamaño en memoria:** {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
                report_lines.append("")
            
            if "validacion_datos" in sections and validation_report:
                report_lines.append("## 🔍 Validación de Datos")
                summary = validation_report['summary']
                report_lines.append(f"- **Puntuación de calidad:** {summary['validation_score']}/100")
                report_lines.append(f"- **Errores detectados:** {summary['total_errors']}")
                report_lines.append(f"- **Advertencias:** {summary['total_warnings']}")
                report_lines.append(f"- **Sugerencias:** {summary['total_suggestions']}")
                report_lines.append("")
            
            if "estadisticas_descriptivas" in sections:
                report_lines.append("## 📊 Estadísticas Descriptivas")
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    stats_df = df[numeric_cols].describe()
                    report_lines.append("### Variables Numéricas")
                    report_lines.append(stats_df.to_markdown())
                    report_lines.append("")
            
            return "\n".join(report_lines)
            
        elif report_format == "html":
            # Generar reporte HTML
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Reporte de Análisis - {file_name}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    h1, h2 {{ color: #2196F3; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    .metric {{ background: #f8f9fa; padding: 10px; margin: 10px 0; border-left: 4px solid #2196F3; }}
                </style>
            </head>
            <body>
                <h1>📊 Reporte de Análisis - {file_name}</h1>
                <p><strong>Fecha:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            """
            
            if "resumen_ejecutivo" in sections:
                html_content += f"""
                <h2>📋 Resumen Ejecutivo</h2>
                <div class="metric">
                    <strong>Archivo:</strong> {file_name}<br>
                    <strong>Filas:</strong> {len(df):,}<br>
                    <strong>Columnas:</strong> {len(df.columns)}<br>
                    <strong>Memoria:</strong> {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB
                </div>
                """
            
            html_content += """
            </body>
            </html>
            """
            
            return html_content
        
        return None
        
    except Exception as e:
        st.error(f"❌ Error al generar reporte: {str(e)}")
        return None

