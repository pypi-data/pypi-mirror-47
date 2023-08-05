.. _compliance_documentation_overview:


########################
Compliance Documentation
########################

Compliance Documentation is a premium add-on product to DataRobot. It allows users to automatically
generate and download documentation to assist with deploying models in highly regulated industries.

Generate and Download
*********************
Using the :class:`ComplianceDocumentation <datarobot.models.compliance_documentation.ComplianceDocumentation>` class, users can generate and download documentation as a DOCX.

.. code-block:: python

    import datarobot as dr
    project = dr.Project.get('5c881d7b79bffe6efc2e16f8')
    model = project.get_models()[0]

    # Using the default template
    doc = dr.ComplianceDocumentation(project.id, model.id)
    # Start a job to generate documentation
    job = doc.generate()
    # Once the job is complete, download as a DOCX
    job.wait_for_completion()
    doc.download('/path/to/save')

If no `template_id` is specified, DataRobot will generate compliance documentation using a default template. To create a custom template, see below:

.. _compliance_doc_template_overview:

#################################
Compliance Documentation Template
#################################
Using the :class:`ComplianceDocTemplate <datarobot.models.compliance_doc_template.ComplianceDocTemplate>` class, users can
define their own templates to make generated documents match their organization guidelines and requirements.

Templates are created from a list of `sections`, which are structured as follows:
    + ``contentId`` : The identifier of the content in this section
    + ``sections`` : A list of sub-section dicts nested under the parent section
    + ``title`` : The title of the section
    + ``type`` : The type of section - must be one of `datarobot`, `user`, or `table_of_contents`

Sections of type `user` are for custom content and include the ability to use two additional fields:
    + ``regularText`` : regular text of the section, optionally separated by \n to split paragraphs.
    + ``highlightedText`` : highlighted text of the section, optionally separated by \n to split paragraphs.

Within the above fields, users can embed DataRobot generated content using tags.
Each tag looks like {{ keyword }} and on generation will be replaced with corresponding content.
Below you can find a table of currently supported tags:

+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+
| Tag                            | Type           | Content                                              | Web Application UI Analog                                      |
+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+
| {{ blueprint_diagram }}        | Image          | Graphical representation of the modeling pipeline.   | Leaderboard >> Model >> Describe >> Blueprint                  |
+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+
| {{ alternative_models }}       | Table          | Comparison of the model with alternatives            | Leaderboard                                                    |
|                                |                | built in the same project.                           |                                                                |
|                                |                | Also known as challenger models.                     |                                                                |
+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+
| {{ model_features }}           | Table          | Description of the model features                    | Data >> Project Data                                           |
|                                |                | and corresponding EDA statistics.                    |                                                                |
+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+
| {{ missing_values }}           | Table          | Description of the missing values and their          | Leaderboard >> Model >> Describe >> Missing Values             |
|                                |                | processing in the model.                             |                                                                |
+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+
| {{ partitioning }}             | Image          | Graphical representation of the data partitioning.   | Data >> Show Advanced Options >> Partitioning                  |
|                                |                |                                                      | (only available before project start)                          |
+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+
| {{ model_scores }}             | Table          | Metric scores of the model on different data sources | Leaderboard >> Model                                           |
+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+
| {{ lift_chart }}               | Image          | Lift chart.                                          | Leaderboard >> Model >> Evaluate >> Lift Chart                 |
+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+
| {{ feature_impact }}           | Image          | Feature Impact chart.                                | Leaderboard >> Model >> Understand >> Feature Impact           |
+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+
| {{ feature_impact_table }}     | Table          | Table representation of Feature Impact data.         | Leaderboard >> Model >> Understand >> Feature Impact >> Export |
+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+
| {{ feature_effects }}          | List of images | Feature Effects charts for the top 3 features.       | Leaderboard >> Model >> Understand >> Feature Effects          |
+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+
| {{ accuracy_over_time }}       | Image          | Accuracy over time chart.                            | Leaderboard >> Model >> Evaluate >> Accuracy Over Time         |
|                                |                | Available only for datetime partitioned projects.    |                                                                |
+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+
| {{ cv_scores }}                | Table          | Project metric scores for each fold.                 | Currently unavailable in the UI                                |
|                                |                | Available only for projects with cross validation.   |                                                                |
+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+
| {{ roc_curve }}                |                | ROC Curve.                                           | Leaderboard >> Model >> Evaluate >> ROC Curve                  |
|                                | Image          | Available only for binary classification projects.   |                                                                |
+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+
| {{ confusion_matrix_summary }} | Table          | Confusion matrix summary for the threshold with      | Leaderboard >> Model >> Evaluate >> ROC Curve                  |
|                                |                | maximal F1 score value (default suggestion in UI).   |                                                                |
|                                |                | Available only for binary classification projects.   |                                                                |
+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+
| {{ prediction_distribution }}  | Image          | Prediction distribution.                             | Leaderboard >> Model >> Evaluate >> ROC Curve                  |
|                                |                | Available only for binary classification projects.   |                                                                |
+--------------------------------+----------------+------------------------------------------------------+----------------------------------------------------------------+

Creating a Custom Template
**************************
A common workflow includes retrieving the default template and using it as a base to extend and customize.

.. code-block:: python

    import datarobot as dr
    default_template = dr.ComplianceDocTemplate.get_default()
    # Download the template and edit sections on your local machine
    default_template.sections_to_json_file('path/to/save')
    # Create a new template from your local file
    my_template = dr.ComplianceDocTemplate.create_from_json_file(name='my_template', path='path/of/file')


Alternatively, custom templates can also be created from scratch.

.. code-block:: python

    sections = [{
                'title': 'Missing Values Report',
                'highlighted_text': 'NOTICE',
                'regular_text': 'This dataset had a lot of Missing Values. See the chart below: {{missing_values}}',
                'type': 'user'
                },
                {
                'title': 'Blueprints',
                'regular_text': '{{blueprint_diagram}} /n Blueprint for this model'
                'type': 'user'
                }]
    template = dr.ComplianceDocTemplate.create(name='Example', sections=sections)

    # Specify the template_id to generate documentation using a custom template
    doc = dr.ComplianceDocumentation(project.id, model.id, template.id)
    job = doc.generate().wait_for_completion()
    doc.download('/path/to/save')
