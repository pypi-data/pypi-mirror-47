#{{ project_name }}


## Local Development

### Run local instance
```bash
$ skaffold dev --port-forward
# visit http://localhost:8000
```

### Run local tests
```bash
$ scripts/test
```

{% if db %}
### Expose database on localhost
```bash
$ kubectl port-forward deployment/{{ project_name }}-db 5432:5432
```

### Troubleshoot init-containers 
If the main application fails to start due to failing init-containers check the logs
```bash
$ kubectl get pods
NAME                         READY   STATUS    RESTARTS   AGE
{{ project_name }}-app-<random_string>   1/1     Running   0          36m
{{ project_name }}-app-<random_string>   0/1     Init:CrashLoopBackOff   2          70s
{{ project_name }}-db-<random_string>   0/1     Running   0          84m
# Get logs for the crashing pod
$ kubectl logs {{ project_name}}-<random_string> -c init-migrate
# ... log output
```
{% endif %}

### Customize scripts
The following scripts are called for different tasks and may have to be customized depending on the project

* `scripts/dev` - Run a development server (e.g. with auto-reloading)
* `scripts/lint` - Run a linter on the `src/` folder (default: `flake8`)
* `scripts/prod` - Run a production server for remote deployments (e.g. uvicorn, gunicorn, uwsgi)
* `scripts/test` - Run tests found in `tests/` (default: `py.test`)
{%if db %}
* `scripts/migrate` - Run database migrations (e.g. django, alembic)
{% endif %}

