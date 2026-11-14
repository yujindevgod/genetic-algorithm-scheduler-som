# Genetic Algorithm TV Program Scheduler

Streamlit app for optimizing TV program scheduling using a genetic algorithm.

## Deploy on Streamlit Community Cloud

1. Upload all files in this folder to the root of your GitHub repository.
2. Go to https://share.streamlit.io/ and create a new app from GitHub.
3. Select your repository and branch (`main`).
4. Set the main file path to `Genetical Algorithm TV program scheduler.py`.
5. Deploy.

## Run locally

```bash
pip install -r requirements.txt
streamlit run "Genetical Algorithm TV program scheduler.py"
```

**Note:** The assignment specifies a mutation-rate default of `0.20`, but an allowed range of `0.01–0.05`. The app displays `0.20` initially, then requires selection of an allowed value before execution.
