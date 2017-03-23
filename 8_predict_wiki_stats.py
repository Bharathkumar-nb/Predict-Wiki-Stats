import numpy as np
from sklearn import linear_model
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split

#data = np.loadtxt('./final_dataset.csv', delimiter=',')
#data = np.loadtxt('./final_dataset_addition.csv', delimiter=',')
data = np.loadtxt('./final_dataset_mult.csv', delimiter=',')

split = int(data.shape[0]*0.9)

#X, test_X, y, test_y = train_test_split(data[:,:-1], data[:,-1], test_size=0.15)

X = data[:split,:-1]
y = data[:split,-1]

test_X = data[split+1:,:-1]
test_y = data[split+1:,-1]

print('Taining matrix size: ', X.shape)
print('Test matrix size: ', test_X.shape)


print('Linear Regression')
linear_reg = linear_model.LinearRegression()

linear_reg.fit(X,y)
#print('Coefficients: \n', linear_reg.coef_)
# The mean squared error
print("Mean squared error: %.2f" % np.mean((linear_reg.predict(test_X) - test_y) ** 2))
print()

print('Ridge: alpha = 0.5')
ridge_reg = linear_model.Ridge (alpha = .5)

ridge_reg.fit(X,y)
#print('Coefficients: \n', ridge_reg.coef_)
# The mean squared error
print("Mean squared error: %.2f" % np.mean((ridge_reg.predict(test_X) - test_y) ** 2))
print()

print('Ridge: alpha = 0.3')
ridge_reg = linear_model.Ridge (alpha = .3)

ridge_reg.fit(X,y)
#print('Coefficients: \n', ridge_reg.coef_)
# The mean squared error
print("Mean squared error: %.2f" % np.mean((ridge_reg.predict(test_X) - test_y) ** 2))
print()

print('Ridge: alpha = 0.1')
ridge_reg = linear_model.Ridge (alpha = .1)

ridge_reg.fit(X,y)
#print('Coefficients: \n', ridge_reg.coef_)
# The mean squared error
print("Mean squared error: %.2f" % np.mean((ridge_reg.predict(test_X) - test_y) ** 2))
print()

print('Lasso: alpha = 0.1')
lasso_reg = linear_model.Lasso(alpha = 0.1,max_iter=5000)

lasso_reg.fit(X,y)
#print('Coefficients: \n', lasso_reg.coef_)
# The mean squared error
print("Mean squared error: %.2f" % np.mean((lasso_reg.predict(test_X) - test_y) ** 2))
print()

print('Lasso: alpha = 0.2')
lasso_reg = linear_model.Lasso(alpha = 0.2)

lasso_reg.fit(X,y)
#print('Coefficients: \n', lasso_reg.coef_)
# The mean squared error
print("Mean squared error: %.2f" % np.mean((lasso_reg.predict(test_X) - test_y) ** 2))
print()

print('Lasso: alpha = 0.3')
lasso_reg = linear_model.Lasso(alpha = 0.3)

lasso_reg.fit(X,y)
#print('Coefficients: \n', lasso_reg.coef_)
# The mean squared error
print("Mean squared error: %.2f" % np.mean((lasso_reg.predict(test_X) - test_y) ** 2))
print()

print('Bayesian Ridge Regression')
bayes_reg = linear_model.BayesianRidge()

bayes_reg.fit(X,y)
#print('Coefficients: \n', bayes_reg.coef_)
# The mean squared error
#print(bayes_reg.predict(test_X))
print("Mean squared error: %.2f" % np.mean((bayes_reg.predict(test_X) - test_y) ** 2))
print()


print('SVR')
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
svr_lin = SVR(kernel='linear', C=1e3)
svr_poly = SVR(kernel='poly', C=1e3, degree=2)
y_rbf = svr_rbf.fit(X, y).predict(test_X)
y_lin = svr_lin.fit(X, y).predict(test_X)
y_poly = svr_poly.fit(X, y).predict(test_X)

print('SVR - kernel=rbf, C=1e3, gamma=0.1')
print("Mean squared error: %.2f" % np.mean((y_rbf - test_y) ** 2))
print('SVR - kernel=linear, C=1e3')
print("Mean squared error: %.2f" % np.mean((y_lin - test_y) ** 2))
print('SVR - kernel=poly, C=1e3, degree=2')
print("Mean squared error: %.2f" % np.mean((y_poly - test_y) ** 2))

print()
svr_rbf = SVR(kernel='rbf', C=5e3, gamma=0.1)
svr_lin = SVR(kernel='linear', C=5e3)
svr_poly = SVR(kernel='poly', C=5e3, degree=3)
y_rbf = svr_rbf.fit(X, y).predict(test_X)
y_lin = svr_lin.fit(X, y).predict(test_X)
y_poly = svr_poly.fit(X, y).predict(test_X)

print('SVR - kernel=rbf, C=1e3, gamma=0.05')
print("Mean squared error: %.2f" % np.mean((y_rbf - test_y) ** 2))
print('SVR - kernel=linear, C=1e3')
print("Mean squared error: %.2f" % np.mean((y_lin - test_y) ** 2))
print('SVR - kernel=poly, C=1e3, degree=3')
print("Mean squared error: %.2f" % np.mean((y_poly - test_y) ** 2))
