import pandas as pd
import sklearn as sk
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA, IncrementalPCA
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler # normalizar los datos
from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    df_heart = pd.read_csv('.\Data\heart.csv')
    print(df_heart.head(3))

    # the data most be saparated between features & target
    df_features = df_heart.drop(['target'], axis = 1)
    df_target   = df_heart['target']

    # Para realizar el PCA se deben normalizar los datos
    # en este caso utilizo StandardScaler
    df_features = StandardScaler().fit_transform(df_features) #load data, fit the model and applies the transformation

    # separate the data between Train, Test and validation
    X_train, X_test, y_train, y_test = train_test_split(df_features, df_target, test_size=0.3, random_state=42)

    print(X_train.shape)
    print(y_train.shape)

    # n_components = min(n_observations, n_features)
    pca = PCA(n_components = 10 )
    pca.fit(X_train)

    ipca = IncrementalPCA(n_components = 3, batch_size = 10)
    ipca.fit(X_train)

    # range between zero and the n_components, and importance ratio of each component 
    plt.plot(range(len(pca.explained_variance_)), pca.explained_variance_ratio_)
    plt.show()

    logistic = LogisticRegression(solver='lbfgs')

    df_train = pca.transform(X_train)
    df_test  = pca.transform(X_test)
    logistic.fit(df_train, y_train)
    print('Score: ', logistic.score(df_test, y_test))

    df_train = ipca.transform(X_train)
    df_test  = ipca.transform(X_test)
    logistic.fit(df_train, y_train)
    print('Score: ', logistic.score(df_test, y_test))
