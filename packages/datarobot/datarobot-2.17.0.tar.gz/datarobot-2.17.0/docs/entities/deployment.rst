.. _deployments_overview:

###########
Deployments
###########

Deployment is the central hub for users to deploy, manage and monitor their models.

Manage Deployments
******************

The following commands can be used to manage deployments.

Create a Deployment
===================

When creating a new deployment, a DataRobot ``model_id`` and ``label`` must be provided.
A ``description`` can be optionally provided to document the purpose of the deployment.

The default prediction server is used when making predictions against the deployment,
and is a requirement for creating a deployment on DataRobot cloud.
For on-prem installations, a user must not provide a default prediction server
and a pre-configured prediction server will be used instead.
Refer to :class:`datarobot.PredictionServer.list` for more information on retrieving available prediction servers.

.. code-block:: python

    import datarobot as dr

    project = dr.Project.get('5506fcd38bd88f5953219da0')
    model = project.get_models()[0]
    prediction_server = dr.PredictionServer.list()[0]

    deployment = dr.Deployment.create_from_learning_model(
        model.id, label='New Deployment', description='A new deployment',
        default_prediction_server_id=prediction_server.id')
    deployment
    >>> Deployment('New Deployment')

List Deployments
================

Use the following command to list deployments a user can view.

.. code-block:: python

    import datarobot as dr

    deployments = dr.Deployment.list()
    deployments
    >>> [Deployment('New Deployment'), Deployment('Previous Deployment')]

Refer to :class:`~datarobot.Deployment` for properties of the deployment object.


Retrieve a Deployment
=====================

It is possible to retrieve a single deployment with its identifier,
rather than list all deployments.

.. code-block:: python

    import datarobot as dr

    deployment = dr.Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    deployment.id
    >>> '5c939e08962d741e34f609f0'
    deployment.label
    >>> 'New Deployment'

Refer to :class:`~datarobot.Deployment` for properties of the deployment object.

Delete a Deployment
===================

To mark a deployment as deleted, use the following command.

.. code-block:: python

    import datarobot as dr

    deployment = dr.Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    deployment.delete()


Model Replacement
*****************

The model of a deployment can be replaced effortlessly with zero interruption of predictions.

Model replacement is an asynchronous process, which means there are some
preparatory works to complete before the process is fully finished.
However, predictions made against this deployment will start
using the new model as soon as you initiate the process.
The :meth:`~datarobot.Deployment.replace_model` function won't return until this asynchronous process is fully finished.

Alongside the identifier of the new model, a ``reason`` is also required.
The reason is stored in model history of the deployment for bookkeeping purpose.
An enum `MODEL_REPLACEMENT_REASON` is provided for convenience, all possible values are documented below:

- MODEL_REPLACEMENT_REASON.ACCURACY
- MODEL_REPLACEMENT_REASON.DATA_DRIFT
- MODEL_REPLACEMENT_REASON.ERRORS
- MODEL_REPLACEMENT_REASON.SCHEDULED_REFRESH
- MODEL_REPLACEMENT_REASON.SCORING_SPEED
- MODEL_REPLACEMENT_REASON.OTHER

Here is an example of model replacement:

.. code-block:: python

    import datarobot as dr
    from datarobot.enum import MODEL_REPLACEMENT_REASON

    project = dr.Project.get('5cc899abc191a20104ff446a')
    model = project.get_models()[0]

    deployment = Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    deployment.model['id'], deployment.model['type']
    >>> ('5c0a979859b00004ba52e431', 'Decision Tree Classifier (Gini)')

    deployment.replace_model('5c0a969859b00004ba52e41b', MODEL_REPLACEMENT_REASON.ACCURACY)
    deployment.model['id'], deployment.model['type']
    >>> ('5c0a969859b00004ba52e41b', 'Support Vector Classifier (Linear Kernel)')

Validation
==========

Before initiating the model replacement request, it is usually a good idea to use
the :meth:`~datarobot.Deployment.validate_replacement_model` function to validate if the new model can be used as a replacement.

The :meth:`~datarobot.Deployment.validate_replacement_model` function returns the validation status, a message and a checks dictionary.
If the status is 'passing' or 'warning', use :meth:`~datarobot.Deployment.replace_model` to perform model the replacement.
If status is 'failing', refer to the `checks` dict for more details on why the new model cannot be used as a replacement.

.. code-block:: python

    import datarobot as dr

    project = dr.Project.get('5cc899abc191a20104ff446a')
    model = project.get_models()[0]
    deployment = dr.Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    status, message, checks = deployment.validate_replacement_model(new_model_id=model.id)
    status
    >>> 'passing'

    # `checks` can be inspected for detail, showing two examples here:
    checks['target']
    >>> {'status': 'passing', 'message': 'Target is compatible.'}
    checks['permission']
    >>> {'status': 'passing', 'message': 'User has permission to replace model.'}

Drift Tracking Setting
**********************

Drift tracking is used to help analyze and monitor the performance of a model after it is deployed.
When the model of a deployment is replaced drift tracking status will not be altered.

Use :meth:`~datarobot.Deployment.get_drift_tracking_settings` to retrieve the current tracking status for target drift and feature drift.

.. code-block:: python

    import datarobot as dr

    deployment = dr.Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    settings = deployment.get_drift_tracking_settings()
    settings
    >>> {'target_drift': {'enabled': True}, 'feature_drift': {'enabled': True}}

Use :meth:`~datarobot.Deployment.update_drift_tracking_settings` to update target drift and feature drift tracking status.

.. code-block:: python

    import datarobot as dr

    deployment = dr.Deployment.get(deployment_id='5c939e08962d741e34f609f0')
    deployment.update_drift_tracking_settings(target_drift_enabled=True, feature_drift_enabled=True)