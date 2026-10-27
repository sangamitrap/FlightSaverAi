FLIGHTSAVER AI — WEB INTERFACE SETUP
====================================

IMPORTANT
---------
This package contains the new web-interface files only. It does NOT replace
your existing FlightSaverAI.ipynb notebook, datasets, or trained model files.

COPY THESE FILES INTO YOUR EXISTING PROJECT FOLDER:
C:\Users\sanga\OneDrive\Desktop\FlightSaverAI

Expected project layout:
FlightSaverAI/
  app.py
  requirements.txt
  FlightSaverAI.ipynb        (keep your existing file)
  models/
    flight_price_model.cbm   (keep your existing file)
    flight_delay_model.cbm   (keep your existing file)
  templates/
    index.html
  static/
    style.css
  Flight_price_prediction/   (keep your existing folder)
  Flight_delay/              (keep your existing folder)

VS CODE STEPS
-------------
1. Download and extract FlightSaverAI_Web_Interface.zip.
2. Open your existing FlightSaverAI folder in VS Code.
3. Copy app.py and requirements.txt into that folder.
4. Copy the templates and static folders into that folder.
5. If asked to merge folders, choose merge. Do not replace the models folder.
6. Open Terminal > New Terminal in VS Code.
7. Run:
   .\.venv\Scripts\Activate.ps1
8. Install Flask:
   python -m pip install Flask
   (CatBoost and pandas should already be installed in your environment.)
9. Start the app:
   python app.py
10. Open this address in your browser:
    http://127.0.0.1:5000

TO STOP
-------
Click the terminal and press Ctrl+C.

NOTES
-----
- Keep both .cbm files inside the existing models folder.
- The notebook is preserved; this package does not include or modify it.
- This interface uses the trained model files. It does not retrain them.
- The price prediction is an estimate, not a live airline fare.
- Delay predictions are estimates based on the trained dataset and selected
  0.30 probability threshold. They are not real-time operational information.
- Airport/carrier codes should be codes represented in the training data.
