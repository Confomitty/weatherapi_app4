from flask import Flask , render_template
import pandas as pd

app = Flask(__name__)       # here __name__ is __main__

stations = pd.read_csv("data_small/stations.txt" , skiprows = 17)
stations = stations[["STAID","STANAME                                 "]]

@app.route("/")             # any url or by default you're on the home page
def home():
    return render_template("home.html",data = stations.to_html())


@app.route("/api/v1/<station>")
def all_data(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename,skiprows=20,parse_dates = ["    DATE"])
    result = df.to_dict(orient = "records")
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station , year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename,skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    yearly = df.loc[df['    DATE'].str.startswith(str(year))].to_dict(orient = "records")
    return yearly


@app.route("/api/v1/<station>/<date>")
def specific(station , date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename,skiprows=20,parse_dates = ["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    return {"station" : station,
            "date" : date,
            "temperature" : temperature}


if __name__ == "__main__":
    app.run(debug=True,port=5001)