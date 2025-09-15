
# SmartHousing Madrid — v2 (visual-first + bandas P10–P90)

Este proyecto refactoriza tu app para priorizar **experiencia visual** y añade la **Calculadora con bandas (P10–P90)**.

## Estructura
- `app.py` — landing/hero y CTA hacia el asistente.
- `pages/1_Flujo_Usuario.py` — asistente guiado (dónde + **cuándo**).
- `pages/2_Comparador.py` — comparador de distritos.
- `pages/3_Calculadora_Bandas.py` — **mediana + P10–P90** y **SHAP** (si disponible).
- `pages/4_Importancia.py` — importancia global (placeholder).
- `pages/5_Datos_y_Descargas.py` — datasets y tabla.
- `utils/ui.py` y `assets/style.css` — branding y microinteracciones.
- `data/` — tus activos (Barrios.json, Distritos.json, vivienda_imputada.xlsx, etc.).
- `models/` — coloca aquí: `feature_columns.json`, `model_p10.pkl`, `model_p50.pkl`, `model_p90.pkl`, `preprocessor.pkl` (opcional), `shap_explainer.pkl` (opcional).
- `train_quantiles.py` — script para entrenar **cuantiles** P10/P50/P90.

## Instalación
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Entrenar modelos cuantílicos (si aún no los tienes)
1) Asegúrate de que `data/vivienda_imputada.xlsx` y `data_columns.json` existan (copiado de tu `columns.json` original).
2) Ejecuta:
```bash
python train_quantiles.py
```
Esto generará en `models/`:
- `feature_columns.json` (orden exacto de features)
- `model_p10.pkl`, `model_p50.pkl`, `model_p90.pkl`
- `shap_explainer.pkl` (opcional)

> Si prefieres mantener tu `RandomForestRegressor`, crea intervalos por **bootstrap de residuales** y exporta modelos/señales equivalentes o ajusta la página para consumir `y_hat ± k·RMSE` (menos riguroso que cuantiles).

## Conectar la calculadora
- Revisa `pages/3_Calculadora_Bandas.py`. Por defecto busca artefactos en `models/`.
- Si tus nombres de columnas difieren, edita el bloque `build_row()` o actualiza `models/feature_columns.json` para alinear.

## Nota sobre BARRIO/DISTRITO
- `columns.json` original incluye `DISTRITO_x` y `BARRIO`. Si sólo usas *distrito*, puedes mapear `BARRIO = Distrito` (dummy) o usar `catalogo_distritos_barrios.csv` para seleccionar un barrio válido.

¡Listo para lucir tu TFM con un flujo **intuitivo, suave y visual** y una calculadora **con confianza cuantificada**! 🎯
