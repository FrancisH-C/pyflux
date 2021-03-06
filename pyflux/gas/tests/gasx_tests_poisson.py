import numpy as np
import pandas as pd
import pyflux as pf

# Set up some data to use for the tests

countdata = np.random.poisson(3,500)
x1 = np.random.normal(0,1,500)
x2 = np.random.normal(0,1,500)
data = pd.DataFrame([countdata,x1,x2]).T
data.columns = ['y', 'x1', 'x2']

x1_oos = np.random.normal(0,1,30)
x2_oos = np.random.normal(0,1,30)
countdata_oos = np.random.poisson(3,30)

data_oos = pd.DataFrame([countdata_oos,x1_oos,x2_oos]).T
data_oos.columns = ['y', 'x1', 'x2']


def test_poisson_no_terms():
    """
    Tests the length of the latent variable vector for an GASX model
    with no AR or SC terms, and tests that the values are not nan
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=0, sc=0, family=pf.Poisson())
    x = model.fit()
    assert(len(model.latent_variables.z_list) == 2)
    lvs = np.array([i.value for i in model.latent_variables.z_list])
    assert(len(lvs[np.isnan(lvs)]) == 0)

def test_poisson_couple_terms():
    """
    Tests the length of the latent variable vector for an GASX model
    with 1 AR and 1 SC term, and tests that the values are not nan
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit()
    assert(len(model.latent_variables.z_list) == 4)
    lvs = np.array([i.value for i in model.latent_variables.z_list])
    assert(len(lvs[np.isnan(lvs)]) == 0)

def test_poisson_bbvi():
    """
    Tests an GASX model estimated with BBVI, and tests that the latent variable
    vector length is correct, and that value are not nan
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('BBVI',iterations=100)
    assert(len(model.latent_variables.z_list) == 4)
    lvs = np.array([i.value for i in model.latent_variables.z_list])
    assert(len(lvs[np.isnan(lvs)]) == 0)

def test_bbvi_mini_batch():
    """
    Tests an GASX model estimated with BBVI and that the length of the latent variable
    list is correct, and that the estimated latent variables are not nan
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('BBVI',iterations=500, mini_batch=32)
    assert(len(model.latent_variables.z_list) == 4)
    lvs = np.array([i.value for i in model.latent_variables.z_list])
    assert(len(lvs[np.isnan(lvs)]) == 0)

def test_bbvi_elbo():
    """
    Tests that the ELBO increases
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('BBVI',iterations=500, record_elbo=True, map_start=False)
    assert(x.elbo_records[-1]>x.elbo_records[0])

def test_bbvi_mini_batch_elbo():
    """
    Tests that the ELBO increases
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('BBVI',iterations=500, mini_batch=32, record_elbo=True, map_start=False)
    assert(x.elbo_records[-1]>x.elbo_records[0])

def test_poisson_mh():
    """
    Tests an GASX model estimated with Metropolis-Hastings, and tests that the latent variable
    vector length is correct, and that value are not nan
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('M-H',nsims=300)
    assert(len(model.latent_variables.z_list) == 4)
    lvs = np.array([i.value for i in model.latent_variables.z_list])
    assert(len(lvs[np.isnan(lvs)]) == 0)

def test_poisson_laplace():
    """
    Tests an GASX model estimated with Laplace approximation, and tests that the latent variable
    vector length is correct, and that value are not nan
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('Laplace')
    assert(len(model.latent_variables.z_list) == 4)
    lvs = np.array([i.value for i in model.latent_variables.z_list])
    assert(len(lvs[np.isnan(lvs)]) == 0)

def test_poisson_pml():
    """
    Tests an GASX model estimated with PML, and tests that the latent variable
    vector length is correct, and that value are not nan
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('PML')
    assert(len(model.latent_variables.z_list) == 4)
    lvs = np.array([i.value for i in model.latent_variables.z_list])
    assert(len(lvs[np.isnan(lvs)]) == 0)

def test_poisson_predict_length():
    """
    Tests that the length of the predict dataframe is equal to no of steps h
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit()
    x.summary()
    assert(model.predict(h=5, oos_data=data_oos).shape[0] == 5)

