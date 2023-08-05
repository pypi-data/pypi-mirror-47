from pyspark.sql import Row, types
from pyspark.ml import feature, classification
from nose.tools import assert_equal
import pyspark
import py_sparkling

from optimus import Optimus

import optimus.ml.feature as fe

op = Optimus()
spark = op.spark
sc = op.sc


df_cancer = spark.read.csv('tests/data_cancer.csv', sep=',', header=True, inferSchema=True)
columns = ['diagnosis', 'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
           'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean',
           'fractal_dimension_mean']

columns_h2o = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
           'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean',
           'fractal_dimension_mean']


def assert_spark_df(df):
    assert isinstance(df, pyspark.sql.dataframe.DataFrame), "Not a Spark DF"


def assert_spark_model(model):
    assert isinstance(model, pyspark.ml.PipelineModel), "Not a model"


def test_ml_pipe():
    df = sc. \
         parallelize([Row(sentence='this is a test', label=0.),
                     Row(sentence='this is another test', label=1.)]). \
         toDF()

    pl = feature.Tokenizer().setInputCol('sentence') | feature.CountVectorizer()
    ml = pl | classification.LogisticRegression()

    ml_model = ml.fit(df)
    assert_equal(ml_model.transform(df).count(), 2)


def test_logistic_regression_text():
    df = op.sc. \
        parallelize([Row(sentence='this is a test', label=0.),
                     Row(sentence='this is another test', label=1.)]). \
        toDF()

    df_predict, ml_model = op.ml.logistic_regression_text(df, "sentence")

    assert_spark_df(df_predict)

    assert_spark_model(ml_model)


def test_n_gram():
    df = op.sc. \
        parallelize([['this is the best sentence ever'],
                     ['this is however the worst sentence available']]). \
        toDF(schema=types.StructType().add('sentence', types.StringType()))

    df_model, tfidf_model = fe.n_gram(df, input_col="sentence", n=2)

    assert_spark_df(df_model)

    assert_spark_model(tfidf_model)

    assert_equal(df_model.select('sentence', 'features').count(), 2)


def test_random_forest():
    df_model, rf_model = op.ml.random_forest(df_cancer, columns, "diagnosis")

    assert_spark_df(df_model)

    assert isinstance(rf_model, pyspark.ml.classification.RandomForestClassificationModel), "Not a RF model"


def test_decision_tree():
    df_model, rf_model = op.ml.decision_tree(df_cancer, columns, "diagnosis")

    assert_spark_df(df_model)

    assert isinstance(rf_model, pyspark.ml.classification.DecisionTreeClassificationModel), "Not a DT model"


def test_gbt():
    df_model, rf_model = op.ml.gbt(df_cancer, columns, "diagnosis")

    assert_spark_df(df_model)

    assert isinstance(rf_model, pyspark.ml.classification.GBTClassificationModel), "Not a GBT model"


def test_h2o_automl():
    df_model, automl_model = op.ml.h2o_automl(df_cancer, "diagnosis", columns_h2o)

    assert_spark_df(df_model)

    assert isinstance(automl_model, py_sparkling.ml.models.H2OAutoMLModel), "Not a H2OAutoMLModel"

def test_h2o_deeplearning():
    df_model, dl_model = op.ml.h2o_deeplearning(df_cancer, "diagnosis", columns_h2o)

    assert_spark_df(df_model)

    assert isinstance(dl_model, py_sparkling.ml.models.H2ODeepLearningModel), "Not a H2ODeepLearningModel"

def test_h2o_xgboost():
    df_model, xgboost_model = op.ml.h2o_xgboost(df_cancer, "diagnosis", columns_h2o)

    assert_spark_df(df_model)

    assert isinstance(xgboost_model, py_sparkling.ml.models.H2OXGBoostModel), "Not a H2OXGBoostModel"

def test_h2o_gbm():
    df_model, gbm_model = op.ml.h2o_gbm(df_cancer, "diagnosis", columns_h2o)

    assert_spark_df(df_model)

    assert isinstance(gbm_model, py_sparkling.ml.models.H2OGBMModel), "Not a H2OGBMModel"
