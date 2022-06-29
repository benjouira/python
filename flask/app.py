from flask import Flask, render_template
import pymssql
from flask import request

app = Flask(__name__)
conn=pymssql.connect(server='192.168.10.216', user='sa', password='123', database='MAS')
cursor = conn.cursor(as_dict = True)
from Util.write_read_CMD_from_lunix_VM import VM
import Util.select_from_elk_with_sql as sfews

p=VM()

@app.route('/')
def my_form():
    return render_template('run_command.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['cmd_text']
    
    if request.method == 'POST':
        output = p.CMD(text)
        return render_template('run_command.html', result_of_commend= output)
    else:
        return render_template('run_command.html',result_of_commend= '')


@app.route('/openConnection')
def openConnection():
    return render_template('run_command.html')

@app.route('/closeConnection')
def closeConnection():
    return render_template('run_command.html')



@app.route('/api/valide_chart')
def total_releve_valide_par_banque():
    df= sfews.total_releve_valide_par_banque()

    data = {'lv':  list(df['Valider']), 'lb': list(df['Banque'].unique()), 'lt': list(df['total'])}

    # return render_template('valide_par_banque_chart.html', data = data)
    return data


@app.route('/bar_chart')
def bar_chart():

    return render_template('valide_par_banque_chart.html')
    


if __name__ == "__main__":
    app.run( debug=True)
