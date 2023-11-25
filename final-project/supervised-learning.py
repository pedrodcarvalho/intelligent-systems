# Supervised Learning to predict the best model for the scikit-learn digits dataset
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import RidgeClassifier
from sklearn.model_selection import GridSearchCV

# Load the scikit-learn digits dataset
digits = datasets.load_digits()
X, y = digits.data, digits.target

# Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the hyperparameters to be tested
param_grid_knn = {'n_neighbors': [1, 3, 5, 7, 10, 15, 20]}
param_grid_ridge = {'alpha': [0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]}

# Define the models to be tested
knn_model = KNeighborsClassifier()
ridge_model = RidgeClassifier()

# Run the Grid Search for KNN
grid_search_knn = GridSearchCV(knn_model, param_grid_knn, cv=5)
grid_search_knn.fit(X_train, y_train)

# Run the Grid Search for Ridge Regression
grid_search_ridge = GridSearchCV(ridge_model, param_grid_ridge, cv=5)
grid_search_ridge.fit(X_train, y_train)

# Print the accuracies for each model
means_knn = grid_search_knn.cv_results_['mean_test_score']
means_ridge = grid_search_ridge.cv_results_['mean_test_score']
print(f"KNN accuracy: {means_knn}")
print(f"Ridge Regression accuracy: {means_ridge}")

# Get the best parameters for each model
best_params_knn = grid_search_knn.best_params_
best_params_ridge = grid_search_ridge.best_params_

# Train the models with the best parameters
best_knn_model = KNeighborsClassifier(n_neighbors=best_params_knn['n_neighbors'])
best_knn_model.fit(X_train, y_train)

best_ridge_model = RidgeClassifier(alpha=best_params_ridge['alpha'])
best_ridge_model.fit(X_train, y_train)

# Get the accuracies for each model
accuracy_best_knn = best_knn_model.score(X_test, y_test)
accuracy_best_ridge = best_ridge_model.score(X_test, y_test)

# Print the best parameters and accuracies found for each model
print(f"Best parameters for KNN: {best_params_knn['n_neighbors']}, Accuracy: {accuracy_best_knn}")
print(f"Best parameters for Ridge Regression: {best_params_ridge['alpha']}, Accuracy: {accuracy_best_ridge}")

if accuracy_best_knn > accuracy_best_ridge:
    print(f"The best model is KNN, with accuracy of {accuracy_best_knn}")
else:
    print(f"The best model is Ridge Regression, with accuracy of {accuracy_best_ridge}")
