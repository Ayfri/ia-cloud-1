
def build_model():
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    import mlflow

    mlflow.set_experiment("housing_prices")
    mlflow.sklearn.autolog()

    df = pd.read_csv('data/houses.csv')

    X = df[['size', 'nb_rooms', 'garden']]
    y = df['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    with mlflow.start_run():
        model = LinearRegression()
        model.fit(X_train, y_train)

        model.score(X_test, y_test)

        print("Run ID:", mlflow.active_run().info.run_id)

build_model()
