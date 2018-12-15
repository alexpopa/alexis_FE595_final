from app import flask_app as app
from flask import render_template, request, send_file, render_template_string
import psycopg2 as psql
import io
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.tools as tls
from plotly.offline import init_notebook_mode, iplot, plot, offline
import plotly.graph_objs as go

dataset = pd.read_csv("real_estate.csv", encoding='ISO-8859-1' )


# -----------------------creating BAR PLOT for the data collected-----------------------#
def show_bar_plot(city_name, col, Title):
    fig = tls.make_subplots(rows=1, cols=1)
    for city in city_name:
        for each in col:
            plot = go.Bar(
                x=dataset[dataset['city'] == city]['city'],
                y=dataset[dataset['city'] == city][each]
                , showlegend=True
                , name=each + ' --- ' + city
            )

            fig.append_trace(plot, 1, 1)
    fig['layout'].update(title=Title)
    div = offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)

    return '<script src="https://cdn.plot.ly/plotly-1.2.0.min.js"></script>' + div



# -----------------------creating BOX PLOT for the data collected-----------------------#
def show_box_plot(city_name, col, Title):
    fig = tls.make_subplots(rows=1, cols=1)
    for city in city_name:
        for each in col:
            plot = go.Box(
                x=dataset[dataset['city'] == city]['city'],
                y=dataset[dataset['city'] == city][each]
                , showlegend=True
                , name=each + ' --- ' + city
            )

            fig.append_trace(plot, 1, 1)
    fig['layout'].update(title=Title)
    div = offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)

    return div
    # return iplot(fig)


#-----------------------creating the lists for all the values that user want to see about the cities-----------------------#
rent , population , mortgage, salary, degree, age = [],[],[],[],[],[]

#-----------------------mapping all the values that user wants to see about the city to all the values available in the data set-----------------------#
for each in dataset.columns.values:
    if 'rent' in each:
        rent.append(each)
    if 'population' in each:
        population.append(each)
    if 'mortgage' in each:
        mortgage.append(each)
    if "salary" in each:
        salary.append(each)
    if "degree" in each:
        degree.append(each)
    if ("age" in each) and ('mortgage' not in each):
        age.append(each)


#Database parameters
params = {
    'user': "alexis",
    'password': "password",
    'dbname': 'dvdrentals',
    'host': 'localhost',
    'port': 5432
}

#main page
@app.route("/", methods=["GET"])
def index():

    return render_template('homepage.html')


#takes in the data of state, cities, plot_type, and data_type
#and then returns the graph of the data

@app.route('/by_cities', methods=['GET', 'POST'])
def by_cities():
    print('cities')

    try:
        print('trying')
        data = request.form
        print(data)
        cities = data['cities'].strip().split('+')
        city_name = [x.replace('"',"'").strip().strip("'") for x in cities]
        print(city_name)

        state = data['state']
        name = data['data_type']
        plot_type = data['plot_type']
        box=True

        print(name)

        ## creating list of the columns the variable "col" on the basis of what is selected on the webpage
        if name == 'Rent':
            col = rent
        if name == 'Mortgage':
            col = mortgage
        if name == 'Salary':
            col = salary
        if name == 'Population':
            col = population
        if (name == 'Age'):
            col = age
        if name == 'HS':
            col = degree

        col

        # -----------------------creating TITLE for each type of plot-----------------------#


        Title = None

        if "population" in col[0]:
            Title = 'POPULATION'
        if "rent" in col[0]:
            Title = 'RENT'
        if "salary" in col[0]:
            Title = 'FAMILY SALARY'
        if "mortgage" in col[0]:
            Title = 'MORTGAGE'
        if "degree" in col[0]:
            Title = 'GRADUATE RATE'
        if ("age" in col[0]) and ("mortgage" not in col[0]):
            Title = 'AGE'

        if (plot_type=='Box'):
            return show_box_plot(city_name, col, Title)
        else:
            return show_bar_plot(city_name, col, Title)


    except Exception as e:
        print(e)


#Gets state name from user and returns in alphabetical order
#the list of cities from that state
@app.route('/state', methods=['GET', 'POST'])
def get_cities():
    print(request)
    print(request.form)
    state = request.form['state']
    print(state)
    df = pd.DataFrame(dataset)
    gdf = df.groupby(df['state_ab'])
    cities = list(gdf.get_group(state).city.unique())
    cities = str(sorted(cities))[1:-1]
    return render_template_string(cities)

city_count = dataset.city.value_counts()
#city_count


# In[ ]:

@app.route('/plot')
def show_city_frequency(number_of_city = 10):
    plot_1 = go.Histogram(
        x=dataset[dataset.city.isin(city_count[:number_of_city].index.values)]['city'],
        showlegend=False)

    ## Creating the grid for the above plot
    fig = tls.make_subplots(rows=1, cols=1)

    ## appending the plot on to the grid
    fig.append_trace(plot_1, 1, 1)

    ## displaying the figure
    fig['layout'].update(showlegend=True, title="Frequency of cities in the dataset ")

    div = offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)

    return '<script src="https://cdn.plot.ly/plotly-1.2.0.min.js"></script>' + div
    #return send_file(img, mimetype='image/png')
    #return render_template_string(plot(fig))