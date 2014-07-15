# PluginPress

Yet another simple plugin system for Python like WordPress plugin system

## Usage

Install from PYPI

    pip install pluginplot

Install from github

	pip install git+https://github.com/zeuxisoo/python-pluginplot.git

## Hooks

### Filter

Base style

    from pluginplot import Plugin

    def strong(value):
        return "<strong>{0}</strong>".format(value)

	plugin = Plugin()
    plugin.add_filter('strong', strong)

	# Output: <strong>This is test message</strong>
    print(plugin.apply_filter('strong', 'This is test message'))

Plot style

	from pluginplot import Plot

	plot = Plot()

	@plot.filter('strong')
	def strong(value):
        return "<strong>{0}</strong>".format(value)

### Action

Base style

	from pluginplot import Plugin

    def puts(value):
        print(value)

	plugin = Plugin()
	plugin.add_action('puts', puts)

	# Output: Hello World
    plugin.do_action('puts', 'Hello World')

Plot style

	from pluginplot import Plot

	plot = Plot()

	@plot.action('puts')
	def puts(value):
        print(value)

## Examples

More examples cloud be found at the `examples` directory like

- How to create plugin in single file or directory by `Plot`.
- How to load all plugins at once.
