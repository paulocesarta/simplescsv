from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

# Caminho para o arquivo CSV
CSV_FILE = 'usuarios.csv'

# Rota inicial para exibir os dados
@app.route('/')
def index():
    with open(CSV_FILE, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)
    return render_template('index.html', data=data)

# Rota para editar os dados
@app.route('/edit/<username>', methods=['GET', 'POST'])
def edit(username):
    with open(CSV_FILE, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)
    
    user_data = None
    for row in data:
        if row['nome'] == username:
            user_data = row
            break
    
    if request.method == 'POST':
        user_data['senha'] = request.form['senha']
        with open(CSV_FILE, 'w', newline='') as csv_file:
            fieldnames = ['nome', 'senha']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(data)
        return redirect(url_for('index'))

    return render_template('edit.html', user_data=user_data)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        new_user = {
            'nome': request.form['nome'],
            'senha': request.form['senha']
        }

        with open(CSV_FILE, 'a', newline='') as csv_file:
            fieldnames = ['nome', 'senha']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Verifica se o arquivo está vazio para adicionar o cabeçalho
            if csv_file.tell() == 0:
                csv_writer.writeheader()

            csv_writer.writerow(new_user)

        return redirect(url_for('index'))

    return render_template('add_user.html')

# Rota para excluir usuário
@app.route('/delete/<username>')
def delete_user(username):
    data = []
    with open(CSV_FILE, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)

    for row in data:
        if row['nome'] == username:
            data.remove(row)
            break

    with open(CSV_FILE, 'w', newline='') as csv_file:
        fieldnames = ['nome', 'senha']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

