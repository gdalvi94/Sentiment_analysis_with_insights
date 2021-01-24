import pickle
import pandas as pd
import webbrowser
import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output ,State
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import plotly.graph_objects as go 
from wordcloud import WordCloud
import matplotlib.pyplot as plt


df1 = pd.read_csv('tocheck.csv')
labels=["Positive","Negative"]
values1=len(df1[df1["Positivity"]==1])
values2=len(df1[df1["Positivity"]==0])
values=[values1,values2]
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7)])
x2011 = df1["reviewText"][df1["Positivity"]==1]
x2012 = df1["reviewText"][df1["Positivity"]==0]

plt.subplots(figsize = (8,8))

wordcloud1 = WordCloud (
                    background_color = 'white',
                    width = 512,
                    height = 384
                        ).generate(' '.join(x2011))
fig1=plt.imshow(wordcloud1) 
fig1=plt.axis('off') 
plt.savefig('assets/Plotly-World_Cloudpos.png')
wordcloud2 = WordCloud (
                    background_color = 'white',
                    width = 512,
                    height = 384
                        ).generate(' '.join(x2012))
fig1=plt.imshow(wordcloud2) 
fig1=plt.axis('off')
plt.savefig('assets/Plotly-World_Cloudneg.png')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
project_name = None

def load_model():
    global df
    df = pd.read_csv('reviews.csv')
    df=df.dropna()
  
    global pickle_model
    file = open("pickle_model.pkl", 'rb') 
    pickle_model = pickle.load(file)

    global vocab
    file = open("feature.pkl", 'rb') 
    vocab = pickle.load(file)
    

def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')
    

def check_review(reviewText):

    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
    reviewText = transformer.fit_transform(loaded_vec.fit_transform([reviewText]))

    return pickle_model.predict(reviewText)
 
def create_app_ui():
    main_layout = html.Div(
    [

    html.H1(children='Sentiments Analysis with Insights', id='Main_title',style={'text-align':'center','font-weight': 'bold'}),
     html.Div([dcc.Graph(figure=fig),]),
     html.Hr(),
     html.H2(children='Important Words',style={'text-align':'center','font-weight': 'bold'}),
     html.Div([
        html.Div([
            html.H3('Positive Words',style={'font-weight': 'bold'}),
            html.Img(src = app.get_asset_url ('Plotly-World_Cloudpos.png')),

        ], className="six columns"),
        html.Div([
        html.H3('Negative Words',style={'font-weight': 'bold'}),
            html.Img(src = app.get_asset_url ('Plotly-World_Cloudneg.png')),

        ], className="six columns"),
    ], className="row",style={'marginLeft': 50,'text-align':'center','font-weight': 'bold'}),
    html.Hr(),
    html.H2(children='Analyze the Sentiments',style={'text-align':'center','font-weight': 'bold'}),

    dcc.Dropdown(
        id='dropdown',
        options=[{'label':i,'value':i}for i in df["reviews"]],
        value='',style={'padding-left': 50,'marginRight': 80}),

    html.Br(),

    dcc.Textarea(
        id='textarea_review',
        placeholder='Enter the review here...',
        value='',
        style={'marginLeft': 50, 'width':'91%','height': 100}
        ),
    html.Br(),
    html.Button(children='Find Review', id='button_review',n_clicks=0,
                style={'marginLeft': 650,'height':'40px','backgroundColor':'#4CAF50'}),
        


    html.H2(children=None, id='result',style={'text-align':'center','font-weight': 'bold','text-decoration': 'underline'}),
    ], style={'marginLeft': 30, 'marginRight': 30,   
            'backgroundColor':'#F7FBFE',
               'border': 'thin lightgrey dashed'}

    )
     
    
    
    return main_layout

@app.callback(
    Output('result', 'children'),
    [
    Input('button_review', 'n_clicks'),
    State('dropdown','value'),
    State('textarea_review','value')

    ]
    )
def update_app_ui(n_click,textarea_value,textarea_value1):
    
    if len(textarea_value1)!=0:
        textarea_value=textarea_value1
    result_list = check_review(textarea_value)
    if n_click > 0:
        if (result_list[0] == 0 ):
            result = 'Negative'
        elif (result_list[0] == 1 ):
            result = 'Positive'
        else:
            result = 'Unknown'
        
    return result
    
    
def main():
    load_model()    
    open_browser()
    

    global project_name
    project_name = "Sentiments Analysis with Insights" 
      
    global app
    app.layout = create_app_ui()
    app.title = project_name
    app.run_server() 
  
    print("This would be executed only after the script is closed")
    app = None
    project_name = None

if __name__ == '__main__':
    main()