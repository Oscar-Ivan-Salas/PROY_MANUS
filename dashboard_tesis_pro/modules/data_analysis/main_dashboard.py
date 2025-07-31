#!/usr/bin/env python3
"""
Dashboard Tesis Pro - Módulo de Análisis Estadístico Interactivo
Panel Central en Streamlit

Este módulo proporciona la interfaz principal para el análisis de datos:
- Carga de archivos desde el explorador
- Análisis estadístico descriptivo e inferencial
- Visualizaciones interactivas
- Exportación de resultados
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
import os
from datetime import datetime
import io
import base64

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Tesis Pro - Análisis Estadístico",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2196F3, #1976D2);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2196F3;
    }
    
    .success-box {
        background: #E8F5E8;
        border: 1px solid #4CAF50;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    
    .warning-box {
        background: #FFF3E0;
        border: 1px solid #FF9800;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    
    .error-box {
        background: #FFEBEE;
        border: 1px solid #F44336;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    
    .stSelectbox > div > div > select {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

class DataAnalysisModule:
    def __init__(self):
        self.file_api_url = "http://localhost:8060/api"
        self.data = None
        self.analysis_history = []
        
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
        """Cargar archivo para análisis"""
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
                    else:
                        df = pd.json_normalize(data)
            elif extension == "parquet":
                df = pd.read_parquet(full_path)
            else:
                st.error(f"❌ Formato de archivo no soportado: {extension}")
                return None
            
            return df
            
        except Exception as e:
            st.error(f"❌ Error al cargar el archivo: {str(e)}")
            return None
    
    def get_descriptive_stats(self, df):
        """Calcular estadísticas descriptivas"""
        stats = {}
        
        # Estadísticas numéricas
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            stats['numeric'] = {
                'count': df[numeric_cols].count(),
                'mean': df[numeric_cols].mean(),
                'median': df[numeric_cols].median(),
                'std': df[numeric_cols].std(),
                'min': df[numeric_cols].min(),
                'max': df[numeric_cols].max(),
                'q25': df[numeric_cols].quantile(0.25),
                'q75': df[numeric_cols].quantile(0.75),
                'skewness': df[numeric_cols].skew(),
                'kurtosis': df[numeric_cols].kurtosis()
            }
        
        # Estadísticas categóricas
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            stats['categorical'] = {}
            for col in categorical_cols:
                stats['categorical'][col] = {
                    'unique_count': df[col].nunique(),
                    'most_frequent': df[col].mode().iloc[0] if not df[col].mode().empty else None,
                    'frequency': df[col].value_counts().head(10).to_dict()
                }
        
        # Información general
        stats['general'] = {
            'rows': len(df),
            'columns': len(df.columns),
            'missing_values': df.isnull().sum().to_dict(),
            'data_types': df.dtypes.astype(str).to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum()
        }
        
        return stats
    
    def create_visualizations(self, df, viz_type, columns):
        """Crear visualizaciones con Plotly"""
        fig = None
        
        try:
            if viz_type == "histogram":
                if len(columns) == 1:
                    fig = px.histogram(df, x=columns[0], title=f"Histograma de {columns[0]}")
                
            elif viz_type == "scatter":
                if len(columns) >= 2:
                    color_col = columns[2] if len(columns) > 2 else None
                    fig = px.scatter(df, x=columns[0], y=columns[1], color=color_col,
                                   title=f"Gráfico de Dispersión: {columns[0]} vs {columns[1]}")
                
            elif viz_type == "box":
                if len(columns) == 1:
                    fig = px.box(df, y=columns[0], title=f"Diagrama de Caja de {columns[0]}")
                elif len(columns) == 2:
                    fig = px.box(df, x=columns[0], y=columns[1], 
                               title=f"Diagrama de Caja: {columns[1]} por {columns[0]}")
                
            elif viz_type == "bar":
                if len(columns) >= 2:
                    fig = px.bar(df, x=columns[0], y=columns[1], 
                               title=f"Gráfico de Barras: {columns[1]} por {columns[0]}")
                
            elif viz_type == "line":
                if len(columns) >= 2:
                    fig = px.line(df, x=columns[0], y=columns[1], 
                                title=f"Gráfico de Líneas: {columns[1]} vs {columns[0]}")
                
            elif viz_type == "correlation_heatmap":
                numeric_df = df.select_dtypes(include=[np.number])
                if len(numeric_df.columns) > 1:
                    corr_matrix = numeric_df.corr()
                    fig = px.imshow(corr_matrix, 
                                  title="Matriz de Correlación",
                                  color_continuous_scale="RdBu_r",
                                  aspect="auto")
                
            elif viz_type == "violin":
                if len(columns) == 1:
                    fig = px.violin(df, y=columns[0], title=f"Gráfico de Violín de {columns[0]}")
                elif len(columns) == 2:
                    fig = px.violin(df, x=columns[0], y=columns[1], 
                                  title=f"Gráfico de Violín: {columns[1]} por {columns[0]}")
            
            if fig:
                fig.update_layout(
                    template="plotly_white",
                    font=dict(size=12),
                    title_font_size=16,
                    showlegend=True
                )
                
            return fig
            
        except Exception as e:
            st.error(f"❌ Error al crear visualización: {str(e)}")
            return None

# Inicializar módulo
@st.cache_resource
def init_analysis_module():
    return DataAnalysisModule()

analysis_module = init_analysis_module()

# Header principal
st.markdown("""
<div class="main-header">
    <h1>📊 Dashboard Tesis Pro - Análisis Estadístico Interactivo</h1>
    <p>Panel central para análisis de datos, visualización y estadísticas</p>
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
            with st.spinner("Cargando archivo..."):
                data = analysis_module.load_file(selected_file_path)
                if data is not None:
                    st.session_state['data'] = data
                    st.session_state['file_name'] = available_files["files"][selected_file_index]["name"]
                    st.sidebar.success(f"✅ Archivo cargado: {st.session_state['file_name']}")
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
        
        st.session_state['data'] = data
        st.session_state['file_name'] = uploaded_file.name
        st.sidebar.success(f"✅ Archivo cargado: {uploaded_file.name}")
    except Exception as e:
        st.sidebar.error(f"❌ Error al cargar archivo: {str(e)}")

