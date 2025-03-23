#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para ajustar modelos predictivos de dos targets:
  1. VIC_EDAD (edad de la víctima, valores válidos 1-98; 99 = ignorado)
  2. TOTAL_HIJOS (número de hijos, valores válidos 0-20; 99 = ignorado)

Se comparan dos algoritmos (RandomForestRegressor y GradientBoostingRegressor)
usando GridSearchCV para buscar parámetros que mejoren el desempeño (R²).

Nota: Para TOTAL_HIJOS se excluyen las columnas NUM_HIJ_HOM y NUM_HIJ_MUJ para evitar leakage.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def get_predictors(df, target, exclude_list=[]):
    # Selecciona únicamente las columnas numéricas
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if target in numeric_cols:
        numeric_cols.remove(target)
    # Excluir columnas que causen leakage u otras no deseadas
    for col in exclude_list:
        if col in numeric_cols:
            numeric_cols.remove(col)
    return numeric_cols

def grid_search_model(model, param_grid, X_train, y_train):
    gs = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring='r2', n_jobs=-1)
    gs.fit(X_train, y_train)
    return gs.best_estimator_, gs.best_params_, gs.best_score_

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2  = r2_score(y_test, y_pred)
    return mae, mse, r2

def train_target_model(df, target, exclude_predictors=[]):
    # Filtrar registros válidos (target != 99 y no nulo)
    df_valid = df[(df[target] != 99) & (~df[target].isnull())].copy()
    n_records = len(df_valid)
    print(f"\n=== Modelo para {target} ===")
    print(f"{target} - Registros válidos: {n_records}")
    
    # Seleccionar predictores
    predictors = get_predictors(df_valid, target, exclude_list=exclude_predictors)
    X = df_valid[predictors]
    y = df_valid[target]
    
    # Imputación de valores faltantes en predictores
    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)
    
    # Dividir en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)
    
    # Definir grids para cada modelo
    # Para RandomForest
    rf = RandomForestRegressor(random_state=42)
    param_grid_rf = {
        'n_estimators': [100, 200],
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5]
    }
    
    # Para GradientBoosting
    gb = GradientBoostingRegressor(random_state=42)
    param_grid_gb = {
        'n_estimators': [100, 200],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.05, 0.1]
    }
    
    print(f"\nIniciando GridSearchCV para {target} con RandomForest...")
    best_rf, best_params_rf, score_rf = grid_search_model(rf, param_grid_rf, X_train, y_train)
    mae_rf, mse_rf, r2_rf = evaluate_model(best_rf, X_test, y_test)
    print("Mejor modelo RandomForest para {}:".format(target))
    print("  Parámetros:", best_params_rf)
    print("  CV R²:", score_rf)
    print("  Test MAE: {:.2f} | MSE: {:.2f} | R²: {:.2f}".format(mae_rf, mse_rf, r2_rf))
    
    print(f"\nIniciando GridSearchCV para {target} con GradientBoosting...")
    best_gb, best_params_gb, score_gb = grid_search_model(gb, param_grid_gb, X_train, y_train)
    mae_gb, mse_gb, r2_gb = evaluate_model(best_gb, X_test, y_test)
    print("Mejor modelo GradientBoosting para {}:".format(target))
    print("  Parámetros:", best_params_gb)
    print("  CV R²:", score_gb)
    print("  Test MAE: {:.2f} | MSE: {:.2f} | R²: {:.2f}".format(mae_gb, mse_gb, r2_gb))
    
    # Seleccionar el mejor de los dos según R² en test
    if r2_rf >= r2_gb:
        best_model = best_rf
        best_model_name = "RandomForestRegressor"
        best_r2 = r2_rf
    else:
        best_model = best_gb
        best_model_name = "GradientBoostingRegressor"
        best_r2 = r2_gb
        
    print(f"\n--> Mejor modelo final para {target}: {best_model_name} con R² de {best_r2:.2f}")
    return best_model

def main():
    ruta_csv = "bdvif.csv"  # Ajusta la ruta a tu CSV
    df = pd.read_csv(ruta_csv)
    
    # Modelo para VIC_EDAD (usar todos los predictores numéricos)
    best_model_edad = train_target_model(df, "VIC_EDAD")
    
    # Modelo para TOTAL_HIJOS: eliminar columnas NUM_HIJ_HOM y NUM_HIJ_MUJ para evitar leakage
    best_model_hijos = train_target_model(df, "TOTAL_HIJOS", exclude_predictors=["NUM_HIJ_HOM", "NUM_HIJ_MUJ"])
    
if __name__ == "__main__":
    main()