def test_poisson_predict_is_length():
    """
    Tests that the length of the predict IS dataframe is equal to no of steps h
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit()
    assert(model.predict_is(h=5).shape[0] == 5)

def test_poisson_predict_nans():
    """
    Tests that the predictions are not NaNs
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit()
    x.summary()
    assert(len(model.predict(h=5, oos_data=data_oos).values[np.isnan(model.predict(h=5, 
        oos_data=data_oos).values)]) == 0)

def test_poisson_predict_is_nans():
    """
    Tests that the predictions in-sample are not NaNs
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit()
    x.summary()
    assert(len(model.predict_is(h=5).values[np.isnan(model.predict_is(h=5).values)]) == 0)

def test_predict_nonconstant():
    """
    We should not really have predictions that are constant (should be some difference)...
    This captures bugs with the predict function not iterating forward
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    assert(not np.all(predictions.values==predictions.values[0]))
    
def test_predict_is_nonconstant():
    """
    We should not really have predictions that are constant (should be some difference)...
    This captures bugs with the predict function not iterating forward
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    assert(not np.all(predictions.values==predictions.values[0]))
    
def test_predict_intervals():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    model.fit()
    predictions = model.predict(h=10, oos_data=data_oos, intervals=True)

    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test_predict_is_intervals():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    model.fit()
    predictions = model.predict_is(h=10, intervals=True)
    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test_predict_intervals_bbvi():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('BBVI', iterations=100)
    predictions = model.predict(h=10, oos_data=data_oos, intervals=True)

    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test_predict_is_intervals_bbvi():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('BBVI', iterations=100)
    predictions = model.predict_is(h=10, intervals=True)
    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test_predict_intervals_mh():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('M-H', nsims=400)
    predictions = model.predict(h=10, oos_data=data_oos, intervals=True)

    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test_predict_is_intervals_mh():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('M-H', nsims=400)
    predictions = model.predict_is(h=10, intervals=True)
    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test_sample_model():
    """
    Tests sampling function
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('BBVI', iterations=100)
    sample = model.sample(nsims=100)
    assert(sample.shape[0]==100)
    assert(sample.shape[1]==len(data)-1)

