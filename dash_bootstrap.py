import base64
from html.entities import name2codepoint
import io
import os
from turtle import width
from urllib.parse import quote as urlquote

from flask import Flask, send_from_directory
import dash
from dash import html , dcc , dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output , State
from matplotlib.pyplot import margins
from sqlalchemy import true
import pandas as pd

import Releve_AmenBank as rab
import pdf_to_elk as pdf_elk
import pdfplumber
import re

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

app = dash.Dash(external_stylesheets=[dbc.themes.MINTY , dbc.icons.FONT_AWESOME])

UPLOAD_DIRECTORY = "/project/app_uploaded_files"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)



app.layout = dbc.Container(
    
    dbc.Row([
            dbc.NavbarSimple(
                children=[
                    
                    dbc.NavItem(dbc.NavLink("tableau de bord personnalisé", href="#")),
                    html.Div([dbc.Button(html.Span([html.I(className="fa-solid fa-pen-to-square")," Edit"]), id="open-offcanvas", n_clicks=0,)]),
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("More pages", header=True),
                            dbc.DropdownMenuItem("enregistrer csv", href="#" , id= "saveCsv"),
                            dbc.DropdownMenuItem("enregistrer Json", href="#", id= "saveJson"),
                            dbc.DropdownMenuItem("enregistrer excel", href="#", id= "savexlsx"),
                            dcc.Download(id="download-dataframe-csv"),

                            dbc.DropdownMenuItem("visualisé PDF", href="#" , id= "visualisePDF"),
                            dbc.DropdownMenuItem("enregistrer dans ELK", href="#" , id= "send_to_elk"),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="More",
                    ),
                ],
                brand="Extration de PDF",
                brand_href="#",
                color="primary",
                dark=True,
            ),
            
            
            
            # offcanvas compenent           
            dbc.Row([
                dbc.Offcanvas(
                    html.Div([
                        dbc.Col([
                            dcc.Upload(
                                id="upload-data",
                                children=html.Div(
                                    ["Drag and drop or click to select a file to upload.".upper()],
                                    style={
                                    "textAlign": "center",
                                    "color":"#4DB7AD",
                                    "font-family": "Arial",
                                    "font-weight": "bold",
                                    },
                                ),
                                style={
                                    "width": "100%",
                                    "height": "60px",
                                    "lineHeight": "60px",
                                    "borderWidth": "1px",
                                    "border-color": "#4DB7AD",
                                    "borderStyle": "dashed",
                                    "borderRadius": "5px",
                                    "textAlign": "center",
                                    "margin": "10px",
                                },
                                multiple=True,
                                
                            ),
                        ], width=12), # close Col
                        dbc.Col([
                            html.Div(
                                [ html.Div(id='dropdown_offcanvas', children=[]) ], 
                                className='row'
                                ),
                        ]),
                    ]), # close div
                    id="offcanvas",
                    title="Title",
                    is_open=False,
                    placement= "top",
                    scrollable=True,
                    style={'height' : 500}
                ), # Offcanvas close
            ]), #col close
            
            

            dbc.Row([
                html.Div(
                        [ html.Div(id='banque_toast', children=[]) ], 
                        className='row' ),

                html.Div(
                        [ html.Div(id='date_toast', children=[]) ], 
                        className='row' ),

                html.Div(
                        [ html.Div(id='total_debit_toast', children=[]) ], 
                        className='row' ),

                html.Div(
                        [ html.Div(id='total_credit_toast', children=[]) ], 
                        className='row' ),
            
                
                # dbc.Toast(
                #     [html.P("This is the content of the toast", className="mb-0")],
                #     header="Date",
                #     style={'margin': 20}
                #  ),
                # dbc.Toast(
                #     [html.P("This is the content of the toast", className="mb-0")],
                #     header="Total Debit",
                #     style={'margin': 20}
                #  ),
                # dbc.Toast(
                #     [html.P("This is the content of the toast", className="mb-0")],
                #     header="Total Credit",
                #     style={'margin': 20}
                #  ),
            ]),#close Row

            

            dbc.Col([
                dcc.Loading(children=[ 
                    html.Div(
                        [ html.Div(id='table-placeholder', children=[]) ], 
                        className='row'
                        ),
                    ], 
                    color="#119DFF", type="dot", fullscreen=True,
                ),

                 

            ]),# close Col

            dbc.Col([
                
            # ********************************************************************
                html.Div(
                    [ html.Div(id='pdf_frame', children=[], ) ], 
                    className='row',
                    ),
            ]),
            




            dbc.Col([
                # invisible compenent who allow ou to store data temporarly
                dcc.Store(id= 'store-data', data= {}, storage_type= 'memory'),
                # dcc.Store(id= 'store-filtred-data', data= {}, storage_type= 'memory'),
            ]),# close Col
            # dbc.Row([
            #     dbc.Alert("Save as CSV", color="success" ,style={'width' : 130}),
            #     dbc.Alert("Save as Json", color="info" ,style={'width' : 130}),
            # ])
            
        ]),# close Row
    # style={"max-width": "800px"},
    className="p-1",
    
)


