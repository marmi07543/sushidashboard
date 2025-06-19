import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Загрузка данных
results_df = pd.read_excel("данные по рынку суши.xlsx", sheet_name="результаты")
profile_df = pd.read_excel("данные по рынку суши.xlsx", sheet_name="профиль потребителя")

# Предварительная обработка данных (пример)
# Удаление пустых строк, если нужно
results_df = results_df.dropna(how='all')
profile_df = profile_df.dropna(how='all')

# Инициализация Dash-приложения
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📊 Дашборд: Анализ рынка суши в Омске", style={'textAlign': 'center'}),
    
    # Вкладки для разделов
    dcc.Tabs([
        # Вкладка 1: Результаты опроса
        dcc.Tab(label='Результаты опроса', children=[
            html.Div([
                html.H3("Частота посещения суши-ресторанов"),
                dcc.Graph(
                    figure=px.bar(
                        results_df,
                        x='Как часто посещают суши-рестораны',
                        y='кол-во',
                        title='Распределение по частоте посещений'
                    )
                ),
                
                html.H3("Популярные суши-рестораны"),
                dcc.Graph(
                    figure=px.pie(
                        results_df,
                        names='Какие суши-рестораны в г. Омск знают',
                        values='кол-во',
                        title='Известность суши-ресторанов'
                    )
                ),
                
                html.H3("Удовлетворенность заведениями"),
                dcc.Graph(
                    figure=px.histogram(
                        results_df,
                        x='На сколько удовлетворены суши-рестораном, который посещают чаще всего',
                        y='кол-во',
                        title='Уровень удовлетворенности'
                    )
                )
            ])
        ]),
        
        # Вкладка 2: Профиль потребителя
        dcc.Tab(label='Профиль потребителя', children=[
            html.Div([
                html.H3("Распределение по возрасту и полу"),
                dcc.Graph(
                    figure=px.histogram(
                        profile_df,
                        x='возраст',
                        color='пол',
                        title='Демография потребителей'
                    )
                ),
                
                html.H3("Любимые виды суши/роллов"),
                dcc.Graph(
                    figure=px.treemap(
                        profile_df,
                        path=['Какие суши\роллы любят больше всего'],
                        title='Предпочтения по видам роллов'
                    )
                ),
                
                html.H3("Доход vs. Любимые роллы"),
                dcc.Graph(
                    figure=px.scatter(
                        profile_df,
                        x='доход',
                        y='Какие суши\роллы любят больше всего',
                        color='пол',
                        title='Зависимость предпочтений от дохода'
                    )
                )
            ])
        ]),
        
        # Вкладка 3: Ценовые предпочтения
        dcc.Tab(label='Ценовые предпочтения', children=[
            html.Div([
                html.H3("Максимальная цена за порцию (8 шт.)"),
                dcc.Graph(
                    figure=px.box(
                        results_df,
                        y='Выше какой цены никогда не приобретут порцию суши/роллов, потому что это дорого (8 шт., «Калифорния»)',
                        title='Верхний порог цены'
                    )
                ),
                
                html.H3("Справедливая цена за порцию"),
                dcc.Graph(
                    figure=px.violin(
                        results_df,
                        y='Справедливая цена за порцию суши/роллов (8 шт., «Калифорния»)',
                        title='Распределение справедливых цен'
                    )
                )
            ])
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)