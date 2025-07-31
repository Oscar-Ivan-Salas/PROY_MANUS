#!/usr/bin/env python3
"""
Dashboard Tesis Pro - Tab de Análisis Avanzados

Este módulo implementa la interfaz para análisis estadísticos inferenciales:
- Pruebas t, ANOVA, chi-cuadrado
- Análisis de correlación y regresión
- Clustering automático
- Panel de configuración avanzada
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statistical_analysis import StatisticalAnalysis
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import json
from datetime import datetime

def render_advanced_analysis_tab(df, file_name):
    """Renderizar el tab de análisis avanzados"""
    
    if df is None or df.empty:
        st.info("📊 Carga un archivo primero para realizar análisis avanzados")
        return
    
    # Inicializar analizador estadístico
    if 'stat_analyzer' not in st.session_state:
        st.session_state.stat_analyzer = StatisticalAnalysis()
    
    stat_analyzer = st.session_state.stat_analyzer
    
    st.subheader("🔬 Análisis Estadísticos Avanzados")
    
    # Subtabs para diferentes tipos de análisis
    subtab1, subtab2, subtab3, subtab4, subtab5 = st.tabs([
        "📊 Pruebas Estadísticas",
        "🔗 Correlación y Regresión", 
        "🎯 Clustering",
        "⚙️ Configuración",
        "📚 Historial"
    ])
    
    with subtab1:
        render_statistical_tests(df, stat_analyzer)
    
    with subtab2:
        render_correlation_regression(df, stat_analyzer)
    
    with subtab3:
        render_clustering_analysis(df, stat_analyzer)
    
    with subtab4:
        render_analysis_configuration()
    
    with subtab5:
        render_analysis_history(stat_analyzer)

def render_statistical_tests(df, stat_analyzer):
    """Renderizar pruebas estadísticas"""
    
    st.markdown("### 📊 Pruebas de Hipótesis")
    
    # Selector de tipo de prueba
    test_type = st.selectbox(
        "Seleccionar tipo de prueba:",
        [
            "t_test_one_sample",
            "t_test_two_samples", 
            "anova_one_way",
            "chi_square_test"
        ],
        format_func=lambda x: {
            "t_test_one_sample": "📈 Prueba t de una muestra",
            "t_test_two_samples": "📊 Prueba t de dos muestras",
            "anova_one_way": "📋 ANOVA de un factor",
            "chi_square_test": "🔄 Chi-cuadrado de independencia"
        }[x]
    )
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### ⚙️ Configuración")
        
        # Configuración específica según el tipo de prueba
        if test_type == "t_test_one_sample":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if not numeric_cols:
                st.error("❌ No hay columnas numéricas disponibles")
                return
            
            column = st.selectbox("Variable a analizar:", numeric_cols)
            test_value = st.number_input("Valor de prueba:", value=0.0)
            alpha = st.slider("Nivel de significancia (α):", 0.01, 0.10, 0.05, 0.01)
            
            if st.button("🧪 Ejecutar Prueba t (una muestra)", type="primary"):
                with st.spinner("Realizando análisis..."):
                    result = stat_analyzer.t_test_one_sample(df, column, test_value, alpha)
                    st.session_state['last_test_result'] = result
        
        elif test_type == "t_test_two_samples":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            if not numeric_cols or not categorical_cols:
                st.error("❌ Se necesitan columnas numéricas y categóricas")
                return
            
            column = st.selectbox("Variable numérica:", numeric_cols)
            group_column = st.selectbox("Variable de agrupación:", categorical_cols)
            
            # Verificar que la variable de agrupación tenga exactamente 2 grupos
            unique_groups = df[group_column].nunique()
            if unique_groups != 2:
                st.warning(f"⚠️ La variable '{group_column}' tiene {unique_groups} grupos. Se necesitan exactamente 2.")
                return
            
            equal_var = st.checkbox("Asumir varianzas iguales", value=True)
            alpha = st.slider("Nivel de significancia (α):", 0.01, 0.10, 0.05, 0.01)
            
            if st.button("🧪 Ejecutar Prueba t (dos muestras)", type="primary"):
                with st.spinner("Realizando análisis..."):
                    result = stat_analyzer.t_test_two_samples(df, column, group_column, alpha, equal_var)
                    st.session_state['last_test_result'] = result
        
        elif test_type == "anova_one_way":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            if not numeric_cols or not categorical_cols:
                st.error("❌ Se necesitan columnas numéricas y categóricas")
                return
            
            dependent_var = st.selectbox("Variable dependiente (numérica):", numeric_cols)
            independent_var = st.selectbox("Variable independiente (categórica):", categorical_cols)
            
            # Verificar que haya al menos 2 grupos
            unique_groups = df[independent_var].nunique()
            if unique_groups < 2:
                st.warning(f"⚠️ La variable '{independent_var}' tiene solo {unique_groups} grupo(s). Se necesitan al menos 2.")
                return
            
            alpha = st.slider("Nivel de significancia (α):", 0.01, 0.10, 0.05, 0.01)
            
            if st.button("🧪 Ejecutar ANOVA", type="primary"):
                with st.spinner("Realizando análisis..."):
                    result = stat_analyzer.anova_one_way(df, dependent_var, independent_var, alpha)
                    st.session_state['last_test_result'] = result
        
        elif test_type == "chi_square_test":
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            if len(categorical_cols) < 2:
                st.error("❌ Se necesitan al menos 2 columnas categóricas")
                return
            
            var1 = st.selectbox("Primera variable categórica:", categorical_cols)
            var2 = st.selectbox("Segunda variable categórica:", 
                              [col for col in categorical_cols if col != var1])
            alpha = st.slider("Nivel de significancia (α):", 0.01, 0.10, 0.05, 0.01)
            
            if st.button("🧪 Ejecutar Chi-cuadrado", type="primary"):
                with st.spinner("Realizando análisis..."):
                    result = stat_analyzer.chi_square_test(df, var1, var2, alpha)
                    st.session_state['last_test_result'] = result
    
    with col2:
        st.markdown("#### 📊 Resultados")
        
        if 'last_test_result' in st.session_state:
            result = st.session_state['last_test_result']
            
            if 'error' in result:
                st.error(f"❌ {result['error']}")
            else:
                # Mostrar resultados según el tipo de prueba
                display_test_results(result)
        else:
            st.info("👈 Configura y ejecuta una prueba para ver los resultados aquí")

def render_correlation_regression(df, stat_analyzer):
    """Renderizar análisis de correlación y regresión"""
    
    st.markdown("### 🔗 Análisis de Correlación y Regresión")
    
    analysis_type = st.radio(
        "Tipo de análisis:",
        ["correlation", "regression"],
        format_func=lambda x: "🔗 Correlación" if x == "correlation" else "📈 Regresión Lineal"
    )
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### ⚙️ Configuración")
        
        if analysis_type == "correlation":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) < 2:
                st.error("❌ Se necesitan al menos 2 columnas numéricas")
                return
            
            var1 = st.selectbox("Primera variable:", numeric_cols)
            var2 = st.selectbox("Segunda variable:", 
                              [col for col in numeric_cols if col != var1])
            
            method = st.selectbox(
                "Método de correlación:",
                ["pearson", "spearman", "kendall"],
                format_func=lambda x: {
                    "pearson": "Pearson (lineal)",
                    "spearman": "Spearman (monotónica)",
                    "kendall": "Kendall (tau)"
                }[x]
            )
            
            alpha = st.slider("Nivel de significancia (α):", 0.01, 0.10, 0.05, 0.01)
            
            if st.button("🔗 Calcular Correlación", type="primary"):
                with st.spinner("Calculando correlación..."):
                    result = stat_analyzer.correlation_analysis(df, var1, var2, method, alpha)
                    st.session_state['last_correlation_result'] = result
        
        elif analysis_type == "regression":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) < 2:
                st.error("❌ Se necesitan al menos 2 columnas numéricas")
                return
            
            dependent_var = st.selectbox("Variable dependiente (Y):", numeric_cols)
            independent_vars = st.multiselect(
                "Variables independientes (X):",
                [col for col in numeric_cols if col != dependent_var],
                default=[col for col in numeric_cols if col != dependent_var][:1]
            )
            
            if not independent_vars:
                st.warning("⚠️ Selecciona al menos una variable independiente")
                return
            
            alpha = st.slider("Nivel de significancia (α):", 0.01, 0.10, 0.05, 0.01)
            
            if st.button("📈 Ejecutar Regresión", type="primary"):
                with st.spinner("Ejecutando regresión..."):
                    result = stat_analyzer.linear_regression(df, dependent_var, independent_vars, alpha)
                    st.session_state['last_regression_result'] = result
    
    with col2:
        st.markdown("#### 📊 Resultados")
        
        if analysis_type == "correlation" and 'last_correlation_result' in st.session_state:
            result = st.session_state['last_correlation_result']
            display_correlation_results(result, df)
        
        elif analysis_type == "regression" and 'last_regression_result' in st.session_state:
            result = st.session_state['last_regression_result']
            display_regression_results(result, df)
        
        else:
            st.info("👈 Configura y ejecuta un análisis para ver los resultados aquí")

def render_clustering_analysis(df, stat_analyzer):
    """Renderizar análisis de clustering"""
    
    st.markdown("### 🎯 Análisis de Clustering")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 2:
        st.error("❌ Se necesitan al menos 2 columnas numéricas para clustering")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### ⚙️ Configuración")
        
        variables = st.multiselect(
            "Variables para clustering:",
            numeric_cols,
            default=numeric_cols[:min(3, len(numeric_cols))]
        )
        
        if not variables:
            st.warning("⚠️ Selecciona al menos 2 variables")
            return
        
        n_clusters = st.slider("Número de clusters:", 2, 10, 3)
        
        # Método de clustering
        method = st.selectbox(
            "Método de clustering:",
            ["kmeans", "hierarchical"],
            format_func=lambda x: "K-means" if x == "kmeans" else "Jerárquico"
        )
        
        if st.button("🎯 Ejecutar Clustering", type="primary"):
            with st.spinner("Ejecutando clustering..."):
                if method == "kmeans":
                    result = stat_analyzer.kmeans_clustering(df, variables, n_clusters)
                    st.session_state['last_clustering_result'] = result
                else:
                    st.info("🚧 Clustering jerárquico en desarrollo")
    
    with col2:
        st.markdown("#### 📊 Resultados")
        
        if 'last_clustering_result' in st.session_state:
            result = st.session_state['last_clustering_result']
            display_clustering_results(result, df)
        else:
            st.info("👈 Configura y ejecuta clustering para ver los resultados aquí")

def render_analysis_configuration():
    """Renderizar configuración de análisis"""
    
    st.markdown("### ⚙️ Configuración de Análisis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎨 Configuración de Visualizaciones")
        
        # Configuración de colores
        color_palette = st.selectbox(
            "Paleta de colores:",
            ["plotly", "viridis", "plasma", "inferno", "magma", "cividis"],
            index=0
        )
        
        # Configuración de tema
        plot_theme = st.selectbox(
            "Tema de gráficos:",
            ["plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white"],
            index=0
        )
        
        # Tamaño de figuras
        figure_width = st.slider("Ancho de figuras:", 400, 1200, 800, 50)
        figure_height = st.slider("Alto de figuras:", 300, 800, 500, 50)
        
        # Guardar configuración
        if st.button("💾 Guardar Configuración Visual"):
            config = {
                'color_palette': color_palette,
                'plot_theme': plot_theme,
                'figure_width': figure_width,
                'figure_height': figure_height
            }
            st.session_state['plot_config'] = config
            st.success("✅ Configuración guardada")
    
    with col2:
        st.markdown("#### 📊 Configuración Estadística")
        
        # Nivel de significancia por defecto
        default_alpha = st.slider("Nivel de significancia por defecto:", 0.01, 0.10, 0.05, 0.01)
        
        # Configuración de clustering
        default_clusters = st.slider("Número de clusters por defecto:", 2, 10, 3)
        
        # Configuración de outliers
        outlier_method = st.selectbox(
            "Método de detección de outliers:",
            ["iqr", "zscore", "isolation_forest"],
            format_func=lambda x: {
                "iqr": "IQR (Rango Intercuartílico)",
                "zscore": "Z-Score",
                "isolation_forest": "Isolation Forest"
            }[x]
        )
        
        # Configuración de valores faltantes
        missing_strategy = st.selectbox(
            "Estrategia para valores faltantes:",
            ["drop", "mean", "median", "mode", "forward_fill"],
            format_func=lambda x: {
                "drop": "Eliminar filas",
                "mean": "Imputar con media",
                "median": "Imputar con mediana", 
                "mode": "Imputar con moda",
                "forward_fill": "Propagación hacia adelante"
            }[x]
        )
        
        # Guardar configuración estadística
        if st.button("💾 Guardar Configuración Estadística"):
            config = {
                'default_alpha': default_alpha,
                'default_clusters': default_clusters,
                'outlier_method': outlier_method,
                'missing_strategy': missing_strategy
            }
            st.session_state['stat_config'] = config
            st.success("✅ Configuración estadística guardada")
    
    # Mostrar configuración actual
    st.markdown("---")
    st.markdown("#### 📋 Configuración Actual")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'plot_config' in st.session_state:
            st.json(st.session_state['plot_config'])
        else:
            st.info("No hay configuración visual guardada")
    
    with col2:
        if 'stat_config' in st.session_state:
            st.json(st.session_state['stat_config'])
        else:
            st.info("No hay configuración estadística guardada")

def render_analysis_history(stat_analyzer):
    """Renderizar historial de análisis"""
    
    st.markdown("### 📚 Historial de Análisis")
    
    history = stat_analyzer.get_analysis_history()
    
    if not history:
        st.info("📝 No hay análisis en el historial")
        return
    
    # Mostrar resumen del historial
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Total de Análisis", len(history))
    
    with col2:
        test_types = [item.get('test_type', item.get('analysis_type', 'Desconocido')) for item in history]
        unique_types = len(set(test_types))
        st.metric("🔬 Tipos de Análisis", unique_types)
    
    with col3:
        if st.button("🗑️ Limpiar Historial"):
            stat_analyzer.clear_history()
            st.rerun()
    
    # Mostrar historial detallado
    st.markdown("#### 📋 Análisis Realizados")
    
    for i, analysis in enumerate(reversed(history)):
        with st.expander(f"📊 {analysis.get('test_type', analysis.get('analysis_type', 'Análisis'))} #{len(history)-i}"):
            
            # Información básica
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Tipo:** " + analysis.get('test_type', analysis.get('analysis_type', 'N/A')))
                
                if 'variable' in analysis:
                    st.markdown(f"**Variable:** {analysis['variable']}")
                elif 'variables' in analysis:
                    st.markdown(f"**Variables:** {', '.join(analysis['variables'])}")
                
                if 'sample_size' in analysis:
                    st.markdown(f"**Tamaño de muestra:** {analysis['sample_size']}")
            
            with col2:
                if 'p_value' in analysis:
                    st.markdown(f"**p-valor:** {analysis['p_value']:.4f}")
                
                if 'is_significant' in analysis:
                    significance = "✅ Significativo" if analysis['is_significant'] else "❌ No significativo"
                    st.markdown(f"**Resultado:** {significance}")
            
            # Interpretación
            if 'interpretation' in analysis:
                st.markdown("**Interpretación:**")
                st.info(analysis['interpretation'])
            
            # Botón para exportar resultado
            if st.button(f"📤 Exportar Análisis #{len(history)-i}", key=f"export_{i}"):
                export_analysis_result(analysis, len(history)-i)

def display_test_results(result):
    """Mostrar resultados de pruebas estadísticas"""
    
    if 'error' in result:
        st.error(f"❌ {result['error']}")
        return
    
    # Información básica
    st.markdown(f"**📊 {result['test_type']}**")
    
    # Métricas principales
    col1, col2, col3 = st.columns(3)
    
    if 't_statistic' in result:
        with col1:
            st.metric("Estadístico t", f"{result['t_statistic']:.4f}")
    elif 'f_statistic' in result:
        with col1:
            st.metric("Estadístico F", f"{result['f_statistic']:.4f}")
    elif 'chi2_statistic' in result:
        with col1:
            st.metric("Chi-cuadrado", f"{result['chi2_statistic']:.4f}")
    
    with col2:
        st.metric("p-valor", f"{result['p_value']:.4f}")
    
    with col3:
        significance = "✅ Significativo" if result['is_significant'] else "❌ No significativo"
        st.metric("Resultado", significance)
    
    # Interpretación
    if 'interpretation' in result:
        st.markdown("**📝 Interpretación:**")
        st.info(result['interpretation'])
    
    # Detalles específicos según el tipo de prueba
    if result['test_type'] == 'ANOVA de un factor' and 'group_statistics' in result:
        st.markdown("**📊 Estadísticas por Grupo:**")
        group_df = pd.DataFrame(result['group_statistics'])
        st.dataframe(group_df, use_container_width=True)
    
    elif 'contingency_table' in result:
        st.markdown("**📋 Tabla de Contingencia:**")
        contingency_df = pd.DataFrame(result['contingency_table'])
        st.dataframe(contingency_df, use_container_width=True)

def display_correlation_results(result, df):
    """Mostrar resultados de correlación"""
    
    if 'error' in result:
        st.error(f"❌ {result['error']}")
        return
    
    # Métricas principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Correlación", f"{result['correlation_coefficient']:.4f}")
    
    with col2:
        st.metric("p-valor", f"{result['p_value']:.4f}")
    
    with col3:
        significance = "✅ Significativo" if result['is_significant'] else "❌ No significativo"
        st.metric("Resultado", significance)
    
    # Interpretación
    st.markdown("**📝 Interpretación:**")
    st.info(result['interpretation'])
    
    # Gráfico de dispersión
    st.markdown("**📈 Gráfico de Dispersión:**")
    
    var1, var2 = result['variable_1'], result['variable_2']
    
    fig = px.scatter(
        df, 
        x=var1, 
        y=var2,
        title=f"Correlación entre {var1} y {var2}",
        trendline="ols"
    )
    
    fig.update_layout(
        template="plotly_white",
        title_font_size=16
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_regression_results(result, df):
    """Mostrar resultados de regresión"""
    
    if 'error' in result:
        st.error(f"❌ {result['error']}")
        return
    
    # Métricas principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("R²", f"{result['r_squared']:.4f}")
    
    with col2:
        st.metric("R² Ajustado", f"{result['adj_r_squared']:.4f}")
    
    with col3:
        st.metric("RMSE", f"{result['rmse']:.4f}")
    
    # Interpretación
    st.markdown("**📝 Interpretación:**")
    st.info(result['interpretation'])
    
    # Coeficientes
    st.markdown("**📊 Coeficientes:**")
    coef_data = []
    for var, coef in result['coefficients'].items():
        p_val = result['p_values'][var]
        ci = result['confidence_intervals'][var]
        coef_data.append({
            'Variable': var,
            'Coeficiente': f"{coef:.4f}",
            'p-valor': f"{p_val:.4f}",
            'IC 95%': f"[{ci[0]:.4f}, {ci[1]:.4f}]"
        })
    
    coef_df = pd.DataFrame(coef_data)
    st.dataframe(coef_df, use_container_width=True)

def display_clustering_results(result, df):
    """Mostrar resultados de clustering"""
    
    if 'error' in result:
        st.error(f"❌ {result['error']}")
        return
    
    # Métricas principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Clusters", result['n_clusters'])
    
    with col2:
        st.metric("Muestras", result['sample_size'])
    
    with col3:
        st.metric("Inercia", f"{result['inertia']:.2f}")
    
    # Estadísticas por cluster
    st.markdown("**📊 Estadísticas por Cluster:**")
    cluster_df = pd.DataFrame(result['cluster_statistics'])
    st.dataframe(cluster_df, use_container_width=True)
    
    # Visualización de clusters (si hay 2 o 3 variables)
    variables = result['variables']
    
    if len(variables) >= 2:
        st.markdown("**📈 Visualización de Clusters:**")
        
        # Crear DataFrame con clusters
        cluster_data = pd.DataFrame(result['data_with_clusters'])
        
        if len(variables) == 2:
            fig = px.scatter(
                cluster_data,
                x=variables[0],
                y=variables[1],
                color='cluster',
                title=f"Clusters: {variables[0]} vs {variables[1]}",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
        else:
            fig = px.scatter_3d(
                cluster_data,
                x=variables[0],
                y=variables[1],
                z=variables[2],
                color='cluster',
                title=f"Clusters 3D: {variables[0]}, {variables[1]}, {variables[2]}",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
        
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

def export_analysis_result(analysis, analysis_number):
    """Exportar resultado de análisis"""
    
    # Crear nombre de archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"analisis_{analysis_number}_{timestamp}.json"
    
    # Convertir a JSON
    analysis_json = json.dumps(analysis, indent=2, default=str, ensure_ascii=False)
    
    # Botón de descarga
    st.download_button(
        label=f"⬇️ Descargar {filename}",
        data=analysis_json,
        file_name=filename,
        mime="application/json"
    )