def save_file(name, content):   
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

# ***************       prediction      ******************
def predict_bank (path):
    # prepper text
    pdf = pdfplumber.open(path)
    page = pdf.pages[0]
    text = page.extract_text()
    # delete tabs, newlines, etc,' ':
    text = re.sub('\s+',' ',text)
    pdf_head_text = text[0:100]

    # load model and old dataSet to re-transform to TFIDF
    model1 = pickle.load(open('./ML/model.pkl','rb'))
    df_tfidf = pickle.load(open("./ML/data_frame_for_TFIDF.pickle", "rb"))
    tfidf_new = TfidfVectorizer()

    # prepper df
    df2 = {'text' : pdf_head_text  ,'target' :'other' , 'Y' : '20'}
    df = df_tfidf
    df = df.append(df2 , ignore_index = True  )
    df3 = df[df['Y']== '20']

    tfidf_new = TfidfVectorizer()
    # apply TFIDF on old data
    features_new = tfidf_new.fit_transform(df_tfidf.text).toarray()

    # apply TFIDF on new data
    new_X_test = tfidf_new.transform(df3.text).toarray()
    

    # predict bank
    y_pred = model1.predict(new_X_test)

    return y_pred[0]

    



def parse_contents(path ):
    try:
        if 'pdf' in path:
            return pd.DataFrame(rab.Amen_Bank(path))
            # Assume that the user uploaded a CSV file
            if (predict_bank(path)=='0'):
                return pd.DataFrame(rab.Amen_Bank(path))
            elif (predict_bank(path)=='1'):
                return pd.DataFrame(rab.ATB(path))
            elif (predict_bank(path)=='2'):
                return pd.DataFrame(rab.BH(path))

    except Exception as e:
        print(e)
        return 'There was an error processing this file.'



# callback for storing data inside the browser or localy
@app.callback(
    Output('store-data', 'data'),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def store_Data(uploaded_filenames, uploaded_file_contents):
    """delete all files in the temporary forder """
    for file in os.listdir(UPLOAD_DIRECTORY):
        os.remove(os.path.join(UPLOAD_DIRECTORY, file))

    """Save uploaded files and regenerate the file list."""
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)
            return parse_contents(UPLOAD_DIRECTORY+'/'+uploaded_filenames[0]).to_dict('records')
            

@app.callback(
    Output('table-placeholder', 'children'),
    [Input('store-data', 'data'),
     Input('my-dropdown', 'value'),])
def create_dataTable(data,value):
    # 2. convert string like JSON to pandas dataframe
    dff = pd.DataFrame(data)
    print (value)
    df2 = dff
    if value == None:
        df2 = dff[["DATE", "LIBELLE","VALEUR","DEBIT","CREDIT"]]
    else :
        df2 = dff[value]

    my_table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df2.columns],
        data=df2.to_dict('records')
    )
    return my_table

# *************** vew pdf ****************
# @app.callback(
#     Output('pdf-placeholder', 'children'),
#     [Input("upload-data", "filename"),
#      Input("upload-data", "contents"),])
     
# def create_pdfviewer(name,cont):

