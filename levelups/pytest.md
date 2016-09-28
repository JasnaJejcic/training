<center>
![](http://docs.pytest.org/en/latest/_static/pytest1.png)
# Level Up
</center>

## Why?

* nose is deprecated
* pytest is more pythonic
* prettier fail reports
* cool features!

## Quick Features

* Backward compatible with nose
* Use plain assert statements with clever introspection

```python
assert 1 + 1 == 2  # pytest
self.assertEqual(1 + 1, 2)  # nose/unittest
```

## Differences

write tests as functions

```python
def test_the_thing():
    assert …
```

But you can still group with classes

```python
class FeatureTests:
    def test_is_a_company(self):
        assert …
        
    def test_has_is_b2b(self):
        assert …
```

Testing exceptions are raised

```python
with pytest.raises(ZeroDivisionError, message="Damn zeros in my denominator"):
	1/0

with pytest.raises(ValueError) as excinfo:
        	myfunc()
    	excinfo.match(r'.* 123 .*')
```

Comparing floating points

```python
from pytest import approx

0.1 + 0.2 == approx(0.3)
(0.1 + 0.2, 0.2 + 0.4) == approx((0.3, 0.6))

1.0001 == approx(1, rel=1e-3)
1.0001 == approx(1, abs=1e-3)
```

## Running


pytest [directory]

pytest test_mod.py::TestClass::test_method

**-x** stops on first fail

**--pdb** drop to pdb on failure

**--pdbcls=modulename:classname** custom debugger (i.e ipdb)

**-k** run tests that match a string “test_feature”

**-m** run tests with certain markers “unit and not slow”

**--fixtures** show available fixtures

**--full-trace** full tracebacks

**-s** no capture - sometimes needed to make pdb work

## Test discovery

* All folders
* files matching `test_*.py` and `*_test.py`
* `conftest.py` files
* `Test` prefixed classes
* `test_` prefixed functions

## Conftest

* Directory specific hooks. 
* Are ran and apply to all files in the current directory and all directoires below. 
* Can put fixture here or `import` fixture from plainly labelled files.

## Fixture

Powerful replacement for setup/teardown

Can be rebuilt on a per test, module or session basis

Just decorate a function with `@pytest.fixture` with optional `scope` [function/module/session] and include the function name as a parameter to any test functions.


### File based

```python
@pytest.fixture
def grade_row_metrics():
    grade_row_metrics = [
        metrics.num_positives,
        metrics.num_negatives,
        metrics.num_client,
        metrics.percent_positive,
        metrics.num_universe,
        metrics.num_universe_minus_opps,
        metrics.num_universe_minus_client,
        metrics.num_universe_minus_client_and_tps,
    ]
    return grade_row_metrics


@pytest.fixture
def grade_row(grade_row_dataset, grade_row_metrics):
    dataset = grade_row_dataset
    return helpers.GradeRow(dataset, 'A', grade_row_metrics)


class Test_GradeRow:

    def test_get_stats(self, grade_row):
        result = grade_row.get_stats()
        expected = {
            'Grade': 'A',
            'Positives': 3,
            'Negatives': 3,
            'Client': 7,
            'Percent positive': 0.5,
            'Universe': 15,
            'Universe (-Opps)': 12,
            'Universe (-Opps -Client)': 8,
            'Universe (-Opps -Client -TPS)': 6,
        }
        assert result == expected

    def test_when_frame_empty(self, grade_row_metrics):
        df = pd.DataFrame(
            columns=('cid', 'label', 'set_', 'source', 'url', 'score',
                     'is_background', 'grade', 'TPS')
        )
        grade_row = helpers.GradeRow(Dataset(df, None), 'X', grade_row_metrics)
        result = grade_row.get_stats()
        expected = {
            'Grade': 'X',
            'Positives': 0,
            'Negatives': 0,
            'Client': 0,
            'Percent positive': np.nan,
            'Universe': 0,
            'Universe (-Opps)': 0,
            'Universe (-Opps -Client)': 0,
            'Universe (-Opps -Client -TPS)': None,
        }

        assert result == expected
```

### Module based

Setting up feature file fixture for the mario feature tests

```
@pytest.fixture
def rfa_feature_df():
    data = pd.DataFrame({
        "cid": [1, 2, 3],
        "rfa/turnover": [100, 0 , 10],
        "rfa/trade_debtors": [1000, 100, 0],
        "rfa/stocks": [int(4.5e3), int(3e9), 0],
        "rfa/total_fixed_assets": [int(1.125e4), int(2e6), 0]
    })
    return data
```

### Session based

In plug we can only have one spark instance. With fixture we can set it up at the begining and pass it around.

```python
@pytest.fixture(scope="session")
def spark_context(request):
    """ fixture for creating a spark context
    Args:
        request: pytest.FixtureRequest object
    """
    conf = SparkConf()
    conf.set("spark.executor.memory", "512m")
    conf.set("spark.cores.max", "1")
    conf.set("spark.app.name", "nosetest")

    spark_context = SparkContext(conf=conf)
    return spark_context


@pytest.fixture(scope="session")
def hive_context(spark_context):
    return HiveContext(spark_context)
```

Fixture can have fixture (of the same scope).

Tests can use this as before.

```python
def test_loading_spam(hive_context):
    """Test that correct set of spammy domains is returned."""
    csv_filepath = os.path.join(lookup_fixture, 'spam.csv')
    spam = data_loaders.read_and_format_dataframe(
        csv_filepath, hive_context, data_loaders.filter_spam_urls,
        header=True)

    expected = {'conservatories-in-hertfordshire.co.uk', 'auto-wash.co.uk',
                'msindustries.co.uk', 'midlandbuildingsolutions.com',
                'about.me', 'anallighten.co.uk'}
    assert spam == expected
```

[Previous implementation](https://github.com/pelucid/plug/blob/a116da1bd195734683519bc5a367794eea81143a/etl/tests/__init__.py) was hacky.

### Teardown with yield

```
@pytest.fixture(scope="module")
def smtp(request):
    smtp = smtplib.SMTP("smtp.gmail.com")
    yield smtp  # provide the fixture value
    print("teardown smtp")
    smtp.close()
```

```
@pytest.fixture
def passwd():
    with open("/etc/passwd") as f:
        yield f.readlines()
```

## Built in fixtures

* cache - key/value store to persist state between test sessions
* pytestconfig - access to command line args
* tempdir - temporary directories

## Temporary directories

tmpdir is a py.path.local object which offers os.path methods and more

* each tmpdir is unique to the test (in a base tmp directory and incremented as pytest-NUM)
* py.test keeps the last 3 and cleans up the rest 

Use cases:

* Fixture - i.e. fake feature files
* In a flow for intermediate outputs
* end-to-end mario tests
* Anything that reads or writes

```python
def test_read_model_eval_set(tmpdir, simple_dataframe):
    fn = tmpdir.join("evaluation-scored-set.csv")
    simple_dataframe.to_csv(str(fn), index=False)

    result = mri.read_model_eval_set(str(tmpdir))

    assert isinstance(result, mri.AnalysisDataset)
    assert_frame_equal(result._df, simple_dataframe)
```

[read more](http://doc.pytest.org/en/latest/tmpdir.html)

## Parametrising

You can run the same test logic multiple times with different parameters.

* Makes it easy to add new test cases
* Encourages rigorous testing
* Easier to see whats going on

```python
@pytest.mark.parametrize("feature,expected", [
    (financials.LogTurnover, [2, 0, 1, None]),
    (financials.LogTradeDebtors, [3, 2, 0, None]),
    (financials.LogStock, [np.log10(4.5e3), np.log10(3e9), 0, None]),
])
def test_financial_features(feature, expected, client_data, rfa_feature_df):
    cols = feature.fields + [feature.keyed_by]
    feature_name = feature.feature_name

    result = feature().join_feature(dataset=client_data, feature_df=feature_df[cols])
    expected = pd.Series(expected)
    assert_series_equal(result[feature_name], expected, check_names=False)
```

Examples:

* [plug regex checking](https://github.com/pelucid/plug/blob/682417de728993045451917db6c6d386506f7121/etl/tests/processing/extraction/test_regex.py)
* Mario feature tests [before](https://github.com/pelucid/mario/blob/0188dfeb7718ab56543e306003deafbf7c406eef/tests/unittests/test_features/test_tech_features.py) | [after](https://github.com/pelucid/mario/blob/06ba74a05f78a1c44dd81bd312186c8ee9b1eb6e/tests/unittests/test_features/test_production_features/test_tech_features.py)

## Marking tests

```python
@pytest.mark.xfail(reason='Hard to test')
@pytest.mark.xfail(raises=RuntimeError) # why its failing
@pytest.mark.xfail(sys.version_info >= (3,3))  # fail condition
@pytest.mark.xpass
@pytest.mark.skip('High effort.')
@pytest.mark.skipif()

# custom
@pytest.mark.regression
@pytest.mark.staging
```

Can be used with parametrize! See [plug regex checking](https://github.com/pelucid/plug/blob/682417de728993045451917db6c6d386506f7121/etl/tests/processing/extraction/test_regex.py)

## Plugins

* pytest-catchlog - shows logging in test failures
* pytest-cov - test coverage reporting
* pytest-twisted - tests for twisted apps
* pytest-instafail - report failures as they happen
* Oejskit - runs javascript tests in live browsers
* pytest-xdist - Re-runs all tests then watches for changes to project files re-running any failed tests on changes.
* pytest-sugar

![](https://dl.dropboxusercontent.com/s/j2cfa7sbxroqlg3/Screenshot%202016-09-27%2016.50.03.png?dl=0)