def test_ppc():
    """
    Tests PPC value
    """
    model = pf.GASX(formula="y ~ x1", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('BBVI', iterations=100)
    p_value = model.ppc()
    assert(0.0 <= p_value <= 1.0)







## Try more than one predictor

def test2_poisson_no_terms():
    """
    Tests the length of the latent variable vector for an GASX model
    with no AR or SC terms, and two predictors, and tests that the values 
    are not nan
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=0, sc=0, family=pf.Poisson())
    x = model.fit()
    assert(len(model.latent_variables.z_list) == 3)
    lvs = np.array([i.value for i in model.latent_variables.z_list])
    assert(len(lvs[np.isnan(lvs)]) == 0)

def test2_poisson_couple_terms():
    """
    Tests the length of the latent variable vector for an GASX model
    with 1 AR and 1 SC term, and two predictors, and tests that the values 
    are not nan
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit()
    assert(len(model.latent_variables.z_list) == 5)
    lvs = np.array([i.value for i in model.latent_variables.z_list])
    assert(len(lvs[np.isnan(lvs)]) == 0)

def test2_poisson_bbvi():
    """
    Tests an GASX model estimated with BBVI, with multiple predictors, and 
    tests that the latent variable vector length is correct, and that value are not nan
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('BBVI', iterations=100)
    assert(len(model.latent_variables.z_list) == 5)
    lvs = np.array([i.value for i in model.latent_variables.z_list])
    assert(len(lvs[np.isnan(lvs)]) == 0)

def test_bbvi_mini_batch():
    """
    Tests an GASX model estimated with BBVI and that the length of the latent variable
    list is correct, and that the estimated latent variables are not nan
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('BBVI',iterations=500, mini_batch=32)
    assert(len(model.latent_variables.z_list) == 5)
    lvs = np.array([i.value for i in model.latent_variables.z_list])
    assert(len(lvs[np.isnan(lvs)]) == 0)

def test_bbvi_elbo():
    """
    Tests that the ELBO increases
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('BBVI',iterations=500, record_elbo=True, map_start=False)
    assert(x.elbo_records[-1]>x.elbo_records[0])

def test_bbvi_mini_batch_elbo():
    """
    Tests that the ELBO increases
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('BBVI',iterations=500, mini_batch=32, record_elbo=True, map_start=False)
    assert(x.elbo_records[-1]>x.elbo_records[0])

def test2_poisson_mh():
    """
    Tests an GASX model estimated with MEtropolis-Hastings, with multiple predictors, and 
    tests that the latent variable vector length is correct, and that value are not nan
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('M-H', nsims=300)
    assert(len(model.latent_variables.z_list) == 5)
    lvs = np.array([i.value for i in model.latent_variables.z_list])
    assert(len(lvs[np.isnan(lvs)]) == 0)

def test2_poisson_laplace():
    """
    Tests an GASX model estimated with Laplace, with multiple predictors, and 
    tests that the latent variable vector length is correct, and that value are not nan
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('Laplace')
    assert(len(model.latent_variables.z_list) == 5)
    lvs = np.array([i.value for i in model.latent_variables.z_list])
    assert(len(lvs[np.isnan(lvs)]) == 0)

def test2_poisson_pml():
    """
    Tests an GASX model estimated with PML, with multiple predictors, and 
    tests that the latent variable vector length is correct, and that value are not nan
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('PML')
    assert(len(model.latent_variables.z_list) == 5)
    lvs = np.array([i.value for i in model.latent_variables.z_list])
    assert(len(lvs[np.isnan(lvs)]) == 0)

def test2_poisson_predict_length():
    """
    Tests that the length of the predict dataframe is equal to no of steps h
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit()
    x.summary()
    assert(model.predict(h=5, oos_data=data_oos).shape[0] == 5)

def test2_poisson_predict_is_length():
    """
    Tests that the length of the predict IS dataframe is equal to no of steps h
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit()
    assert(model.predict_is(h=5).shape[0] == 5)

def test2_poisson_predict_nans():
    """
    Tests that the predictions are not NaNs
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit()
    x.summary()
    assert(len(model.predict(h=5, oos_data=data_oos).values[np.isnan(model.predict(h=5, 
        oos_data=data_oos).values)]) == 0)

def test2_poisson_predict_is_nans():
    """
    Tests that the predictions in-sample are not NaNs
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit()
    x.summary()
    assert(len(model.predict_is(h=5).values[np.isnan(model.predict_is(h=5).values)]) == 0)

def test2_predict_nonconstant():
    """
    We should not really have predictions that are constant (should be some difference)...
    This captures bugs with the predict function not iterating forward
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    assert(not np.all(predictions.values==predictions.values[0]))
    
def test2_predict_is_nonconstant():
    """
    We should not really have predictions that are constant (should be some difference)...
    This captures bugs with the predict function not iterating forward
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    assert(not np.all(predictions.values==predictions.values[0]))
    
def test2_predict_intervals():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    model.fit()
    predictions = model.predict(h=10, oos_data=data_oos, intervals=True)

    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test2_predict_is_intervals():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    model.fit()
    predictions = model.predict_is(h=10, intervals=True)
    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test2_predict_intervals_bbvi():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('BBVI', iterations=100)
    predictions = model.predict(h=10, oos_data=data_oos, intervals=True)

    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test2_predict_is_intervals_bbvi():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('BBVI', iterations=100)
    predictions = model.predict_is(h=10, intervals=True)
    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test2_predict_intervals_mh():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('M-H', nsims=400)
    predictions = model.predict(h=10, oos_data=data_oos, intervals=True)

    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test2_predict_is_intervals_mh():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('M-H', nsims=400)
    predictions = model.predict_is(h=10, intervals=True)
    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test2_sample_model():
    """
    Tests sampling function
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('BBVI', iterations=100)
    sample = model.sample(nsims=100)
    assert(sample.shape[0]==100)
    assert(sample.shape[1]==len(data)-1)

def test2_ppc():
    """
    Tests PPC value
    """
    model = pf.GASX(formula="y ~ x1 + x2", data=data, ar=1, sc=1, family=pf.Poisson())
    x = model.fit('BBVI', iterations=100)
    p_value = model.ppc()
    assert(0.0 <= p_value <= 1.0)

