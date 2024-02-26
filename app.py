import csv
from flask import Flask, jsonify, render_template, request
import datetime
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/loadshedding")
def week_results():
    now = datetime.datetime.now()
    current_date = datetime.datetime.date(now).day
    schedule = find_weekly_schedule(str(current_date))
    return jsonify(schedule)


@app.route("/loadshedding")
def load_shedding():
    schedule = find_schedule("24", "4")
    return jsonify(schedule)

@app.route("/loadshedding/towns")
def town_list():
    try:
        with open("city-power-7.txt", "r") as towns_list:
            towns = towns_list.readlines()[0].split(",")
            return jsonify(towns)
    except FileNotFoundError as file_error:
        return jsonify([])


@app.route("/schedule")
def schedule():
    date = request.args.get("date")
    stage = request.args.get("stage")
    results = find_schedule(date, stage)


    return render_template("schedule.html", date=date, stage=stage, times=results["times"])



# non router functions
def find_weekly_schedule(current_date):
    results = []
    for date in range(int(current_date), int(current_date) + 8):
        current_schedule = find_schedule(str(date), "4")
        results.append(current_schedule)
    return results



def find_schedule(date_of_month:str, power_stage:str) -> list:
    """Finds the schedule for the day given the month and stage

    Args:
        date_of_month (str): The date of the month for which we want to obtain
        the schedule
        power_stage (str): The loadshedding stage

    Returns:
        list: a list of the times loadshedding will take place on that day
    """
    with open("city-power-7.csv", "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        day_schedule = {
            "times":[]
            }
        for row in csv_reader:
            date, start, end, stage = row # unpacking the details
            if date == date_of_month and stage == power_stage:
                day_schedule["date"] = date
                day_schedule["stage"] = stage

                day_schedule["times"].append({
                    "start_time": start,
                    "end_time": end
                })
                
        return day_schedule
    



    
if __name__ == '__main__':
    app.run(debug=True)