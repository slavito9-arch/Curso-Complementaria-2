
import streamlit as st
import pandas as pd
st.title("📊 Comparador de usuarios entre dos archivos")
# Subida de archivos
file1 = st.file_uploader("Sube el primer archivo Excel", type=["xlsx", "xls"])
file2 = st.file_uploader("Sube el segundo archivo Excel", type=["xlsx", "xls"])
if file1 and file2:
   # Leer archivos
   df1 = pd.read_excel(file1)
   df2 = pd.read_excel(file2)
   st.subheader("📁 Vista previa de los archivos")
   st.write("**Archivo 1**")
   st.dataframe(df1.head())
   st.write("**Archivo 2**")
   st.dataframe(df2.head())
   # Contar ocurrencias de usuarios
   conteo1 = df1['usuario'].value_counts().rename_axis('usuario').reset_index(name='apariciones_archivo1')
   conteo2 = df2['usuario'].value_counts().rename_axis('usuario').reset_index(name='apariciones_archivo2')
   # Cruzar ambos conteos
   comparativo = pd.merge(conteo1, conteo2, on='usuario', how='outer').fillna(0)
   # Calcular diferencia
   comparativo['diferencia'] = comparativo['apariciones_archivo2'] - comparativo['apariciones_archivo1']
   st.subheader("📈 Comparativo de usuarios")
   st.dataframe(comparativo)
   # Métricas generales
   total_usuarios = comparativo['usuario'].nunique()
   aumentaron = (comparativo['diferencia'] > 0).sum()
   disminuyeron = (comparativo['diferencia'] < 0).sum()
   iguales = (comparativo['diferencia'] == 0).sum()
   st.subheader("📊 Métricas generales")
   col1, col2, col3, col4 = st.columns(4)
   col1.metric("Total de usuarios", total_usuarios)
   col2.metric("Usuarios con aumento", aumentaron)
   col3.metric("Usuarios con disminución", disminuyeron)
   col4.metric("Usuarios sin cambio", iguales)
   # Mostrar gráfico
   st.subheader("📉 Gráfico comparativo")
   st.bar_chart(comparativo.set_index('usuario')[['apariciones_archivo1', 'apariciones_archivo2']])
else:
   st.info("👆 Sube dos archivos Excel para iniciar el análisis.")