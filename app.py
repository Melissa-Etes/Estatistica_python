from flask import Flask, request, render_template_string
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    table_img = None
    bar_chart_img = None
    mean_values = {}
    mode_values = {}
    median_values = {}
    var_values = {}
    std_values = {}
    skew_values = {}
    kurtosis_values = {}
    describe_values = {}
    corr_pearson_values = {}
    corr_spearman_values = {}

    if request.method == 'POST':
        # Captura os dados do input
        data = request.form['user_input']
        
        # Processa os dados
        categories = data.split(';')
        data_dict = {}
        
        for category in categories:
            cat_name, values = category.split(':')
            data_dict[cat_name] = [float(v) for v in values.split(',')]  # Convertendo para float
        
        # Cria um DataFrame com os dados
        df = pd.DataFrame(data_dict)
        
        # Cria uma figura e um eixo para a tabela
        fig, ax = plt.subplots(figsize=(8, 4))  # Tamanho da figura pode ser ajustado
        ax.axis('off')  # Desliga os eixos

        # Adiciona a tabela
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

        # Salva a figura da tabela em um buffer de bytes
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        table_img = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        
        # Cria uma figura e um eixo para o gráfico de barras
        fig, ax = plt.subplots(figsize=(6, 4))
        df.plot(kind='bar', ax=ax)
        ax.set_title('Gráfico de Barras das Categorias')
        ax.set_ylabel('Valores')
        ax.set_xlabel('Índice')
        
        # Salva a figura do gráfico em um buffer de bytes
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        bar_chart_img = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        # Calcula as médias das categorias
        mean_values = df.mean().to_dict()
        # Calcula a moda das categorias
        mode_values = df.mode().iloc[0].to_dict()  # `iloc[0]` para obter a moda como uma série
        # Calcula as medianas das categorias
        median_values = df.median().to_dict()
        # Calcula a variância das categorias
        var_values = df.var().to_dict()
        # Calcula o desvio padrão das categorias
        std_values = df.std().to_dict()
        # Calcula a assimetria das categorias
        skew_values = df.skew().to_dict()
        # Calcula a curtose das categorias
        kurtosis_values = df.kurtosis().to_dict()
        # Calcula as medidas estatísticas das categorias
        describe_values = df.describe().to_dict()
        # Correlação do DataFrame, segundo pearson
        corr_pearson_values = df.corr(method="pearson").to_dict()
        # Correlação do DataFrame, segundo spearman
        corr_spearman_values = df.corr(method="spearman").to_dict()

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dados Estatísticos</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    width: 80%;
                    margin: auto;
                    overflow: hidden;
                }
                h1, h3 {
                    color: #0056b3;
                }
                form {
                    margin: 20px 0;
                    padding: 20px;
                    background: #fff;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                input[type="text"] {
                    padding: 10px;
                    font-size: 16px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    width: 100%;
                }
                input[type="submit"] {
                    padding: 10px 20px;
                    font-size: 16px;
                    border: none;
                    border-radius: 4px;
                    background: #0056b3;
                    color: #fff;
                    cursor: pointer;
                    transition: background 0.3s ease;
                    margin-top: 10px;
                }
                input[type="submit"]:hover {
                    background: #004494;
                }
                .result {
                    margin: 20px 0;
                    padding: 20px;
                    background: #fff;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                ul {
                    list-style: none;
                    padding: 0;
                }
                li {
                    margin: 5px 0;
                }
                img {
                    max-width: 100%;
                    height: auto;
                    display: block;
                    margin: 10px 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Gerador de Tabela e Gráfico</h1>
                <form method="post">
                    Digite dados no formato `categoria1:valor1,valor2;categoria2:valor3,valor4`:
                    <input type="text" name="user_input">
                    <input type="submit" value="Gerar Tabela e Gráfico">
                </form>
                {% if table_img %}
                    <div class="result">
                        <h3>Tabela Gerada:</h3>
                        <img src="data:image/png;base64,{{ table_img }}" alt="Tabela">
                    </div>
                {% endif %}
                {% if bar_chart_img %}
                    <div class="result">
                        <h3>Gráfico de Barras:</h3>
                        <img src="data:image/png;base64,{{ bar_chart_img }}" alt="Gráfico de Barras">
                    </div>
                {% endif %}
                {% if mean_values %}
                    <div class="result">
                        <h3>Médias das Categorias:</h3>
                        <ul>
                            {% for cat, mean in mean_values.items() %}
                                <li>{{ cat }}: {{ mean }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                {% endif %}
                {% if mode_values %}
                    <div class="result">
                        <h3>Moda das Categorias:</h3>
                        <ul>
                            {% for cat, mode in mode_values.items() %}
                                <li>{{ cat }}: {{ mode }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                {% endif %}
                {% if median_values %}
                    <div class="result">
                        <h3>Medianas das Categorias:</h3>
                        <ul>
                            {% for cat, median in median_values.items() %}
                                <li>{{ cat }}: {{ median }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                {% endif %}
                {% if var_values %}
                    <div class="result">
                        <h3>Variância das Categorias:</h3>
                        <ul>
                            {% for cat, var in var_values.items() %}
                                <li>{{ cat }}: {{ var }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                {% endif %}
                {% if std_values %}
                    <div class="result">
                        <h3>Desvio padrão das Categorias:</h3>
                        <ul>
                            {% for cat, std in std_values.items() %}
                                <li>{{ cat }}: {{ std }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                {% endif %}
                {% if skew_values %}
                    <div class="result">
                        <h3>A assimetria das categorias:</h3>
                        <ul>
                            {% for cat, skew in skew_values.items() %}
                                <li>{{ cat }}: {{ skew }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                {% endif %}
                {% if kurtosis_values %}
                    <div class="result">
                        <h3>A curtose das Categorias:</h3>
                        <ul>
                            {% for cat, kurtosis in kurtosis_values.items() %}
                                <li>{{ cat }}: {{ kurtosis }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                {% endif %}
                {% if describe_values %}
                    <div class="result">
                        <h3>As medidas estatísticas das Categorias:</h3>
                        <ul>
                            {% for cat, describe in describe_values.items() %}
                                <li>{{ cat }}: {{ describe['mean'] }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                {% endif %}
                {% if corr_pearson_values %}
                    <div class="result">
                        <h3>Correlação do DataFrame, segundo Pearson:</h3>
                        <ul>
                            {% for cat1, cat_dict in corr_pearson_values.items() %}
                                {% for cat2, corr in cat_dict.items() %}
                                    <li>{{ cat1 }} - {{ cat2 }}: {{ corr }}</li>
                                {% endfor %}
                            {% endfor %}
                        </ul>
                    </div>
                {% endif %}
                {% if corr_spearman_values %}
                    <div class="result">
                        <h3>Correlação do DataFrame, segundo Spearman:</h3>
                        <ul>
                            {% for cat1, cat_dict in corr_spearman_values.items() %}
                                {% for cat2, corr in cat_dict.items() %}
                                    <li>{{ cat1 }} - {{ cat2 }}: {{ corr }}</li>
                                {% endfor %}
                            {% endfor %}
                        </ul>
                    </div>
                {% endif %}
            </div>
        </body>
        </html>
    ''', table_img=table_img, bar_chart_img=bar_chart_img, mean_values=mean_values, mode_values=mode_values, median_values=median_values,
    var_values=var_values, std_values=std_values, skew_values=skew_values, kurtosis_values=kurtosis_values, describe_values=describe_values,
    corr_pearson_values=corr_pearson_values, corr_spearman_values=corr_spearman_values,)

if __name__ == '__main__':
    app.run(debug=True)
