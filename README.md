# App template for the shirtracer platform

Start here for an app on the shirtracer platform. A push to `main` deploys it to
`https://<name>.apps.platform.shirtracer.gmbh`; you never need access to the server.

**Use this template → Create a new repository**, in the `shirtracer` organization or in your own
account. Then follow [Getting started](https://github.com/shirtracer/platform-workflows/blob/v1/docs/getting-started.md).

| File | What it is |
|------|------------|
| `platform.yaml` | the manifest: app name, route, login, shared services, secret names |
| `deploy/compose.yaml` | the app's stack, checked against the platform's rules |
| `Dockerfile`, `app/` | the example app (a small Python web service); replace with yours |
| `.github/workflows/deploy.yml` | calls the platform's deploy workflow at `@v1` |
| `.platform/platform.schema.json` | the manifest schema for your editor (don't edit) |
| `.github/workflows/template-ci.yml` | checks this template only; does nothing in your repository, delete it if you like |

Edit the lines marked `change:` in `platform.yaml` and `deploy/compose.yaml` (at least the app
name `myapp`); keep the lines marked `keep:`.

Documentation for app teams: [shirtracer/platform-workflows/docs](https://github.com/shirtracer/platform-workflows/blob/v1/docs/README.md).
Changes to this template don't reach existing apps; [Operations](https://github.com/shirtracer/platform-workflows/blob/v1/docs/operations.md#template-updates)
says how to take them over.
