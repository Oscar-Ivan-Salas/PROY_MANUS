#!/usr/bin/env python3
"""
Dashboard Tesis Pro - Módulo de Validación de Datos

Este módulo proporciona funciones para:
- Validación de datos de entrada
- Detección de problemas comunes
- Mensajes de error amigables
- Sugerencias de corrección
- Limpieza automática de datos
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
import warnings

class DataValidator:
    def __init__(self):
        self.validation_results = {}
        self.error_messages = []
        self.warnings = []
        self.suggestions = []
    
    def validate_dataframe(self, df, file_name="archivo"):
        """Validación completa de un DataFrame"""
        self.validation_results = {}
        self.error_messages = []
        self.warnings = []
        self.suggestions = []
        
        # Validaciones básicas
        self._validate_basic_structure(df, file_name)
        self._validate_data_types(df)
        self._validate_missing_values(df)
        self._validate_duplicates(df)
        self._validate_outliers(df)
        self._validate_data_consistency(df)
        self._validate_column_names(df)
        
        return {
            'is_valid': len(self.error_messages) == 0,
            'errors': self.error_messages,
            'warnings': self.warnings,
            'suggestions': self.suggestions,
            'validation_details': self.validation_results
        }
    
    def _validate_basic_structure(self, df, file_name):
        """Validar estructura básica del DataFrame"""
        try:
            # Verificar que no esté vacío
            if df.empty:
                self.error_messages.append({
                    'type': 'estructura',
                    'severity': 'error',
                    'message': f"❌ El archivo '{file_name}' está vacío",
                    'suggestion': "Verifica que el archivo contenga datos válidos"
                })
                return
            
            # Verificar dimensiones mínimas
            if len(df) < 2:
                self.warnings.append({
                    'type': 'estructura',
                    'severity': 'warning',
                    'message': f"⚠️ El archivo '{file_name}' tiene muy pocas filas ({len(df)})",
                    'suggestion': "Se recomiendan al menos 10 filas para análisis estadísticos"
                })
            
            if len(df.columns) < 1:
                self.error_messages.append({
                    'type': 'estructura',
                    'severity': 'error',
                    'message': f"❌ El archivo '{file_name}' no tiene columnas",
                    'suggestion': "Verifica el formato del archivo"
                })
                return
            
            # Información básica
            self.validation_results['basic_info'] = {
                'rows': len(df),
                'columns': len(df.columns),
                'size_mb': df.memory_usage(deep=True).sum() / 1024**2,
                'is_large': len(df) > 100000
            }
            
            # Advertencia para archivos grandes
            if len(df) > 100000:
                self.warnings.append({
                    'type': 'rendimiento',
                    'severity': 'warning',
                    'message': f"⚠️ Archivo grande detectado ({len(df):,} filas)",
                    'suggestion': "El procesamiento puede ser lento. Considera usar una muestra para pruebas iniciales"
                })
            
        except Exception as e:
            self.error_messages.append({
                'type': 'estructura',
                'severity': 'error',
                'message': f"❌ Error al validar estructura: {str(e)}",
                'suggestion': "Verifica que el archivo esté en un formato compatible"
            })
    
    def _validate_data_types(self, df):
        """Validar tipos de datos"""
        try:
            type_info = {}
            problematic_columns = []
            
            for column in df.columns:
                col_data = df[column]
                dtype = str(col_data.dtype)
                
                # Detectar columnas que deberían ser numéricas
                if dtype == 'object':
                    # Verificar si contiene números como strings
                    non_null_values = col_data.dropna()
                    if len(non_null_values) > 0:
                        # Intentar convertir a numérico
                        numeric_convertible = 0
                        for value in non_null_values.head(100):  # Muestra de 100 valores
                            try:
                                float(str(value).replace(',', '.').replace(' ', ''))
                                numeric_convertible += 1
                            except:
                                pass
                        
                        if numeric_convertible / len(non_null_values.head(100)) > 0.8:
                            problematic_columns.append({
                                'column': column,
                                'issue': 'numeric_as_text',
                                'convertible_ratio': numeric_convertible / len(non_null_values.head(100))
                            })
                
                # Detectar fechas como strings
                if dtype == 'object':
                    sample_values = col_data.dropna().head(10)
                    date_like_count = 0
                    for value in sample_values:
                        if self._looks_like_date(str(value)):
                            date_like_count += 1
                    
                    if date_like_count / len(sample_values) > 0.5 and len(sample_values) > 0:
                        problematic_columns.append({
                            'column': column,
                            'issue': 'date_as_text',
                            'date_like_ratio': date_like_count / len(sample_values)
                        })
                
                type_info[column] = {
                    'dtype': dtype,
                    'non_null_count': col_data.count(),
                    'unique_count': col_data.nunique()
                }
            
            self.validation_results['data_types'] = type_info
            
            # Generar sugerencias para columnas problemáticas
            for prob_col in problematic_columns:
                if prob_col['issue'] == 'numeric_as_text':
                    self.suggestions.append({
                        'type': 'tipo_datos',
                        'severity': 'suggestion',
                        'message': f"💡 La columna '{prob_col['column']}' parece contener números como texto",
                        'suggestion': f"Considera convertir a numérico. {prob_col['convertible_ratio']:.1%} de los valores son convertibles"
                    })
                elif prob_col['issue'] == 'date_as_text':
                    self.suggestions.append({
                        'type': 'tipo_datos',
                        'severity': 'suggestion',
                        'message': f"💡 La columna '{prob_col['column']}' parece contener fechas como texto",
                        'suggestion': "Considera convertir a tipo datetime para análisis temporales"
                    })
            
        except Exception as e:
            self.error_messages.append({
                'type': 'tipos_datos',
                'severity': 'error',
                'message': f"❌ Error al validar tipos de datos: {str(e)}",
                'suggestion': "Revisa el formato de los datos en el archivo"
            })
    
    def _validate_missing_values(self, df):
        """Validar valores faltantes"""
        try:
            missing_info = {}
            critical_missing = []
            
            for column in df.columns:
                missing_count = df[column].isnull().sum()
                missing_pct = (missing_count / len(df)) * 100
                
                missing_info[column] = {
                    'missing_count': missing_count,
                    'missing_percentage': missing_pct,
                    'has_missing': missing_count > 0
                }
                
                # Identificar columnas con muchos valores faltantes
                if missing_pct > 50:
                    critical_missing.append({
                        'column': column,
                        'missing_pct': missing_pct
                    })
                elif missing_pct > 20:
                    self.warnings.append({
                        'type': 'valores_faltantes',
                        'severity': 'warning',
                        'message': f"⚠️ La columna '{column}' tiene {missing_pct:.1f}% de valores faltantes",
                        'suggestion': "Considera estrategias de imputación o eliminación de esta columna"
                    })
            
            self.validation_results['missing_values'] = missing_info
            
            # Errores críticos por demasiados valores faltantes
            for crit in critical_missing:
                self.error_messages.append({
                    'type': 'valores_faltantes',
                    'severity': 'error',
                    'message': f"❌ La columna '{crit['column']}' tiene {crit['missing_pct']:.1f}% de valores faltantes",
                    'suggestion': "Esta columna no es útil para análisis. Considera eliminarla"
                })
            
            # Sugerencia general si hay valores faltantes
            total_missing = sum([info['missing_count'] for info in missing_info.values()])
            if total_missing > 0:
                self.suggestions.append({
                    'type': 'valores_faltantes',
                    'severity': 'suggestion',
                    'message': f"💡 Se detectaron {total_missing} valores faltantes en total",
                    'suggestion': "Revisa las estrategias de manejo de valores faltantes antes del análisis"
                })
            
        except Exception as e:
            self.error_messages.append({
                'type': 'valores_faltantes',
                'severity': 'error',
                'message': f"❌ Error al validar valores faltantes: {str(e)}",
                'suggestion': "Verifica la integridad de los datos"
            })
    
    def _validate_duplicates(self, df):
        """Validar filas duplicadas"""
        try:
            duplicate_count = df.duplicated().sum()
            duplicate_pct = (duplicate_count / len(df)) * 100
            
            self.validation_results['duplicates'] = {
                'duplicate_count': duplicate_count,
                'duplicate_percentage': duplicate_pct,
                'has_duplicates': duplicate_count > 0
            }
            
            if duplicate_count > 0:
                if duplicate_pct > 10:
                    self.warnings.append({
                        'type': 'duplicados',
                        'severity': 'warning',
                        'message': f"⚠️ Se encontraron {duplicate_count} filas duplicadas ({duplicate_pct:.1f}%)",
                        'suggestion': "Considera eliminar duplicados antes del análisis"
                    })
                else:
                    self.suggestions.append({
                        'type': 'duplicados',
                        'severity': 'suggestion',
                        'message': f"💡 Se encontraron {duplicate_count} filas duplicadas ({duplicate_pct:.1f}%)",
                        'suggestion': "Revisa si los duplicados son intencionales"
                    })
            
        except Exception as e:
            self.error_messages.append({
                'type': 'duplicados',
                'severity': 'error',
                'message': f"❌ Error al validar duplicados: {str(e)}",
                'suggestion': "Verifica la estructura de los datos"
            })
    
    def _validate_outliers(self, df):
        """Detectar valores atípicos en columnas numéricas"""
        try:
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            outlier_info = {}
            
            for column in numeric_columns:
                col_data = df[column].dropna()
                if len(col_data) < 4:  # Necesitamos al menos 4 valores
                    continue
                
                # Método IQR
                Q1 = col_data.quantile(0.25)
                Q3 = col_data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
                outlier_count = len(outliers)
                outlier_pct = (outlier_count / len(col_data)) * 100
                
                outlier_info[column] = {
                    'outlier_count': outlier_count,
                    'outlier_percentage': outlier_pct,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound,
                    'has_outliers': outlier_count > 0
                }
                
                if outlier_pct > 5:  # Más del 5% son outliers
                    self.warnings.append({
                        'type': 'outliers',
                        'severity': 'warning',
                        'message': f"⚠️ La columna '{column}' tiene {outlier_count} valores atípicos ({outlier_pct:.1f}%)",
                        'suggestion': "Revisa estos valores antes del análisis estadístico"
                    })
                elif outlier_count > 0:
                    self.suggestions.append({
                        'type': 'outliers',
                        'severity': 'suggestion',
                        'message': f"💡 La columna '{column}' tiene {outlier_count} valores atípicos",
                        'suggestion': "Considera si estos valores son errores o datos válidos"
                    })
            
            self.validation_results['outliers'] = outlier_info
            
        except Exception as e:
            self.error_messages.append({
                'type': 'outliers',
                'severity': 'error',
                'message': f"❌ Error al detectar outliers: {str(e)}",
                'suggestion': "Verifica que las columnas numéricas tengan datos válidos"
            })
    
    def _validate_data_consistency(self, df):
        """Validar consistencia de datos"""
        try:
            consistency_issues = []
            
            # Verificar columnas con pocos valores únicos (posibles categóricas)
            for column in df.columns:
                col_data = df[column].dropna()
                if len(col_data) == 0:
                    continue
                
                unique_ratio = col_data.nunique() / len(col_data)
                
                # Posible variable categórica con muchos valores únicos
                if col_data.dtype == 'object' and unique_ratio > 0.8 and col_data.nunique() > 50:
                    consistency_issues.append({
                        'column': column,
                        'issue': 'high_cardinality_categorical',
                        'unique_count': col_data.nunique(),
                        'unique_ratio': unique_ratio
                    })
                
                # Posible variable numérica con pocos valores únicos
                elif col_data.dtype in ['int64', 'float64'] and col_data.nunique() < 10 and len(col_data) > 100:
                    consistency_issues.append({
                        'column': column,
                        'issue': 'low_cardinality_numeric',
                        'unique_count': col_data.nunique(),
                        'unique_ratio': unique_ratio
                    })
            
            # Generar sugerencias
            for issue in consistency_issues:
                if issue['issue'] == 'high_cardinality_categorical':
                    self.suggestions.append({
                        'type': 'consistencia',
                        'severity': 'suggestion',
                        'message': f"💡 La columna '{issue['column']}' tiene muchos valores únicos ({issue['unique_count']})",
                        'suggestion': "Podría ser un identificador. Considera si es útil para análisis"
                    })
                elif issue['issue'] == 'low_cardinality_numeric':
                    self.suggestions.append({
                        'type': 'consistencia',
                        'severity': 'suggestion',
                        'message': f"💡 La columna numérica '{issue['column']}' tiene pocos valores únicos ({issue['unique_count']})",
                        'suggestion': "Podría ser una variable categórica codificada numéricamente"
                    })
            
            self.validation_results['consistency'] = consistency_issues
            
        except Exception as e:
            self.error_messages.append({
                'type': 'consistencia',
                'severity': 'error',
                'message': f"❌ Error al validar consistencia: {str(e)}",
                'suggestion': "Revisa la estructura y tipos de datos"
            })
    
    def _validate_column_names(self, df):
        """Validar nombres de columnas"""
        try:
            column_issues = []
            
            for column in df.columns:
                issues = []
                
                # Espacios al inicio o final
                if column != column.strip():
                    issues.append('trailing_spaces')
                
                # Caracteres especiales problemáticos
                if re.search(r'[^\w\s\-_]', column):
                    issues.append('special_characters')
                
                # Nombres muy largos
                if len(column) > 50:
                    issues.append('too_long')
                
                # Nombres muy cortos o poco descriptivos
                if len(column) < 2:
                    issues.append('too_short')
                
                # Nombres que parecen códigos
                if re.match(r'^[A-Z]{1,3}\d+$', column):
                    issues.append('code_like')
                
                if issues:
                    column_issues.append({
                        'column': column,
                        'issues': issues
                    })
            
            # Generar sugerencias
            for col_issue in column_issues:
                column = col_issue['column']
                issues = col_issue['issues']
                
                if 'trailing_spaces' in issues:
                    self.suggestions.append({
                        'type': 'nombres_columnas',
                        'severity': 'suggestion',
                        'message': f"💡 La columna '{column}' tiene espacios al inicio o final",
                        'suggestion': "Considera limpiar los nombres de columnas"
                    })
                
                if 'special_characters' in issues:
                    self.suggestions.append({
                        'type': 'nombres_columnas',
                        'severity': 'suggestion',
                        'message': f"💡 La columna '{column}' contiene caracteres especiales",
                        'suggestion': "Usa solo letras, números, guiones y guiones bajos"
                    })
                
                if 'too_long' in issues:
                    self.suggestions.append({
                        'type': 'nombres_columnas',
                        'severity': 'suggestion',
                        'message': f"💡 La columna '{column}' tiene un nombre muy largo",
                        'suggestion': "Considera usar un nombre más corto y descriptivo"
                    })
                
                if 'code_like' in issues:
                    self.suggestions.append({
                        'type': 'nombres_columnas',
                        'severity': 'suggestion',
                        'message': f"💡 La columna '{column}' parece ser un código",
                        'suggestion': "Considera usar un nombre más descriptivo"
                    })
            
            self.validation_results['column_names'] = column_issues
            
        except Exception as e:
            self.error_messages.append({
                'type': 'nombres_columnas',
                'severity': 'error',
                'message': f"❌ Error al validar nombres de columnas: {str(e)}",
                'suggestion': "Verifica que los nombres de columnas sean válidos"
            })
    
    def _looks_like_date(self, value):
        """Verificar si un valor parece una fecha"""
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # DD/MM/YYYY
            r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
            r'\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, str(value)):
                return True
        return False
    
    def get_validation_summary(self):
        """Obtener resumen de validación"""
        return {
            'total_errors': len(self.error_messages),
            'total_warnings': len(self.warnings),
            'total_suggestions': len(self.suggestions),
            'is_ready_for_analysis': len(self.error_messages) == 0,
            'validation_score': self._calculate_validation_score()
        }
    
    def _calculate_validation_score(self):
        """Calcular puntuación de calidad de datos (0-100)"""
        score = 100
        
        # Penalizar errores
        score -= len(self.error_messages) * 20
        
        # Penalizar advertencias
        score -= len(self.warnings) * 5
        
        # Penalizar sugerencias (menos)
        score -= len(self.suggestions) * 1
        
        return max(0, min(100, score))
    
    def suggest_data_cleaning(self, df):
        """Sugerir acciones de limpieza de datos"""
        cleaning_suggestions = []
        
        # Sugerir eliminación de duplicados
        if df.duplicated().sum() > 0:
            cleaning_suggestions.append({
                'action': 'remove_duplicates',
                'description': 'Eliminar filas duplicadas',
                'code': 'df = df.drop_duplicates()'
            })
        
        # Sugerir manejo de valores faltantes
        missing_cols = df.columns[df.isnull().any()].tolist()
        if missing_cols:
            cleaning_suggestions.append({
                'action': 'handle_missing',
                'description': f'Manejar valores faltantes en: {", ".join(missing_cols)}',
                'code': 'df = df.dropna()  # o usar df.fillna()'
            })
        
        # Sugerir conversión de tipos
        for column in df.columns:
            if df[column].dtype == 'object':
                # Intentar detectar si debería ser numérico
                try:
                    pd.to_numeric(df[column], errors='coerce')
                    cleaning_suggestions.append({
                        'action': 'convert_numeric',
                        'description': f'Convertir {column} a numérico',
                        'code': f'df["{column}"] = pd.to_numeric(df["{column}"], errors="coerce")'
                    })
                except:
                    pass
        
        return cleaning_suggestions
    
    def create_validation_report(self, df, file_name="archivo"):
        """Crear reporte completo de validación"""
        validation_result = self.validate_dataframe(df, file_name)
        summary = self.get_validation_summary()
        cleaning_suggestions = self.suggest_data_cleaning(df)
        
        report = {
            'file_name': file_name,
            'validation_timestamp': datetime.now().isoformat(),
            'summary': summary,
            'validation_result': validation_result,
            'cleaning_suggestions': cleaning_suggestions,
            'data_profile': {
                'shape': df.shape,
                'dtypes': df.dtypes.astype(str).to_dict(),
                'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
                'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
                'categorical_columns': df.select_dtypes(include=['object', 'category']).columns.tolist()
            }
        }
        
        return report

