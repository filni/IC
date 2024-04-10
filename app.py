from flask import Flask, render_template, redirect, send_file
import sqlite3
import pandas as pd
import os
import xlwings as xw
import numpy as np
from datetime import datetime, timedelta
from werkzeug.serving import run_simple
from importlib import reload
import importlib.util
from urllib.parse import quote
import sys
sys.path.append('C:/Users/fniccolini.AZIMUTNET/Documents/PythonProjects')



app = Flask(__name__)

@app.route('/')
def index():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    two_days_ago = datetime.now() - timedelta(days=6)
    current_date = two_days_ago.strftime('%Y-%m-%d')
    path = 'Z:\\IC ITALIA\\Mappatura limiti AIM\\Derivati\\Derivati_Analysis\\Derivatives_haircuts'
    file_name = f'Derivatives_covered_short_p_summary - {current_date}.xlsx'
    df_path = os.path.join(path, file_name)

    if os.path.exists(df_path):
        df = pd.read_excel(df_path)
        columns_to_format = ['nav', 'short_derivatives_exp', 'cash_available_and_RiskFree', 'future_bond_exp',
                             'Listed_government_bond_with_haircuts', 'future_eq_exp',
                             'Listed_common_stocks_with_haircuts',
                             'Tot_exp_after_cover']
        for col in columns_to_format:
            df[col] = df[col].astype(float)
        df[columns_to_format] = df[columns_to_format].applymap('{:,.2f}'.format)
        df['Ratio_tot'] = df['Ratio_tot'].apply(lambda x: f"{x:.2%}")
        df['Ratio_tot'] = df.apply(
            lambda row: f'<span style="color: red;">{row["Ratio_tot"]}</span>' if row['Check_tot'] == 'KO' else
            row['Ratio_tot'], axis=1)

        df = df.rename(columns={'Unnamed: 0': 'Fund_code'})
        df_html = df.to_html(classes='table table-sm', escape=False, index=False)
    else:
        df_html = "DataFrame non disponibile"

    # Passa i post e la tabella HTML al template
    return render_template('index_scarica.html', posts=posts, df_html=df_html)

@app.route('/<int:idx>/delete', methods=('POST',))
def delete(idx):
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection.execute('DELETE FROM posts WHERE id=?', (idx,))
    connection.commit()
    connection.close()
    return redirect('/')

@app.route('/download_excel')
def download_excel():
    # Qui viene generato il nome del file basato sulla data corrente o qualsiasi altra logica necessaria
    two_days_ago = datetime.now() - timedelta(days=2)
    current_date = two_days_ago.strftime('%Y-%m-%d')
    file_name = f'Derivatives_covered_short_p_summary - {current_date}.xlsx'
    file_path = os.path.join('Z:', 'IC ITALIA', 'Mappatura limiti AIM', 'Derivati', 'Derivati_Analysis',
                             'Derivatives_haircuts', file_name)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, attachment_filename=file_name)
    else:
        return "File non trovato"


if __name__ == '__main__':
    app.run(debug=True, port=5000)







