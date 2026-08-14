# SuperKart Sales Forecasting

Predicts `Product_Store_Sales_Total` for a product/store combination using a
hyperparameter-tuned Gradient Boosting Regressor trained on SuperKart's
historical sales data.

## Live app

Deployed for free on [Streamlit Community Cloud](https://streamlit.io/cloud)
(no Hugging Face, no paid tier). Entry point: `streamlit_app.py` at the repo
root, which loads `model/best_superkart_model.joblib` directly and runs
inference in-process — no separate backend needs to stay online.

## Repo structure

- `streamlit_app.py`, `requirements.txt`, `model/` — the self-contained app
  that is actually deployed live.
- `backend/` — a Flask REST API (`POST /v1/predict`) wrapping the same model,
  plus a `Dockerfile` for running it as a standalone container. Useful if you
  want a pure API endpoint (e.g. for other clients) or want to deploy it
  separately (Render, Fly.io, Cloud Run, etc.).
- `frontend/` — the original two-tier Streamlit UI that calls the Flask API
  over HTTP instead of loading the model directly. Points at
  `BACKEND_API_URL` (defaults to `http://127.0.0.1:7860/v1/predict`). Kept
  for reference / local Docker use.

## Model

Trained in `train.py`-equivalent notebook cells: OneHotEncoding for
categorical features inside a `sklearn` `Pipeline`, feeding a
`GradientBoostingRegressor` tuned via `GridSearchCV`. See the project
notebook for full EDA, preprocessing rationale, and model comparison
(Gradient Boosting vs. XGBoost, baseline vs. tuned).

## Running locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
