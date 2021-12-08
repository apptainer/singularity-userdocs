def variableReplace(app, docname, source):
    """
    Takes the source on rst and replaces all the needed variables declared on 
    variable_replacements structure
    """
    result = source[0]
    for key in app.config.variable_replacements:
        result = result.replace(key, app.config.variable_replacements[key])
    source[0] = result


# Add the needed variables to be replaced either on code or on text on the next
# dictionary structure.
variable_replacements = {
    "{InstallationVersion}" : "3.8.5",
    "\{admindocs\}" : "https://singularity.hpcng.org/admin-docs/3.8",
    "\{version\}": "3.8",
    "\{adminversion\}": "3.8",
    # The 'Singularity' noun is now a replacement so we can have
    # {Singularity}  rather than bare 'Singularity'... and HPCng can
    # replace to SingularityPRO so that it is clearer where docs
    # diverge a bit from Singularity<->SingularityPRO due to long-term backports etc.
    "{Singularity}": "Singularity",
}


def setup(app):
    app.add_config_value('variable_replacements', {}, True)
    app.connect('source-read', variableReplace)
