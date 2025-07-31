#!/usr/bin/env python3
"""
Dashboard Tesis Pro - Módulo de Análisis Estadísticos Inferenciales

Este módulo implementa análisis estadísticos avanzados:
- Pruebas t (una muestra, dos muestras, pareadas)
- ANOVA (uno y múltiples factores)
- Pruebas de chi-cuadrado
- Análisis de correlación
- Regresión lineal y múltiple
- Clustering (K-means, jerárquico)
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency, pearsonr, spearmanr, kendalltau
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import r2_score, mean_squared_error, classification_report
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class StatisticalAnalysis:
    def __init__(self):
        self.results_history = []
    
    def t_test_one_sample(self, data, column, test_value, alpha=0.05):
        """Prueba t de una muestra"""
        try:
            sample_data = data[column].dropna()
            
            # Realizar prueba t
            t_stat, p_value = stats.ttest_1samp(sample_data, test_value)
            
            # Calcular estadísticas descriptivas
            n = len(sample_data)
            mean = sample_data.mean()
            std = sample_data.std()
            se = std / np.sqrt(n)
            
            # Intervalo de confianza
            ci = stats.t.interval(1-alpha, n-1, loc=mean, scale=se)
            
            # Interpretación
            is_significant = p_value < alpha
            effect_size = (mean - test_value) / std  # Cohen's d
            
            result = {
                'test_type': 'Prueba t de una muestra',
                'variable': column,
                'test_value': test_value,
                'sample_size': n,
                'sample_mean': mean,
                'sample_std': std,
                'standard_error': se,
                't_statistic': t_stat,
                'p_value': p_value,
                'alpha': alpha,
                'is_significant': is_significant,
                'confidence_interval': ci,
                'effect_size': effect_size,
                'interpretation': self._interpret_t_test_one_sample(mean, test_value, p_value, alpha)
            }
            
            self.results_history.append(result)
            return result
            
        except Exception as e:
            return {'error': f"Error en prueba t de una muestra: {str(e)}"}
    
    def t_test_two_samples(self, data, column, group_column, alpha=0.05, equal_var=True):
        """Prueba t de dos muestras independientes"""
        try:
            groups = data[group_column].unique()
            if len(groups) != 2:
                return {'error': 'La variable de agrupación debe tener exactamente 2 grupos'}
            
            group1_data = data[data[group_column] == groups[0]][column].dropna()
            group2_data = data[data[group_column] == groups[1]][column].dropna()
            
            # Realizar prueba t
            if equal_var:
                t_stat, p_value = stats.ttest_ind(group1_data, group2_data, equal_var=True)
            else:
                t_stat, p_value = stats.ttest_ind(group1_data, group2_data, equal_var=False)
            
            # Estadísticas descriptivas
            n1, n2 = len(group1_data), len(group2_data)
            mean1, mean2 = group1_data.mean(), group2_data.mean()
            std1, std2 = group1_data.std(), group2_data.std()
            
            # Tamaño del efecto (Cohen's d)
            pooled_std = np.sqrt(((n1-1)*std1**2 + (n2-1)*std2**2) / (n1+n2-2))
            effect_size = (mean1 - mean2) / pooled_std
            
            result = {
                'test_type': 'Prueba t de dos muestras independientes',
                'variable': column,
                'group_variable': group_column,
                'groups': list(groups),
                'sample_sizes': [n1, n2],
                'means': [mean1, mean2],
                'std_devs': [std1, std2],
                't_statistic': t_stat,
                'p_value': p_value,
                'alpha': alpha,
                'is_significant': p_value < alpha,
                'effect_size': effect_size,
                'equal_variances': equal_var,
                'interpretation': self._interpret_t_test_two_samples(mean1, mean2, p_value, alpha)
            }
            
            self.results_history.append(result)
            return result
            
        except Exception as e:
            return {'error': f"Error en prueba t de dos muestras: {str(e)}"}
    
    def anova_one_way(self, data, dependent_var, independent_var, alpha=0.05):
        """ANOVA de un factor"""
        try:
            # Preparar datos
            groups = []
            group_names = []
            
            for group_name in data[independent_var].unique():
                group_data = data[data[independent_var] == group_name][dependent_var].dropna()
                if len(group_data) > 0:
                    groups.append(group_data)
                    group_names.append(group_name)
            
            if len(groups) < 2:
                return {'error': 'Se necesitan al menos 2 grupos para ANOVA'}
            
            # Realizar ANOVA
            f_stat, p_value = stats.f_oneway(*groups)
            
            # Estadísticas descriptivas por grupo
            group_stats = []
            for i, group in enumerate(groups):
                group_stats.append({
                    'group': group_names[i],
                    'n': len(group),
                    'mean': group.mean(),
                    'std': group.std(),
                    'min': group.min(),
                    'max': group.max()
                })
            
            # Eta cuadrado (tamaño del efecto)
            ss_between = sum([len(group) * (group.mean() - data[dependent_var].mean())**2 for group in groups])
            ss_total = sum([(x - data[dependent_var].mean())**2 for group in groups for x in group])
            eta_squared = ss_between / ss_total if ss_total > 0 else 0
            
            result = {
                'test_type': 'ANOVA de un factor',
                'dependent_variable': dependent_var,
                'independent_variable': independent_var,
                'groups': group_names,
                'group_statistics': group_stats,
                'f_statistic': f_stat,
                'p_value': p_value,
                'alpha': alpha,
                'is_significant': p_value < alpha,
                'eta_squared': eta_squared,
                'interpretation': self._interpret_anova(f_stat, p_value, alpha, eta_squared)
            }
            
            self.results_history.append(result)
            return result
            
        except Exception as e:
            return {'error': f"Error en ANOVA: {str(e)}"}
    
    def chi_square_test(self, data, var1, var2, alpha=0.05):
        """Prueba de chi-cuadrado de independencia"""
        try:
            # Crear tabla de contingencia
            contingency_table = pd.crosstab(data[var1], data[var2])
            
            # Realizar prueba de chi-cuadrado
            chi2, p_value, dof, expected = chi2_contingency(contingency_table)
            
            # Calcular V de Cramer (tamaño del efecto)
            n = contingency_table.sum().sum()
            cramers_v = np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))
            
            result = {
                'test_type': 'Prueba de chi-cuadrado de independencia',
                'variable_1': var1,
                'variable_2': var2,
                'contingency_table': contingency_table.to_dict(),
                'expected_frequencies': pd.DataFrame(expected, 
                                                   index=contingency_table.index,
                                                   columns=contingency_table.columns).to_dict(),
                'chi2_statistic': chi2,
                'p_value': p_value,
                'degrees_of_freedom': dof,
                'alpha': alpha,
                'is_significant': p_value < alpha,
                'cramers_v': cramers_v,
                'interpretation': self._interpret_chi_square(chi2, p_value, alpha, cramers_v)
            }
            
            self.results_history.append(result)
            return result
            
        except Exception as e:
            return {'error': f"Error en prueba de chi-cuadrado: {str(e)}"}
    
    def correlation_analysis(self, data, var1, var2, method='pearson', alpha=0.05):
        """Análisis de correlación"""
        try:
            # Filtrar datos válidos
            valid_data = data[[var1, var2]].dropna()
            
            if len(valid_data) < 3:
                return {'error': 'Se necesitan al menos 3 observaciones válidas'}
            
            # Calcular correlación según el método
            if method == 'pearson':
                corr_coef, p_value = pearsonr(valid_data[var1], valid_data[var2])
            elif method == 'spearman':
                corr_coef, p_value = spearmanr(valid_data[var1], valid_data[var2])
            elif method == 'kendall':
                corr_coef, p_value = kendalltau(valid_data[var1], valid_data[var2])
            else:
                return {'error': 'Método no válido. Use: pearson, spearman, o kendall'}
            
            # Interpretación de la fuerza de correlación
            strength = self._interpret_correlation_strength(abs(corr_coef))
            
            result = {
                'test_type': f'Correlación de {method.capitalize()}',
                'variable_1': var1,
                'variable_2': var2,
                'method': method,
                'sample_size': len(valid_data),
                'correlation_coefficient': corr_coef,
                'p_value': p_value,
                'alpha': alpha,
                'is_significant': p_value < alpha,
                'strength': strength,
                'interpretation': self._interpret_correlation(corr_coef, p_value, alpha, strength)
            }
            
            self.results_history.append(result)
            return result
            
        except Exception as e:
            return {'error': f"Error en análisis de correlación: {str(e)}"}
    
    def linear_regression(self, data, dependent_var, independent_vars, alpha=0.05):
        """Análisis de regresión lineal"""
        try:
            # Preparar datos
            if isinstance(independent_vars, str):
                independent_vars = [independent_vars]
            
            # Filtrar datos válidos
            all_vars = [dependent_var] + independent_vars
            valid_data = data[all_vars].dropna()
            
            if len(valid_data) < len(independent_vars) + 2:
                return {'error': 'Datos insuficientes para regresión'}
            
            X = valid_data[independent_vars]
            y = valid_data[dependent_var]
            
            # Agregar constante para el intercepto
            X_with_const = sm.add_constant(X)
            
            # Ajustar modelo
            model = sm.OLS(y, X_with_const).fit()
            
            # Predicciones
            y_pred = model.predict(X_with_const)
            
            # Métricas
            r_squared = model.rsquared
            adj_r_squared = model.rsquared_adj
            mse = mean_squared_error(y, y_pred)
            rmse = np.sqrt(mse)
            
            result = {
                'test_type': 'Regresión lineal',
                'dependent_variable': dependent_var,
                'independent_variables': independent_vars,
                'sample_size': len(valid_data),
                'r_squared': r_squared,
                'adj_r_squared': adj_r_squared,
                'mse': mse,
                'rmse': rmse,
                'f_statistic': model.fvalue,
                'f_p_value': model.f_pvalue,
                'coefficients': dict(zip(['const'] + independent_vars, model.params)),
                'p_values': dict(zip(['const'] + independent_vars, model.pvalues)),
                'confidence_intervals': dict(zip(['const'] + independent_vars, 
                                                model.conf_int().values.tolist())),
                'is_significant': model.f_pvalue < alpha,
                'summary': str(model.summary()),
                'interpretation': self._interpret_regression(r_squared, model.f_pvalue, alpha)
            }
            
            self.results_history.append(result)
            return result
            
        except Exception as e:
            return {'error': f"Error en regresión lineal: {str(e)}"}
    
    def kmeans_clustering(self, data, variables, n_clusters=3, random_state=42):
        """Análisis de clustering K-means"""
        try:
            # Preparar datos
            cluster_data = data[variables].dropna()
            
            if len(cluster_data) < n_clusters:
                return {'error': f'Se necesitan al menos {n_clusters} observaciones'}
            
            # Estandarizar datos
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(cluster_data)
            
            # Aplicar K-means
            kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
            cluster_labels = kmeans.fit_predict(scaled_data)
            
            # Agregar etiquetas al dataframe original
            result_data = cluster_data.copy()
            result_data['cluster'] = cluster_labels
            
            # Calcular centroides en escala original
            centroids_scaled = kmeans.cluster_centers_
            centroids = scaler.inverse_transform(centroids_scaled)
            
            # Estadísticas por cluster
            cluster_stats = []
            for i in range(n_clusters):
                cluster_subset = result_data[result_data['cluster'] == i]
                stats_dict = {
                    'cluster': i,
                    'size': len(cluster_subset),
                    'percentage': len(cluster_subset) / len(result_data) * 100
                }
                
                for var in variables:
                    stats_dict[f'{var}_mean'] = cluster_subset[var].mean()
                    stats_dict[f'{var}_std'] = cluster_subset[var].std()
                
                cluster_stats.append(stats_dict)
            
            # Inercia (suma de distancias cuadradas a centroides)
            inertia = kmeans.inertia_
            
            result = {
                'analysis_type': 'K-means Clustering',
                'variables': variables,
                'n_clusters': n_clusters,
                'sample_size': len(cluster_data),
                'cluster_labels': cluster_labels.tolist(),
                'centroids': centroids.tolist(),
                'cluster_statistics': cluster_stats,
                'inertia': inertia,
                'data_with_clusters': result_data.to_dict('records')
            }
            
            self.results_history.append(result)
            return result
            
        except Exception as e:
            return {'error': f"Error en clustering K-means: {str(e)}"}
    
    def create_statistical_visualizations(self, result, data=None):
        """Crear visualizaciones para resultados estadísticos"""
        try:
            test_type = result.get('test_type', result.get('analysis_type', ''))
            
            if 'Prueba t' in test_type:
                return self._create_t_test_viz(result, data)
            elif 'ANOVA' in test_type:
                return self._create_anova_viz(result, data)
            elif 'chi-cuadrado' in test_type:
                return self._create_chi_square_viz(result)
            elif 'Correlación' in test_type:
                return self._create_correlation_viz(result, data)
            elif 'Regresión' in test_type:
                return self._create_regression_viz(result, data)
            elif 'Clustering' in test_type:
                return self._create_clustering_viz(result)
            else:
                return None
                
        except Exception as e:
            return None
    
    # Métodos de interpretación
    def _interpret_t_test_one_sample(self, sample_mean, test_value, p_value, alpha):
        if p_value < alpha:
            direction = "mayor" if sample_mean > test_value else "menor"
            return f"La media muestral ({sample_mean:.3f}) es significativamente {direction} que el valor de prueba ({test_value}) (p = {p_value:.4f})."
        else:
            return f"No hay evidencia suficiente para concluir que la media poblacional difiere de {test_value} (p = {p_value:.4f})."
    
    def _interpret_t_test_two_samples(self, mean1, mean2, p_value, alpha):
        if p_value < alpha:
            higher_group = "Grupo 1" if mean1 > mean2 else "Grupo 2"
            return f"Existe una diferencia significativa entre los grupos (p = {p_value:.4f}). {higher_group} tiene una media mayor."
        else:
            return f"No hay evidencia suficiente de diferencia entre los grupos (p = {p_value:.4f})."
    
    def _interpret_anova(self, f_stat, p_value, alpha, eta_squared):
        if p_value < alpha:
            effect_size = "pequeño" if eta_squared < 0.06 else "mediano" if eta_squared < 0.14 else "grande"
            return f"Existe al menos una diferencia significativa entre los grupos (F = {f_stat:.3f}, p = {p_value:.4f}). Tamaño del efecto: {effect_size} (η² = {eta_squared:.3f})."
        else:
            return f"No hay evidencia de diferencias significativas entre los grupos (F = {f_stat:.3f}, p = {p_value:.4f})."
    
    def _interpret_chi_square(self, chi2, p_value, alpha, cramers_v):
        if p_value < alpha:
            strength = "débil" if cramers_v < 0.3 else "moderada" if cramers_v < 0.5 else "fuerte"
            return f"Existe una asociación significativa entre las variables (χ² = {chi2:.3f}, p = {p_value:.4f}). Fuerza de asociación: {strength} (V = {cramers_v:.3f})."
        else:
            return f"No hay evidencia de asociación entre las variables (χ² = {chi2:.3f}, p = {p_value:.4f})."
    
    def _interpret_correlation_strength(self, abs_corr):
        if abs_corr < 0.1:
            return "muy débil"
        elif abs_corr < 0.3:
            return "débil"
        elif abs_corr < 0.5:
            return "moderada"
        elif abs_corr < 0.7:
            return "fuerte"
        else:
            return "muy fuerte"
    
    def _interpret_correlation(self, corr_coef, p_value, alpha, strength):
        direction = "positiva" if corr_coef > 0 else "negativa"
        if p_value < alpha:
            return f"Existe una correlación {direction} {strength} y estadísticamente significativa (r = {corr_coef:.3f}, p = {p_value:.4f})."
        else:
            return f"La correlación {direction} {strength} no es estadísticamente significativa (r = {corr_coef:.3f}, p = {p_value:.4f})."
    
    def _interpret_regression(self, r_squared, f_p_value, alpha):
        if f_p_value < alpha:
            variance_explained = r_squared * 100
            return f"El modelo es estadísticamente significativo (p = {f_p_value:.4f}) y explica {variance_explained:.1f}% de la varianza en la variable dependiente."
        else:
            return f"El modelo no es estadísticamente significativo (p = {f_p_value:.4f})."
    
    # Métodos de visualización (simplificados)
    def _create_t_test_viz(self, result, data):
        # Implementar visualización para prueba t
        return None
    
    def _create_anova_viz(self, result, data):
        # Implementar visualización para ANOVA
        return None
    
    def _create_chi_square_viz(self, result):
        # Implementar visualización para chi-cuadrado
        return None
    
    def _create_correlation_viz(self, result, data):
        # Implementar visualización para correlación
        return None
    
    def _create_regression_viz(self, result, data):
        # Implementar visualización para regresión
        return None
    
    def _create_clustering_viz(self, result):
        # Implementar visualización para clustering
        return None
    
    def get_analysis_history(self):
        """Obtener historial de análisis"""
        return self.results_history
    
    def clear_history(self):
        """Limpiar historial de análisis"""
        self.results_history = []
    
    def export_results(self, results, format='dict'):
        """Exportar resultados en diferentes formatos"""
        if format == 'dict':
            return results
        elif format == 'dataframe':
            return pd.DataFrame([results])
        elif format == 'json':
            import json
            return json.dumps(results, indent=2, default=str)
        else:
            return results