# Contenido principal
if 'data' in st.session_state and st.session_state['data'] is not None:
    df = st.session_state['data']
    file_name = st.session_state.get('file_name', 'archivo_cargado')
    
    # Tabs principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Vista General", 
        "📊 Estadísticas Descriptivas", 
        "📈 Visualizaciones", 
        "🔬 Análisis Inferencial",
        "📤 Exportar Resultados"
    ])
    
    with tab1:
        st.subheader(f"📋 Vista General - {file_name}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Filas", f"{len(df):,}")
        with col2:
            st.metric("📋 Columnas", len(df.columns))
        with col3:
            st.metric("💾 Memoria", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        with col4:
            missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
            st.metric("❓ Datos Faltantes", f"{missing_pct:.1f}%")
        
        st.markdown("### 🔍 Vista Previa de Datos")
        st.dataframe(df.head(100), use_container_width=True)
        
        st.markdown("### 📋 Información de Columnas")
        info_df = pd.DataFrame({
            'Columna': df.columns,
            'Tipo de Dato': df.dtypes.astype(str),
            'Valores No Nulos': df.count(),
            'Valores Nulos': df.isnull().sum(),
            '% Nulos': (df.isnull().sum() / len(df) * 100).round(2)
        })
        st.dataframe(info_df, use_container_width=True)
    
    with tab2:
        st.subheader("📊 Estadísticas Descriptivas")
        
        # Calcular estadísticas
        stats = analysis_module.get_descriptive_stats(df)
        
        # Estadísticas numéricas
        if 'numeric' in stats:
            st.markdown("### 🔢 Variables Numéricas")
            numeric_stats_df = pd.DataFrame(stats['numeric']).T
            st.dataframe(numeric_stats_df.round(4), use_container_width=True)
            
            # Gráfico de distribución de estadísticas
            fig_stats = go.Figure()
            for stat in ['mean', 'median']:
                if stat in numeric_stats_df.columns:
                    fig_stats.add_trace(go.Bar(
                        name=stat.capitalize(),
                        x=numeric_stats_df.index,
                        y=numeric_stats_df[stat]
                    ))
            
            fig_stats.update_layout(
                title="Comparación Media vs Mediana",
                xaxis_title="Variables",
                yaxis_title="Valor",
                template="plotly_white"
            )
            st.plotly_chart(fig_stats, use_container_width=True)
        
        # Estadísticas categóricas
        if 'categorical' in stats:
            st.markdown("### 📝 Variables Categóricas")
            for col, col_stats in stats['categorical'].items():
                with st.expander(f"📊 {col}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Valores únicos", col_stats['unique_count'])
                        st.metric("Más frecuente", str(col_stats['most_frequent']))
                    with col2:
                        freq_df = pd.DataFrame(list(col_stats['frequency'].items()), 
                                             columns=['Valor', 'Frecuencia'])
                        st.dataframe(freq_df)
    
    with tab3:
        st.subheader("📈 Visualizaciones Interactivas")
        
        # Panel de configuración de visualizaciones
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("#### ⚙️ Configuración")
            
            viz_type = st.selectbox(
                "Tipo de gráfico:",
                ["histogram", "scatter", "box", "bar", "line", "correlation_heatmap", "violin"],
                format_func=lambda x: {
                    "histogram": "📊 Histograma",
                    "scatter": "🔵 Dispersión", 
                    "box": "📦 Caja",
                    "bar": "📊 Barras",
                    "line": "📈 Líneas",
                    "correlation_heatmap": "🔥 Mapa de Calor",
                    "violin": "🎻 Violín"
                }[x]
            )
            
            # Selección de columnas según el tipo de gráfico
            if viz_type == "correlation_heatmap":
                columns = df.select_dtypes(include=[np.number]).columns.tolist()
            else:
                max_cols = 3 if viz_type == "scatter" else 2
                columns = st.multiselect(
                    "Seleccionar columnas:",
                    df.columns.tolist(),
                    max_selections=max_cols
                )
            
            if st.button("🎨 Generar Gráfico", type="primary"):
                if viz_type != "correlation_heatmap" and len(columns) == 0:
                    st.error("❌ Selecciona al menos una columna")
                else:
                    fig = analysis_module.create_visualizations(df, viz_type, columns)
                    if fig:
                        st.session_state['current_viz'] = fig
        
        with col2:
            if 'current_viz' in st.session_state:
                st.plotly_chart(st.session_state['current_viz'], use_container_width=True)
            else:
                st.info("👈 Configura y genera un gráfico para visualizar aquí")
    
    with tab4:
        st.subheader("🔬 Análisis Inferencial")
        st.info("🚧 Módulo en desarrollo - Próximamente disponible")
        
        # Placeholder para análisis estadísticos
        st.markdown("""
        ### Análisis Disponibles (Próximamente):
        - 📊 **Pruebas t**: t-test de una muestra, dos muestras independientes, muestras pareadas
        - 📈 **ANOVA**: Análisis de varianza de uno y múltiples factores
        - 🔄 **Chi-cuadrado**: Pruebas de independencia y bondad de ajuste
        - 📉 **Correlación**: Pearson, Spearman, Kendall
        - 📊 **Regresión**: Lineal simple, múltiple, logística
        - 🎯 **Clustering**: K-means, clustering jerárquico
        """)
    
    with tab5:
        st.subheader("📤 Exportar Resultados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💾 Exportar Datos")
            
            if st.button("📊 Exportar a Excel", type="primary"):
                # Crear archivo Excel con múltiples hojas
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name='Datos', index=False)
                    
                    # Estadísticas descriptivas
                    if 'numeric' in stats:
                        pd.DataFrame(stats['numeric']).to_excel(writer, sheet_name='Estadísticas')
                
                st.download_button(
                    label="⬇️ Descargar Excel",
                    data=output.getvalue(),
                    file_name=f"analisis_{file_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            if st.button("📄 Exportar a CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Descargar CSV",
                    data=csv,
                    file_name=f"datos_{file_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            st.markdown("#### 📊 Exportar Visualizaciones")
            
            if 'current_viz' in st.session_state:
                if st.button("🖼️ Exportar Gráfico como PNG"):
                    img_bytes = st.session_state['current_viz'].to_image(format="png")
                    st.download_button(
                        label="⬇️ Descargar PNG",
                        data=img_bytes,
                        file_name=f"grafico_{datetime.now().strftime('%Y%m%d_%H%M')}.png",
                        mime="image/png"
                    )
            else:
                st.info("💡 Genera un gráfico primero para poder exportarlo")

else:
    # Pantalla de bienvenida
    st.markdown("""
    ## 👋 ¡Bienvenido al Módulo de Análisis Estadístico!
    
    ### 🚀 Para comenzar:
    1. **📁 Carga un archivo** desde el explorador o sube uno manualmente
    2. **📊 Explora tus datos** en la vista general
    3. **📈 Genera visualizaciones** interactivas
    4. **🔬 Realiza análisis** estadísticos
    5. **📤 Exporta resultados** en múltiples formatos
    
    ### 📋 Formatos Soportados:
    - **CSV** (.csv)
    - **Excel** (.xlsx, .xls) 
    - **JSON** (.json)
    - **Parquet** (.parquet)
    
    ### 🔧 Características:
    - ✅ Integración con explorador de archivos
    - ✅ Estadísticas descriptivas automáticas
    - ✅ Visualizaciones interactivas con Plotly
    - ✅ Exportación a Excel y CSV
    - ✅ Interfaz responsive y profesional
    """)
    
    # Mostrar estado de conexión con el explorador
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔌 Estado de Conexiones")
        try:
            response = requests.get(f"{analysis_module.file_api_url}/status", timeout=3)
            if response.status_code == 200:
                st.success("✅ Explorador de archivos conectado")
            else:
                st.error("❌ Explorador de archivos no responde")
        except:
            st.error("❌ No se puede conectar al explorador de archivos")
    
    with col2:
        st.markdown("### 📊 Estadísticas del Sistema")
        if available_files["count"] > 0:
            st.info(f"📁 {available_files['count']} archivos analizables disponibles")
            
            # Mostrar tipos de archivo
            extensions = {}
            for file in available_files["files"]:
                ext = file["extension"]
                extensions[ext] = extensions.get(ext, 0) + 1
            
            st.markdown("**Tipos de archivo:**")
            for ext, count in extensions.items():
                st.markdown(f"- {ext.upper()}: {count} archivos")
        else:
            st.warning("⚠️ No hay archivos disponibles para análisis")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8em;">
    Dashboard Tesis Pro - Módulo de Análisis Estadístico v1.0.0<br>
    🔧 Panel ejecutándose en puerto 8050 | 📁 Explorador en puerto 8058 | 🔌 API en puerto 8060
</div>
""", unsafe_allow_html=True)

