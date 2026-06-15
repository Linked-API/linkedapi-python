This official Python SDK is the synchronous way to integrate with Linked API. It provides pre-defined workflow operations, direct account/statistics methods, admin APIs, authentication headers, polling, and structured error responses.

## Get started

To get started with Linked API Python SDK, read these essential guides first:

1. [Core concepts](https://linkedapi.io/sdks/core-concepts-0/) - understand how Linked API works.
2. [Installation & authorization](https://linkedapi.io/sdks/installation-authorization/) - install the SDK and authorize it.
3. [Predefined vs. custom workflows](https://linkedapi.io/sdks/predefined-vs-custom-workflows/) - choose ready-made operations or custom workflow definitions.
4. [Handling results and errors](https://linkedapi.io/sdks/handling-results-and-errors/) - process successful data and action errors.
5. [Persisting and cancelling workflows](https://linkedapi.io/sdks/persisting-and-cancelling-workflows/) - save, resume, and cancel workflows.

Install the package:

```bash
pip install linkedapi
```

Initialize the client:

```python
from linkedapi import LinkedApi, LinkedApiConfig

linkedapi = LinkedApi(
    LinkedApiConfig(
        linked_api_token="your-linked-api-token",
        identification_token="your-identification-token",
    )
)
```

Run a predefined workflow and poll the result:

```python
from linkedapi import FetchPersonParams

workflow = linkedapi.fetch_person.execute(
    FetchPersonParams(
        person_url="https://www.linkedin.com/in/john-doe",
        retrieve_experience=True,
        retrieve_posts=True,
        posts_retrieval_config={"limit": 10},
    )
)

result = linkedapi.fetch_person.result(workflow.workflow_id)
if result.data:
    print(result.data.name)
for error in result.errors:
    print(error.type, error.message)
```

Execute a custom workflow:

```python
workflow = linkedapi.custom_workflow.execute(
    {
        "actionType": "st.searchCompanies",
        "term": "Tech Inc",
        "filter": {
            "sizes": ["51-200", "2001-5000"],
            "locations": ["San Francisco", "New York"],
            "industries": ["Software Development"],
        },
        "then": {"actionType": "st.openCompanyPage", "basicInfo": True},
    }
)

result = linkedapi.custom_workflow.result(workflow.workflow_id)
print(result.data)
```

Continue polling after a workflow timeout:

```python
from linkedapi import LinkedApiWorkflowTimeoutError

try:
    result = linkedapi.fetch_person.result(workflow.workflow_id, timeout=30.0)
except LinkedApiWorkflowTimeoutError as error:
    result = linkedapi.fetch_person.result(error.workflow_id)
```

Cancel a workflow:

```python
cancelled = linkedapi.fetch_person.cancel(workflow.workflow_id)
print(cancelled)
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
