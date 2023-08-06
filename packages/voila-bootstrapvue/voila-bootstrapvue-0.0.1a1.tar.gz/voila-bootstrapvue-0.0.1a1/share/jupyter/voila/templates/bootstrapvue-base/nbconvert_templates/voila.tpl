<!DOCTYPE html>
<html>
    <head>
        <!-- Load required Bootstrap and BootstrapVue CSS -->
        <link type="text/css" rel="stylesheet" href="//unpkg.com/bootstrap/dist/css/bootstrap.min.css" />
        <link type="text/css" rel="stylesheet" href="//unpkg.com/bootstrap-vue@latest/dist/bootstrap-vue.min.css" />

        <!-- Load polyfills to support older browsers -->
        <script src="//polyfill.io/v3/polyfill.min.js?features=es2015%2CMutationObserver" crossorigin="anonymous"></script>

        <!-- Load Vue followed by BootstrapVue -->
        <script src="//unpkg.com/vue@latest/dist/vue.min.js"></script>
        <script src="//unpkg.com/bootstrap-vue@latest/dist/bootstrap-vue.min.js"></script>

        <link href='https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900|Material+Icons' rel="stylesheet">
        <script src="{{resources.base_url}}voila/static/require.min.js" integrity="sha256-Ae2Vz/4ePdIu6ZyI/5ZGsYnb+m0JlOmKPjt6XZ9JJkA=" crossorigin="anonymous"></script>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui">
    </head>

    <body data-base-url="{{resources.base_url}}voila/">
        <script>
            {% include "util.js" %}
        </script>

        {% include "app.html" %}
    </body>

    <script id="jupyter-config-data" type="application/json">
        {
          "baseUrl": "{{resources.base_url}}",
          "kernelId": "{{resources.kernel_id}}"
        }
    </script>

    <script>
        requirejs.config({
            baseUrl: '{{resources.base_url}}voila',
            waitSeconds: 3000,
            map: {
                '*': {
                     'jupyter-bootstrapvue': 'nbextensions/jupyter-bootstrapvue/nodeps',
                },
            },
        });
        requirejs(['static/voila'], (voila) => init(voila));
        requirejs([
            {% for ext in resources.nbextensions if ext != 'jupyter-bootstrapvue/extension' -%}
                "{{resources.base_url}}voila/nbextensions/{{ ext }}.js",
            {% endfor %}
        ]);
    </script>
</html>
