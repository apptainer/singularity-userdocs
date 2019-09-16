def variableReplace(app, docname, source):
    """
    Takes the source on rst and replaces all the needed variables declared on variable_replacements structure
    """
    result = source[0]
    for key in app.config.variable_replacements:
        result = result.replace(key, app.config.variable_replacements[key])
    source[0] = result

#Add the needed variables to be replaced either on code or on text on the next dictionary structure.
variable_replacements = {
    "{InstallationVersion}" : "3.4.0",
    "\{version\}" : "3.4",
    "\{adminversion\}" : "3.2"
}

def setup(app):
   app.add_config_value('variable_replacements', {}, True)
   app.connect('source-read', variableReplace)

