
### PluginPress

WIP

### Usage

Install from github

	pip install git+https://github.com/zeuxisoo/python-pluginpress.git

### Example

Filter

    from pluginpress import Plugin

    def strong(value):
        return "<strong>{0}</strong>".format(value)

	plugin = Plugin()
    plugin.add_filter('strong', strong)

	# Output: <strong>This is test message</strong>
    print(plugin.apply_filter('strong', 'This is test message'))

Action

	from pluginpress import Plugin

    def puts(value):
        print(value)
        
	plugin = Plugin()
	plugin.add_action('puts', puts)

	# Output: Hello World
    plugin.do_action('puts', 'Hello World')
