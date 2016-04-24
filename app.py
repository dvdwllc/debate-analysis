from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.decomposition import TruncatedSVD
from flask import Flask, render_template, send_from_directory, request
from src.tools import plot_ideology
import dill
from flask import make_response
from functools import update_wrapper


app = Flask(__name__)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

IMG_FOLDER = '/static/img/'

linmod = dill.load(open('dills/linmod.dill', 'rb'))
forestmod = dill.load(open('dills/forestmod.dill', 'rb'))


def predict_ideology(text):
    """
    predicts the political spectrum value for a given chunk of text.
    plots this value on a -10 to 10 scale along with the values of
    several politicians for reference.
    """

    lm_pred = linmod.predict([text])
    rf_pred = forestmod.predict([text])

    return (lm_pred + rf_pred) / 2.


@app.route('/', methods=['GET', 'POST'])
def index():
    # on initial landing, show the default query
    if request.method == 'GET':
        with open('txt/sanders.txt') as default:
            default_query = default.readline()

        return render_template(
            'index.html',
            text=default_query,
            plot='liberal.png',
            result='Liberal'
        )

    else:
        query_text = request.form['query_text'].strip('\n')  # read query
        ideology = predict_ideology(query_text)

        if ideology < -5:
            result = 'Very Liberal'
        elif ideology < -1:
            result = 'Liberal'
        elif ideology < 1:
            result = 'Moderate'
        elif ideology < 5:
            result = 'Conservative'
        else:
            result = 'Very Conservative'

        plot_ideology(ideology, 'query')  # produce plot

        return render_template(
            'index.html',
            text=query_text,
            plot='query.png',
            result = result
        )


@app.route('/img/<filename>')
def send_file(filename):
    return send_from_directory('static/img/', filename)


if __name__ == '__main__':
    app.run(debug=False)
