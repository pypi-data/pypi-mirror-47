# ACOE Custom Jupyter Widgets

## Overview

<table><tr><td><a href="/ytics/multi-emr-on-glue-catalog"><img src="src/data-analytics/multi-emr-on-glue-catalog/thumbnail.png"/></a></td><td>This architecture demonstrates how to architect an analytics solution with multiple EMR clusters to query S3 datalake via Glue Catalog.</td></tr></table>

![JupyterWidgetArchitecture](images/jupyter-widget-ipython-schematic.png)

## Design

## Installation

To install use pip:

```sh
    pip install acoewidgets
    jupyter nbextension enable --py --sys-prefix acoewidgets
```

For a development installation (requires npm),

```sh
    git clone ssh://git@coxrepo.corp.cox.com/acoe/acoewidgets.git
    cd acoewidgets
    python setup.py build
    pip install -e .
    jupyter nbextension install --py --symlink --sys-prefix acoewidgets
    jupyter nbextension enable --py --sys-prefix acoewidgets
```

The last command should show the status of the widget as **OK**.  The widget works with both classic jupyter and jupyter lab.  Make sure you have valid AWS STS session before starting your notebook app.

## How to use

Import acoewidget module and use the command below to use the widget.

```python
from acoewidgets import endpoint

w = endpoint.EMRWidget()

w
```

Select the appropriate instance type and no of nodes and click launch button.

## References

## To Dos