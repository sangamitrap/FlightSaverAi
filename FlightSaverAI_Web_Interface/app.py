
from flask import Flask, render_template, request
from catboost import CatBoostRegressor, CatBoostClassifier
import pandas as pd
import json
from pathlib import Path

app = Flask(__name__)

# Main project folder: FlightSaverAI
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

# Load model configuration
with open(MODEL_DIR / "model_config.json", "r") as file:
    CONFIG = json.load(file)

# Load saved price model
price_model = CatBoostRegressor()
price_model.load_model(
    str(MODEL_DIR / "flight_price_model.cbm")
)

# Load improved full-year delay model
delay_model = CatBoostClassifier()
delay_model.load_model(
    str(MODEL_DIR / CONFIG["delay_model_file"])
)

PRICE_CATEGORICAL = CONFIG["price_categorical_features"]
DELAY_CATEGORICAL = CONFIG["delay_categorical_features"]
DELAY_THRESHOLD = CONFIG["delay_threshold"]


@app.route("/", methods=["GET", "POST"])
def index():
    price_result = None
    delay_result = None
    error = None

    if request.method == "POST":
        action = request.form.get("action")

        try:
            if action == "price":
                flight = pd.DataFrame([{
                    "airline": request.form["airline"],
                    "source_city": request.form["source_city"],
                    "departure_time": request.form["departure_time"],
                    "stops": request.form["stops"],
                    "arrival_time": request.form["arrival_time"],
                    "destination_city": request.form["destination_city"],
                    "class": request.form["travel_class"],
                    "duration": float(request.form["duration"]),
                    "days_left": int(request.form["days_left"])
                }])

                for col in PRICE_CATEGORICAL:
                    flight[col] = flight[col].astype(str)

                prediction = float(price_model.predict(flight)[0])
                price_result = f"₹{prediction:,.2f}"

            elif action == "delay":
                flight = pd.DataFrame([{
                    "month": int(request.form["month"]),
                    "day_of_month": int(request.form["day_of_month"]),
                    "day_of_week": int(request.form["day_of_week"]),
                    "op_unique_carrier": request.form["carrier"].strip().upper(),
                    "origin": request.form["origin"].strip().upper(),
                    "dest": request.form["dest"].strip().upper(),
                    "crs_dep_time": int(request.form["crs_dep_time"]),
                    "crs_arr_time": int(request.form["crs_arr_time"]),
                    "crs_elapsed_time": float(request.form["crs_elapsed_time"]),
                    "distance": float(request.form["distance"])
                }])

                for col in DELAY_CATEGORICAL:
                    flight[col] = flight[col].astype(str)

                probability = float(
                    delay_model.predict_proba(flight)[0][1]
                )

                status = (
                    "Higher delay risk (15+ minutes)"
                    if probability >= DELAY_THRESHOLD
                    else "Lower delay risk"
                )

                delay_result = {
                    "probability": f"{probability:.1%}",
                    "status": status,
                    "threshold": f"{DELAY_THRESHOLD:.0%}"
                }

            else:
                error = "Please submit one of the prediction forms."

        except (KeyError, ValueError):
            error = "Please check that every field contains a valid value."
        except Exception as exc:
            print("Prediction error:", exc)
            error = (
                "Prediction failed. Check the model files and form fields."
            )

    return render_template(
        "index.html",
        price_result=price_result,
        delay_result=delay_result,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
