#!/usr/bin/env python3
"""
Dashboard Tesis Pro - Generador de Datos de Ejemplo

Este script genera datasets de ejemplo para probar el módulo de análisis:
- Datos de encuesta de estudiantes
- Datos de ventas
- Datos de experimento científico
- Datos con problemas comunes (valores faltantes, outliers, etc.)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

def generate_student_survey_data(n_students=500):
    """Generar datos de encuesta de estudiantes universitarios"""
    np.random.seed(42)
    random.seed(42)
    
    # Listas de valores categóricos
    carreras = ['Ingeniería', 'Medicina', 'Derecho', 'Psicología', 'Administración', 'Educación']
    ciudades = ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao', 'Málaga']
    generos = ['Masculino', 'Femenino', 'Otro']
    
    data = []
    
    for i in range(n_students):
        # Datos demográficos
        edad = np.random.normal(22, 3)
        edad = max(18, min(35, int(edad)))  # Limitar entre 18 y 35
        
        genero = np.random.choice(generos, p=[0.45, 0.50, 0.05])
        carrera = np.random.choice(carreras)
        ciudad = np.random.choice(ciudades)
        
        # Datos académicos (correlacionados)
        base_performance = np.random.normal(7.5, 1.5)
        
        # Horas de estudio influyen en las notas
        horas_estudio = max(0, np.random.normal(25, 10))
        nota_promedio = base_performance + (horas_estudio - 25) * 0.05 + np.random.normal(0, 0.5)
        nota_promedio = max(0, min(10, nota_promedio))
        
        # Satisfacción correlacionada con notas
        satisfaccion = min(10, max(1, nota_promedio + np.random.normal(0, 1)))
        
        # Datos económicos
        ingresos_familia = np.random.lognormal(9, 0.5)  # Distribución log-normal
        trabaja = np.random.choice([True, False], p=[0.3, 0.7])
        
        if trabaja:
            horas_trabajo = np.random.normal(15, 5)
            horas_trabajo = max(0, min(40, horas_trabajo))
            # Trabajar afecta las horas de estudio
            horas_estudio = max(0, horas_estudio - horas_trabajo * 0.3)
        else:
            horas_trabajo = 0
        
        # Introducir algunos valores faltantes de forma realista
        if np.random.random() < 0.05:  # 5% de datos faltantes en ingresos
            ingresos_familia = None
        
        if np.random.random() < 0.02:  # 2% de datos faltantes en satisfacción
            satisfaccion = None
        
        data.append({
            'id_estudiante': f'EST_{i+1:04d}',
            'edad': edad,
            'genero': genero,
            'carrera': carrera,
            'ciudad': ciudad,
            'horas_estudio_semanal': round(horas_estudio, 1),
            'horas_trabajo_semanal': round(horas_trabajo, 1) if horas_trabajo > 0 else 0,
            'trabaja': trabaja,
            'nota_promedio': round(nota_promedio, 2),
            'satisfaccion_carrera': round(satisfaccion, 1) if satisfaccion is not None else None,
            'ingresos_familia_euros': round(ingresos_familia, 2) if ingresos_familia is not None else None,
            'fecha_encuesta': (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d')
        })
    
    return pd.DataFrame(data)

def generate_sales_data(n_records=1000):
    """Generar datos de ventas de una empresa"""
    np.random.seed(42)
    random.seed(42)
    
    productos = ['Laptop', 'Smartphone', 'Tablet', 'Auriculares', 'Monitor', 'Teclado', 'Mouse']
    regiones = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
    vendedores = [f'Vendedor_{i}' for i in range(1, 21)]
    
    data = []
    
    for i in range(n_records):
        fecha = datetime.now() - timedelta(days=np.random.randint(0, 365))
        producto = np.random.choice(productos)
        region = np.random.choice(regiones)
        vendedor = np.random.choice(vendedores)
        
        # Precios base por producto
        precios_base = {
            'Laptop': 800, 'Smartphone': 400, 'Tablet': 300,
            'Auriculares': 50, 'Monitor': 200, 'Teclado': 30, 'Mouse': 20
        }
        
        precio_base = precios_base[producto]
        precio_unitario = precio_base * (1 + np.random.normal(0, 0.2))  # Variación del 20%
        precio_unitario = max(precio_base * 0.5, precio_unitario)  # Mínimo 50% del precio base
        
        # Cantidad vendida (algunos productos se venden más)
        if producto in ['Auriculares', 'Teclado', 'Mouse']:
            cantidad = np.random.poisson(3) + 1
        else:
            cantidad = np.random.poisson(1) + 1
        
        ventas_total = precio_unitario * cantidad
        
        # Descuento ocasional
        descuento = 0
        if np.random.random() < 0.15:  # 15% de probabilidad de descuento
            descuento = np.random.uniform(0.05, 0.25)  # 5% a 25%
            ventas_total *= (1 - descuento)
        
        # Introducir algunos outliers
        if np.random.random() < 0.01:  # 1% de outliers
            cantidad *= 10  # Venta muy grande
            ventas_total *= 10
        
        data.append({
            'fecha': fecha.strftime('%Y-%m-%d'),
            'producto': producto,
            'region': region,
            'vendedor': vendedor,
            'cantidad': cantidad,
            'precio_unitario': round(precio_unitario, 2),
            'descuento_aplicado': round(descuento, 3),
            'ventas_total': round(ventas_total, 2),
            'mes': fecha.month,
            'trimestre': (fecha.month - 1) // 3 + 1
        })
    
    return pd.DataFrame(data)

def generate_experiment_data(n_subjects=200):
    """Generar datos de experimento científico (efecto de tratamiento)"""
    np.random.seed(42)
    
    data = []
    
    for i in range(n_subjects):
        # Asignación aleatoria a grupos
        grupo = np.random.choice(['Control', 'Tratamiento_A', 'Tratamiento_B'], p=[0.4, 0.3, 0.3])
        
        # Variables demográficas
        edad = np.random.normal(35, 12)
        edad = max(18, min(80, int(edad)))
        
        genero = np.random.choice(['M', 'F'], p=[0.5, 0.5])
        
        # Medición pre-tratamiento (baseline)
        baseline = np.random.normal(100, 15)
        
        # Efecto del tratamiento
        if grupo == 'Control':
            efecto = np.random.normal(0, 5)  # Sin efecto real
        elif grupo == 'Tratamiento_A':
            efecto = np.random.normal(10, 8)  # Efecto moderado
        else:  # Tratamiento_B
            efecto = np.random.normal(15, 10)  # Efecto mayor pero más variable
        
        # Medición post-tratamiento
        post_tratamiento = baseline + efecto + np.random.normal(0, 3)
        
        # Calcular mejora
        mejora = post_tratamiento - baseline
        
        # Adherencia al tratamiento (solo para grupos de tratamiento)
        if grupo == 'Control':
            adherencia = None
        else:
            adherencia = np.random.beta(8, 2) * 100  # Mayoría con alta adherencia
        
        # Efectos secundarios (solo para tratamientos)
        efectos_secundarios = 0
        if grupo != 'Control':
            efectos_secundarios = np.random.poisson(0.5)  # Pocos efectos secundarios
        
        # Introducir algunos valores faltantes
        if np.random.random() < 0.03:  # 3% de datos faltantes
            post_tratamiento = None
            mejora = None
        
        data.append({
            'sujeto_id': f'S_{i+1:03d}',
            'grupo_tratamiento': grupo,
            'edad': edad,
            'genero': genero,
            'medicion_baseline': round(baseline, 2),
            'medicion_post': round(post_tratamiento, 2) if post_tratamiento is not None else None,
            'mejora': round(mejora, 2) if mejora is not None else None,
            'adherencia_porcentaje': round(adherencia, 1) if adherencia is not None else None,
            'efectos_secundarios_count': efectos_secundarios,
            'fecha_inicio': (datetime.now() - timedelta(days=np.random.randint(30, 180))).strftime('%Y-%m-%d'),
            'semanas_seguimiento': np.random.randint(4, 25)
        })
    
    return pd.DataFrame(data)

def generate_problematic_data(n_records=300):
    """Generar datos con problemas comunes para probar validación"""
    np.random.seed(42)
    
    data = []
    
    for i in range(n_records):
        # Datos con problemas intencionados
        
        # ID con formato inconsistente
        if i < 100:
            id_registro = f'ID_{i+1:03d}'
        elif i < 200:
            id_registro = f'{i+1}'  # Sin prefijo
        else:
            id_registro = f'REG{i+1}'  # Prefijo diferente
        
        # Números como texto (problema común)
        edad_texto = str(np.random.randint(18, 80))
        if np.random.random() < 0.1:  # 10% con espacios
            edad_texto = f' {edad_texto} '
        
        # Valores numéricos con formato europeo (coma decimal)
        precio = np.random.uniform(10, 1000)
        if np.random.random() < 0.5:
            precio_texto = f'{precio:.2f}'.replace('.', ',')  # Formato europeo
        else:
            precio_texto = f'{precio:.2f}'  # Formato americano
        
        # Fechas en diferentes formatos
        fecha_base = datetime.now() - timedelta(days=np.random.randint(0, 365))
        formatos_fecha = [
            fecha_base.strftime('%Y-%m-%d'),
            fecha_base.strftime('%d/%m/%Y'),
            fecha_base.strftime('%d-%m-%Y'),
            fecha_base.strftime('%Y/%m/%d')
        ]
        fecha_inconsistente = np.random.choice(formatos_fecha)
        
        # Categorías con inconsistencias
        categorias_inconsistentes = ['Tipo A', 'tipo a', 'TIPO A', 'Tipo_A', 'TipoA']
        categoria = np.random.choice(categorias_inconsistentes)
        
        # Valores extremos/outliers
        valor_normal = np.random.normal(50, 10)
        if np.random.random() < 0.02:  # 2% de outliers extremos
            valor_normal *= 10
        
        # Muchos valores faltantes en algunas columnas
        campo_opcional = None
        if np.random.random() < 0.3:  # 70% de valores faltantes
            campo_opcional = np.random.choice(['Opción 1', 'Opción 2', 'Opción 3'])
        
        # Duplicados intencionados
        if i > 250 and np.random.random() < 0.1:  # Algunos duplicados al final
            id_registro = 'ID_001'  # Forzar duplicado
        
        data.append({
            'ID ': id_registro,  # Nombre con espacio al final
            'Edad_Texto': edad_texto,
            'Precio$': precio_texto,  # Nombre con carácter especial
            'Fecha_Inconsistente': fecha_inconsistente,
            'Categoría': categoria,
            'Valor_Con_Outliers': round(valor_normal, 2),
            'Campo_Con_Muchos_Nulos': campo_opcional,
            'Columna_Muy_Larga_Con_Nombre_Poco_Descriptivo_Que_Debería_Ser_Más_Corta': 'valor',
            'X1': np.random.randint(1, 5),  # Nombre poco descriptivo
            '': 'columna_sin_nombre'  # Columna sin nombre
        })
    
    return pd.DataFrame(data)

def save_sample_datasets():
    """Generar y guardar todos los datasets de ejemplo"""
    data_dir = '../../shared/data/01_datos_originales'
    
    print("🔄 Generando datasets de ejemplo...")
    
    # Dataset 1: Encuesta de estudiantes
    print("📊 Generando datos de encuesta de estudiantes...")
    students_df = generate_student_survey_data(500)
    students_df.to_csv(f'{data_dir}/encuesta_estudiantes.csv', index=False)
    students_df.to_excel(f'{data_dir}/encuesta_estudiantes.xlsx', index=False)
    print(f"   ✅ Guardado: encuesta_estudiantes.csv ({len(students_df)} registros)")
    
    # Dataset 2: Datos de ventas
    print("💰 Generando datos de ventas...")
    sales_df = generate_sales_data(1000)
    sales_df.to_csv(f'{data_dir}/ventas_empresa.csv', index=False)
    print(f"   ✅ Guardado: ventas_empresa.csv ({len(sales_df)} registros)")
    
    # Dataset 3: Experimento científico
    print("🔬 Generando datos de experimento...")
    experiment_df = generate_experiment_data(200)
    experiment_df.to_csv(f'{data_dir}/experimento_tratamiento.csv', index=False)
    print(f"   ✅ Guardado: experimento_tratamiento.csv ({len(experiment_df)} registros)")
    
    # Dataset 4: Datos problemáticos
    print("⚠️ Generando datos con problemas...")
    problematic_df = generate_problematic_data(300)
    problematic_df.to_csv(f'{data_dir}/datos_problematicos.csv', index=False)
    print(f"   ✅ Guardado: datos_problematicos.csv ({len(problematic_df)} registros)")
    
    # Dataset 5: Datos en formato JSON
    print("📄 Generando datos JSON...")
    json_data = {
        'metadata': {
            'title': 'Datos de Ejemplo en JSON',
            'created': datetime.now().isoformat(),
            'version': '1.0'
        },
        'records': students_df.head(50).to_dict('records')
    }
    
    with open(f'{data_dir}/datos_ejemplo.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)
    print(f"   ✅ Guardado: datos_ejemplo.json")
    
    # Generar resumen de datasets
    summary = {
        'datasets_generados': [
            {
                'nombre': 'encuesta_estudiantes.csv',
                'descripcion': 'Encuesta a 500 estudiantes universitarios',
                'filas': len(students_df),
                'columnas': len(students_df.columns),
                'casos_uso': ['Análisis descriptivo', 'Correlaciones', 'Regresión']
            },
            {
                'nombre': 'ventas_empresa.csv',
                'descripcion': 'Datos de ventas de una empresa durante un año',
                'filas': len(sales_df),
                'columnas': len(sales_df.columns),
                'casos_uso': ['Análisis temporal', 'ANOVA', 'Clustering']
            },
            {
                'nombre': 'experimento_tratamiento.csv',
                'descripcion': 'Experimento científico con grupos de control y tratamiento',
                'filas': len(experiment_df),
                'columnas': len(experiment_df.columns),
                'casos_uso': ['Pruebas t', 'ANOVA', 'Análisis de efectividad']
            },
            {
                'nombre': 'datos_problematicos.csv',
                'descripcion': 'Datos con problemas comunes para probar validación',
                'filas': len(problematic_df),
                'columnas': len(problematic_df.columns),
                'casos_uso': ['Validación de datos', 'Limpieza', 'Detección de errores']
            },
            {
                'nombre': 'datos_ejemplo.json',
                'descripcion': 'Muestra de datos en formato JSON',
                'filas': 50,
                'columnas': len(students_df.columns),
                'casos_uso': ['Prueba de carga JSON', 'Análisis básico']
            }
        ],
        'total_registros': len(students_df) + len(sales_df) + len(experiment_df) + len(problematic_df) + 50,
        'fecha_generacion': datetime.now().isoformat()
    }
    
    with open(f'{data_dir}/README_datasets.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Generación completada!")
    print(f"📁 Ubicación: {data_dir}")
    print(f"📊 Total de registros generados: {summary['total_registros']:,}")
    print(f"📋 Datasets disponibles: {len(summary['datasets_generados'])}")
    
    return summary

if __name__ == "__main__":
    summary = save_sample_datasets()
    
    print("\n📋 Resumen de datasets generados:")
    for dataset in summary['datasets_generados']:
        print(f"   • {dataset['nombre']}: {dataset['filas']} filas, {dataset['columnas']} columnas")
        print(f"     {dataset['descripcion']}")
        print(f"     Casos de uso: {', '.join(dataset['casos_uso'])}")
        print()

