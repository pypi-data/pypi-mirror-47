def enum(*vals, **enums):
    """
    Enum without third party libs and compatible with py2 and py3 versions.
    """
    enums.update(dict(zip(vals, vals)))
    return type('Enum', (), enums)


CV_METHOD = enum(
    DATETIME='datetime',
    GROUP='group',
    RANDOM='random',
    STRATIFIED='stratified',
    USER='user',
)


SCORING_TYPE = enum(
    cross_validation='crossValidation',
    validation='validation',
)


DATETIME_AUTOPILOT_DATA_SELECTION_METHOD = enum(
    DURATION='duration',
    ROW_COUNT='rowCount',
)


VERBOSITY_LEVEL = enum(
    SILENT=0,
    VERBOSE=2,
)


# This is deprecated, to be removed in 3.0.
MODEL_JOB_STATUS = enum(
    ERROR='error',
    INPROGRESS='inprogress',
    QUEUE='queue',
)


# This is the job/queue status enum we want to keep.
# In 3.0 this will be INITIALIZED, RUNNING, ABORTED, COMPLETED, ERROR.
# And maybe the name will change to JobStatus.
QUEUE_STATUS = enum(
    ABORTED='ABORTED',
    COMPLETED='COMPLETED',
    ERROR='error',
    INPROGRESS='inprogress',
    QUEUE='queue',
)


AUTOPILOT_MODE = enum(
    FULL_AUTO='auto',
    MANUAL='manual',
    QUICK='quick',
)


PROJECT_STAGE = enum(
    AIM='aim',
    EDA='eda',
    EMPTY='empty',
    MODELING='modeling',
)


ASYNC_PROCESS_STATUS = enum(
    ABORTED='ABORTED',
    COMPLETED='COMPLETED',
    ERROR='ERROR',
    INITIALIZED='INITIALIZED',
    RUNNING='RUNNING',
)


LEADERBOARD_SORT_KEY = enum(
    PROJECT_METRIC='metric',
    SAMPLE_PCT='samplePct',
)


TARGET_TYPE = enum(
    BINARY='Binary',
    MULTICLASS='Multiclass',
    REGRESSION='Regression',
)


JOB_TYPE = enum(
    FEATURE_IMPACT='featureImpact',
    MODEL='model',
    MODEL_EXPORT='modelExport',
    PREDICT='predict',
    TRAINING_PREDICTIONS='trainingPredictions',
    PRIME_MODEL='primeModel',
    PRIME_RULESETS='primeRulesets',
    PRIME_VALIDATION='primeDownloadValidation',
    REASON_CODES='reasonCodes',
    REASON_CODES_INITIALIZATION='reasonCodesInitialization',
    PREDICTION_EXPLANATIONS='predictionExplanations',
    PREDICTION_EXPLANATIONS_INITIALIZATION='predictionExplanationsInitialization',
    RATING_TABLE_VALIDATION='validateRatingTable',
)


PREDICT_JOB_STATUS = enum(
    ABORTED='ABORTED',
    ERROR='error',
    INPROGRESS='inprogress',
    QUEUE='queue',
)

PREDICTION_PREFIX = enum(
    DEFAULT='class_'
)

PRIME_LANGUAGE = enum(
    JAVA='Java',
    PYTHON='Python',
)


VARIABLE_TYPE_TRANSFORM = enum(
    CATEGORICAL='categorical',
    CATEGORICAL_INT='categoricalInt',
    NUMERIC='numeric',
    TEXT='text',
)


DATE_EXTRACTION = enum(
    MONTH='month',
    MONTH_DAY='monthDay',
    WEEK='week',
    WEEK_DAY='weekDay',
    YEAR='year',
    YEAR_DAY='yearDay',
)


POSTGRESQL_DRIVER = enum(
    ANSI='PostgreSQL ANSI',
    UNICODE='PostgreSQL Unicode',
)

BLENDER_METHOD = enum(
    AVERAGE='AVG',
    ENET='ENET',
    GLM='GLM',
    MAE='MAE',
    MAEL1='MAEL1',
    MEDIAN='MED',
    PLS='PLS',
    RANDOM_FOREST='RF',
    LIGHT_GBM='LGBM',
    TENSORFLOW='TF',
    FORECAST_DISTANCE='FORECAST_DISTANCE'
)


CHART_DATA_SOURCE = enum(
    CROSSVALIDATION='crossValidation',
    HOLDOUT='holdout',
    VALIDATION='validation',
)


SCALEOUT_MODELING_MODE = enum(
    AUTOPILOT='autopilot',
    DISABLED='disabled',
    REPOSITORY_ONLY='repositoryOnly',
)


DATA_SUBSET = enum(
    ALL='all',
    VALIDATION_AND_HOLDOUT='validationAndHoldout',
    HOLDOUT='holdout',
    ALL_BACKTESTS='allBacktests',
)

DEFAULT_MAX_WAIT = 600

# default time out values in seconds for waiting response from client
DEFAULT_TIMEOUT = enum(
    CONNECT=6.05,  # time in seconds for the connection to server to be established
    READ=60,  # time in seconds after which to conclude the server isn't responding anymore
    UPLOAD=600,  # time in seconds after which to conclude that project dataset cannot be uploaded
)

# Time in seconds after which to conclude the server isn't responding anymore
# same as in DEFAULT_TIMEOUT, keeping for backwards compatibility
DEFAULT_READ_TIMEOUT = DEFAULT_TIMEOUT.READ

TARGET_LEAKAGE_TYPE = enum(
    SKIPPED_DETECTION='SKIPPED_DETECTION',
    FALSE='FALSE',
    MODERATE_RISK='MODERATE_RISK',
    HIGH_RISK='HIGH_RISK'
)

TREAT_AS_EXPONENTIAL = enum(
    ALWAYS='always',
    NEVER='never',
    AUTO='auto'
)

DIFFERENCING_METHOD = enum(
    AUTO='auto',
    SIMPLE='simple',
    NONE='none',
    SEASONAL='seasonal'
)

TIME_UNITS = enum(
    MILLISECOND='MILLISECOND',
    SECOND='SECOND',
    MINUTE='MINUTE',
    HOUR='HOUR',
    DAY='DAY',
    WEEK='WEEK',
    MONTH='MONTH',
    QUARTER='QUARTER',
    YEAR='YEAR')

PERIODICITY_MAX_TIME_STEP = 9223372036854775807

RECOMMENDED_MODEL_TYPE = enum(
    MOST_ACCURATE='Most Accurate',
    FAST_ACCURATE='Fast & Accurate',
    RECOMMENDED_FOR_DEPLOYMENT='Recommended for Deployment'
)

SERIES_AGGREGATION_TYPE = enum(
    AVERAGE='average',
    TOTAL='total'
)

MONOTONICITY_FEATURELIST_DEFAULT = object()


SHARING_ROLE = enum(
    OWNER='OWNER',
    READ_WRITE='READ_WRITE',
    USER='USER',
    EDITOR='EDITOR',
    READ_ONLY='READ_ONLY',
    CONSUMER='CONSUMER'
)

MODEL_REPLACEMENT_REASON = enum(
    ACCURACY='ACCURACY',
    DATA_DRIFT='DATA_DRIFT',
    ERRORS='ERRORS',
    SCHEDULED_REFRESH='SCHEDULED_REFRESH',
    SCORING_SPEED='SCORING_SPEED',
    OTHER='OTHER',
)