#     print ( UPLOAD_DIRECTORY , name )
#     # df2 = dff
#     # if value == None:
#     #     df2 = dff[["DATE", "LIBELLE","VALEUR","DEBIT","CREDIT"]]
#     # else :
#     #     df2 = dff[value]

#     # my_table = dash_table.DataTable(
#     #     columns=[{"name": i, "id": i} for i in df2.columns],
#     #     data=df2.to_dict('records')
#     # )
#     return True

# ****************************************

# offcanvas componet 
@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


@app.callback(
    [Output('banque_toast', 'children'),
    #  Output('date_toast', 'children'),
    #  Output('total_debit_toast', 'children'),
    #  Output('total_credit_toast', 'children'),
    ],
    Input('store-data', 'data') 
    )
def create_toast(data):
    dff = pd.DataFrame(data)
    # sum_debit = 0
    # sum_credit = 0
    # for d in dff['DEBIT']:
    #     sum_debit = sum_debit + int(d)
    # for c in dff['CREDIT']:
    #     sum_credit = sum_credit + int(c)

    banque_toast = dbc.Toast(
            [html.P(dff['BANQUE'].unique(), className="mb-0")],
            header="Banque",
            style={'margin': 10}
            ),
    # date_toast = dbc.Toast(
    #         [html.P(dff['DEVISE'].unique(), className="mb-0")],
    #         header="DEVISE",
    #         style={'margin': 10}
    #         ),
    # total_debit_toast = dbc.Toast(
    #         [html.P(sum_credit, className="mb-0")],
    #         header="Total credit",
    #         style={'margin': 10}
    #         ),
    # total_credit_toast = dbc.Toast(
    #         [html.P(sum_debit, className="mb-0")],
    #         header="Total debit",
    #         style={'margin': 10}
    #         ),
    
    
    return banque_toast, #date_toast, total_debit_toast, total_credit_toast

@app.callback(
    [Output('dropdown_offcanvas', 'children'),],
    Input('store-data', 'data') 
    )
def create_dropdown(data):
    dff = pd.DataFrame(data)
    drop_down= dcc.Dropdown(id='my-dropdown', multi=True,
                     options=[{'label': x, 'value': x}  for x in dff.columns],
                     value=["DATE", "LIBELLE","VALEUR","DEBIT","CREDIT"]),
    return drop_down

@app.callback(
    Output("download-dataframe-csv", "data"),
    [Input('store-data', 'data'), Input("saveCsv", "n_clicks"),Input("saveJson", "n_clicks"), Input("savexlsx", "n_clicks"), Input("send_to_elk", "n_clicks") ],
    prevent_initial_call=True,
)
def func(data , n1, n2, n3, n4):
    if n1:
        if data:
            df =  pd.DataFrame(data)
            return dcc.send_data_frame(df.to_csv, "releve.csv")
    elif n2:
        if data:
            df =  pd.DataFrame(data)
            return dcc.send_data_frame(df.to_json, "releve.json")
    elif n3:
        if data:
            df =  pd.DataFrame(data)
            return dcc.send_data_frame(df.to_excel, "releve.xlsx", sheet_name="Sheet_1")
    elif n4:
        if data:
            df =  pd.DataFrame(data)
            pdf_elk.doc_generator(df)


# ************************

@app.callback(
    Output("pdf_frame", "children"),
    [Input('store-data', 'data'), Input("visualisePDF", "n_clicks") ],
    prevent_initial_call=True,
)
def func(data , n1 ):
    if n1:
        if data:
            df =  pd.DataFrame(data)
            for file in os.listdir(UPLOAD_DIRECTORY):
                source = UPLOAD_DIRECTORY+"/"  
                # iframe = html.Iframe(src=UPLOAD_DIRECTORY+"/"+file)
                with open(UPLOAD_DIRECTORY+"/"+file, 'rb') as pdf:
                    pdf_data = base64.b64encode(pdf.read()).decode('utf-8')
                # frame = html.Iframe (src=os.path.join(source, file))
                frame = html.ObjectEl(data='data:application/pdf;base64,'+ pdf_data,type='application/pdf',height=695, width=470) 
                return frame
   




if __name__ == "__main__":
    app.run_server()